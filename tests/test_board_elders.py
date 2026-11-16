"""Bounded execution of the two board focuses and the mediation decision."""
from decimal import Decimal
import unittest

from tests.test_assembly import AssemblyWorld, MEMBERS, ROOT, block, read
from tools.validate_mod import children, field


RULES = 'WFL_board_bierdeckel_rules'
ELDERS = 'WFL_board_elders_unlocked'


class BoardEldersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = read('common/national_focus/WFL_focus.txt')[0]
        cls.focuses = {field(node, 'id'): node for node in children(tree) if node.key == 'focus'}
        cls.decision = children(read('common/decisions/WFL_board_elders_decisions.txt')[0])[0]
        cls.available = children(block(cls.decision, 'available'))
        cls.reward = children(block(cls.decision, 'complete_effect'))
        cls.lobby = {node.key: node for node in children(read('common/decisions/WFL_assembly.txt')[0])}

    def world(self, rules=False, elders=False):
        world = AssemblyWorld()
        world.triggers.update({node.key: children(node) for node in read('common/scripted_triggers/WFL_board_elders_triggers.txt')})
        world.hook('on_startup')
        if rules:
            world.flags.add(RULES)
        if elders:
            world.flags.add(ELDERS)
        return world

    def test_focus_chain_rewards_unlock_only_the_requested_functions(self):
        first = self.focuses['WFL_geschaeftsordnung_bierdeckel']
        second = self.focuses['WFL_aeltestenrat_tresen']
        for focus, prerequisite in ((first, 'WFL_rat_der_buergerhalle'),
                                    (second, 'WFL_geschaeftsordnung_bierdeckel')):
            self.assertEqual(field(block(focus, 'prerequisite'), 'focus'), prerequisite)
            self.assertEqual(field(focus, 'cost'), '5')
        world = self.world()
        world.effects(children(block(first, 'completion_reward')))
        self.assertIn(RULES, world.flags)
        self.assertNotIn(ELDERS, world.flags)
        world.effects(children(block(second, 'completion_reward')))
        self.assertIn(ELDERS, world.flags)
        self.assertEqual(world.number('WFL_board_mood'), 75)
        self.assertFalse(world.ideas)

    def test_each_cost_helper_reduces_its_loss_by_exactly_one_quarter(self):
        for helper, old, reduced in (('WFL_board_lobby_mood_cost', '12', '9'),
                                     ('WFL_board_collateral_mood_cost', '6', '4.5'),
                                     ('WFL_board_self_mood_cost', '8', '6')):
            for has_rules, cost in ((False, old), (True, reduced)):
                with self.subTest(helper=helper, rules=has_rules):
                    world = self.world(rules=has_rules)
                    world.run(helper)
                    self.assertEqual(world.number('WFL_board_mood'), Decimal(75) - Decimal(cost))
            self.assertEqual(Decimal(reduced), Decimal(old) * Decimal('.75'))

    def test_every_member_uses_reduced_costs_in_all_actual_lobby_branches(self):
        for member in MEMBERS:
            for choices, expected in (([0], '66'), ([1, 0], '61.5'), ([2], '60')):
                with self.subTest(member=member, choices=choices):
                    world = self.world(rules=True)
                    world.choices = list(choices)
                    world.effects(children(block(self.lobby[f'WFL_board_lobby_{member}'], 'complete_effect')))
                    self.assertEqual(world.number('WFL_board_mood'), Decimal(expected))
                    self.assertEqual(world.random_trace[0], (85, 10, 5))
                    self.assertIn(f'WFL_board_{member}_used', world.flags)

    def test_rules_do_not_reduce_assembly_losses_or_monthly_spiral(self):
        for branch, expected in ((1, 65), (2, 55)):
            world = self.world(rules=True)
            world.flags.update(f'WFL_board_{member}_angry' for member in MEMBERS[:2])
            world.choices = [branch]
            world.run('WFL_assembly_resolve')
            self.assertEqual(world.number('WFL_board_mood'), expected)
        world = self.world(rules=True)
        world.variables['WFL_board_mood'] = Decimal(30)
        world.run('WFL_board_mood_refresh')
        world.run('WFL_board_mood_monthly')
        self.assertEqual(world.number('WFL_board_mood'), 28)

    def test_elders_calm_only_first_angry_member_in_portrait_order(self):
        for index in range(len(MEMBERS)):
            with self.subTest(first_angry=MEMBERS[index]):
                world = self.world(elders=True)
                remaining = MEMBERS[index:]
                world.flags.update(f'WFL_board_{member}_angry' for member in remaining)
                world.flags.update(f'WFL_board_{member}_used' for member in MEMBERS)
                world.flags.update(f'WFL_board_{member}_backed' for member in MEMBERS)
                world.variables['WFL_board_mood'] = Decimal(35)
                world.run('WFL_board_mood_refresh')
                self.assertTrue(world.matches(self.available))
                world.effects(self.reward)
                self.assertEqual(world.number('WFL_board_mood'), 45)
                self.assertNotIn('WFL_board_mood_divided_idea', world.ideas)
                self.assertEqual({m for m in MEMBERS if f'WFL_board_{m}_angry' in world.flags}, set(remaining[1:]))
                for member in MEMBERS:
                    self.assertIn(f'WFL_board_{member}_used', world.flags)
                    self.assertIn(f'WFL_board_{member}_backed', world.flags)
                self.assertFalse(world.random_trace)

    def test_mediation_is_locked_guarded_rechecked_and_grants_no_free_promise(self):
        for state in ('locked', 'no_anger', 'capitulated', 'valid'):
            with self.subTest(state=state):
                world = self.world(elders=state != 'locked')
                if state != 'no_anger':
                    world.flags.add('WFL_board_nils_meyer_angry')
                if state == 'capitulated':
                    world.capitulated = True
                self.assertEqual(world.matches(self.available), state == 'valid')
                before = world.number('WFL_board_mood'), set(world.flags)
                if state == 'valid':
                    # The target can be calmed between selecting and executing.
                    world.flags.remove('WFL_board_nils_meyer_angry')
                    before = world.number('WFL_board_mood'), set(world.flags)
                world.effects(self.reward)
                self.assertEqual((world.number('WFL_board_mood'), world.flags), before)
        world = self.world(elders=True)
        world.flags.add('WFL_board_nils_meyer_angry')
        world.effects(self.reward)
        self.assertNotIn('WFL_board_nils_meyer_backed', world.flags)
        self.assertNotIn('WFL_board_nils_meyer_used', world.flags)

    def test_mediation_cost_cooldown_and_high_mood_clamp(self):
        self.assertEqual(field(self.decision, 'cost'), '50')
        self.assertEqual(field(self.decision, 'days_re_enable'), '30')
        self.assertEqual(field(self.decision, 'fire_only_once'), None)
        world = self.world(elders=True)
        world.variables['WFL_board_mood'] = Decimal(99)
        world.flags.add('WFL_board_tim_wissing_angry')
        world.effects(self.reward)
        self.assertEqual(world.number('WFL_board_mood'), 100)
        self.assertNotIn('WFL_board_tim_wissing_angry', world.flags)
        self.assertFalse(world.matches(self.available))


if __name__ == '__main__':
    unittest.main()
