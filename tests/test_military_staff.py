"""Military cabinet parity, country isolation and paid appointment safety."""
from dataclasses import asdict
import json
import os
from pathlib import Path
import struct
from tempfile import TemporaryDirectory
import unittest

from tools.import_german_military_staff import build, military_roles, recruitment_block
from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))


def read_nodes(path):
    return parse(path.read_text(encoding='utf-8-sig'))


class MilitaryStaffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'tools/data/WFL_military_staff.json').read_text(encoding='utf-8'))
        cls.characters = {c.key: c for c in children(read_nodes(ROOT / 'common/characters/WFL_military_staff.txt')[0])}

    def test_complete_catalog_has_every_staff_category_and_no_field_commanders(self):
        self.assertEqual(len(self.characters), 36)
        self.assertEqual(self.manifest['role_counts'], {
            'army_chief': 6, 'navy_chief': 3, 'air_chief': 4, 'high_command': 16, 'theorist': 8})
        self.assertEqual(set(self.characters), {s['id'] for s in self.manifest['staff']})
        self.assertNotIn('GER_nikolaus_von_falkenhorst', {s['source_character'] for s in self.manifest['staff']})
        for char in self.characters.values():
            self.assertTrue(char.key.startswith('WFL_staff_'))
            self.assertFalse({'corps_commander', 'field_marshal', 'navy_leader', 'country_leader', 'scientist'}
                             & {n.key for n in children(char)})
            self.assertFalse(any(n.key == 'advisor' and field(n, 'slot') == 'political_advisor'
                                 for n in children(char)))

    def test_paid_hiring_uses_wfl_eligibility_and_no_german_focus_locks(self):
        history = list(walk(read_nodes(ROOT / 'history/countries/WFL - Wesel-Flueren.txt')))
        recruits = [n.value for n in history if n.key == 'recruit_character']
        for own_id, char in self.characters.items():
            self.assertEqual(recruits.count(own_id), 1)
            for role in (n for n in children(char) if n.key == 'advisor'):
                allowed = next(n for n in children(role) if n.key == 'allowed')
                self.assertEqual(field(allowed, 'original_tag'), 'WFL')
                self.assertNotIn('political_advisor', [field(role, 'slot')])
                self.assertIsNotNone(field(role, 'cost'))
                self.assertGreater(int(field(role, 'cost')), 0)
        for node in history:
            if node.key == 'add_ideas':
                ids = [n.key for n in children(node)] if children(node) else [node.value]
                self.assertFalse(set(ids) & set(self.characters))
        nodes = list(walk(read_nodes(ROOT / 'common/characters/WFL_military_staff.txt')))
        self.assertFalse({'has_completed_focus', 'has_country_flag', 'has_global_flag', 'on_add', 'on_remove',
                          'has_country_leader', 'has_government'} & {n.key for n in nodes})

    def test_fritsch_cannot_fill_two_slots_and_army_chief_retains_dlc_requirement(self):
        char = self.characters['WFL_staff_werner_von_fritsch']
        roles = {field(r, 'slot'): r for r in children(char) if r.key == 'advisor'}
        self.assertEqual(set(roles), {'high_command', 'army_chief'})
        for slot, role in roles.items():
            available = next(n for n in children(role) if n.key == 'available')
            self.assertEqual(field(available, 'not_already_hired_except_as'), slot)
            dlcs = [n.value for n in walk(children(role)) if n.key == 'has_dlc']
            self.assertEqual(dlcs, ['Gotterdammerung'] if slot == 'army_chief' else [])

    def test_localized_historical_names_and_both_photo_sizes_are_connected(self):
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(read_nodes(ROOT / 'interface/WFL_advisor_portraits.gfx')) if n.key == 'spriteType'}
        for language in ('german', 'english'):
            raw = (ROOT / f'localisation/{language}/WFL_military_staff_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            text = raw.decode('utf-8-sig')
            for item in self.manifest['staff']:
                self.assertIn(f'{item["id"]}:0 {json.dumps(item["names"][language], ensure_ascii=False)}', text)
                self.assertNotIn('$', item['names'][language])
        for char in self.characters.values():
            portraits = next(n for n in children(char) if n.key == 'portraits')
            self.assertEqual({n.key for n in children(portraits)}, {'army', 'civilian'})
            for node in walk(children(portraits)):
                if node.key in ('large', 'small'):
                    self.assertTrue(node.value.startswith('GFX_portrait_WFL_advisor_'))
                    data = (ROOT / sprites[node.value]).read_bytes()
                    self.assertEqual(data[:4], b'DDS ')
                    h, w = struct.unpack_from('<II', data, 12)
                    self.assertEqual((w, h), (65, 67) if node.key == 'small' else (156, 210))

    @unittest.skipUnless((GAME / 'common/characters/GER.txt').is_file(), 'local vanilla required')
    def test_all_vanilla_prices_ledgers_traits_and_nested_effects_match(self):
        sources = {c.key: c for tag in ('GER', 'AUS')
                   for c in children(read_nodes(GAME / f'common/characters/{tag}.txt')[0])}
        self.assertEqual({s['source_character'] for s in self.manifest['staff']},
                         {c.key for c in sources.values() if military_roles(c)})
        vanilla_traits = {n.key: n for g in read_nodes(GAME / 'common/country_leader/00_traits.txt')
                          if g.key == 'leader_traits' for n in children(g)}
        default = str(self.manifest['default_military_advisor_cost'])
        self.assertEqual(default, '50')
        for item in self.manifest['staff']:
            self.assertEqual(item['source_file'],
                             f'common/characters/{item["source_character"].split("_", 1)[0]}.txt')
            source_roles = military_roles(sources[item['source_character']])
            own_roles = [n for n in children(self.characters[item['id']]) if n.key == 'advisor']
            self.assertEqual(len(source_roles), len(own_roles))
            for source, own, snapshot in zip(source_roles, own_roles, item['roles']):
                self.assertEqual(field(source, 'slot'), field(own, 'slot'))
                self.assertEqual(field(source, 'ledger'), field(own, 'ledger'))
                self.assertEqual(field(source, 'cost') or default, field(own, 'cost'))
                original_traits = next(n for n in children(source) if n.key == 'traits')
                own_traits = next(n for n in children(own) if n.key == 'traits')
                self.assertEqual(original_traits, own_traits)
                for trait in children(own_traits):
                    self.assertIn(trait.key, vanilla_traits)
                    self.assertEqual(snapshot['trait_definitions'][trait.key], asdict(vanilla_traits[trait.key]))
        # Retaining the full original traits preserves nested aircraft/tank
        # equipment bonuses as well as all XP and command-power variables.
        for trait_id in ('blitzkrieg_theorist', 'dive_bomber', 'GER_reich_marshal'):
            self.assertTrue(any(n.key == 'equipment_bonus' for n in children(vanilla_traits[trait_id])))

    @unittest.skipUnless((GAME / 'common/characters/GER.txt').is_file(), 'local vanilla required')
    def test_regeneration_is_reproducible_and_does_not_write_country_history(self):
        with TemporaryDirectory() as directory:
            target = Path(directory)
            manifest = build(target, GAME)
            self.assertFalse((target / 'history').exists())
            self.assertEqual(manifest, self.manifest)
            for relative in ('common/characters/WFL_military_staff.txt',
                             'tools/data/WFL_military_staff.json',
                             'localisation/german/WFL_military_staff_l_german.yml',
                             'localisation/english/WFL_military_staff_l_english.yml'):
                self.assertEqual((target / relative).read_bytes(), (ROOT / relative).read_bytes())
            self.assertEqual(recruitment_block(manifest).count('recruit_character = '), 36)

    def test_both_austrian_profiles_explicitly_allowed_for_germany_are_included(self):
        additions = {s['source_character']: s for s in self.manifest['staff']
                     if s['source_file'].endswith('/AUS.txt')}
        self.assertEqual(set(additions), {'AUS_wilhelm_gebauer', 'AUS_eugen_beyer'})
        self.assertEqual(additions['AUS_wilhelm_gebauer']['roles'][0]['traits'], ['army_chief_morale_3'])
        self.assertEqual(additions['AUS_eugen_beyer']['roles'][0]['traits'], ['army_commando_2'])
        self.assertTrue(all(r['base_cost'] == 100 for s in additions.values() for r in s['roles']))
        self.assertEqual(additions['AUS_wilhelm_gebauer']['roles'][0]['required_dlc'], [])
        self.assertEqual(additions['AUS_eugen_beyer']['roles'][0]['required_dlc'], ['Gotterdammerung'])
        beyer = self.characters['WFL_staff_eugen_beyer']
        roles = [n for n in children(beyer) if n.key == 'advisor']
        self.assertEqual(len(roles), 1)
        allowed = next(n for n in children(roles[0]) if n.key == 'allowed')
        self.assertEqual(field(allowed, 'has_dlc'), 'Gotterdammerung')
        self.assertEqual(field(allowed, 'original_tag'), 'WFL')


if __name__ == '__main__':
    unittest.main()
