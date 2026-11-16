"""Country-scoped portrait pool regressions; no dependency on a game installation."""

from pathlib import Path
import unittest

from tools.validate_mod import children, parse, walk


ROOT = Path(__file__).resolve().parents[1]
MALE = {f'GFX_portrait_WFL_advisor_{i:02d}' for i in range(1, 19) if i != 12}
FEMALE = {'GFX_portrait_WFL_advisor_12'}
JAN = {'GFX_portrait_WFL_jan_graf_von_insel_i'}
ROLES = {'army', 'navy', 'operative', 'scientist'}
IDEOLOGIES = {'democratic', 'communism', 'fascism', 'neutrality'}


def child(parent, key):
    matches = [node for node in children(parent) if node.key == key]
    if len(matches) != 1:
        raise AssertionError(f'Expected one {key} pool, got {len(matches)}')
    return matches[0]


def sprite_list(node):
    entries = children(node)
    if any(entry.value is not None for entry in entries):
        raise AssertionError('Portrait pools must contain bare sprite names')
    values = [entry.key for entry in entries]
    if len(values) != len(set(values)):
        raise AssertionError('Duplicate sprites change the random selection weights')
    return set(values)


class PortraitPoolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.countries = parse((ROOT / 'portraits/WFL_portraits.txt').read_text(encoding='utf-8-sig'))

    def test_pools_apply_only_to_wfl_and_its_cosmetic_tags(self):
        self.assertEqual([node.key for node in self.countries],
                         ['WFL', 'WFL_KINGDOM', 'WFL_GREATER_REICH'])
        for country in self.countries:
            self.assertEqual(
                {node.key for node in children(country)},
                ROLES | {'political', 'male', 'female'},
            )

    def test_all_native_person_roles_and_gender_fallbacks_have_photo_pools(self):
        for country in self.countries:
            with self.subTest(country=country.key, role='fallback'):
                self.assertEqual(sprite_list(child(country, 'male')), MALE)
                self.assertEqual(sprite_list(child(country, 'female')), FEMALE)
            for role in ROLES:
                with self.subTest(country=country.key, role=role):
                    group = child(country, role)
                    self.assertEqual({node.key for node in children(group)}, {'male', 'female'})
                    self.assertEqual(sprite_list(child(group, 'male')), MALE)
                    self.assertEqual(sprite_list(child(group, 'female')), FEMALE)

    def test_all_political_groups_exist_and_neutrality_uses_jan(self):
        for country in self.countries:
            political = child(country, 'political')
            self.assertEqual({node.key for node in children(political)}, IDEOLOGIES)
            for ideology in IDEOLOGIES:
                with self.subTest(country=country.key, ideology=ideology):
                    group = child(political, ideology)
                    self.assertEqual(sprite_list(child(group, 'female')), FEMALE)
                    self.assertEqual(
                        sprite_list(child(group, 'male')),
                        JAN if ideology == 'neutrality' else MALE,
                    )

    def test_no_global_or_vanilla_sprite_reference_is_introduced(self):
        references = {
            node.key for node in walk(self.countries)
            if node.value is None and node.key.startswith('GFX_')
        }
        self.assertEqual(references, MALE | FEMALE | JAN)
        self.assertTrue(all(name.startswith('GFX_portrait_WFL_') for name in references))


if __name__ == '__main__':
    unittest.main()
