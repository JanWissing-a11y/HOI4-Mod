"""Behavioural data tests for the research and aviation branches.

The small interpreter below exercises the one-time research slot reward.
It cannot replace Clausewitz engine, production UI or project tests.
"""

from dataclasses import dataclass, field as data_field
from decimal import Decimal
import os
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))


def read_script(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def child(node, key):
    return next(part for part in children(node) if part.key == key)


@dataclass
class Country:
    flags: set[str] = data_field(default_factory=set)
    research_slots: int = 3


class ResearchWorld:
    def __init__(self):
        self.country = Country()

    def conditions(self, nodes):
        for node in nodes:
            key, value = node.key, node.value
            if key == 'NOT':
                matches = not self.conditions(children(node))
            elif key == 'has_country_flag':
                matches = value in self.country.flags
            else:
                raise AssertionError(f'Unsupported condition: {key}')
            if not matches:
                return False
        return True

    def effects(self, nodes):
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                if self.conditions(children(child(node, 'limit'))):
                    self.effects([part for part in children(node) if part.key != 'limit'])
            elif key == 'set_country_flag':
                self.country.flags.add(value)
            elif key == 'add_research_slot':
                self.country.research_slots += int(value)
            else:
                raise AssertionError(f'Unsupported effect: {key}')


class FocusExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = read_script('common/national_focus/WFL_focus.txt')[0]
        cls.focuses = {field(node, 'id'): node for node in children(tree) if node.key == 'focus'}
        ideas = read_script('common/ideas/WFL_focus_expansion_ideas.txt')[0]
        cls.ideas = {node.key: node for node in children(child(ideas, 'country'))}

    def test_extra_slot_is_exactly_one_and_cannot_repeat(self):
        world = ResearchWorld()
        reward = children(child(self.focuses['WFL_zusaetzlicher_forschungsrat'], 'completion_reward'))
        world.effects(reward)
        self.assertEqual(world.country.research_slots, 4)
        world.effects(reward)
        self.assertEqual(world.country.research_slots, 4)

    def test_nuclear_bonus_targets_nuclear_projects_only(self):
        idea = self.ideas['WFL_auesee_atomoffensive']
        research = child(idea, 'research_bonus')
        self.assertEqual(field(research, 'nuclear'), '3.0')
        modifiers = {node.key: node.value for node in children(child(idea, 'modifier'))}
        project_modifiers = {key: value for key, value in modifiers.items() if key.startswith('sp_')}
        self.assertEqual(set(project_modifiers), {
            'sp_nuclear_reactor_speed_factor', 'sp_nuclear_bomb_speed_factor',
            'sp_thermo_nuclear_bomb_speed_factor', 'sp_nuclear_warheads_speed_factor'})
        self.assertTrue(all(Decimal(value) == 4 for value in project_modifiers.values()))
        self.assertNotIn('special_project_speed_factor', modifiers)
        self.assertFalse(any(node.key in ('complete_special_project', 'add_nuclear_bombs')
                             for node in walk(children(idea))))

    @unittest.skipUnless((GAME_ROOT / 'common/units/equipment').is_dir(), 'local HoI4 installation required')
    def test_all_installed_aircraft_and_carrier_variants_have_triple_base_throughput(self):
        # Read actual game definitions rather than reproducing the idea's list.
        files = ('plane_airframes.txt', 'x_plane_airframes.txt', 'quad_engine_airframe.txt',
                 'intercontinental_bomber.txt', 'mothership.txt')
        catalog = {}
        for filename in files:
            for group in parse((GAME_ROOT / 'common/units/equipment' / filename).read_text(encoding='utf-8-sig')):
                catalog.update((node.key, node) for node in children(group))
        bonus = child(self.ideas['WFL_dreifache_flugzeugfertigung'], 'equipment_bonus')
        bonuses = {node.key: node for node in children(bonus)}
        self.assertTrue(set(bonuses) <= set(catalog), 'non-air equipment or unknown bonus target')
        self.assertEqual(len(bonuses), 20)
        for equipment, node in catalog.items():
            with self.subTest(equipment=equipment):
                seen = set()
                current = equipment
                while current not in bonuses:
                    self.assertNotIn(current, seen, 'cyclic equipment ancestry')
                    seen.add(current)
                    parent = catalog[current]
                    current = field(parent, 'archetype') or field(parent, 'parent')
                    self.assertIsNotNone(current, f'no production bonus for {equipment}')
                reduction = Decimal(field(bonuses[current], 'build_cost_ic'))
                throughput = Decimal(1) / (Decimal(1) + reduction)
                self.assertAlmostEqual(float(throughput), 3.0, places=6)
                self.assertEqual(field(bonuses[current], 'instant'), 'yes')
        self.assertFalse(any(node.key == 'modifier' for node in children(self.ideas['WFL_dreifache_flugzeugfertigung'])))


if __name__ == '__main__':
    unittest.main()
