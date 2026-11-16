"""Bounded execution of the real Dorfkeller guards/reward, not engine simulation."""
from dataclasses import dataclass, field as data_field
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
FOCUS = 'WFL_dorfkeller_diplomatie'
SUCCESS = 'WFL_zapfhahn_success'
RESOLVED = 'WFL_dorfkeller_resolved'
JOINED = 'WFL_dorfkeller_joined_allies'
EVENT = 'wfl_dorfkeller.1'


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return next(n for n in children(node) if n.key == key)


@dataclass
class Country:
    tag: str
    exists: bool = True
    capitulated: bool = False
    subject: bool = False
    faction: str | None = None
    government: str = 'neutrality'
    flags: set[str] = data_field(default_factory=set)
    pp: int = 0


class DorfkellerWorld:
    """Reject unknown operations; implement only this focus's small subset."""
    def __init__(self, triggers):
        self.triggers = triggers
        self.countries = {tag: Country(tag) for tag in ('WFL', 'ENG', 'FRA', 'GER')}
        self.root = self.countries['WFL']
        self.root.flags.add(SUCCESS)
        self.countries['ENG'].government = 'democratic'
        self.countries['ENG'].faction = 'allies'
        self.countries['FRA'].faction = 'allies'
        self.factions = {'allies': ('ENG', 'faction_template_allies'),
                         'foreign': ('GER', 'faction_template_axis'),
                         'own': ('WFL', 'faction_template_generic')}
        self.wars = set()
        self.join_calls = []
        self.join_blocked = False
        self.scheduled = []

    def country(self, tag):
        return self.root if tag == 'ROOT' else self.countries[tag]

    def matches(self, nodes, current=None):
        current = current or self.root
        for node in nodes:
            key, value = node.key, node.value
            if key in self.countries or key == 'ROOT':
                result = self.matches(children(node), self.country(key))
            elif key == 'faction_leader':
                result = bool(current.faction) and self.matches(children(node), self.country(self.factions[current.faction][0]))
            elif key in self.triggers:
                result = self.matches(self.triggers[key], current) == (value == 'yes')
            elif key == 'NOT':
                result = not self.matches(children(node), current)
            elif key == 'OR':
                result = any(self.matches([n], current) for n in children(node))
            elif key == 'custom_trigger_tooltip':
                result = self.matches([n for n in children(node) if n.key != 'tooltip'], current)
            elif key == 'any_country':
                result = any(self.matches(children(node), c) for c in self.countries.values() if c.exists)
            elif key == 'tag':
                result = current.tag == value
            elif key == 'exists':
                result = current.exists == (value == 'yes')
            elif key == 'has_capitulated':
                result = current.capitulated == (value == 'yes')
            elif key == 'is_subject':
                result = current.subject == (value == 'yes')
            elif key == 'is_in_faction':
                result = (current.faction is not None) == (value == 'yes')
            elif key == 'is_faction_leader':
                result = bool(current.faction and self.factions[current.faction][0] == current.tag) == (value == 'yes')
            elif key == 'has_government':
                result = current.government == value
            elif key == 'has_faction_template':
                result = bool(current.faction and self.factions[current.faction][1] == value)
            elif key == 'is_in_faction_with':
                result = current.faction is not None and current.faction == self.country(value).faction
            elif key == 'has_war_with':
                result = frozenset((current.tag, self.country(value).tag)) in self.wars
            elif key == 'has_country_flag':
                result = value in current.flags
            else:
                raise AssertionError('Unsupported Dorfkeller trigger: ' + key)
            if not result:
                return False
        return True

    def effects(self, nodes, current=None):
        current = current or self.root
        preceding_if = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                preceding_if = self.matches(children(block(node, 'limit')), current)
                if preceding_if:
                    self.effects([n for n in children(node) if n.key != 'limit'], current)
            elif key == 'else':
                if preceding_if is False:
                    self.effects(children(node), current)
            elif key in self.countries or key == 'ROOT':
                self.effects(children(node), self.country(key))
            elif key == 'faction_leader':
                self.effects(children(node), self.country(self.factions[current.faction][0]))
            elif key == 'hidden_effect':
                self.effects(children(node), current)
            elif key == 'custom_effect_tooltip':
                pass
            elif key == 'set_country_flag':
                current.flags.add(value)
            elif key == 'add_political_power':
                current.pp += int(value)
            elif key == 'add_to_faction':
                assert current.faction and self.factions[current.faction][0] == current.tag
                target = self.country(value)
                self.join_calls.append((current.tag, target.tag))
                if not self.join_blocked:
                    target.faction = current.faction
            elif key == 'country_event':
                self.scheduled.append((current.tag, field(node, 'id'), field(node, 'days')))
            else:
                raise AssertionError('Unsupported Dorfkeller effect: ' + key)


class DorfkellerDiplomacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.triggers = {n.key: children(n) for n in read('common/scripted_triggers/WFL_dorfkeller_triggers.txt')}
        tree = read('common/national_focus/WFL_focus.txt')[0]
        cls.focus = next(n for n in children(tree) if n.key == 'focus' and field(n, 'id') == FOCUS)
        cls.available = children(block(cls.focus, 'available'))
        cls.reward = children(block(cls.focus, 'completion_reward'))
        cls.bypass = children(block(cls.focus, 'bypass'))

    def world(self):
        return DorfkellerWorld(self.triggers)

    def invalidations(self):
        return {
            'WFL subject': lambda w: setattr(w.root, 'subject', True),
            'WFL capitulated': lambda w: setattr(w.root, 'capitulated', True),
            'foreign faction': lambda w: setattr(w.root, 'faction', 'foreign'),
            'own faction': lambda w: setattr(w.root, 'faction', 'own'),
            'absent Britain': lambda w: setattr(w.countries['ENG'], 'exists', False),
            'British subject': lambda w: setattr(w.countries['ENG'], 'subject', True),
            'Britain capitulated': lambda w: setattr(w.countries['ENG'], 'capitulated', True),
            'Britain no faction': lambda w: setattr(w.countries['ENG'], 'faction', None),
            'different British template': lambda w: w.factions.update(allies=('ENG', 'faction_template_generic')),
            'war with Britain': lambda w: w.wars.add(frozenset(('WFL', 'ENG'))),
            'war with another ally': lambda w: w.wars.add(frozenset(('WFL', 'FRA'))),
        }

    def test_both_successful_crisis_paths_join_allies_immediately_without_changing_government(self):
        for path in ('WFL_zapfhahn_trade', 'WFL_zapfhahn_duel'):
            with self.subTest(path=path):
                world = self.world()
                world.root.flags.add(path)
                self.assertTrue(world.matches(self.available))
                world.effects(self.reward)
                self.assertEqual(world.join_calls, [('ENG', 'WFL')])
                self.assertEqual(world.root.faction, 'allies')
                self.assertEqual(world.root.government, 'neutrality')
                self.assertEqual(world.root.pp, 0)
                self.assertTrue({RESOLVED, JOINED} <= world.root.flags)
                self.assertEqual(world.scheduled, [('WFL', EVENT, '1')])
                world.effects(self.reward)
                self.assertEqual(world.join_calls, [('ENG', 'WFL')])
                self.assertEqual(world.scheduled, [('WFL', EVENT, '1')])
                self.assertEqual(world.root.pp, 0)

    def test_invalid_participants_and_conflicts_block_selection(self):
        for label, mutate in self.invalidations().items():
            with self.subTest(case=label):
                world = self.world()
                mutate(world)
                self.assertFalse(world.matches(self.available))

    def test_old_save_or_timeout_without_hidden_success_flag_can_join(self):
        world = self.world()
        world.root.flags.discard(SUCCESS)
        self.assertTrue(world.matches(self.available))
        world.effects(self.reward)
        self.assertEqual(world.root.faction, 'allies')
        self.assertIn(JOINED, world.root.flags)

    def test_changed_government_or_allies_leadership_does_not_block_joining(self):
        world = self.world()
        world.countries['ENG'].government = 'neutrality'
        world.factions['allies'] = ('FRA', 'faction_template_allies')
        # Britain may remain in its faction even after capitulation or subjection.
        world.countries['ENG'].capitulated = True
        world.countries['ENG'].subject = True
        self.assertTrue(world.matches(self.available))
        world.effects(self.reward)
        self.assertEqual(world.join_calls, [('FRA', 'WFL')])
        self.assertEqual(world.root.faction, 'allies')
        self.assertTrue({RESOLVED, JOINED} <= world.root.flags)

    def test_actual_allies_leader_must_exist_and_be_free_and_uncapitulated(self):
        for attribute in ('exists', 'subject', 'capitulated'):
            with self.subTest(attribute=attribute):
                world = self.world()
                world.factions['allies'] = ('FRA', 'faction_template_allies')
                setattr(world.countries['FRA'], attribute, attribute != 'exists')
                self.assertFalse(world.matches(self.available))

    def test_changed_conditions_at_completion_pay_fallback_once_without_forcing_faction_change(self):
        for label, mutate in self.invalidations().items():
            with self.subTest(case=label):
                world = self.world()
                self.assertTrue(world.matches(self.available))
                mutate(world)
                before = {tag: c.faction for tag, c in world.countries.items()}
                world.effects(self.reward)
                world.effects(self.reward)
                self.assertEqual(world.root.pp, 50)
                self.assertEqual(world.join_calls, [])
                self.assertEqual(world.scheduled, [])
                self.assertNotIn(JOINED, world.root.flags)
                self.assertIn(RESOLVED, world.root.flags)
                self.assertEqual({tag: c.faction for tag, c in world.countries.items()}, before)

    def test_existing_allies_membership_bypasses_but_other_british_factions_do_not(self):
        world = self.world()
        world.root.faction = 'allies'
        self.assertFalse(world.matches(self.available))
        self.assertTrue(world.matches(self.bypass))
        world.factions['allies'] = ('ENG', 'faction_template_generic')
        self.assertFalse(world.matches(self.bypass))

    def test_unsuccessful_join_never_claims_success_or_schedules_the_celebration(self):
        world = self.world()
        world.join_blocked = True
        self.assertTrue(world.matches(self.available))
        world.effects(self.reward)
        world.effects(self.reward)
        self.assertEqual(world.join_calls, [('ENG', 'WFL')])
        self.assertIsNone(world.root.faction)
        self.assertNotIn(JOINED, world.root.flags)
        self.assertEqual(world.scheduled, [])
        self.assertEqual(world.root.pp, 50)

    def test_focus_follows_zapfhahnkrise_and_cancels_when_its_guard_becomes_invalid(self):
        self.assertEqual(field(block(self.focus, 'prerequisite'), 'focus'), 'WFL_zapfhahnkrise')
        self.assertEqual(field(self.focus, 'cost'), '5')
        self.assertEqual(field(self.focus, 'cancel_if_invalid'), 'yes')
        self.assertEqual((field(self.focus, 'x'), field(self.focus, 'y')), ('28', '5'))

    def test_confirmation_event_has_no_join_or_other_gameplay_effect(self):
        event = next(n for n in read('events/WFL_dorfkeller_diplomacy.txt')
                     if n.key == 'country_event' and field(n, 'id') == EVENT)
        self.assertEqual(field(event, 'is_triggered_only'), 'yes')
        self.assertFalse(any(n.key == 'immediate' for n in children(event)))
        options = [n for n in children(event) if n.key == 'option']
        self.assertEqual(len(options), 1)
        self.assertEqual({n.key for n in children(options[0])}, {'name'})
        self.assertFalse(any(n.key == 'add_to_faction' for n in walk([event])))
        trigger = children(block(event, 'trigger'))
        world = self.world()
        self.assertFalse(world.matches(trigger))
        world.effects(self.reward)
        self.assertTrue(world.matches(trigger))
        world.root.faction = None
        self.assertFalse(world.matches(trigger))


if __name__ == '__main__':
    unittest.main()
