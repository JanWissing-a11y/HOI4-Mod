"""Catalog parity and hiring safety, independent of engine UI behaviour."""
import json
from pathlib import Path
import re
import struct
from tempfile import TemporaryDirectory
import unittest

from tools.import_german_advisors import build
from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')


def read_nodes(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


class AdvisorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'tools/data/WFL_advisors.json').read_text(encoding='utf-8'))
        cls.characters = {n.key: n for n in children(read_nodes('common/characters/WFL_advisors.txt')[0])}
        cls.traits = {n.key: n for n in children(read_nodes('common/country_leader/WFL_advisor_traits.txt')[0])}

    def test_complete_initial_catalog_and_base_prices(self):
        self.assertEqual(len(self.characters), 37)
        self.assertEqual(len(self.traits), 39)
        self.assertEqual(sum(len(a['roles']) for a in self.catalog['advisors']), 39)
        for item in self.catalog['advisors']:
            roles = [n for n in walk(children(self.characters[item['id']])) if n.key == 'advisor']
            self.assertEqual(len(roles), len(item['roles']))
            for role, snapshot in zip(roles, item['roles']):
                self.assertEqual(field(role, 'slot'), 'political_advisor')
                self.assertEqual(int(field(role, 'cost')), snapshot['base_cost'])
                self.assertIn(('original_tag', 'WFL'), [(n.key, n.value) for n in walk(children(role))])
                actual = {n.key: n.value for n in children(self.traits[snapshot['trait']])
                          if n.key not in ('sprite', 'random')}
                self.assertEqual(actual, snapshot['modifiers'])

    @unittest.skipUnless((GAME / 'common/characters/GER.txt').is_file(), 'Local vanilla install unavailable')
    def test_effects_match_installed_vanilla_including_negative_effects(self):
        source_traits = {n.key: n for group in parse((GAME / 'common/country_leader/00_traits.txt').read_text(encoding='utf-8-sig'))
                         if group.key == 'leader_traits' for n in children(group)}
        source_chars = children(parse((GAME / 'common/characters/GER.txt').read_text(encoding='utf-8-sig'))[0])
        source_ids = {c.key for c in source_chars if any(n.key == 'advisor' and field(n, 'slot') == 'political_advisor'
                                                       for n in walk(children(c)))}
        self.assertEqual(source_ids, {a['source_character'] for a in self.catalog['advisors']})
        for item in self.catalog['advisors']:
            for role in item['roles']:
                effects = {n.key: n.value for n in children(source_traits[role['source_trait']])
                           if n.key not in ('sprite', 'random', 'ai_will_do')}
                self.assertEqual(effects, role['modifiers'])

    def test_recruited_once_without_free_hiring_or_german_story_hooks(self):
        history = list(walk(read_nodes('history/countries/WFL - Wesel-Flueren.txt')))
        recruited = [n.value for n in history if n.key == 'recruit_character']
        for own_id in self.characters:
            self.assertEqual(recruited.count(own_id), 1)
        for addition in (n for n in history if n.key == 'add_ideas'):
            idea_ids = [n.key for n in children(addition)] if children(addition) else [addition.value]
            self.assertTrue(all(own_id not in self.characters for own_id in idea_ids))
        text = (ROOT / 'common/characters/WFL_advisors.txt').read_text(encoding='utf-8')
        self.assertNotRegex(text, r'\bGER_|\bUSA_|\bCOG\b')
        self.assertNotIn('on_add', text)
        self.assertNotIn('has_completed_focus', text)

    def test_dlc_pairs_are_complementary_and_do_not_stack(self):
        for own_id, dlc in [('WFL_advisor_16', 'La Resistance'), ('WFL_advisor_31', 'Gotterdammerung')]:
            instances = [n for n in children(self.characters[own_id]) if n.key == 'instance']
            self.assertEqual(len(instances), 2)
            # A character with DLC variants must consist only of instance
            # blocks. Otherwise the engine treats it as a plain body and
            # reports each subsequent instance as an unexpected token.
            self.assertEqual({n.key for n in children(self.characters[own_id])}, {'instance'})
            for instance in instances:
                self.assertEqual(field(instance, 'name'), own_id)
                self.assertEqual(len([n for n in children(instance) if n.key == 'portraits']), 1)
                pictures = {n.value for n in walk(children(instance)) if n.key in ('large', 'small')}
                self.assertEqual(len(pictures), 2)
                self.assertTrue(all(picture.startswith('GFX_portrait_WFL_') for picture in pictures))
            conditions = [next(n for n in children(i) if n.key == 'allowed') for i in instances]
            self.assertEqual(sum(n.key == 'NOT' for c in conditions for n in children(c)), 1)
            self.assertTrue(all([n.value for n in walk(children(c)) if n.key == 'has_dlc'] == [dlc]
                                for c in conditions))

    @unittest.skipUnless((GAME / 'common/characters/GER.txt').is_file(), 'Local vanilla install unavailable')
    def test_rebuilding_catalog_keeps_engine_compatible_instance_bodies(self):
        with TemporaryDirectory() as directory:
            generated = Path(directory)
            for relative in ('common/characters', 'common/country_leader', 'localisation/german',
                             'localisation/english', 'tools/data', 'history/countries'):
                (generated / relative).mkdir(parents=True, exist_ok=True)
            (generated / 'history/countries/WFL - Wesel-Flueren.txt').write_text('', encoding='utf-8')
            build(generated, GAME)
            self.assertEqual(
                (generated / 'common/characters/WFL_advisors.txt').read_text(encoding='utf-8-sig'),
                (ROOT / 'common/characters/WFL_advisors.txt').read_text(encoding='utf-8-sig'),
            )

    def test_effect_activation_and_competing_cabinets(self):
        for own_id, ideology in [('WFL_advisor_09', 'fascism'), ('WFL_advisor_22', 'democratic')]:
            roles = [n for n in walk(children(self.characters[own_id])) if n.key == 'advisor']
            self.assertTrue(any(n.key == 'do_effect' and any(x.key == 'has_government' and x.value == ideology
                             for x in walk(children(n))) for r in roles for n in children(r)))
        for first, second in [(7, 8), (8, 25), (10, 12)]:
            for a, b in [(first, second), (second, first)]:
                self.assertTrue(any(n.key == f'WFL_advisor_{b:02}' and field(n, 'is_hired_as_advisor') == 'no'
                                    for n in walk(children(self.characters[f'WFL_advisor_{a:02}']))))

    def test_all_person_pictures_are_supplied_photos_at_both_sizes(self):
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(read_nodes('interface/WFL_advisor_portraits.gfx')) if n.key == 'spriteType'}
        for char in self.characters.values():
            for ref in [n.value for n in walk(children(char)) if n.key in ('large', 'small')]:
                self.assertIn(ref, sprites)
                data = (ROOT / sprites[ref]).read_bytes()
                self.assertEqual(data[:4], b'DDS ')
                height, width = struct.unpack_from('<II', data, 12)
                self.assertEqual((width, height), (65, 67) if ref.endswith('_small') else (156, 210))
        self.assertNotRegex((ROOT / 'common/characters/WFL_characters.txt').read_text(), r'GFX_\w*Generic')


if __name__ == '__main__':
    unittest.main()
