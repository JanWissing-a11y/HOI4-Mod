"""Starting national spirit raises the population quota, without granting a flat pool."""
from decimal import Decimal
import os
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(os.environ.get('HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'))
SPIRIT = 'WFL_volk_unter_schuetzenhut'


def block(node, key):
    return next(n for n in children(node) if n.key == key)


class MobilisationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spirit = children(block(parse((ROOT / 'common/ideas/WFL_mobilisation.txt')
            .read_text(encoding='utf-8-sig'))[0], 'country'))[0]

    def test_starts_active_permanently_and_only_for_wfl(self):
        history = parse((ROOT / 'history/countries/WFL - Wesel-Flueren.txt')
                        .read_text(encoding='utf-8-sig'))
        starting_ideas = [idea for n in history if n.key == 'add_ideas'
                          for idea in ([n.value] if isinstance(n.value, str)
                                       else [entry.key for entry in children(n)])]
        self.assertEqual(starting_ideas.count(SPIRIT), 1)
        self.assertEqual(self.spirit.key, SPIRIT)
        self.assertEqual(field(block(self.spirit, 'allowed'), 'tag'), 'WFL')
        self.assertEqual(field(self.spirit, 'removal_cost'), '-1')
        self.assertEqual({n.key for n in children(self.spirit)},
                         {'picture', 'allowed', 'removal_cost', 'modifier'})
        # No calendar/event/decision gate, forced conscription-law change or
        # on-add manpower grant is attached to this passive national spirit.
        self.assertEqual({n.key for n in children(block(self.spirit, 'modifier'))}, {'conscription'})

    @unittest.skipUnless((GAME / 'common/ideas/_manpower.txt').is_file(), 'local game required')
    def test_adds_twenty_percentage_points_to_the_real_starting_law(self):
        source = parse((GAME / 'common/ideas/_manpower.txt').read_text(encoding='utf-8-sig'))
        law = next(n for n in walk(source) if n.key == 'volunteer_only' and children(n))
        starting_quota = Decimal(field(block(law, 'modifier'), 'conscription'))
        extra_quota = Decimal(field(block(self.spirit, 'modifier'), 'conscription'))
        self.assertEqual(extra_quota, Decimal('0.20'))
        self.assertEqual(starting_quota + extra_quota, Decimal('0.215'))
        self.assertNotEqual(starting_quota + extra_quota,
                            starting_quota * (1 + extra_quota))
        # At the prototype's 240,000 core population, the quota increases by
        # 48,000 potential recruits before mobilization and already-used men.
        state = parse((ROOT / 'history/states/1082-Wesel-Flueren.txt')
                      .read_text(encoding='utf-8-sig'))[0]
        population = Decimal(field(state, 'manpower'))
        self.assertEqual(population * extra_quota, Decimal('48000'))

    def test_both_localisations_explain_the_additive_quota_and_mobilization(self):
        for language, expected in [('german', ('20 Prozentpunkte', 'Mobilisierung')),
                                   ('english', ('20 percentage points', 'mobilization'))]:
            raw = (ROOT / f'localisation/{language}/WFL_mobilisation_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            text = raw.decode('utf-8-sig')
            self.assertIn(f' {SPIRIT}:0 ', text)
            self.assertIn(f' {SPIRIT}_desc:0 ', text)
            self.assertTrue(all(phrase in text for phrase in expected))


if __name__ == '__main__':
    unittest.main()
