"""Exercise the actual delayed diplomacy scripts against changed participants.

This bounded interpreter covers only the effects used here, not the HOI4 engine.
"""
from dataclasses import dataclass, field as data_field
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]


def block(node, key):
    return next(part for part in children(node) if part.key == key)


@dataclass
class Country:
    tag: str
    exists: bool = True
    capitulated: bool = False
    pp: int = 50
    flags: set = data_field(default_factory=set)
    wars: set = data_field(default_factory=set)
    opinions: set = data_field(default_factory=set)


class DiplomacyWorld:
    def __init__(self, events):
        self.events = events
        self.countries = {tag: Country(tag) for tag in ('WFL', 'GER', 'HOL', 'ENG')}
        self.countries['WFL'].pp = 0
        self.scheduled = []

    def scope(self, key, root):
        return root if key == 'ROOT' else self.countries[key]

    def matches(self, nodes, current, root):
        for node in nodes:
            key, value = node.key, node.value
            if key in self.countries or key == 'ROOT':
                result = self.matches(children(node), self.scope(key, root), root)
            elif key == 'NOT':
                result = not self.matches(children(node), current, root)
            elif key == 'OR':
                result = any(self.matches([part], current, root) for part in children(node))
            elif key == 'has_country_flag':
                result = value in current.flags
            elif key == 'exists':
                result = current.exists == (value == 'yes')
            elif key == 'has_capitulated':
                result = current.capitulated == (value == 'yes')
            elif key == 'has_war_with':
                result = value in current.wars
            elif key == 'has_political_power':
                result = current.pp > int(value)
            elif key == 'tag':
                result = current.tag == value
            elif key == 'has_completed_focus':
                # These tests begin after completing the triggering focuses.
                result = True
            else:
                raise AssertionError('Unsupported trigger: ' + key)
            if not result:
                return False
        return True

    def effects(self, nodes, current, root):
        preceding_if = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                preceding_if = self.matches(children(block(node, 'limit')), current, root)
                if preceding_if:
                    self.effects([part for part in children(node) if part.key != 'limit'], current, root)
            elif key == 'else':
                if preceding_if is False:
                    self.effects(children(node), current, root)
            elif key in self.countries or key == 'ROOT':
                self.effects(children(node), self.scope(key, root), root)
            elif key == 'set_country_flag':
                current.flags.add(value)
            elif key == 'clr_country_flag':
                current.flags.discard(value)
            elif key == 'add_political_power':
                current.pp += int(value)
            elif key == 'add_opinion_modifier':
                current.opinions.add((field(node, 'target'), field(node, 'modifier')))
            elif key == 'country_event':
                self.scheduled.append((current.tag, field(node, 'id')))
            else:
                raise AssertionError('Unsupported effect: ' + key)

    def option(self, event_id, recipient, choice=0):
        event = self.events[event_id]
        current = self.countries[recipient]
        option = [n for n in children(event) if n.key == 'option'][choice]
        self.effects([part for part in children(option) if part.key not in ('name', 'ai_chance')], current, current)

    def event(self, event_id, recipient, choice=0):
        event = self.events[event_id]
        current = self.countries[recipient]
        if not self.matches(children(block(event, 'trigger')), current, current):
            return False
        for node in children(event):
            if node.key == 'immediate':
                self.effects(children(node), current, current)
        if any(n.key == 'option' for n in children(event)):
            self.option(event_id, recipient, choice)
        return True


class BeerDiplomacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = parse((ROOT / 'events/WFL_beer_diplomacy.txt').read_text(encoding='utf-8-sig'))
        cls.events = {field(n, 'id'): n for n in cls.nodes if n.key == 'country_event'}

    def world(self):
        return DiplomacyWorld(self.events)

    def test_acceptance_and_refusal_both_reward_rhine_once(self):
        for choice in (0, 1):
            with self.subTest(choice=choice):
                world = self.world()
                self.assertTrue(world.event('wfl_beer.1', 'WFL'))
                for event_id, tag in (('wfl_beer.2', 'GER'), ('wfl_beer.3', 'HOL')):
                    self.assertTrue(world.event(event_id, tag, choice))
                    world.option(event_id, tag, 1 - choice)
                    self.assertFalse(world.event(event_id, tag, choice))
                    self.assertEqual(world.countries[tag].pp, 25 if choice == 0 else 50)
                self.assertEqual(world.countries['WFL'].pp, 100)
                self.assertFalse(world.event('wfl_beer.7', 'WFL'))
                world.option('wfl_beer.1', 'WFL')
                self.assertEqual(world.countries['WFL'].pp, 100)

    def test_war_capitulation_missing_country_or_insufficient_pp_never_spends_partner_pp(self):
        for condition in ('war', 'capitulated', 'missing', 'poor', 'exactly_25', 'wfl_capitulated'):
            with self.subTest(condition=condition):
                world = self.world()
                world.event('wfl_beer.1', 'WFL')
                partner = world.countries['GER']
                if condition == 'war': partner.wars.add('WFL')
                elif condition == 'capitulated': partner.capitulated = True
                elif condition == 'missing': partner.exists = False
                elif condition == 'poor': partner.pp = 0
                elif condition == 'exactly_25': partner.pp = 25
                elif condition == 'wfl_capitulated': world.countries['WFL'].capitulated = True
                before = partner.pp
                world.event('wfl_beer.2', 'GER')
                self.assertEqual(partner.pp, before)
                self.assertEqual(partner.opinions, set())
                self.assertEqual(world.countries['WFL'].pp, 50)

    def test_missing_partners_and_unanswered_replies_still_settle_once(self):
        world = self.world()
        world.countries['GER'].exists = False
        world.countries['HOL'].exists = False
        world.event('wfl_beer.1', 'WFL')
        self.assertEqual(world.countries['WFL'].pp, 100)
        self.assertFalse(world.event('wfl_beer.7', 'WFL'))
        world = self.world()
        world.event('wfl_beer.1', 'WFL')
        self.assertTrue(world.event('wfl_beer.7', 'WFL'))
        self.assertEqual(world.countries['WFL'].pp, 100)
        self.assertFalse(world.event('wfl_beer.7', 'WFL'))
        self.assertFalse(world.event('wfl_beer.2', 'GER'))
        self.assertFalse(world.event('wfl_beer.3', 'HOL'))

    def test_british_friendship_is_mutual_permanent_and_granted_once(self):
        world = self.world()
        world.event('wfl_beer.4', 'WFL')
        world.event('wfl_beer.5', 'ENG')
        expected = {'WFL_anglo_bierfreundschaft', 'WFL_anglo_bierhandel'}
        for tag, partner in (('WFL', 'ENG'), ('ENG', 'WFL')):
            self.assertEqual(world.countries[tag].opinions, {(partner, key) for key in expected})
        self.assertEqual(world.countries['WFL'].pp, 75)
        world.option('wfl_beer.5', 'ENG')
        self.assertEqual(world.countries['WFL'].pp, 75)
        self.assertFalse(world.event('wfl_beer.8', 'WFL'))
        modifiers = parse((ROOT / 'common/opinion_modifiers/WFL_beer_diplomacy.txt').read_text())[0]
        definitions = {n.key: n for n in children(modifiers)}
        self.assertEqual(field(definitions['WFL_anglo_bierfreundschaft'], 'value'), '100')
        self.assertEqual(field(definitions['WFL_anglo_bierhandel'], 'value'), '50')
        self.assertEqual(field(definitions['WFL_anglo_bierhandel'], 'trade'), 'yes')
        for key in expected:
            self.assertFalse({'days', 'months', 'years', 'decay'} & {n.key for n in children(definitions[key])})

    def test_changed_britain_or_wfl_and_timeout_use_compensation_without_friendship(self):
        for condition in ('eng_missing', 'eng_capitulated', 'wfl_capitulated', 'war', 'timeout'):
            with self.subTest(condition=condition):
                world = self.world()
                world.event('wfl_beer.4', 'WFL')
                if condition == 'eng_missing': world.countries['ENG'].exists = False
                elif condition == 'eng_capitulated': world.countries['ENG'].capitulated = True
                elif condition == 'wfl_capitulated': world.countries['WFL'].capitulated = True
                elif condition == 'war': world.countries['ENG'].wars.add('WFL')
                if condition == 'timeout':
                    world.event('wfl_beer.8', 'WFL')
                    self.assertFalse(world.event('wfl_beer.5', 'ENG'))
                else:
                    world.event('wfl_beer.5', 'ENG')
                    self.assertFalse(world.event('wfl_beer.8', 'WFL'))
                self.assertEqual(world.countries['WFL'].pp, 50)
                self.assertEqual(world.countries['WFL'].opinions, set())
                self.assertEqual(world.countries['ENG'].opinions, set())

    def test_ineligible_britain_at_outset_compensates_immediately_once(self):
        world = self.world()
        world.countries['ENG'].exists = False
        world.event('wfl_beer.4', 'WFL')
        world.option('wfl_beer.4', 'WFL')
        self.assertEqual(world.countries['WFL'].pp, 50)
        self.assertFalse(world.event('wfl_beer.8', 'WFL'))

    def test_no_forced_war_territory_factory_or_alliance_effects(self):
        forbidden = {'transfer_state', 'add_state_core', 'add_core_of', 'declare_war_on',
                     'create_wargoal', 'add_building_construction', 'add_to_faction', 'set_autonomy'}
        self.assertFalse(forbidden & {n.key for n in walk(self.nodes)})
        self.assertTrue(all(field(n, 'fire_only_once') == 'yes' for n in self.events.values()))


if __name__ == '__main__':
    unittest.main()
