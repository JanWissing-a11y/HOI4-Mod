"""Static behaviour and installed-source checks for political advisor upgrades.

Vanilla's remove_trait/add_trait approach is exercised against simplified hired
advisor state. This does not simulate Clausewitz modifier recalculation.
"""

import json
import os
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))
SOURCE_UPGRADES = {
    '01': 'GER_secretary_of_state_security',
    '02': 'GER_militant_communist',
    '03': 'GER_stakhonovite_collectivist2',
    '04': 'GER_staunch_stalinist',
    '05': 'GER_staunch_socialist',
    '06': 'head_of_the_abwehr_improved',
    '07': 'intelligence_service_deputy',
    '08': 'GER_minister_of_the_colonies_2',
}


def block(node, key):
    return children(next(part for part in children(node) if part.key == key))


class AdvisorWorld:
    def __init__(self, decision):
        removal = next(node for node in walk(children(decision)) if node.key == 'remove_trait')
        self.advisor = field(removal, 'character')
        self.recruited = {self.advisor, 'another_advisor', 'third_advisor'}
        self.hired = set(self.recruited)
        self.roles = {self.advisor: 'political_advisor'}
        self.traits = {self.advisor: {field(removal, 'trait')}}
        self.focuses = {'WFL_technikschule'}
        self.dlcs = {'Gotterdammerung', 'Waking the Tiger', 'La Resistance'}
        self.flags = set()
        self.agency = True
        self.government = 'neutrality'
        self.political_power = 500

    def conditions(self, nodes, character=None):
        for node in nodes:
            key, value = node.key, node.value
            if key == 'NOT':
                matches = not self.conditions(children(node), character)
            elif key == 'has_completed_focus':
                matches = value in self.focuses
            elif key == 'has_character':
                matches = value in self.recruited
            elif key.startswith('WFL_advisor_'):
                matches = self.conditions(children(node), key)
            elif key == 'has_advisor_role':
                matches = self.roles.get(character) == value
            elif key == 'is_hired_as_advisor':
                matches = (character in self.hired) == (value == 'yes')
            elif key == 'has_country_flag':
                matches = value in self.flags
            elif key == 'has_dlc':
                matches = value in self.dlcs
            elif key == 'has_intelligence_agency':
                matches = self.agency == (value == 'yes')
            elif key == 'has_government':
                matches = self.government == value
            else:
                raise AssertionError(f'unsupported condition: {key}')
            if not matches:
                return False
        return True

    def effects(self, nodes):
        for node in nodes:
            if node.key == 'if':
                if self.conditions(block(node, 'limit')):
                    self.effects([part for part in children(node) if part.key != 'limit'])
            elif node.key in ('remove_trait', 'add_trait'):
                self.assert_political_slot(node)
                traits = self.traits[field(node, 'character')]
                if node.key == 'remove_trait':
                    traits.discard(field(node, 'trait'))
                else:
                    traits.add(field(node, 'trait'))
            elif node.key == 'set_country_flag':
                self.flags.add(node.value)
            else:
                raise AssertionError(f'unsupported effect: {node.key}')

    @staticmethod
    def assert_political_slot(node):
        if field(node, 'slot') != 'political_advisor':
            raise AssertionError('upgrade changes a non-political advisor slot')

    def use(self, decision):
        if not self.conditions(block(decision, 'available')):
            return False
        cost = int(field(decision, 'cost'))
        if self.political_power < cost:
            return False
        self.political_power -= cost
        self.effects(block(decision, 'complete_effect'))
        return True


class AdvisorDevelopmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        decisions = parse((ROOT / 'common/decisions/WFL_advisor_development.txt').read_text(encoding='utf-8-sig'))
        cls.decisions = {node.key.rsplit('_', 1)[1]: node for group in decisions for node in children(group)}
        traits = parse((ROOT / 'common/country_leader/WFL_advisor_upgrade_traits.txt').read_text(encoding='utf-8-sig'))
        cls.traits = {node.key: node for group in traits for node in children(group)}

    def test_all_eight_replace_traits_without_changing_hired_slots(self):
        self.assertEqual(set(self.decisions), set(SOURCE_UPGRADES))
        for number, decision in self.decisions.items():
            with self.subTest(upgrade=number):
                world = AdvisorWorld(decision)
                hired_before = set(world.hired)
                self.assertTrue(world.use(decision))
                self.assertEqual(world.traits[world.advisor], {'WFL_advisor_upgrade_' + number})
                self.assertEqual(world.hired, hired_before)
                self.assertEqual(world.political_power, 400)
                self.assertFalse(world.use(decision))
                self.assertEqual(world.political_power, 400)
                self.assertEqual(world.traits[world.advisor], {'WFL_advisor_upgrade_' + number})
                self.assertEqual(field(decision, 'fire_only_once'), 'yes')

    def test_missing_recruitment_job_role_or_school_cannot_apply_an_upgrade(self):
        for number, decision in self.decisions.items():
            for situation in ('unrecruited', 'not_hired', 'wrong_slot', 'no_school'):
                with self.subTest(upgrade=number, situation=situation):
                    world = AdvisorWorld(decision)
                    before = set(world.traits[world.advisor])
                    if situation == 'unrecruited': world.recruited.discard(world.advisor)
                    elif situation == 'not_hired': world.hired.discard(world.advisor)
                    elif situation == 'wrong_slot': world.roles[world.advisor] = 'high_command'
                    else: world.focuses.clear()
                    self.assertFalse(world.use(decision))
                    # Also recheck the actual reward's guards after conditions change.
                    world.effects(block(decision, 'complete_effect'))
                    self.assertEqual(world.traits[world.advisor], before)
                    self.assertEqual(world.political_power, 500)
                    self.assertEqual(world.flags, set())

    def test_each_required_dlc_is_enforced(self):
        for number, decision in self.decisions.items():
            required = {node.value for node in block(decision, 'available') if node.key == 'has_dlc'}
            self.assertIn('Gotterdammerung', required)
            for dlc in required:
                with self.subTest(upgrade=number, missing=dlc):
                    world = AdvisorWorld(decision)
                    world.dlcs.remove(dlc)
                    self.assertFalse(world.use(decision))
                    self.assertEqual(world.political_power, 500)
                    self.assertEqual(world.flags, set())

    def test_intelligence_upgrades_require_an_existing_agency(self):
        for number in ('01', '06', '07'):
            world = AdvisorWorld(self.decisions[number])
            world.agency = False
            self.assertFalse(world.use(self.decisions[number]))

    def test_democratic_reformer_role_condition_is_preserved(self):
        world = AdvisorWorld(self.decisions['05'])
        world.government = 'democratic'
        self.assertFalse(world.use(self.decisions['05']))
        self.assertEqual(world.political_power, 500)
        characters = parse((ROOT / 'common/characters/WFL_advisors.txt').read_text(encoding='utf-8-sig'))
        advisor = next(node for group in characters for node in children(group) if node.key == world.advisor)
        role = next(node for node in children(advisor) if node.key == 'advisor')
        condition = block(role, 'do_effect')
        self.assertEqual(len(condition), 1)
        self.assertEqual(condition[0].key, 'NOT')
        self.assertTrue(any(node.key == 'has_government' and node.value == 'democratic'
                            for node in children(condition[0])))

    def test_updates_do_not_recreate_roles_or_reference_german_characters(self):
        forbidden = {'add_advisor_role', 'remove_advisor_role', 'recruit_character', 'retire_character',
                     'promote_character', 'add_ideas', 'remove_ideas'}
        for decision in self.decisions.values():
            for node in walk(children(decision)):
                self.assertNotIn(node.key, forbidden)
                self.assertFalse(node.key.startswith('GER_'))
                if isinstance(node.value, str):
                    self.assertFalse(node.value.startswith('GER_'))

    def test_base_trait_mapping_matches_the_existing_manifest(self):
        manifest = json.loads((ROOT / 'tools/data/WFL_advisors.json').read_text(encoding='utf-8-sig'))
        advisors = {entry['id']: entry for entry in manifest['advisors']}
        for number, decision in self.decisions.items():
            removal = next(node for node in walk(children(decision)) if node.key == 'remove_trait')
            base = advisors[field(removal, 'character')]
            allowed_old_traits = {role['trait'] for role in base['roles']}
            self.assertIn(field(removal, 'trait'), allowed_old_traits)
            if number == '02':
                role = next(role for role in base['roles'] if role['trait'] == field(removal, 'trait'))
                self.assertEqual(role['source_trait'], 'GER_proletarian_leader')

    @unittest.skipUnless((GAME_ROOT / 'common/country_leader/00_traits.txt').is_file(), 'local HoI4 installation required')
    def test_all_upgrade_values_and_drawbacks_match_installed_vanilla_exactly(self):
        sources = {node.key: node for group in parse((GAME_ROOT / 'common/country_leader/00_traits.txt').read_text(encoding='utf-8-sig'))
                   for node in children(group)}
        for number, source_id in SOURCE_UPGRADES.items():
            with self.subTest(upgrade=number):
                own = self.traits['WFL_advisor_upgrade_' + number]
                self.assertEqual(children(own), children(sources[source_id]))


if __name__ == '__main__':
    unittest.main()
