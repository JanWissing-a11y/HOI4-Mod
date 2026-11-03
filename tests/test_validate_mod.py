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
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))

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

    def test_focus_cycle(self):
        self.replace('common/national_focus/WFL_focus.txt',
                     'id = WFL_rat_der_buergerhalle',
                     'id = WFL_rat_der_buergerhalle\n prerequisite = { focus = WFL_werkbank_am_niederrhein }')
        self.assert_problem('focus prerequisite cycle')

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
                     'recruit_character = WFL_schuetzenkoenig',
                     'recruit_character = WFL_missing')
        self.assert_problem('unknown character reference: WFL_missing')


if __name__ == '__main__':
    unittest.main()
