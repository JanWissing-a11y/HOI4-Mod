"""The named economic advisor is hireable and uses the supplied portrait."""
from pathlib import Path
import struct
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
ADVISOR = 'WFL_florian_klaus'
TRAIT = 'WFL_wirtschaftsstratege_mit_ruhiger_hand'


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


class FlorianKlausTests(unittest.TestCase):
    def test_paid_political_advisor_is_available_from_start_with_economic_and_stability_bonuses(self):
        character = children(read('common/characters/WFL_florian_klaus.txt')[0])[0]
        self.assertEqual(character.key, ADVISOR)
        self.assertFalse({'country_leader', 'corps_commander', 'field_marshal'}
                         & {n.key for n in children(character)})
        role = next(n for n in children(character) if n.key == 'advisor')
        self.assertEqual(field(role, 'slot'), 'political_advisor')
        self.assertEqual(field(role, 'cost'), '150')
        allowed = next(n for n in children(role) if n.key == 'allowed')
        self.assertEqual(field(allowed, 'original_tag'), 'WFL')
        self.assertFalse({'available', 'visible', 'do_effect'} & {n.key for n in children(role)})
        self.assertEqual([n.key for n in children(next(n for n in children(role) if n.key == 'traits'))], [TRAIT])
        history = read('history/countries/WFL - Wesel-Flueren.txt')
        self.assertEqual(sum(n.key == 'recruit_character' and n.value == ADVISOR for n in history), 1)
        self.assertFalse(any(n.key == 'add_ideas' and n.value == ADVISOR for n in walk(history)))
        trait = children(read('common/country_leader/WFL_florian_klaus_traits.txt')[0])[0]
        self.assertEqual(trait.key, TRAIT)
        effects = {n.key: float(n.value) for n in children(trait) if n.key not in ('random', 'sprite')}
        self.assertEqual(effects, {'production_speed_industrial_complex_factor': .20,
                                  'production_speed_arms_factory_factor': .20,
                                  'industrial_capacity_factory': .15, 'stability_factor': .10})

    def test_name_and_both_portrait_sizes_are_connected(self):
        character = children(read('common/characters/WFL_florian_klaus.txt')[0])[0]
        portraits = next(n for n in children(character) if n.key == 'portraits')
        civilian = next(n for n in children(portraits) if n.key == 'civilian')
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(read('interface/WFL_florian_klaus.gfx')) if n.key == 'spriteType'}
        for size, dimensions in [('large', (156, 210)), ('small', (65, 67))]:
            data = (ROOT / sprites[field(civilian, size)]).read_bytes()
            self.assertEqual(data[:4], b'DDS ')
            height, width = struct.unpack_from('<II', data, 12)
            self.assertEqual((width, height), dimensions)
            self.assertEqual(len(data), 128 + width * height * 4)
        for language in ('german', 'english'):
            raw = (ROOT / f'localisation/{language}/WFL_florian_klaus_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertIn(f' {ADVISOR}:0 "Florian Klaus"', raw.decode('utf-8-sig'))


if __name__ == '__main__':
    unittest.main()
