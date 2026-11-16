"""Execute the real German integration guards in bounded state fixtures.

Only the trigger/effect subset used here is modelled, not the game engine.
"""
from pathlib import Path
import unittest

from tests.test_expansion_safety import Country, ScopeFixture, State
from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
DECISION = 'WFL_deutschland_unter_schuetzenhut_vereinen'
DONE = 'WFL_deutschland_vereint_done'
SPIRIT = 'WFL_volk_unter_schuetzenhut'
# Independently recorded from vanilla 1.19's undated German state history,
# plus the mod's Wesel-Flueren split. Later German gains are not prerequisites.
GERMANY_1936 = (5, 42, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                61, 62, 63, 64, 65, 66, 67, 68, 763, 909, 978, 1082)
EASTERN_CLAIMS = (85, 188, 807, 86, 762)


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return next(n for n in children(node) if n.key == key)


class GermanIntegrationWorld(ScopeFixture):
    def __init__(self):
        super().__init__()
        self.ideas = {SPIRIT}
        self.triggers = {n.key: children(n) for n in
                         read('common/scripted_triggers/WFL_german_integration_triggers.txt')}
        self.states = {key: State('WFL', 'WFL', {'GER'}) for key in GERMANY_1936}
        self.states[1082].cores.add('WFL')
        # Danzig and the other eastern claims are deliberately outside the
        # 1936 border and are not all German cores at the start of a campaign.
        self.states.update({key: State('POL', 'POL', {'POL'}) for key in EASTERN_CLAIMS})
        self.states[463] = State('WFL', 'WFL', {'USA'})
        self.states[464] = State('USA', 'USA', {'USA'})
        self.states[465] = State('USA', 'USA', {'USA'})
        self.claims = {85: {'GER'}, 464: {'WFL'}}

    def target(self, value, stack):
        # Core ownership is a tag relation even if the original country no
        # longer exists on the map, as after annexation.
        if value not in ('ROOT', 'PREV'):
            return self.countries.get(value, Country(value))
        return super().target(value, stack)

    def conditions(self, nodes, stack):
        for node in nodes:
            if node.key in self.triggers:
                valid = self.conditions(self.triggers[node.key], stack) == (node.value == 'yes')
            elif node.key == 'any_state':
                valid = any(self.conditions(children(node), stack + [state])
                            for state in self.states.values())
            elif node.key == 'OR':
                valid = any(self.conditions([entry], stack) for entry in children(node))
            elif node.key == 'AND':
                valid = self.conditions(children(node), stack)
            elif node.key == 'tag':
                valid = stack[-1].tag == node.value
            else:
                valid = super().conditions([node], stack)
            if not valid:
                return False
        return True

    def effects(self, nodes, stack=None):
        stack = stack or [self.root]
        for node in nodes:
            if node.key == 'every_state':
                limit = children(block(node, 'limit'))
                body = [entry for entry in children(node) if entry.key != 'limit']
                for state in self.states.values():
                    if self.conditions(limit, stack + [state]):
                        self.effects(body, stack + [state])
            elif node.key == 'add_core_of':
                stack[-1].cores.add(self.target(node.value, stack).tag)
            elif node.key == 'add_claim_by':
                key = next(key for key, state in self.states.items() if state is stack[-1])
                self.claims.setdefault(key, set()).add(self.target(node.value, stack).tag)
            elif node.key == 'remove_ideas':
                self.ideas.discard(node.value)
            else:
                super().effects([node], stack)


class GermanIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.category = parse((ROOT / 'common/decisions/categories/WFL_german_integration.txt')
                             .read_text(encoding='utf-8-sig'))[0]
        group = parse((ROOT / 'common/decisions/WFL_german_integration.txt')
                      .read_text(encoding='utf-8-sig'))[0]
        cls.decision = next(n for n in children(group) if n.key == DECISION)
        cls.available = children(block(cls.decision, 'available'))
        cls.effect = children(block(cls.decision, 'complete_effect'))

    def test_complete_germany_gets_cores_and_loses_only_the_mobilisation_spirit(self):
        world = GermanIntegrationWorld()
        world.ideas.add('WFL_rheinhandel')
        owners = {key: state.owner for key, state in world.states.items()}
        original_cores = {key: set(state.cores) for key, state in world.states.items()}
        self.assertTrue(world.conditions(self.available, [world.root]))
        world.effects(self.effect)
        for key in GERMANY_1936:
            self.assertIn('WFL', world.states[key].cores)
            self.assertTrue(original_cores[key] <= world.states[key].cores)
        self.assertEqual(world.states[463].cores, {'USA'})
        self.assertEqual(owners, {key: state.owner for key, state in world.states.items()})
        self.assertEqual(world.ideas, {'WFL_rheinhandel'})
        self.assertIn(DONE, world.root.flags)

    def test_incomplete_ownership_or_control_never_removes_the_spirit_or_grants_cores(self):
        for change, value in [('owner', 'GER'), ('owner', 'HOL'), ('controller', 'HOL'),
                              ('partial_control', True)]:
            with self.subTest(change=change, value=value):
                world = GermanIntegrationWorld()
                setattr(world.states[57], change, value)
                before = {key: set(s.cores) for key, s in world.states.items()}
                self.assertFalse(world.conditions(self.available, [world.root]))
                world.effects(self.effect)
                self.assertEqual(before, {key: s.cores for key, s in world.states.items()})
                self.assertIn(SPIRIT, world.ideas)
                self.assertNotIn(DONE, world.root.flags)
                self.assertNotIn('WFL', world.claims[85])

    def test_annexed_germany_war_or_subject_status_do_not_add_unrequested_gates(self):
        world = GermanIntegrationWorld()
        del world.countries['GER']
        world.root.wars.add('HOL')
        world.root.overlord = 'USA'
        self.assertTrue(world.conditions(self.available, [world.root]))
        world.effects(self.effect)
        self.assertIn(DONE, world.root.flags)
        self.assertNotIn(SPIRIT, world.ideas)

    def test_foreign_later_german_cores_do_not_gate_unification_and_receive_claims(self):
        world = GermanIntegrationWorld()
        world.states[999] = State('HOL', 'HOL', {'GER'})
        self.assertTrue(world.conditions(self.available, [world.root]))
        world.effects(self.effect)
        self.assertEqual(world.states[999].cores, {'GER'})
        self.assertEqual(world.claims[999], {'WFL'})
        self.assertNotIn(SPIRIT, world.ideas)

    def test_acquired_later_german_core_is_integrated_only_with_full_control(self):
        for control in ('WFL', 'HOL'):
            with self.subTest(control=control):
                world = GermanIntegrationWorld()
                world.states[999] = State('WFL', control, {'GER'})
                self.assertTrue(world.conditions(self.available, [world.root]))
                world.effects(self.effect)
                self.assertEqual('WFL' in world.states[999].cores, control == 'WFL')
                self.assertNotIn(999, world.claims)

    def test_1936_border_is_fixed_even_if_germany_loses_its_original_cores(self):
        world = GermanIntegrationWorld()
        for key in GERMANY_1936:
            world.states[key].cores.discard('GER')
        self.assertTrue(world.conditions(self.available, [world.root]))
        world.effects(self.effect)
        self.assertTrue(all('WFL' in world.states[key].cores for key in GERMANY_1936))
        self.assertNotIn(SPIRIT, world.ideas)

    def test_danzig_and_other_eastern_claims_remain_foreign_without_blocking_or_auto_coring(self):
        world = GermanIntegrationWorld()
        self.assertTrue(world.conditions(self.available, [world.root]))
        world.effects(self.effect)
        for key in EASTERN_CLAIMS:
            self.assertEqual(world.states[key].owner, 'POL')
            self.assertNotIn('WFL', world.states[key].cores)
            self.assertIn('WFL', world.claims[key])
        self.assertIn('GER', world.claims[85])
        # Existing unrelated claims survive; no new claim is fabricated there.
        self.assertEqual(world.claims[464], {'WFL'})
        self.assertNotIn(463, world.claims)
        self.assertNotIn(465, world.claims)

    def test_every_1936_state_is_required_and_no_later_gain_is_required(self):
        trigger = GermanIntegrationWorld().triggers['WFL_controls_germany_1936']
        self.assertEqual({int(node.key) for node in trigger}, set(GERMANY_1936))
        for key in GERMANY_1936:
            with self.subTest(state=key):
                world = GermanIntegrationWorld()
                world.states[key].owner = 'GER'
                self.assertFalse(world.conditions(self.available, [world.root]))
                world.effects(self.effect)
                self.assertNotIn(DONE, world.root.flags)
                self.assertIn(SPIRIT, world.ideas)

    def test_execution_rechecks_a_state_lost_after_the_button_became_available(self):
        for change, value in [('owner', 'HOL'), ('controller', 'GER'), ('partial_control', True)]:
            with self.subTest(change=change):
                world = GermanIntegrationWorld()
                self.assertTrue(world.conditions(self.available, [world.root]))
                setattr(world.states[51], change, value)
                world.effects(self.effect)
                self.assertNotIn('WFL', world.states[57].cores)
                self.assertIn(SPIRIT, world.ideas)
                self.assertNotIn(DONE, world.root.flags)
                # A failed execution remains retryable after control returns.
                world.states[51].owner = world.states[51].controller = 'WFL'
                world.states[51].partial_control = False
                self.assertTrue(world.conditions(self.available, [world.root]))
                world.effects(self.effect)
                self.assertNotIn(SPIRIT, world.ideas)

    def test_success_is_once_only_but_does_not_require_the_spirit_to_exist(self):
        world = GermanIntegrationWorld()
        world.ideas.clear()
        world.effects(self.effect)
        self.assertIn('WFL', world.states[51].cores)
        self.assertIn(DONE, world.root.flags)
        self.assertFalse(world.conditions(self.available, [world.root]))
        world.states[999] = State('WFL', 'WFL', {'GER'})
        world.ideas.add(SPIRIT)
        world.effects(self.effect)
        self.assertEqual(world.states[999].cores, {'GER'})
        self.assertIn(SPIRIT, world.ideas)

    def test_country_scope_free_cost_guarded_effects_and_localized_loss_warning(self):
        self.assertEqual(field(block(self.category, 'allowed'), 'tag'), 'WFL')
        self.assertEqual(field(self.decision, 'cost'), '0')
        self.assertIsNone(field(self.decision, 'fire_only_once'))
        self.assertEqual([n.key for n in self.effect], ['if'])
        guarded = self.effect[0]
        self.assertEqual(children(block(guarded, 'limit')), self.available)
        self.assertIn('WFL_controls_germany_1936', {n.key for n in self.available})
        self.assertNotIn('transfer_state', {n.key for n in walk(self.effect)})
        self.assertNotIn('remove_core_of', {n.key for n in walk(self.effect)})
        for language, description in [('german', '20 Prozentpunkte'), ('english', '20 percentage points')]:
            raw = (ROOT / f'localisation/{language}/WFL_german_integration_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            text = raw.decode('utf-8-sig')
            self.assertIn(f' {DECISION}:0 ', text)
            self.assertIn(f' {DECISION}_desc:0 ', text)
            self.assertIn(description, text)


if __name__ == '__main__':
    unittest.main()
