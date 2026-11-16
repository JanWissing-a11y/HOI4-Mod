"""Validate WFL's native generated-character name pools without running HoI4."""
from pathlib import Path
import unittest

from tools.validate_mod import children, parse


ROOT = Path(__file__).resolve().parents[1]


def block(node, key):
    matches = [part for part in children(node) if part.key == key]
    if len(matches) != 1:
        raise AssertionError(f'Expected one {key} block in {node.key}, got {len(matches)}')
    return matches[0]


def names(node):
    entries = children(node)
    if any(entry.value is not None or not entry.key.strip() for entry in entries):
        raise AssertionError('Native name pools must contain nonempty literal strings')
    values = [entry.key for entry in entries]
    if len(values) != len(set(values)):
        raise AssertionError('Duplicate names reduce the available combinations')
    return set(values)


class NamePoolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'common/names/WFL_names.txt'
        cls.pools = parse(cls.path.read_text(encoding='utf-8-sig'))

    def test_only_wfl_and_its_cosmetic_tag_are_defined(self):
        self.assertEqual([pool.key for pool in self.pools], ['WFL', 'WFL_KINGDOM'])
        self.assertNotEqual(self.path.name, '00_names.txt')
        for pool in self.pools:
            self.assertEqual({part.key for part in children(pool)}, {'male', 'female', 'surnames', 'callsigns'})

    def test_both_genders_have_independent_nonempty_first_names(self):
        for pool in self.pools:
            gender_names = []
            for gender in ('male', 'female'):
                with self.subTest(country=pool.key, gender=gender):
                    values = names(block(block(pool, gender), 'names'))
                    self.assertGreaterEqual(len(values), 32)
                    gender_names.append(values)
            self.assertFalse(gender_names[0] & gender_names[1])

    def test_shared_surnames_allow_many_unique_combinations(self):
        for pool in self.pools:
            surnames = names(block(pool, 'surnames'))
            self.assertGreaterEqual(len(surnames), 40)
            for gender in ('male', 'female'):
                with self.subTest(country=pool.key, gender=gender):
                    first_names = names(block(block(pool, gender), 'names'))
                    self.assertGreaterEqual(len(first_names) * len(surnames), 1000)

    def test_optional_callsign_pool_is_present_and_nonempty(self):
        for pool in self.pools:
            self.assertGreaterEqual(len(names(block(pool, 'callsigns'))), 8)

    def test_cosmetic_tag_preserves_both_name_pools(self):
        base, kingdom = self.pools
        for key in ('surnames', 'callsigns'):
            self.assertEqual(names(block(base, key)), names(block(kingdom, key)))
        for gender in ('male', 'female'):
            self.assertEqual(names(block(block(base, gender), 'names')),
                             names(block(block(kingdom, gender), 'names')))


if __name__ == '__main__':
    unittest.main()
