"""Resolve the actual DLC branches and verify their usable vanilla unlocks."""
import os
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))


def block(node, key):
    return next(n for n in children(node) if n.key == key)


def starting_techs(has_bba):
    source = parse((ROOT / 'history/countries/WFL - Wesel-Flueren.txt')
                   .read_text(encoding='utf-8-sig'))
    techs = set()

    def condition(nodes):
        for node in nodes:
            if node.key == 'has_dlc':
                if node.value != 'By Blood Alone':
                    raise AssertionError('Unexpected DLC condition: ' + node.value)
                matches = has_bba
            elif node.key == 'NOT':
                matches = not condition(children(node))
            else:
                raise AssertionError('Unexpected startup condition: ' + node.key)
            if not matches:
                return False
        return True

    def apply(nodes):
        for node in nodes:
            if node.key == 'set_technology':
                techs.update(n.key for n in children(node) if n.value == '1')
            elif node.key == 'if':
                if condition(children(block(node, 'limit'))):
                    apply([n for n in children(node) if n.key != 'limit'])

    apply(source)
    return techs


class StartingAirTechTests(unittest.TestCase):
    def test_designer_and_legacy_branches_have_their_own_light_aircraft(self):
        designer = starting_techs(True)
        legacy = starting_techs(False)
        self.assertTrue({'iw_small_airframe', 'basic_small_airframe', 'aa_lmg',
                         'engines_1', 'engines_2'} <= designer)
        self.assertTrue({'early_fighter', 'fighter1'} <= legacy)
        self.assertNotIn('fighter1', designer)
        self.assertNotIn('basic_small_airframe', legacy)
        self.assertNotIn('aa_lmg', legacy)
        self.assertNotIn('small_plane_airframe_1', designer)  # Equipment, not tech.
        for techs in (designer, legacy):
            self.assertTrue({'paratroopers', 'infantry_weapons', 'infantry_weapons1'} <= techs)
            self.assertNotIn('improved_small_airframe', techs)
            self.assertNotIn('aa_hmg', techs)

    @unittest.skipUnless((GAME_ROOT / 'common/technologies/bba_air_techs.txt').is_file(),
                         'local HoI4 installation required')
    def test_local_vanilla_technology_ids_unlock_airframes_guns_and_engines(self):
        designer = parse((GAME_ROOT / 'common/technologies/bba_air_techs.txt')
                         .read_text(encoding='utf-8-sig'))[0]
        legacy = parse((GAME_ROOT / 'common/technologies/air_techs.txt')
                       .read_text(encoding='utf-8-sig'))[0]
        by_id = {n.key: n for n in children(designer)}
        legacy_by_id = {n.key: n for n in children(legacy)}
        required = {
            'iw_small_airframe': ('enable_equipments', 'small_plane_airframe_0'),
            'basic_small_airframe': ('enable_equipments', 'small_plane_airframe_1'),
            'aa_lmg': ('enable_equipment_modules', 'light_mg_2x'),
            'engines_1': ('enable_equipment_modules', 'engine_1_1x'),
            'engines_2': ('enable_equipment_modules', 'engine_2_1x'),
        }
        for tech, (kind, unlocked) in required.items():
            with self.subTest(tech=tech):
                self.assertIn(tech, starting_techs(True))
                self.assertIn(unlocked, {n.key for n in children(block(by_id[tech], kind))})
        self.assertEqual(field(by_id['basic_small_airframe'], 'start_year'), '1936')
        self.assertIn('fighter_equipment_1', {n.key for n in children(
            block(legacy_by_id['fighter1'], 'enable_equipments'))})


if __name__ == '__main__':
    unittest.main()
