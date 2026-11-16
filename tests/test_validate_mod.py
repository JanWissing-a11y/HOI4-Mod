from pathlib import Path
import shutil
import tempfile
import unittest

from tools.validate_mod import ParseError, parse, validate


ROOT = Path(__file__).resolve().parents[1]


class ParserTests(unittest.TestCase):
    def test_comments_and_quoted_braces(self):
        nodes = parse('outer = { title = "A # { B }" # ignored }\n list = { a b } }')
        self.assertEqual(nodes[0].value[0].value, 'A # { B }')
        self.assertEqual([n.key for n in nodes[0].value[1].value], ['a', 'b'])

    def test_invalid_structures(self):
        for text in ('a = { b = c', '}', 'name =', 'name = "unterminated', 'a = }'):
            with self.subTest(text=text), self.assertRaises(ParseError):
                parse(text)


class ModTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'mod'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.local-test', 'dist'))

    def replace(self, relative, before, after):
        path = self.root / relative
        content = path.read_text(encoding='utf-8-sig')
        self.assertIn(before, content)
        encoding = 'utf-8-sig' if path.suffix == '.yml' else 'utf-8'
        path.write_text(content.replace(before, after, 1), encoding=encoding)

    def assert_problem(self, text):
        errors = validate(self.root).errors
        self.assertTrue(any(text in error for error in errors), errors)

    def test_current_mod(self):
        self.assertEqual(validate(self.root).errors, [])

    def test_unknown_focus(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'prerequisite = { focus = WFL_rat_der_buergerhalle }',
                     'prerequisite = { focus = WFL_missing }')
        self.assert_problem('unknown focus reference: WFL_missing')

    def test_news_event_registration_and_references_are_validated(self):
        self.replace('common/scripted_effects/WFL_assembly_effects.txt',
                     'news_event = { id = wfl_assembly.1 }',
                     'news_event = { id = wfl_assembly.missing }')
        self.assert_problem('unknown event reference: wfl_assembly.missing')

    def test_decision_scripted_gui_binding_and_window_are_validated(self):
        self.replace('common/decisions/categories/WFL_assembly.txt',
                     'scripted_gui = WFL_vorstand_ui', 'scripted_gui = WFL_missing_ui')
        self.replace('common/scripted_guis/WFL_assembly_ui.txt',
                     'window_name = "WFL_vorstand_window"', 'window_name = "WFL_missing_window"')
        self.assert_problem('unknown scripted GUI: WFL_missing_ui')
        self.assert_problem('scripted GUI has unknown window: WFL_vorstand_ui')

    def test_runtime_recruitment_is_rejected_even_with_a_valid_character(self):
        path = self.root / 'common/scripted_effects/WFL_runtime_recruitment_test.txt'
        path.write_text('WFL_invalid_runtime_effect = { recruit_character = WFL_PER_al_hoehne }', encoding='utf-8')
        self.assert_problem('recruit_character is restricted to history files')

    def test_focus_cycle(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'id = WFL_rat_der_buergerhalle',
                     'id = WFL_rat_der_buergerhalle\n prerequisite = { focus = WFL_werkbank_am_niederrhein }')
        self.assert_problem('focus prerequisite cycle')

    def test_overlapping_focus_positions(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'x = 4 y = 3 cost = 5', 'x = 4 y = 2 cost = 5')
        self.assert_problem('overlapping focus positions')

    def test_focus_parent_below_child(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'x = 15 y = 0 cost = 5', 'x = 15 y = 10 cost = 5')
        self.assert_problem('focus prerequisite must be above child')

    def test_unknown_opinion_modifier(self):
        self.replace('events/WFL_beer_diplomacy.txt',
                     'modifier = WFL_anglo_bierfreundschaft', 'modifier = WFL_missing_opinion')
        self.assert_problem('unknown opinion modifier: WFL_missing_opinion')

    def test_missing_conditional_event_description(self):
        self.replace('localisation/german/WFL_beer_diplomacy_l_german.yml',
                     ' wfl_beer.6.fallback:0', ' unused_fallback:0')
        self.assert_problem('german: missing localisation: wfl_beer.6.fallback')

    def test_asymmetric_exclusion(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'focus = WFL_die_krone_von_flueren focus = WFL_niederrhein_direktorium',
                     'focus = WFL_die_krone_von_flueren')
        self.assert_problem('asymmetric focus exclusion')

    def test_duplicate_event(self):
        path = self.root / 'events/WFL_events.txt'
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\ncountry_event = { id = wfl.1 }\n')
        self.assert_problem('duplicate event ID: wfl.1')

    def test_missing_translation(self):
        self.replace('localisation/german/WFL_l_german.yml',
                     ' WFL_schuetzenkoenig:0', ' unused_name:0')
        self.assert_problem('german: missing localisation: WFL_schuetzenkoenig')

    def test_missing_bom(self):
        path = self.root / 'localisation/german/WFL_l_german.yml'
        path.write_bytes(path.read_bytes().removeprefix(b'\xef\xbb\xbf'))
        self.assert_problem('localisation requires UTF-8 BOM')

    def test_missing_country_definition(self):
        (self.root / 'common/countries/Wesel-Flueren.txt').unlink()
        self.assert_problem('missing country definition for WFL')

    def test_unknown_character(self):
        self.replace('events/WFL_events.txt',
                     'promote_character = WFL_schuetzenkoenig',
                     'promote_character = WFL_missing')
        self.assert_problem('unknown character reference: WFL_missing')

    def test_unknown_leader_trait(self):
        self.replace('common/characters/WFL_characters.txt',
                     'traits = { WFL_genialer_schuetzenkoenig }',
                     'traits = { WFL_missing_trait }')
        self.assert_problem('unknown trait reference: WFL_missing_trait')

    def test_duplicate_leader_trait(self):
        path = self.root / 'common/country_leader/WFL_duplicate_traits.txt'
        path.write_text('leader_traits = { WFL_genialer_schuetzenkoenig = { random = no } }', encoding='utf-8')
        self.assert_problem('duplicate trait ID: WFL_genialer_schuetzenkoenig')

    def test_missing_trait_name(self):
        self.replace('localisation/german/WFL_traits_l_german.yml',
                     ' WFL_genialer_schuetzenkoenig:0', ' unused_trait_name:0')
        self.assert_problem('german: missing localisation: WFL_genialer_schuetzenkoenig')

    def test_missing_trait_description(self):
        self.replace('localisation/english/WFL_traits_l_english.yml',
                     ' WFL_genialer_schuetzenkoenig_desc:0', ' unused_trait_description:0')
        self.assert_problem('english: missing localisation: WFL_genialer_schuetzenkoenig_desc')

    def test_invalid_interface_structure(self):
        path = self.root / 'interface/WFL_portraits.gfx'
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\nspriteTypes = {\n')
        self.assert_problem('interface/WFL_portraits.gfx: unclosed block')

    def test_missing_interface_texture(self):
        (self.root / 'gfx/leaders/WFL/Portrait_WFL_jan_graf_von_insel_i.dds').unlink()
        self.assert_problem('missing referenced texture asset: gfx/leaders/WFL/Portrait_WFL_jan_graf_von_insel_i.dds')

    def test_interface_texture_can_resolve_to_vanilla(self):
        self.replace('interface/WFL_portraits.gfx',
                     'gfx/leaders/WFL/Portrait_WFL_jan_graf_von_insel_i.dds',
                     'gfx/leaders/vanilla_portrait.dds')
        self.assert_problem('missing referenced texture asset: gfx/leaders/vanilla_portrait.dds')
        game = self.root / 'vanilla_fixture'
        texture = game / 'gfx/leaders/vanilla_portrait.dds'
        texture.parent.mkdir(parents=True)
        texture.write_bytes(b'existing vanilla texture fixture')
        # This fixture supplies only the asset, so unrelated map/version checks
        # correctly fail. The texture resolution itself must now succeed.
        errors = validate(self.root, game).errors
        self.assertFalse(any('missing referenced texture asset' in error for error in errors), errors)

    def test_unknown_event_in_additional_own_namespace(self):
        path = self.root / 'common/scripted_effects/WFL_validation_test.txt'
        path.parent.mkdir(exist_ok=True)
        path.write_text('WFL_test_effect = { country_event = { id = wfl_referendum.999 } }', encoding='utf-8')
        self.assert_problem('unknown event reference: wfl_referendum.999')

    def test_invalid_top_level_portrait_pool_structure(self):
        path = self.root / 'portraits/WFL_invalid_test.txt'
        path.parent.mkdir(exist_ok=True)
        path.write_text('country = { tag = WFL army = {', encoding='utf-8')
        self.assert_problem('portraits/WFL_invalid_test.txt: unclosed block')

    def test_unknown_sprite_in_top_level_portrait_pool(self):
        path = self.root / 'portraits/WFL_validation_test.txt'
        path.parent.mkdir(exist_ok=True)
        path.write_text('country = { tag = WFL army = { male = { "GFX_portrait_WFL_missing_pool" } } }', encoding='utf-8')
        self.assert_problem('unknown portrait sprite reference: GFX_portrait_WFL_missing_pool')

    def test_pool_sprite_resolves_to_interface_declaration(self):
        pool = self.root / 'portraits/WFL_validation_test.txt'
        pool.parent.mkdir(exist_ok=True)
        pool.write_text('country = { tag = WFL army = { male = { "GFX_portrait_WFL_pool_test" } } }', encoding='utf-8')
        sprite = self.root / 'interface/WFL_validation_test.gfx'
        sprite.write_text('spriteTypes = { spriteType = { name = "GFX_portrait_WFL_pool_test" '
                          'texturefile = "gfx/leaders/WFL/Portrait_WFL_jan_graf_von_insel_i.dds" } }', encoding='utf-8')
        errors = validate(self.root).errors
        self.assertFalse(any('unknown portrait sprite reference: GFX_portrait_WFL_pool_test' in error
                             for error in errors), errors)

    def test_unknown_own_character_portrait_sprite(self):
        self.replace('common/characters/WFL_characters.txt',
                     'GFX_portrait_WFL_jan_graf_von_insel_i', 'GFX_portrait_WFL_missing_character')
        self.assert_problem('unknown portrait sprite reference: GFX_portrait_WFL_missing_character')

    def test_all_manufacturer_sections_register_companies_but_not_metadata(self):
        sections = ('tank_manufacturer', 'naval_manufacturer', 'aircraft_manufacturer',
                    'materiel_manufacturer', 'industrial_concern')
        before = validate(self.root).counts['idea']
        companies = ['WFL_test_mfr_' + section for section in sections]
        source = 'ideas = {\n' + '\n'.join(
            section + ' = { designer = yes ' + company + ' = { cost = 150 } }'
            for section, company in zip(sections, companies)) + '\n}'
        (self.root / 'common/ideas/WFL_manufacturer_validation.txt').write_text(source, encoding='utf-8')
        reference = self.root / 'common/scripted_effects/WFL_manufacturer_validation.txt'
        reference.parent.mkdir(exist_ok=True)
        reference.write_text('WFL_test_effect = { ' + ' '.join('has_idea = ' + key for key in companies) + ' }',
                             encoding='utf-8')
        for language in ('german', 'english'):
            text = ['l_' + language + ':']
            for company in companies:
                text += [f' {company}:0 "Company"', f' {company}_desc:0 "Description"']
            (self.root / 'localisation' / language / f'WFL_manufacturer_validation_l_{language}.yml').write_text(
                '\n'.join(text) + '\n', encoding='utf-8-sig')
        result = validate(self.root)
        self.assertEqual(result.counts['idea'], before + 5)
        self.assertFalse(any('designer' in error or any(company in error for company in companies)
                             for error in result.errors), result.errors)

    def test_unknown_manufacturer_reference(self):
        path = self.root / 'common/scripted_effects/WFL_manufacturer_validation.txt'
        path.parent.mkdir(exist_ok=True)
        path.write_text('WFL_test_effect = { has_idea = WFL_mfr_missing_company }', encoding='utf-8')
        self.assert_problem('unknown idea reference: WFL_mfr_missing_company')

    def test_manufacturer_requires_name_and_description(self):
        path = self.root / 'common/ideas/WFL_manufacturer_validation.txt'
        path.write_text('ideas = { industrial_concern = { designer = yes '
                        'WFL_mfr_untranslated = { cost = 150 } } }', encoding='utf-8')
        self.assert_problem('german: missing localisation: WFL_mfr_untranslated')
        self.assert_problem('english: missing localisation: WFL_mfr_untranslated_desc')

    def test_duplicate_company_across_manufacturer_sections(self):
        path = self.root / 'common/ideas/WFL_manufacturer_validation.txt'
        path.write_text('ideas = { tank_manufacturer = { WFL_mfr_duplicate = { cost = 150 } } '
                        'naval_manufacturer = { WFL_mfr_duplicate = { cost = 150 } } }', encoding='utf-8')
        self.assert_problem('duplicate idea ID: WFL_mfr_duplicate')

    def test_capital_owned_by_another_country(self):
        self.replace('history/states/1082-Wesel-Flueren.txt', 'owner = WFL', 'owner = GER')
        self.assert_problem('capital state 1082 is not owned by WFL')

    def test_division_outside_starting_territory(self):
        self.replace('history/units/WFL_1936.txt', 'location = 3512', 'location = 6583')
        self.assert_problem('division location is outside WFL starting territory: 6583')

    def test_missing_starting_oob(self):
        (self.root / 'history/units/WFL_1936.txt').unlink()
        self.assert_problem('missing starting OOB: WFL_1936')

    def test_invalid_flag_dimensions(self):
        path = self.root / 'gfx/flags/WFL.tga'
        data = bytearray(path.read_bytes())
        data[12:14] = (81).to_bytes(2, 'little')
        path.write_bytes(data)
        self.assert_problem('requires dimensions (82, 52), got (81, 52)')

    def test_truncated_flag(self):
        path = self.root / 'gfx/flags/WFL.tga'
        path.write_bytes(path.read_bytes()[:25])
        self.assert_problem('has truncated pixel data')

    def test_upside_down_flag_export_is_rejected_in_ideology_variants(self):
        path = self.root / 'gfx/flags/small/WFL_neutrality.tga'
        data = bytearray(path.read_bytes())
        data[17] |= 0x20
        path.write_bytes(data)
        self.assert_problem(f'{Path("gfx/flags/small/WFL_neutrality.tga")} requires bottom-left TGA origin for HoI4')

    def test_missing_ideology_flag_is_rejected(self):
        (self.root / 'gfx/flags/medium/WFL_democratic.tga').unlink()
        self.assert_problem('WFL_democratic.tga')

    def test_cosmetic_flags_are_explicit_for_every_size_and_ideology(self):
        for tag in ('WFL_KINGDOM', 'WFL_GREATER_REICH'):
            for folder in ('', 'medium', 'small'):
                for suffix in ('', '_democratic', '_neutrality', '_fascism', '_communism'):
                    with self.subTest(tag=tag, folder=folder, ideology=suffix):
                        path = self.root / 'gfx/flags' / folder / f'{tag}{suffix}.tga'
                        self.assertTrue(path.is_file(), path)
                        expected = self.root / 'gfx/flags' / folder / 'WFL.tga'
                        self.assertEqual(path.read_bytes(), expected.read_bytes())

    def test_missing_cosmetic_flag_is_rejected(self):
        for tag in ('WFL_KINGDOM', 'WFL_GREATER_REICH'):
            path = self.root / f'gfx/flags/small/{tag}_communism.tga'
            with self.subTest(tag=tag):
                data = path.read_bytes()
                path.unlink()
                try:
                    self.assert_problem(f'{tag}_communism.tga')
                finally:
                    path.write_bytes(data)

    def test_cosmetic_flag_uses_same_design_as_base(self):
        path = self.root / 'gfx/flags/medium/WFL_GREATER_REICH_neutrality.tga'
        data = bytearray(path.read_bytes())
        data[18] ^= 0xFF
        path.write_bytes(data)
        self.assert_problem('WFL_GREATER_REICH_neutrality.tga must match WFL.tga in the same size')

    def test_cosmetic_flag_orientation_is_validated(self):
        path = self.root / 'gfx/flags/small/WFL_GREATER_REICH_neutrality.tga'
        data = bytearray(path.read_bytes())
        data[17] |= 0x20
        path.write_bytes(data)
        self.assert_problem('WFL_GREATER_REICH_neutrality.tga requires bottom-left TGA origin for HoI4')

    def test_cosmetic_country_names_require_localisation(self):
        self.replace('localisation/english/WFL_german_integration_l_english.yml',
                     ' WFL_GREATER_REICH_fascism_DEF:0', ' unused_cosmetic_name:0')
        self.assert_problem('english: missing localisation: WFL_GREATER_REICH_fascism_DEF')

    def test_duplicate_province_in_mod_states(self):
        self.replace('history/states/51-Moselland.txt', 'provinces = {', 'provinces = { 3512')
        self.assert_problem('province assigned to multiple mod states: 3512')

    def test_effective_map_loses_no_province(self):
        game = self.root / 'vanilla_fixture'
        (game / 'history/states').mkdir(parents=True)
        (game / 'common/country_tags').mkdir(parents=True)
        (game / 'launcher-settings.json').write_text('{"rawVersion":"1.19.4.1"}', encoding='utf-8')
        source = (self.root / 'history/states/51-Moselland.txt').read_text(encoding='utf-8')
        (game / 'history/states/51-Moselland.txt').write_text(
            source.replace('provinces = {', 'provinces = { 3512 999999'), encoding='utf-8')
        errors = validate(self.root, game).errors
        self.assertTrue(any('effective map changes province assignment count: 999999 (1 -> 0)' in error
                            for error in errors), errors)

    def test_wrong_override_filename(self):
        game = self.root / 'vanilla_fixture'
        (game / 'history/states').mkdir(parents=True)
        (game / 'common/country_tags').mkdir(parents=True)
        (game / 'launcher-settings.json').write_text('{"rawVersion":"1.19.4.1"}', encoding='utf-8')
        original = self.root / 'history/states/51-Moselland.txt'
        shutil.copyfile(original, game / 'history/states/51-Original-Name.txt')
        errors = validate(self.root, game).errors
        self.assertTrue(any('must override exact vanilla filename 51-Original-Name.txt' in error
                            for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
