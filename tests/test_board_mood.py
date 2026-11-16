"""Execute the persistent mood scripts, not a copied mood implementation."""
from datetime import date
from decimal import Decimal
import unittest

from tests.test_assembly import AssemblyWorld, MEMBERS, ROOT, block, read
from tools.validate_mod import children, field


MOOD = 'WFL_board_mood'
INITIALIZED = 'WFL_board_mood_initialized'
DIVIDED = 'WFL_board_mood_divided_idea'
HOSTILE = 'WFL_board_mood_hostile_idea'


class BoardMoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        group = read('common/decisions/WFL_board_mood_decisions.txt')[0]
        cls.recovery = {node.key: node for node in children(group)}
        group = read('common/decisions/WFL_assembly.txt')[0]
        cls.lobby = {node.key: node for node in children(group)}

    def world(self, mood=None):
        world = AssemblyWorld()
        world.hook('on_startup')
        if mood is not None:
            world.variables[MOOD] = Decimal(mood)
            world.run('WFL_board_mood_refresh')
        return world

    def recover(self, world, key):
        decision = self.recovery[key]
        self.assertTrue(world.matches(children(block(decision, 'available'))))
        world.effects(children(block(decision, 'complete_effect')))

    def test_migration_initializes_existing_assembly_once_and_reload_preserves_zero(self):
        world = AssemblyWorld()
        world.now = date(1939, 3, 15)
        world.flags.add('WFL_assembly_initialized')
        world.flag_dates['WFL_assembly_initialized'] = date(1939, 1, 1)
        world.variables['WFL_assembly_months_left'] = Decimal(2)
        world.variables['WFL_assembly_number'] = Decimal(4)
        world.flags.add('WFL_board_nils_meyer_backed')
        world.hook('on_daily_WFL')
        self.assertEqual(world.number(MOOD), 75)
        self.assertIn(INITIALIZED, world.flags)
        self.assertEqual(world.number('WFL_assembly_months_left'), 2)
        self.assertEqual(world.number('WFL_assembly_number'), 4)
        self.assertIn('WFL_board_nils_meyer_backed', world.flags)
        world.variables[MOOD] = Decimal(0)
        world.hook('on_startup')
        world.hook('on_daily_WFL')
        self.assertEqual(world.number(MOOD), 0)
        self.assertIn(HOSTILE, world.ideas)

    def test_mood_boundaries_clamp_and_only_one_stability_tier_survives(self):
        for value, clamped, expected in ((-12, 0, HOSTILE), (0, 0, HOSTILE),
                                        (19, 19, HOSTILE), (20, 20, DIVIDED),
                                        (39, 39, DIVIDED), (40, 40, None),
                                        (60, 60, None), (100, 100, None), (120, 100, None)):
            with self.subTest(value=value):
                world = self.world()
                world.ideas.update((DIVIDED, HOSTILE, 'WFL_rheinhandel'))
                world.variables[MOOD] = Decimal(value)
                world.run('WFL_board_mood_refresh')
                self.assertEqual(world.number(MOOD), clamped)
                self.assertEqual(world.ideas & {DIVIDED, HOSTILE}, {expected} if expected else set())
                self.assertIn('WFL_rheinhandel', world.ideas)

    def test_every_lobby_branch_pays_mood_and_bad_outcomes_pay_extra(self):
        for member in MEMBERS:
            for branch, expected, choices in ((0, 63, [0]), (1, 57, [1, 0]), (2, 55, [2])):
                with self.subTest(member=member, branch=branch):
                    world = self.world()
                    world.choices = choices
                    decision = self.lobby[f'WFL_board_lobby_{member}']
                    world.effects(children(block(decision, 'complete_effect')))
                    self.assertEqual(world.number(MOOD), expected)
                    before = world.number(MOOD)
                    world.effects(children(block(decision, 'complete_effect')))
                    self.assertEqual(world.number(MOOD), before, 'Used decision must not drain mood again')

    def test_three_successful_lobbies_tip_stability_and_six_reach_hostility(self):
        world = self.world()
        for index, member in enumerate(MEMBERS):
            world.effects(children(block(self.lobby[f'WFL_board_lobby_{member}'], 'complete_effect')))
            if index == 2:
                self.assertEqual(world.number(MOOD), 39)
                self.assertIn(DIVIDED, world.ideas)
        self.assertEqual(world.number(MOOD), 3)
        self.assertIn(HOSTILE, world.ideas)
        self.assertNotIn(DIVIDED, world.ideas)

    def test_bad_assemblies_reduce_mood_immediately(self):
        for branch, expected in ((0, 75), (1, 65), (2, 55)):
            world = self.world()
            world.flags.update(f'WFL_board_{member}_angry' for member in MEMBERS[:2])
            world.choices = [branch]
            world.run('WFL_assembly_resolve')
            self.assertEqual(world.number(MOOD), expected)
            self.assertEqual(world.random_trace[0], (70, 20, 10))

    def test_monthly_mali_feed_spiral_and_healthy_months_recover(self):
        cases = ((75, set(), 77), (39, set(), 37),
                 (30, {'WFL_assembly_blockade_idea'}, 27),
                 (30, {'WFL_assembly_eklat_idea'}, 25),
                 (30, {'WFL_assembly_blockade_idea', 'WFL_assembly_eklat_idea'}, 25),
                 (1, {'WFL_assembly_eklat_idea'}, 0), (99, set(), 100))
        for initial, ideas, expected in cases:
            with self.subTest(initial=initial, ideas=ideas):
                world = self.world(initial)
                world.ideas.update(ideas)
                world.run('WFL_board_mood_monthly')
                self.assertEqual(world.number(MOOD), expected)
        world = self.world(30)
        world.capitulated = True
        world.run('WFL_board_mood_monthly')
        self.assertEqual(world.number(MOOD), 30)

    def test_recovery_costs_cooldowns_gains_and_individual_anger_stays(self):
        expected = {
            'WFL_board_kameradschaftsabend': (35, 30, 15),
            'WFL_board_kassensturz': (50, 60, 25),
            'WFL_board_versoehnungsgrillen': (70, 90, 35),
        }
        self.assertEqual(set(self.recovery), set(expected))
        for key, (cost, cooldown, gain) in expected.items():
            with self.subTest(decision=key):
                world = self.world(10)
                world.flags.add('WFL_board_nils_meyer_angry')
                self.assertEqual(field(self.recovery[key], 'cost'), str(cost))
                self.assertEqual(field(self.recovery[key], 'days_re_enable'), str(cooldown))
                self.recover(world, key)
                self.assertEqual(world.number(MOOD), 10 + gain)
                self.assertIn('WFL_board_nils_meyer_angry', world.flags)
                self.assertNotIn(HOSTILE, world.ideas)
                self.assertEqual(DIVIDED in world.ideas, 10 + gain < 40)
                world.variables[MOOD] = Decimal(99)
                self.recover(world, key)
                self.assertEqual(world.number(MOOD), 100)
                self.assertFalse(world.matches(children(block(self.recovery[key], 'available'))))
                world.capitulated = True
                world.variables[MOOD] = Decimal(10)
                world.effects(children(block(self.recovery[key], 'complete_effect')))
                self.assertEqual(world.number(MOOD), 10)

    def test_capitulation_suppresses_stability_penalty_without_resetting_mood(self):
        world = self.world(10)
        self.assertIn(HOSTILE, world.ideas)
        world.capitulated = True
        world.hook('on_daily_WFL')
        self.assertEqual(world.number(MOOD), 10)
        self.assertFalse(world.ideas & {DIVIDED, HOSTILE})
        world.capitulated = False
        world.hook('on_daily_WFL')
        self.assertEqual(world.number(MOOD), 10)
        self.assertIn(HOSTILE, world.ideas)

    def test_monthly_hook_changes_mood_but_assembly_does_not_reset_it_to_default(self):
        world = self.world(50)
        world.now = date(1936, 7, 1)
        world.variables['WFL_assembly_months_left'] = Decimal(1)
        world.hook('on_monthly_WFL')
        self.assertEqual(world.number('WFL_assembly_number'), 1)
        self.assertEqual(world.number(MOOD), 52)
        self.assertEqual(world.scheduled, [('news_event', 'wfl_assembly.1')])

    def test_stability_penalties_have_exact_exclusive_values(self):
        definitions = {}
        for path in (ROOT / 'common/ideas').glob('WFL_*mood*.txt'):
            for group in read(path.relative_to(ROOT)):
                for section in children(group):
                    definitions.update((node.key, node) for node in children(section))
        for key, value in ((DIVIDED, '-0.05'), (HOSTILE, '-0.10')):
            actual = {node.key: Decimal(node.value) for node in children(block(definitions[key], 'modifier'))}
            self.assertEqual(actual, {'stability_factor': Decimal(value)})


if __name__ == '__main__':
    unittest.main()
