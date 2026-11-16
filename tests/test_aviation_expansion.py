"""Römerwardt's training branch uses real country modifiers without more IC discounts."""

import os
import json
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))
IDEAS_FILE = ROOT / 'common/ideas/WFL_aviation_expansion_ideas.txt'
FOCUS_CHAIN = (
    'WFL_roemerwardt_ausbauen',
    'WFL_roemerwardt_flugschule',
    'WFL_roemerwardt_luftfahrtwerkstaetten',
    'WFL_roemerwardt_luftwaffenakademie',
)


def block(node, key):
    return next(part for part in children(node) if part.key == key)


class AviationExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ideas = children(block(parse(IDEAS_FILE.read_text(encoding='utf-8-sig'))[0], 'country'))

    def test_aviation_ideas_are_permanent_and_country_specific(self):
        self.assertEqual(len(self.ideas), 3)
        for idea in self.ideas:
            with self.subTest(idea=idea.key):
                self.assertEqual(field(block(idea, 'allowed'), 'tag'), 'WFL')
                self.assertEqual(field(idea, 'removal_cost'), '-1')
                self.assertTrue(children(block(idea, 'modifier')))
                self.assertFalse(any(node.key == 'equipment_bonus' or 'build_cost' in node.key
                                     for node in walk(children(idea))))

    @unittest.skipUnless((GAME_ROOT / 'common/ideas/air_spirits.txt').is_file(),
                         'local HoI4 installation required')
    def test_every_aviation_modifier_is_used_in_installed_vanilla_ideas(self):
        vanilla_modifiers = set()
        for filename in ('air_spirits.txt', 'belgium.txt'):
            source = parse((GAME_ROOT / 'common/ideas' / filename).read_text(encoding='utf-8-sig'))
            for node in walk(source):
                if node.key == 'modifier':
                    vanilla_modifiers.update(part.key for part in children(node))
        actual = {node.key for idea in self.ideas for node in children(block(idea, 'modifier'))}
        self.assertTrue(actual <= vanilla_modifiers, actual - vanilla_modifiers)
        self.assertNotIn('air_training_xp_factor', actual)

    def test_training_branch_is_linear_and_grants_each_idea_only_at_its_own_stage(self):
        tree = parse((ROOT / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig'))[0]
        focuses = {field(node, 'id'): node for node in children(tree) if node.key == 'focus'}
        for parent, focus_id in zip(FOCUS_CHAIN, FOCUS_CHAIN[1:]):
            with self.subTest(focus=focus_id):
                focus = focuses[focus_id]
                prerequisites = [part.value for node in children(focus) if node.key == 'prerequisite'
                                 for part in children(node) if part.key == 'focus']
                self.assertEqual(prerequisites, [parent])
                rewards = children(block(focus, 'completion_reward'))
                ideas = [node.value for node in walk(rewards) if node.key == 'add_ideas']
                self.assertEqual(ideas, [focus_id + '_idee'])
                self.assertFalse(any(node.key == 'equipment_bonus' or 'build_cost' in node.key
                                     for node in walk(rewards)))

    def test_air_base_is_built_only_at_a_valid_owned_location_and_experience_is_preserved(self):
        tree = parse((ROOT / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig'))[0]
        focuses = {field(node, 'id'): node for node in children(tree) if node.key == 'focus'}
        actual_xp = [int(field(block(focuses[key], 'completion_reward'), 'air_experience'))
                     for key in FOCUS_CHAIN]
        self.assertEqual(actual_xp, [10, 35, 25, 50])
        self.assertEqual(sum(actual_xp), 120)
        recipe = json.loads((ROOT / 'tools/data/building_overrides.json').read_text())
        self.assertEqual(recipe['target_state'], 1082)
        self.assertTrue(any(line.startswith('1082;air_base;') for line in recipe['add_lines']))
        reward = children(block(focuses[FOCUS_CHAIN[0]], 'completion_reward'))
        # The simple shared parser discards comparison operators. Check the
        # real source too so reversing this guard cannot pass the simulation.
        source = (ROOT / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig')
        focus_source = source.split('id = ' + FOCUS_CHAIN[0], 1)[1].split('\n    focus = {', 1)[0]
        self.assertRegex(focus_source, r'limit\s*=\s*\{\s*air_base\s*<\s*5\s*\}')

        # Interpret only this focus's real, bounded construction subset. Unknown
        # guards/effects fail explicitly instead of silently treating them as true.
        def conditions(nodes, state):
            for node in nodes:
                key, value = node.key, node.value
                if key == '1082':
                    result = conditions(children(node), state)
                elif key == 'has_capitulated':
                    result = state['capitulated'] == (value == 'yes')
                elif key == 'is_owned_by':
                    self.assertEqual(value, 'ROOT')
                    result = state['owner'] == 'WFL'
                elif key == 'is_fully_controlled_by':
                    self.assertEqual(value, 'ROOT')
                    result = state['controller'] == 'WFL' and state['full_control']
                elif key == 'is_demilitarized_zone':
                    result = state['demilitarized'] == (value == 'yes')
                elif key == 'air_base':
                    self.assertEqual(value, '5')
                    result = state['airbase_level'] < 5
                else:
                    raise AssertionError('Unsupported air-base guard: ' + key)
                if not result:
                    return False
            return True

        def effects(nodes, state, scope='WFL'):
            preceding_if = None
            for node in nodes:
                key, value = node.key, node.value
                if key == 'if':
                    preceding_if = conditions(children(block(node, 'limit')), state)
                    if preceding_if:
                        effects([part for part in children(node) if part.key != 'limit'], state, scope)
                elif key == 'else':
                    if preceding_if is False:
                        effects(children(node), state, scope)
                elif key == '1082':
                    effects(children(node), state, '1082')
                elif key == 'air_experience':
                    state['xp'] += int(value)
                elif key == 'add_political_power':
                    state['pp'] += int(value)
                elif key == 'set_building_level':
                    self.assertEqual(scope, '1082')
                    self.assertEqual(field(node, 'type'), 'air_base')
                    self.assertEqual(field(node, 'instant_build'), 'yes')
                    state['airbase_level'] = int(field(node, 'level'))
                else:
                    raise AssertionError('Unsupported air-base effect: ' + key)

        changes = ({}, {'owner': 'GER'}, {'controller': 'GER'}, {'full_control': False},
                   {'capitulated': True}, {'demilitarized': True})
        for initial_level in (0, 1, 4, 5, 7, 10):
            for changed in changes:
                with self.subTest(initial_level=initial_level, changed=changed):
                    state = dict(owner='WFL', controller='WFL', full_control=True,
                                 capitulated=False, demilitarized=False,
                                 xp=0, pp=0, airbase_level=initial_level)
                    state.update(changed)
                    effects(reward, state)
                    self.assertEqual(state['xp'], 10)
                    self.assertEqual(state['airbase_level'], initial_level if changed else max(5, initial_level))
                    self.assertEqual(state['pp'], 50 if changed else 0)


if __name__ == '__main__':
    unittest.main()
