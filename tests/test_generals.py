"""User-confirmed named generals, starting roles and vanilla commander compatibility."""
import json
import os
from pathlib import Path
import struct
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))
EXPECTED = {
    'WFL_ian_jannis_foerster': ('Ian Jannis Foerster', 'Porträt eines festlichen Uniformträgers.png'),
    'WFL_nils_schapfeld_i': ('Nils Schapfeld I.', 'Feierliches Porträt im grünen Ordensornat.png'),
    'WFL_lars_stuewe': ('Lars Stüwe', 'Lächelnder Offizier im grünen Ehrenuniform-Look.png'),
}


def block(node, key):
    return next(part for part in children(node) if part.key == key)


class GeneralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.characters = {n.key: n for n in children(parse(
            (ROOT / 'common/characters/WFL_generals.txt').read_text(encoding='utf-8-sig'))[0])}
        cls.roles = {key: block(char, 'corps_commander') for key, char in cls.characters.items()}

    def test_generals_are_recruited_once_and_do_not_replace_the_government_or_marshal(self):
        self.assertEqual(set(self.characters), set(EXPECTED))
        history = parse((ROOT / 'history/countries/WFL - Wesel-Flueren.txt').read_text(encoding='utf-8-sig'))
        for key, char in self.characters.items():
            with self.subTest(character=key):
                self.assertEqual(field(char, 'name'), key)
                self.assertFalse(any(n.key in ('field_marshal', 'country_leader', 'advisor')
                                     for n in children(char)))
                self.assertEqual(sum(n.key == 'recruit_character' and n.value == key for n in history), 1)
                for language in ('german', 'english'):
                    raw = (ROOT / f'localisation/{language}/WFL_commanders_l_{language}.yml').read_bytes()
                    self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
                    self.assertIn(f'{key}:0 "{EXPECTED[key][0]}"', raw.decode('utf-8-sig'))
        self.assertEqual([n.value for n in history if n.key == 'promote_character'], ['WFL_schuetzenkoenig'])
        self.assertEqual(sum(n.key == 'recruit_character' and n.value == 'WFL_lukas_hoehne_i'
                             for n in history), 1)

    def test_confirmed_source_portraits_connect_to_each_general_in_both_sizes(self):
        manifest = json.loads((ROOT / 'tools/data/commander_portraits.json').read_text(encoding='utf-8-sig'))
        entries = {n['id']: n for n in manifest['portraits']}
        self.assertEqual(set(entries), set(EXPECTED))
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(parse((ROOT / 'interface/WFL_commanders.gfx').read_text()))
                   if n.key == 'spriteType'}
        for key, char in self.characters.items():
            entry = entries[key]
            self.assertEqual((entry['name'], entry['file']), EXPECTED[key])
            portraits = block(block(char, 'portraits'), 'army')
            for size, asset, dimensions in (('large', 'output', (156, 210)),
                                             ('small', 'small_output', (65, 67))):
                with self.subTest(character=key, size=size):
                    texture = sprites[field(portraits, size)]
                    self.assertEqual(texture, entry[asset])
                    raw = (ROOT / texture).read_bytes()
                    self.assertEqual(raw[:4], b'DDS ')
                    height, width = struct.unpack_from('<II', raw, 12)
                    self.assertEqual((width, height), dimensions)
                    self.assertEqual(len(raw), 128 + width * height * 4)
            self.assertTrue((ROOT / entry['preview']).is_file())

    def test_strong_generals_have_distinct_military_specialties(self):
        keys = ('attack_skill', 'defense_skill', 'planning_skill', 'logistics_skill')
        for role in self.roles.values():
            self.assertGreaterEqual(int(field(role, 'skill')), 8)
            self.assertTrue(all(7 <= int(field(role, key)) <= 9 for key in keys))
        self.assertEqual(field(self.roles['WFL_ian_jannis_foerster'], 'planning_skill'), '9')
        self.assertEqual(field(self.roles['WFL_nils_schapfeld_i'], 'defense_skill'), '9')
        self.assertEqual(field(self.roles['WFL_nils_schapfeld_i'], 'logistics_skill'), '9')
        self.assertEqual(field(self.roles['WFL_lars_stuewe'], 'attack_skill'), '9')
        selected = {key: {n.key for n in children(block(role, 'traits'))}
                    for key, role in self.roles.items()}
        self.assertIn('fortress_buster', selected['WFL_ian_jannis_foerster'])
        self.assertIn('ambusher', selected['WFL_nils_schapfeld_i'])
        self.assertIn('panzer_expert', selected['WFL_lars_stuewe'])

    @unittest.skipUnless((GAME / 'common/unit_leader/00_traits.txt').is_file(), 'local game required')
    def test_selected_traits_are_valid_for_generals_with_parents_and_no_conflicts(self):
        vanilla = {n.key: n for group in parse((GAME / 'common/unit_leader/00_traits.txt')
                                              .read_text(encoding='utf-8-sig')) for n in children(group)}
        for char, role in self.roles.items():
            selected = {n.key for n in children(block(role, 'traits'))}
            for key in selected:
                with self.subTest(character=char, trait=key):
                    self.assertIn(key, vanilla)
                    definition = vanilla[key]
                    self.assertIn(field(definition, 'type'), ('land', 'corps_commander'))
                    for dependency in children(definition):
                        if dependency.key == 'mutually_exclusive':
                            self.assertNotIn(dependency.value, selected)
                        elif dependency.key == 'any_parent':
                            self.assertTrue({n.key for n in children(dependency)} & selected)
                        elif dependency.key == 'all_parents':
                            self.assertTrue({n.key for n in children(dependency)} <= selected)
                        elif dependency.key == 'parent':
                            parents = {n.key for n in children(block(dependency, 'traits'))}
                            self.assertGreaterEqual(len(parents & selected),
                                                    int(field(dependency, 'num_parents_needed')))

    @unittest.skipUnless((GAME / 'common/unit_leader/00_skills.txt').is_file(), 'local game required')
    def test_each_skill_value_exists_in_vanilla_for_corps_commanders(self):
        files = {'skill': '00_skills.txt', 'attack_skill': '00_attack_skills.txt',
                 'defense_skill': '00_defense_skills.txt', 'planning_skill': '00_planning_skills.txt',
                 'logistics_skill': '00_logistics_skills.txt'}
        for key, filename in files.items():
            supported = {n.key for group in parse((GAME / 'common/unit_leader' / filename)
                                                 .read_text(encoding='utf-8-sig')) for n in children(group)
                         if field(n, 'type') == 'corps_commander'}
            for char, role in self.roles.items():
                with self.subTest(character=char, skill=key):
                    self.assertIn(field(role, key), supported)


if __name__ == '__main__':
    unittest.main()
