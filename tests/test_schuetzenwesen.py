"""Focused static regressions for WFL's own authoritarian leadership.

These check project data and localisation, not the game's political UI.
"""

from pathlib import Path
import re
import unittest

from tools.validate_mod import children, field, parse


ROOT = Path(__file__).resolve().parents[1]
JAN = 'WFL_schuetzenkoenig'
# Types in the installed vanilla neutrality group; no global type is redefined.
NEUTRAL_TYPES = {'despotism', 'oligarchism', 'anarchism', 'moderatism', 'centrism',
                 'japan_militarism_ideology'}


def read_script(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return children(next(part for part in children(node) if part.key == key))


class SchuetzenwesenTests(unittest.TestCase):
    def setUp(self):
        self.characters = {}
        for path in sorted((ROOT / 'common/characters').glob('WFL*.txt')):
            for group in parse(path.read_text(encoding='utf-8-sig')):
                if group.key == 'characters':
                    self.characters.update((char.key, char) for char in children(group))
        self.events = {field(event, 'id'): event for event in read_script('events/WFL_events.txt')
                       if event.key == 'country_event'}

    def test_jan_is_the_only_authoritarian_leader(self):
        authoritarian_leaders = []
        wfl_recruited = {node.value for node in read_script('history/countries/WFL - Wesel-Flueren.txt')
                         if node.key == 'recruit_character'}
        for key, character in self.characters.items():
            if key not in wfl_recruited:
                continue
            for role in children(character):
                if role.key == 'country_leader' and field(role, 'ideology') in NEUTRAL_TYPES:
                    authoritarian_leaders.append(key)
        self.assertEqual(authoritarian_leaders, [JAN])
        for supporting_character in ('WFL_buergerrat', 'WFL_direktorium'):
            self.assertFalse(any(role.key == 'country_leader'
                                 for role in children(self.characters[supporting_character])))

    def test_history_selects_jan_at_start(self):
        history = read_script('history/countries/WFL - Wesel-Flueren.txt')
        promoted = [node.value for node in history if node.key == 'promote_character']
        self.assertEqual(promoted, [JAN])
        politics = next(node for node in history if node.key == 'set_politics')
        self.assertEqual(field(politics, 'ruling_party'), 'neutrality')
        self.assertIn(JAN, [node.value for node in history if node.key == 'recruit_character'])

    def test_both_authoritarian_paths_retain_jan(self):
        for event_id in ('wfl.1', 'wfl.3'):
            with self.subTest(event=event_id):
                option = block(self.events[event_id], 'option')
                self.assertEqual([node.value for node in option if node.key == 'promote_character'], [JAN])
                politics = next(node for node in option if node.key == 'set_politics')
                self.assertEqual(field(politics, 'ruling_party'), 'neutrality')
                self.assertFalse(any(node.key == 'recruit_character' for node in option))

    def test_democratic_alternative_remains_available(self):
        president = self.characters['WFL_buergerpraesidium']
        leader = next(role for role in children(president) if role.key == 'country_leader')
        self.assertEqual(field(leader, 'ideology'), 'conservatism')
        option = block(self.events['wfl.2'], 'option')
        self.assertIn('WFL_buergerpraesidium', [node.value for node in option if node.key == 'promote_character'])
        politics = next(node for node in option if node.key == 'set_politics')
        self.assertEqual(field(politics, 'ruling_party'), 'democratic')
        self.assertEqual(field(politics, 'elections_allowed'), 'yes')
        self.assertNotIn(JAN, [node.value for node in option if node.key == 'retire_character'])

    def test_political_portraits_reference_user_assets(self):
        expected = {
            'WFL_buergerrat': 'GFX_portrait_WFL_advisor_13',
            'WFL_buergerpraesidium': 'GFX_portrait_WFL_advisor_14',
            'WFL_direktorium': 'GFX_portrait_WFL_advisor_15',
            JAN: 'GFX_portrait_WFL_jan_graf_von_insel_i',
        }
        for key, portrait in expected.items():
            with self.subTest(character=key):
                portraits = next(node for node in children(self.characters[key]) if node.key == 'portraits')
                civilian = next(node for node in children(portraits) if node.key == 'civilian')
                self.assertEqual(field(civilian, 'large'), portrait)

    def test_schuetzenwesen_names_are_country_specific_in_both_languages(self):
        for language in ('german', 'english'):
            with self.subTest(language=language):
                path = ROOT / 'localisation' / language / f'WFL_l_{language}.yml'
                self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
                localized = dict(re.findall(r'^ ([\w.]+):\d* "(.*)"$',
                                            path.read_text(encoding='utf-8-sig'), re.MULTILINE))
                self.assertEqual(localized['WFL_neutrality_party'], 'Schützenwesen')
                self.assertEqual(localized['WFL_KINGDOM_neutrality_party'], 'Schützenwesen')
                self.assertEqual(localized['WFL_schuetzenkoenig'], 'Jan Graf von Insel I.')
                for global_key in ('neutrality', 'neutrality_desc', 'despotism', 'despotism_desc'):
                    self.assertNotIn(global_key, localized)
                bookmark = (ROOT / 'localisation' / language / f'WFL_map_l_{language}.yml').read_text(encoding='utf-8-sig')
                self.assertIn('Jan Graf von Insel I.', bookmark)

    def test_country_names_follow_identity_for_every_ideology_in_both_languages(self):
        expected = {'WFL': 'Flüren', 'WFL_KINGDOM': 'Flüren',
                    'WFL_GREATER_REICH': 'Groß Flürener Reich'}
        for language in ('german', 'english'):
            localized = {}
            for path in (ROOT / 'localisation' / language).glob('*.yml'):
                localized.update(re.findall(r'^ ([\w.]+):\d* "(.*)"$',
                                           path.read_text(encoding='utf-8-sig'), re.MULTILINE))
            for tag, name in expected.items():
                for ideology in ('', '_democratic', '_neutrality', '_fascism', '_communism'):
                    with self.subTest(language=language, tag=tag, ideology=ideology):
                        self.assertEqual(localized[tag + ideology], name)
                        self.assertEqual(localized[tag + ideology + '_DEF'], name)
                        adjective = ('großflürener' if tag == 'WFL_GREATER_REICH' else 'flürener')
                        if language == 'english':
                            adjective = 'Greater Flürener' if tag == 'WFL_GREATER_REICH' else 'Flürener'
                        self.assertEqual(localized[tag + ideology + '_ADJ'], adjective)


if __name__ == '__main__':
    unittest.main()
