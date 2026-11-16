"""Check recruitment-drive costs, caps and delayed-reward safety in real scripts.

These inspect Clausewitz data and do not simulate occupation or mobilization.
"""
from decimal import Decimal
from pathlib import Path
import unittest

from tools.validate_mod import Node, children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
STAGES = (
    ('WFL_koenigliche_freibieroffensive', 'WFL_freibierfreiwillige', 50, 30),
    ('WFL_kartoffelsalat_ohne_grenzen', 'WFL_kartoffelsalat_kameraden', 75, 45),
    ('WFL_blasmusik_statt_formulare', 'WFL_blasmusik_bataillone', 100, 60),
    ('WFL_der_grosse_schuetzenpass', 'WFL_schuetzenpass_freiwillige', 125, 90),
)


def block(node: Node, key: str) -> Node:
    matches = [part for part in children(node) if part.key == key]
    if len(matches) != 1:
        raise AssertionError(f'Expected one {key} block in {node.key}, got {len(matches)}')
    return matches[0]


def pairs(node: Node):
    return {(part.key, part.value) for part in children(node) if isinstance(part.value, str)}


class RecruitmentFestivalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.category = parse((ROOT / 'common/decisions/categories/WFL_recruitment_festivals.txt')
                             .read_text(encoding='utf-8-sig'))[0]
        cls.group = parse((ROOT / 'common/decisions/WFL_recruitment_festivals.txt')
                          .read_text(encoding='utf-8-sig'))[0]
        cls.decisions = {node.key: node for node in children(cls.group)}
        ideas = parse((ROOT / 'common/ideas/WFL_recruitment_festivals.txt')
                      .read_text(encoding='utf-8-sig'))[0]
        cls.ideas = {node.key: node for node in children(block(ideas, 'country'))}

    def assert_jan_and_noncore_requirement(self, node):
        self.assertTrue({('tag', 'WFL'), ('exists', 'yes'), ('has_capitulated', 'no')} <= pairs(node))
        self.assertEqual(pairs(block(node, 'has_country_leader')),
                         {('character', 'WFL_schuetzenkoenig'), ('ruling_only', 'yes')})
        choices = block(node, 'OR')
        self.assertEqual({part.key for part in children(choices)}, {'any_owned_state', 'any_controlled_state'})
        for key in ('any_owned_state', 'any_controlled_state'):
            self.assertEqual(pairs(block(block(choices, key), 'NOT')), {('is_core_of', 'ROOT')})

    def test_category_is_limited_to_wfl_under_jan(self):
        self.assertEqual(self.group.key, self.category.key)
        self.assertEqual(pairs(block(self.category, 'allowed')), {('tag', 'WFL')})
        visible = block(self.category, 'visible')
        self.assertIn(('tag', 'WFL'), pairs(visible))
        self.assertEqual(pairs(block(visible, 'has_country_leader')),
                         {('character', 'WFL_schuetzenkoenig'), ('ruling_only', 'yes')})

    def test_four_once_only_paid_and_timed_stages(self):
        self.assertEqual(set(self.decisions), {stage[0] for stage in STAGES})
        for decision_id, _, cost, days in STAGES:
            with self.subTest(decision=decision_id):
                decision = self.decisions[decision_id]
                self.assertEqual(field(decision, 'cost'), str(cost))
                self.assertEqual(field(decision, 'days_remove'), str(days))
                self.assertEqual(field(decision, 'fire_only_once'), 'yes')
                available = block(decision, 'available')
                self.assertTrue(any(('has_country_flag', decision_id + '_started') in pairs(part)
                                    for part in children(available) if part.key == 'NOT'))
                effect = block(decision, 'complete_effect')
                self.assertTrue({('set_country_flag', decision_id + '_started'),
                                 ('set_country_flag', decision_id + '_active')} <= pairs(effect))

    def test_each_stage_rechecks_jan_and_noncore_territory(self):
        for decision_id, _, _, _ in STAGES:
            with self.subTest(decision=decision_id):
                decision = self.decisions[decision_id]
                self.assert_jan_and_noncore_requirement(block(decision, 'available'))
                self.assert_jan_and_noncore_requirement(block(block(block(decision, 'cancel_trigger'), 'NOT'), 'AND'))
                self.assert_jan_and_noncore_requirement(block(block(block(decision, 'remove_effect'), 'if'), 'limit'))
                # Occupation during a war remains eligible; the controlled-state
                # branch must not be disabled by a peacetime-only condition.
                self.assertFalse(any(node.key == 'has_war' and node.value == 'no'
                                     for node in walk(children(decision))))

    def test_stages_require_the_previous_completed_drive(self):
        for index, (decision_id, _, _, _) in enumerate(STAGES):
            decision = self.decisions[decision_id]
            previous = STAGES[index - 1][1] if index else None
            guard = block(block(block(decision, 'remove_effect'), 'if'), 'limit')
            for requirement in (block(decision, 'available'), guard):
                prerequisites = {part.value for part in children(requirement) if part.key == 'has_idea'}
                self.assertEqual(prerequisites, {previous} if previous else set())

    def test_cancellation_negates_one_explicit_conjunction(self):
        for decision_id, _, _, _ in STAGES:
            with self.subTest(decision=decision_id):
                cancellation = block(self.decisions[decision_id], 'cancel_trigger')
                self.assertEqual([part.key for part in children(cancellation)], ['NOT'])
                negation = block(cancellation, 'NOT')
                # Negating one AND has the same outcome whether the engine
                # interprets multiple NOT children as a negated AND or a NOR.
                self.assertEqual([part.key for part in children(negation)], ['AND'])
                self.assert_jan_and_noncore_requirement(block(negation, 'AND'))

    def test_cancelled_or_duplicate_drives_cannot_grant_a_bonus(self):
        for decision_id, idea_id, _, _ in STAGES:
            with self.subTest(decision=decision_id):
                decision = self.decisions[decision_id]
                cancelled = block(decision, 'cancel_effect')
                self.assertIn(('clr_country_flag', decision_id + '_active'), pairs(cancelled))
                for effect_name in ('complete_effect', 'cancel_effect'):
                    self.assertFalse(any(node.key == 'add_ideas' for node in walk(children(block(decision, effect_name)))))
                removal = block(decision, 'remove_effect')
                branch = block(removal, 'if')
                guard = block(branch, 'limit')
                self.assertIn(('has_country_flag', decision_id + '_active'), pairs(guard))
                self.assertTrue(any(('has_idea', idea_id) in pairs(part)
                                    for part in children(guard) if part.key == 'NOT'))
                self.assertIn(('add_ideas', idea_id), pairs(branch))
                rewards = [node for node in walk(children(removal)) if node.key == 'add_ideas']
                self.assertEqual([node.value for node in rewards], [idea_id])
                self.assertIn(('clr_country_flag', decision_id + '_active'), pairs(removal))

    def test_bonus_is_capped_at_twenty_percentage_points(self):
        self.assertEqual(set(self.ideas), {stage[1] for stage in STAGES})
        total = Decimal('0')
        for idea in self.ideas.values():
            self.assertEqual(pairs(block(idea, 'allowed')), {('tag', 'WFL')})
            self.assertEqual(field(idea, 'removal_cost'), '-1')
            modifier = block(idea, 'modifier')
            self.assertEqual(pairs(modifier), {('non_core_manpower', '0.05')})
            total += Decimal(field(modifier, 'non_core_manpower'))
        self.assertEqual(total, Decimal('0.20'))

    def test_no_direct_manpower_unit_or_political_power_rewards(self):
        forbidden = {'add_manpower', 'create_unit', 'add_political_power', 'transfer_state', 'add_core_of', 'add_state_core'}
        self.assertFalse({node.key for node in walk(children(self.group))} & forbidden)


if __name__ == '__main__':
    unittest.main()
