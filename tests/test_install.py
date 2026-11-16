"""Run the Windows installer only against isolated temporary fixtures."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which('powershell.exe')


@unittest.skipUnless(POWERSHELL, 'Windows PowerShell is required')
class InstallerTests(unittest.TestCase):
    def setUp(self):
        # The managed Windows TEMP sandbox denies directory renames. Use the
        # explicitly writable workspace for the installer's atomic-move tests.
        scratch = ROOT / '.local-test'
        scratch.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='WFL Installtest ', dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / 'Quelle mit Umlauten ü'
        self.destination = self.root / 'Mod Ziel ä'
        self.source.mkdir()
        (self.source / 'descriptor.mod').write_text('name="Wesel-Flüren"\nversion="0.1"\n', encoding='utf-8')
        for folder in ('common', 'history', 'events', 'localisation', 'gfx'):
            path = self.source / folder
            path.mkdir()
            (path / 'own.txt').write_text('initial', encoding='utf-8')

    def run_installer(self, *arguments, success=True, explicit_source=True, script=None):
        source_argument = ['-SourceRoot', str(self.source)] if explicit_source else []
        result = subprocess.run(
            [POWERSHELL, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
             '-File', str(script or ROOT / 'tools/install.ps1'), *source_argument,
             '-Destination', str(self.destination), *arguments],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
        output = result.stdout.decode('utf-8', errors='replace')
        self.assertEqual(result.returncode == 0, success, output)
        return output

    def test_paths_reinstall_backup_and_restore(self):
        self.run_installer()
        installed = self.destination / 'wesel_flueren'
        descriptor = (self.destination / 'wesel_flueren.mod').read_text(encoding='utf-8')
        self.assertIn(f'path="{installed.as_posix()}"', descriptor)
        self.assertIn('Wesel-Flüren', descriptor)
        marker = json.loads((installed / '.wesel_flueren_install.json').read_text(encoding='utf-8'))
        self.assertEqual(marker['project'], 'HOI4-Wesel-Flueren')
        (self.source / 'common/own.txt').write_text('new version', encoding='utf-8')
        self.run_installer()
        backups = list((self.destination / '.wesel_flueren-backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual((installed / 'common/own.txt').read_text(), 'new version')
        self.assertEqual((backups[0] / 'wesel_flueren/common/own.txt').read_text(), 'initial')
        self.run_installer('-RestoreBackup', backups[0].name)
        self.assertEqual((installed / 'common/own.txt').read_text(), 'initial')
        self.assertEqual(len(list((self.destination / '.wesel_flueren-backups').iterdir())), 2)
        self.assertEqual(list(self.destination.glob('.wesel_flueren-stage-*')), [])

    def test_default_source_uses_installer_location(self):
        tools = self.source / 'tools'
        tools.mkdir()
        installer = tools / 'install.ps1'
        shutil.copyfile(ROOT / 'tools/install.ps1', installer)
        self.run_installer(explicit_source=False, script=installer)
        self.assertEqual((self.destination / 'wesel_flueren/common/own.txt').read_text(), 'initial')

    def test_installs_and_tracks_top_level_portrait_pools(self):
        portraits = self.source / 'portraits'
        portraits.mkdir()
        source = portraits / 'WFL_portraits.txt'
        source.write_text('country = { tag = WFL male = { "GFX_portrait_WFL_test" } }', encoding='utf-8')
        self.run_installer()
        installed = self.destination / 'wesel_flueren'
        self.assertEqual((installed / 'portraits/WFL_portraits.txt').read_bytes(), source.read_bytes())
        manifest = json.loads((installed / '.wesel_flueren_install.json').read_text(encoding='utf-8'))
        self.assertIn('portraits/WFL_portraits.txt', manifest['files'])

    def make_building_recipe(self):
        game = self.root / 'Originalspiel'
        (game / 'map').mkdir(parents=True)
        original = game / 'map/buildings.txt'
        original.write_bytes(b'51;arms_factory;1;2;3;4;0\n8;air_base;2;3;4;5;0\n')
        recipe = {
            'source_state': 51, 'target_state': 1082,
            'source_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
            'remove_lines': ['51;arms_factory;1;2;3;4;0'],
            'add_lines': ['1082;arms_factory;1;2;3;4;0'],
        }
        data = self.source / 'tools/data'
        data.mkdir(parents=True)
        recipe_path = data / 'building_overrides.json'
        recipe_path.write_text(json.dumps(recipe), encoding='utf-8')
        return game, original, recipe_path

    def make_color_recipe(self):
        game = self.root / 'Originalspiel'
        countries = game / 'common/countries'
        countries.mkdir(parents=True)
        (countries / 'colors.txt').write_text('GER = { color = rgb { 1 2 3 } }\n', encoding='utf-8')
        (countries / 'cosmetic.txt').write_text('GER_monarchy = { color = rgb { 4 5 6 } }\n', encoding='utf-8')
        data = self.source / 'tools/data'
        data.mkdir(parents=True)
        recipe = data / 'WFL_country_colors.json'
        recipe.write_bytes((ROOT / 'tools/data/WFL_country_colors.json').read_bytes())
        return game, countries, recipe

    def test_colors_preserve_vanilla_and_cover_base_kingdom_and_greater_reich(self):
        game, countries, _ = self.make_color_recipe()
        originals = {p.name: p.read_bytes() for p in countries.iterdir()}
        self.run_installer('-GameRoot', str(game))
        installed = self.destination / 'wesel_flueren'
        manifest = json.loads((installed / '.wesel_flueren_install.json').read_text())
        tags = (('colors.txt', 'WFL'), ('cosmetic.txt', 'WFL_KINGDOM'),
                ('cosmetic.txt', 'WFL_GREATER_REICH'))
        for name, tag in tags:
            relative = f'common/countries/{name}'
            output_bytes = (installed / relative).read_bytes()
            output = output_bytes.decode('utf-8')
            self.assertTrue(output_bytes.startswith(originals[name]))
            entry = re.search(rf'(?m)^{tag} = \{{\n([^}}]+)\}}\n([^}}]+)\}}\n\}}', output)
            self.assertIsNotNone(entry, output)
            self.assertIn('color = rgb { 35 107 59 }', entry[0])
            self.assertIn('color_ui = rgb { 57 153 86 }', entry[0])
            self.assertIn(relative, manifest['files'])
            self.assertEqual((countries / name).read_bytes(), originals[name])
        self.run_installer('-GameRoot', str(game))
        for name, tag in tags:
            self.assertEqual((installed / f'common/countries/{name}').read_text().count(f'{tag} = {{'), 1)

    def test_legacy_single_cosmetic_color_recipe_still_installs(self):
        game, _, recipe_path = self.make_color_recipe()
        recipe = json.loads(recipe_path.read_text())
        del recipe['cosmetic_tags']
        recipe_path.write_text(json.dumps(recipe))
        self.run_installer('-GameRoot', str(game))
        cosmetic = (self.destination / 'wesel_flueren/common/countries/cosmetic.txt').read_text()
        self.assertIn('WFL_KINGDOM = {', cosmetic)
        self.assertNotIn('WFL_GREATER_REICH', cosmetic)

    def test_cosmetic_color_tags_are_an_explicit_nonempty_unique_whitelist(self):
        game, _, recipe_path = self.make_color_recipe()
        recipe = json.loads(recipe_path.read_text())
        for value in ('WFL_GREATER_REICH', [], ['GER'], ['WFL_KINGDOM', 'WFL_KINGDOM'],
                      ['wfl_greater_reich'], [None]):
            with self.subTest(cosmetic_tags=value):
                recipe['cosmetic_tags'] = value
                recipe_path.write_text(json.dumps(recipe))
                self.run_installer('-GameRoot', str(game), success=False)
                self.assertFalse(self.destination.exists())

    def test_unknown_or_malformed_base_color_tags_are_rejected(self):
        game, _, recipe_path = self.make_color_recipe()
        original = json.loads(recipe_path.read_text())
        for field, value in (('base_tag', 'GER'), ('base_tag', ['WFL']),
                             ('cosmetic_tag', 'GER_monarchy')):
            with self.subTest(field=field, value=value):
                recipe = dict(original, **{field: value})
                recipe_path.write_text(json.dumps(recipe))
                self.run_installer('-GameRoot', str(game), success=False)
                self.assertFalse(self.destination.exists())

    def test_existing_vanilla_color_tag_collisions_are_preserved_and_refused(self):
        game, countries, _ = self.make_color_recipe()
        original = {p.name: p.read_bytes() for p in countries.iterdir()}
        for name, tag in (('colors.txt', 'WFL'), ('cosmetic.txt', 'WFL_KINGDOM'),
                          ('cosmetic.txt', 'WFL_GREATER_REICH')):
            with self.subTest(tag=tag):
                for filename, content in original.items():
                    (countries / filename).write_bytes(content)
                path = countries / name
                collision = original[name] + f'{tag} = {{ color = rgb {{ 99 98 97 }} }}\n'.encode()
                path.write_bytes(collision)
                self.run_installer('-GameRoot', str(game), success=False)
                self.assertEqual(path.read_bytes(), collision)
                self.assertFalse(self.destination.exists())

    def test_invalid_colors_fail_before_installation(self):
        game, _, recipe_path = self.make_color_recipe()
        recipe = json.loads(recipe_path.read_text())
        recipe['map_color'] = [35, 999, 59]
        recipe_path.write_text(json.dumps(recipe))
        self.run_installer('-GameRoot', str(game), success=False)
        self.assertFalse(self.destination.exists())

    def test_generates_map_only_inside_mod(self):
        game, original, _ = self.make_building_recipe()
        original_bytes = original.read_bytes()
        self.run_installer('-GameRoot', str(game))
        output = (self.destination / 'wesel_flueren/map/buildings.txt').read_text()
        self.assertIn('1082;arms_factory;1;2;3;4;0', output)
        self.assertIn('8;air_base;2;3;4;5;0', output)
        self.assertNotIn('51;arms_factory', output)
        self.assertFalse(output.endswith(('\n', '\r')))
        self.assertTrue(all(len(line.split(';')) == 7 for line in output.splitlines()))
        self.assertEqual(original.read_bytes(), original_bytes)

    def test_original_map_without_newline_keeps_records_separate(self):
        game, original, recipe_path = self.make_building_recipe()
        original.write_bytes(original.read_bytes().rstrip(b'\r\n'))
        recipe = json.loads(recipe_path.read_text())
        recipe['source_sha256'] = hashlib.sha256(original.read_bytes()).hexdigest()
        recipe_path.write_text(json.dumps(recipe), encoding='utf-8')
        original_bytes = original.read_bytes()
        self.run_installer('-GameRoot', str(game))
        output = (self.destination / 'wesel_flueren/map/buildings.txt').read_text()
        self.assertEqual(output.splitlines(), ['8;air_base;2;3;4;5;0', '1082;arms_factory;1;2;3;4;0'])
        self.assertFalse(output.endswith(('\n', '\r')))
        self.assertEqual(original.read_bytes(), original_bytes)

    def test_refuses_unknown_original_map_before_install(self):
        game, original, _ = self.make_building_recipe()
        original.write_bytes(original.read_bytes() + b'# updated vanilla\n')
        self.run_installer('-GameRoot', str(game), success=False)
        self.assertFalse(self.destination.exists())

    def test_refuses_ambiguous_map_recipe_before_install(self):
        game, _, recipe_path = self.make_building_recipe()
        recipe = json.loads(recipe_path.read_text())
        recipe['remove_lines'].append(recipe['remove_lines'][0])
        recipe_path.write_text(json.dumps(recipe), encoding='utf-8')
        self.run_installer('-GameRoot', str(game), success=False)
        self.assertFalse(self.destination.exists())

    def test_refuses_unmarked_existing_directory(self):
        target = self.destination / 'wesel_flueren'
        target.mkdir(parents=True)
        foreign = target / 'private.txt'
        foreign.write_text('preserve me', encoding='utf-8')
        self.run_installer(success=False)
        self.assertEqual(foreign.read_text(), 'preserve me')

    def test_refuses_foreign_file_in_owned_installation(self):
        self.run_installer()
        target = self.destination / 'wesel_flueren'
        foreign = target / 'private.txt'
        foreign.write_text('preserve me', encoding='utf-8')
        self.run_installer(success=False)
        self.assertEqual(foreign.read_text(), 'preserve me')
        self.assertEqual((target / 'common/own.txt').read_text(), 'initial')

    def test_refuses_foreign_launcher_descriptor(self):
        self.destination.mkdir()
        descriptor = self.destination / 'wesel_flueren.mod'
        descriptor.write_text('unrelated descriptor', encoding='utf-8')
        self.run_installer(success=False)
        self.assertEqual(descriptor.read_text(), 'unrelated descriptor')

    def test_launcher_reformatted_owned_descriptor_can_update_and_restore(self):
        self.run_installer()
        descriptor = self.destination / 'wesel_flueren.mod'
        rewritten = descriptor.read_text(encoding='utf-8').split('\n', 1)[1]
        # Launcher strips comments, changes whitespace and moves path to the top.
        lines = rewritten.splitlines()
        descriptor.write_text('\n'.join([lines[-1], *lines[:-1]]) + '\n', encoding='utf-8')
        (self.source / 'common/own.txt').write_text('updated after launcher', encoding='utf-8')
        self.run_installer()
        backups = list((self.destination / '.wesel_flueren-backups').iterdir())
        self.assertEqual((backups[0] / 'wesel_flueren.mod').read_text(encoding='utf-8'),
                         '\n'.join([lines[-1], *lines[:-1]]) + '\n')
        self.run_installer('-RestoreBackup', backups[0].name)
        self.assertEqual((self.destination / 'wesel_flueren/common/own.txt').read_text(), 'initial')

    def test_commentless_descriptor_still_requires_exact_owned_identity(self):
        self.run_installer()
        descriptor = self.destination / 'wesel_flueren.mod'
        rewritten = descriptor.read_text(encoding='utf-8').split('\n', 1)[1]
        for invalid in [rewritten.replace('name="Wesel-Flüren"', 'name="Other Mod"'),
                        rewritten.replace('version="0.1"', 'version="other"'),
                        rewritten.replace('/wesel_flueren"', '/someone_else"'),
                        rewritten + 'replace_path="common"\n']:
            with self.subTest(descriptor=invalid):
                descriptor.write_text(invalid, encoding='utf-8')
                self.run_installer(success=False)
                self.assertEqual(descriptor.read_text(encoding='utf-8'), invalid)
                self.assertFalse((self.destination / '.wesel_flueren-backups').exists())

    def test_missing_source_keeps_previous_installation(self):
        self.run_installer()
        (self.source / 'descriptor.mod').unlink()
        self.run_installer(success=False)
        self.assertEqual((self.destination / 'wesel_flueren/common/own.txt').read_text(), 'initial')
        self.assertFalse((self.destination / '.wesel_flueren-backups').exists())

    def test_refuses_original_game_directory(self):
        self.destination.mkdir()
        original = self.destination / 'hoi4.exe'
        original.write_bytes(b'original game fixture')
        self.run_installer(success=False)
        self.assertEqual(original.read_bytes(), b'original game fixture')
        self.assertFalse((self.destination / 'wesel_flueren').exists())

    def test_refuses_restore_path_traversal(self):
        self.run_installer('-RestoreBackup', '..', success=False)
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
