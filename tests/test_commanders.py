"""Named starting field marshal, portrait assets and compatible vanilla traits."""
import os
from pathlib import Path
import re
import struct
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))
LUKAS = 'WFL_lukas_hoehne_i'


def block(node, key):
    return next(part for part in children(node) if part.key == key)


class CommanderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.character = children(parse((ROOT / 'common/characters/WFL_lukas_hoehne.txt')
                                       .read_text(encoding='utf-8-sig'))[0])[0]
        cls.role = block(cls.character, 'field_marshal')

    def test_named_marshal_starts_recruited_without_changing_jans_government(self):
        self.assertEqual(self.character.key, LUKAS)
        self.assertEqual(field(self.character, 'name'), LUKAS)
        self.assertFalse(any(n.key in ('country_leader', 'advisor', 'corps_commander')
                             for n in children(self.character)))
        history = parse((ROOT / 'history/countries/WFL - Wesel-Flueren.txt').read_text(encoding='utf-8-sig'))
        self.assertEqual(sum(n.key == 'recruit_character' and n.value == LUKAS for n in history), 1)
        self.assertEqual([n.value for n in history if n.key == 'promote_character'], ['WFL_schuetzenkoenig'])
        for lang in ('german', 'english'):
            raw = (ROOT / f'localisation/{lang}/WFL_commanders_l_{lang}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertIn(f'{LUKAS}:0 "Lukas Höhne I."', raw.decode('utf-8-sig'))

    def test_exceptional_stats_and_both_portrait_sizes_are_connected(self):
        for key in ('skill', 'attack_skill', 'defense_skill', 'planning_skill', 'logistics_skill'):
            self.assertEqual(field(self.role, key), '9')
        portraits = block(block(self.character, 'portraits'), 'army')
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(parse((ROOT / 'interface/WFL_commanders.gfx').read_text()))
                   if n.key == 'spriteType'}
        for size, dimensions in (('large', (156, 210)), ('small', (65, 67))):
            sprite = field(portraits, size)
            raw = (ROOT / sprites[sprite]).read_bytes()
            self.assertEqual(raw[:4], b'DDS ')
            height, width = struct.unpack_from('<II', raw, 12)
            self.assertEqual((width, height), dimensions)
            self.assertEqual(len(raw), 128 + width * height * 4)

    @unittest.skipUnless((GAME / 'common/unit_leader/00_traits.txt').is_file(), 'local game required')
    def test_traits_exist_have_required_parents_and_do_not_exclude_each_other(self):
        groups = parse((GAME / 'common/unit_leader/00_traits.txt').read_text(encoding='utf-8-sig'))
        vanilla = {n.key: n for group in groups for n in children(group)}
        selected = {n.key for n in children(block(self.role, 'traits'))}
        self.assertEqual(len(selected), 7)
        for key in selected:
            self.assertIn(key, vanilla)
            definition = vanilla[key]
            self.assertIn(field(definition, 'type'), ('field_marshal', 'land', 'corps_commander'))
            self.assertNotIn(field(definition, 'mutually_exclusive'), selected)
            for parent in children(definition):
                if parent.key == 'any_parent':
                    self.assertTrue({n.key for n in children(parent)} & selected, key)
        self.assertIn('logistics_wizard', selected)
        self.assertIn('inspirational_leader', selected)

    @unittest.skipUnless((GAME / 'common/unit_leader/00_skills.txt').is_file(), 'local game required')
    def test_all_five_skill_levels_are_defined_for_field_marshals(self):
        files = {'skill': '00_skills.txt', 'attack_skill': '00_attack_skills.txt',
                 'defense_skill': '00_defense_skills.txt', 'planning_skill': '00_planning_skills.txt',
                 'logistics_skill': '00_logistics_skills.txt'}
        for key, filename in files.items():
            nodes = parse((GAME / 'common/unit_leader' / filename).read_text(encoding='utf-8-sig'))
            supported = {n.key for group in nodes for n in children(group)
                         if field(n, 'type') == 'field_marshal'}
            self.assertIn(field(self.role, key), supported, filename)


if __name__ == '__main__':
    unittest.main()
