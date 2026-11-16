"""Static execution of the small scope subset used by WFL's expansion scripts.

These tests exercise the actual parsed rewards against changed owners and war
states. They do not validate Clausewitz engine semantics or replace game tests.
"""

from dataclasses import dataclass, field as data_field
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Country:
    tag: str
    faction: str | None = None
    overlord: str | None = None
    wars: set[str] = data_field(default_factory=set)
    flags: set[str] = data_field(default_factory=set)
    capitulated: bool = False


@dataclass
class State:
    owner: str
    controller: str
    cores: set[str] = data_field(default_factory=set)
    partial_control: bool = False


class ScopeFixture:
    """Deliberately limited evaluator; unknown conditions/effects fail loudly."""

    def __init__(self):
        self.countries = {tag: Country(tag) for tag in ('WFL', 'GER', 'HOL')}
        self.root = self.countries['WFL']
        self.states = {51: State('GER', 'GER'), 57: State('GER', 'GER')}
        self.goals = []
        self.political_power = 0

    def target(self, value, stack):
        if value == 'ROOT':
            return self.root
        if value == 'PREV':
            return stack[-2]
        return self.countries[value]

    def scope(self, key, stack):
        if key.isdigit():
            return self.states[int(key)]
        if key == 'owner':
            return self.countries[stack[-1].owner]
        if key == 'ROOT':
            return self.root
        raise AssertionError(f'unsupported scope: {key}')

    def conditions(self, nodes, stack):
        current = stack[-1]
        for node in nodes:
            key, value = node.key, node.value
            if key == 'NOT':
                matches = not self.conditions(children(node), stack)
            elif key.isdigit() or key in ('owner', 'ROOT'):
                matches = self.conditions(children(node), stack + [self.scope(key, stack)])
            elif key in ('is_owned_by', 'is_controlled_by', 'is_fully_controlled_by', 'is_core_of'):
                tag = self.target(value, stack).tag
                matches = (current.owner == tag if key == 'is_owned_by' else
                           current.controller == tag if key == 'is_controlled_by' else
                           current.controller == tag and not current.partial_control
                           if key == 'is_fully_controlled_by' else
                           tag in current.cores)
            elif key == 'has_war':
                matches = bool(current.wars) == (value == 'yes')
            elif key == 'has_capitulated':
                matches = current.capitulated == (value == 'yes')
            elif key == 'is_subject':
                matches = (current.overlord is not None) == (value == 'yes')
            elif key == 'has_country_flag':
                matches = value in current.flags
            elif key == 'is_in_faction_with':
                matches = current.faction is not None and current.faction == self.target(value, stack).faction
            elif key == 'is_subject_of':
                matches = current.overlord == self.target(value, stack).tag
            elif key == 'has_war_with':
                matches = self.target(value, stack).tag in current.wars
            else:
                raise AssertionError(f'unsupported condition: {key}')
            if not matches:
                return False
        return True

    def effects(self, nodes, stack=None):
        stack = stack or [self.root]
        preceding_if = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                limit = next(n for n in children(node) if n.key == 'limit')
                preceding_if = self.conditions(children(limit), stack)
                if preceding_if:
                    self.effects([n for n in children(node) if n.key != 'limit'], stack)
            elif key == 'else':
                if preceding_if is False:
                    self.effects(children(node), stack)
            elif key.isdigit() or key in ('owner', 'ROOT'):
                self.effects(children(node), stack + [self.scope(key, stack)])
            elif key == 'create_wargoal':
                generator = next(n for n in children(node) if n.key == 'generator')
                self.goals.append((stack[-1].tag, self.target(field(node, 'target'), stack).tag,
                                   tuple(int(n.key) for n in children(generator))))
            elif key == 'add_political_power':
                self.political_power += int(value)
            elif key == 'add_state_core':
                self.states[int(value)].cores.add(stack[-1].tag)
            elif key == 'set_country_flag':
                stack[-1].flags.add(value)
            else:
                raise AssertionError(f'unsupported effect: {key}')


class ExpansionSafetyTests(unittest.TestCase):
    def setUp(self):
        tree = parse((ROOT / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig'))[0]
        self.focuses = {field(n, 'id'): n for n in children(tree) if n.key == 'focus'}
        category = parse((ROOT / 'common/decisions/WFL_decisions.txt').read_text(encoding='utf-8-sig'))[0]
        self.decisions = {n.key: n for n in children(category)}

    def block(self, node, key):
        return children(next(n for n in children(node) if n.key == key))

    def test_wargoal_resolves_current_owner_for_each_region(self):
        for state, focus in ((51, 'WFL_rheinland_fordern'), (57, 'WFL_westfalen_fordern')):
            for owner in ('GER', 'HOL'):
                with self.subTest(state=state, owner=owner):
                    world = ScopeFixture()
                    world.states[state].owner = owner
                    world.effects(self.block(self.focuses[focus], 'completion_reward'))
                    self.assertEqual(world.goals, [('WFL', owner, (state,))])
                    self.assertEqual(world.states[state].owner, owner)

    def test_invalid_wargoal_targets_receive_no_wargoal(self):
        for situation in ('owned', 'allied', 'subject', 'already_at_war', 'not_sovereign', 'capitulated'):
            with self.subTest(situation=situation):
                world = ScopeFixture()
                if situation == 'owned':
                    world.states[51].owner = 'WFL'
                elif situation == 'allied':
                    world.root.faction = world.countries['GER'].faction = 'test_faction'
                elif situation == 'subject':
                    world.countries['GER'].overlord = 'WFL'
                elif situation == 'already_at_war':
                    world.countries['GER'].wars.add('WFL')
                elif situation == 'not_sovereign':
                    world.root.overlord = 'HOL'
                else:
                    world.root.capitulated = True
                world.effects(self.block(self.focuses['WFL_rheinland_fordern'], 'completion_reward'))
                self.assertEqual(world.goals, [])
                self.assertEqual(world.political_power, 50)

    def test_integration_requires_ownership_control_and_peace(self):
        for state, decision in ((51, 'WFL_rheinland_integrieren'), (57, 'WFL_westfalen_integrieren')):
            for situation in ('occupied_only', 'lost_control', 'partial_control', 'war', 'valid', 'already_core'):
                with self.subTest(state=state, situation=situation):
                    world = ScopeFixture()
                    target = world.states[state]
                    target.owner = target.controller = 'WFL'
                    if situation == 'occupied_only':
                        target.owner = 'GER'
                    elif situation == 'lost_control':
                        target.controller = 'GER'
                    elif situation == 'partial_control':
                        target.partial_control = True
                    elif situation == 'war':
                        world.root.wars.add('GER')
                    elif situation == 'already_core':
                        target.cores.add('WFL')
                    available = world.conditions(self.block(self.decisions[decision], 'available'), [world.root])
                    self.assertEqual(available, situation == 'valid')
                    world.effects(self.block(self.decisions[decision], 'complete_effect'))
                    self.assertEqual('WFL' in target.cores, situation in ('valid', 'already_core'))
                    self.assertEqual(bool(world.root.flags), situation == 'valid')

    def test_union_accepts_peacefully_acquired_cores(self):
        world = ScopeFixture()
        for target in world.states.values():
            target.owner = target.controller = 'WFL'
            target.cores.add('WFL')
        available = self.block(self.focuses['WFL_niederrheinunion'], 'available')
        self.assertTrue(world.conditions(available, [world.root]))
        world.states[57].controller = 'HOL'
        self.assertFalse(world.conditions(available, [world.root]))


if __name__ == '__main__':
    unittest.main()
