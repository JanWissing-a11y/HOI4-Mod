"""Exercise choices, delayed eligibility changes and one-time event rewards.

This strict interpreter reads the real event/idea scripts. It covers their
country subset, not Clausewitz UI or engine modifier recalculation.
"""

from dataclasses import dataclass, field as data_field
from decimal import Decimal
from pathlib import Path
import unittest

from tools.validate_mod import Node, children, field, parse


ROOT = Path(__file__).resolve().parents[1]
JAN = 'WFL_schuetzenkoenig'


def block(node, key):
    matches = [part for part in children(node) if part.key == key]
    if len(matches) != 1:
        raise AssertionError(f'Expected one {key} block in {node.key}, found {len(matches)}')
    return matches[0]


@dataclass
class Country:
    tag: str = 'WFL'
    government: str = 'neutrality'
    leader: str = JAN
    capitulated: bool = False
    flags: set[str] = data_field(default_factory=set)
    focuses: set[str] = data_field(default_factory=set)
    ideas: set[str] = data_field(default_factory=set)
    political_power: int = 0
    stability: Decimal = Decimal('0.50')
    war_support: Decimal = Decimal('0.30')
    army_experience: int = 0
    research_slots: int = 4
    tech_bonuses: list[tuple] = data_field(default_factory=list)


class CommunityWorld:
    def __init__(self, event, ideas):
        self.country = Country()
        self.ideas = ideas
        self.country.focuses.update(
            node.value for node in children(block(event, 'trigger'))
            if node.key == 'has_completed_focus'
        )

    def conditions(self, nodes, current=None):
        current = current or self.country
        results = []
        for node in nodes:
            key, value = node.key, node.value
            if key == 'NOT':
                matches = not self.conditions(children(node), current)
            elif key == 'AND':
                matches = self.conditions(children(node), current)
            elif key == 'OR':
                matches = any(self.conditions([part], current) for part in children(node))
            elif key == 'tag':
                matches = current.tag == value
            elif key == 'has_completed_focus':
                matches = value in current.focuses
            elif key == 'has_country_flag':
                matches = value in current.flags
            elif key == 'has_government':
                matches = current.government == value
            elif key == 'has_country_leader':
                if field(node, 'ruling_only') != 'yes':
                    raise AssertionError('Fixture requires an explicit ruling leader query')
                matches = current.leader == field(node, 'character')
            else:
                raise AssertionError(f'Unknown community condition: {key}')
            results.append(matches)
        return all(results)

    def effects(self, nodes):
        preceding_if = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                preceding_if = self.conditions(children(block(node, 'limit')))
                if preceding_if:
                    self.effects([part for part in children(node) if part.key != 'limit'])
            elif key == 'else':
                if preceding_if is None:
                    raise AssertionError('else without an evaluated if')
                if not preceding_if:
                    self.effects(children(node))
                preceding_if = None
            elif key == 'set_country_flag':
                self.country.flags.add(value)
            elif key == 'add_political_power':
                self.country.political_power += int(value)
            elif key == 'add_stability':
                self.country.stability += Decimal(value)
            elif key == 'add_war_support':
                self.country.war_support += Decimal(value)
            elif key == 'army_experience':
                self.country.army_experience += int(value)
            elif key == 'add_ideas':
                if value not in self.ideas:
                    raise AssertionError(f'Unknown community idea: {value}')
                self.country.ideas.add(value)
            elif key == 'add_tech_bonus':
                self.country.tech_bonuses.append(tuple((part.key, part.value) for part in children(node)))
            else:
                raise AssertionError(f'Unknown community effect: {key}')

    def open_event(self, event):
        return self.conditions(children(block(event, 'trigger')))

    def choose(self, event, suffix):
        options = [node for node in children(event) if node.key == 'option'
                   and field(node, 'name') == field(event, 'id') + '.' + suffix]
        if len(options) != 1:
            raise AssertionError(f'Expected one option {suffix}')
        self.effects([node for node in children(options[0]) if node.key not in ('name', 'ai_chance')])

    def modifiers(self):
        values = {}
        for idea_id in self.country.ideas:
            for node in children(block(self.ideas[idea_id], 'modifier')):
                values[node.key] = values.get(node.key, Decimal(0)) + Decimal(node.value)
        return values

    def reward_state(self):
        country = self.country
        return (country.political_power, country.stability, country.war_support,
                country.army_experience, country.research_slots, frozenset(country.ideas),
                tuple(country.tech_bonuses))


class CommunityExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = {
            field(node, 'id'): node for node in parse(
                (ROOT / 'events/WFL_community_expansion.txt').read_text(encoding='utf-8-sig'))
            if node.key == 'country_event'
        }
        groups = parse((ROOT / 'common/ideas/WFL_community_expansion_ideas.txt')
                       .read_text(encoding='utf-8-sig'))
        cls.ideas = {node.key: node for group in groups
                     for node in children(block(group, 'country'))}

    def event(self, number):
        return self.events[f'wfl_community.{number}']

    def world(self, number):
        return CommunityWorld(self.event(number), self.ideas)

    def assert_compensation_only(self, world):
        self.assertEqual(world.country.political_power, 50)
        self.assertEqual(world.country.stability, Decimal('0.50'))
        self.assertEqual(world.country.war_support, Decimal('0.30'))
        self.assertEqual(world.country.army_experience, 0)
        self.assertEqual(world.country.research_slots, 4)
        self.assertEqual(world.country.ideas, set())
        self.assertEqual(world.country.tech_bonuses, [])

    def test_each_choice_consumes_the_event_and_blocks_both_reward_replays(self):
        for event in self.events.values():
            self.assertEqual(field(event, 'is_triggered_only'), 'yes')
            self.assertEqual(field(event, 'fire_only_once'), 'yes')
            for suffix in ('a', 'b'):
                with self.subTest(event=field(event, 'id'), choice=suffix):
                    world = CommunityWorld(event, self.ideas)
                    self.assertTrue(world.open_event(event))
                    initial = world.reward_state()
                    world.choose(event, suffix)
                    reward = world.reward_state()
                    self.assertNotEqual(reward, initial)
                    self.assertFalse(world.open_event(event))
                    # Directly replay option effects even when normal event
                    # dispatch would already reject a second opening.
                    world.choose(event, suffix)
                    world.choose(event, 'b' if suffix == 'a' else 'a')
                    self.assertEqual(world.reward_state(), reward)

    def test_wfl_and_the_completed_focus_are_required_to_open(self):
        for event in self.events.values():
            with self.subTest(event=field(event, 'id')):
                world = CommunityWorld(event, self.ideas)
                world.country.tag = 'GER'
                self.assertFalse(world.open_event(event))
                world.country.tag = 'WFL'
                world.country.focuses.clear()
                self.assertFalse(world.open_event(event))

    def test_brewery_olympiad_and_congress_choices_have_distinct_payoffs(self):
        brewery = self.world(1)
        brewery.choose(self.event(1), 'a')
        self.assertEqual((brewery.country.political_power, brewery.country.stability),
                         (50, Decimal('0.55')))
        self.assertEqual(brewery.country.ideas, set())

        olympiad = self.world(2)
        olympiad.choose(self.event(2), 'a')
        self.assertEqual((olympiad.country.army_experience, olympiad.country.war_support),
                         (30, Decimal('0.35')))
        self.assertEqual(olympiad.country.ideas, set())
        youth = self.world(2)
        youth.choose(self.event(2), 'b')
        self.assertEqual(youth.modifiers(), {'conscription': Decimal('0.005'),
                                           'training_time_army_factor': Decimal('-0.05')})
        self.assertEqual((youth.country.army_experience, youth.country.war_support),
                         (0, Decimal('0.30')))

        congress = self.world(5)
        congress.choose(self.event(5), 'a')
        self.assertEqual(congress.modifiers(), {'stability_factor': Decimal('0.10'),
                                              'war_support_factor': Decimal('-0.05')})

    def test_independent_events_stack_only_the_selected_ideas(self):
        world = self.world(1)
        world.choose(self.event(1), 'b')
        world.country.focuses.update(self.world(5).country.focuses)
        self.assertTrue(world.open_event(self.event(5)))
        world.choose(self.event(5), 'b')
        self.assertEqual(world.modifiers(), {
            'political_power_gain': Decimal('0.05'), 'stability_factor': Decimal('0.02'),
            'conscription': Decimal('0.01'), 'non_core_manpower': Decimal('0.05'),
        })
        self.assertEqual(world.country.political_power, 0)
        for number in (1, 5):
            world.choose(self.event(number), 'a')
        self.assertEqual(world.country.political_power, 0)
        self.assertNotIn('WFL_vereinsverstaendigung_idee', world.country.ideas)

    def test_changed_leader_or_government_resolves_with_one_compensation(self):
        for number in (1, 2, 5):
            for suffix in ('a', 'b'):
                for change in ('leader', 'government'):
                    with self.subTest(event=number, choice=suffix, change=change):
                        event, world = self.event(number), self.world(number)
                        self.assertTrue(world.open_event(event))
                        if change == 'leader':
                            world.country.leader = 'a_different_ruler'
                        else:
                            world.country.government = 'democratic'
                        # Completed focuses still get a resolvable event.
                        self.assertTrue(world.open_event(event))
                        world.choose(event, suffix)
                        self.assert_compensation_only(world)
                        world.country.leader, world.country.government = JAN, 'neutrality'
                        world.choose(event, 'a')
                        world.choose(event, 'b')
                        self.assert_compensation_only(world)

    def test_capitulation_does_not_change_community_rewards(self):
        for number in (1, 2, 5):
            for suffix in ('a', 'b'):
                with self.subTest(event=number, choice=suffix):
                    event, world = self.event(number), self.world(number)
                    self.assertTrue(world.open_event(event))
                    world.country.capitulated = True
                    world.choose(event, suffix)
                    expected = self.world(number)
                    expected.choose(event, suffix)
                    self.assertEqual(world.reward_state(), expected.reward_state())
                    reward = world.reward_state()
                    world.country.capitulated = False
                    world.choose(event, 'a')
                    world.choose(event, 'b')
                    self.assertEqual(world.reward_state(), reward)

    def test_open_laboratory_offers_one_industry_bonus_or_civic_rewards_without_slots(self):
        for suffix in ('a', 'b'):
            with self.subTest(choice=suffix):
                event, world = self.event(4), self.world(4)
                world.country.leader = 'a_different_ruler'
                world.country.government = 'democratic'
                self.assertTrue(world.open_event(event))
                world.choose(event, suffix)
                self.assertEqual(world.country.research_slots, 4)
                self.assertEqual(world.country.ideas, set())
                if suffix == 'a':
                    self.assertEqual(len(world.country.tech_bonuses), 1)
                    self.assertEqual(dict(world.country.tech_bonuses[0]), {
                        'name': 'WFL_community_industrieforschung', 'bonus': '1.0',
                        'uses': '1', 'category': 'industry',
                    })
                    self.assertEqual(world.country.political_power, 0)
                    self.assertEqual(world.country.stability, Decimal('0.50'))
                else:
                    self.assertEqual(world.country.tech_bonuses, [])
                    self.assertEqual(world.country.political_power, 100)
                    self.assertEqual(world.country.stability, Decimal('0.55'))
                expected = world.reward_state()
                world.choose(event, 'a')
                world.choose(event, 'b')
                self.assertEqual(world.reward_state(), expected)

    def test_fixture_rejects_unknown_effects_and_conditions(self):
        world = self.world(1)
        with self.assertRaisesRegex(AssertionError, 'Unknown community condition'):
            world.conditions([Node('unmodelled_condition', 'yes')])
        with self.assertRaisesRegex(AssertionError, 'Unknown community effect'):
            world.effects([Node('unmodelled_effect', 'yes')])


if __name__ == '__main__':
    unittest.main()
