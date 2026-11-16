"""Exercise real referendum scripts across two paid, independent attempts.

The bounded scope fixture is deliberately not a Clausewitz engine simulator;
unknown conditions or effects fail rather than silently succeeding.
"""
from pathlib import Path
import unittest

from tests.test_expansion_safety import ScopeFixture
from tools.validate_mod import children, field, parse

ROOT = Path(__file__).resolve().parents[1]


def block(node, key):
    return next(n for n in children(node) if n.key == key)


class ReferendumWorld(ScopeFixture):
    def __init__(self, events, decisions):
        super().__init__()
        self.events, self.decisions = events, decisions
        self.scheduled, self.used_decisions = [], set()
        self.political_power = 1000
        for country in self.countries.values():
            country.exists = True

    def conditions(self, nodes, stack):
        for node in nodes:
            key, value = node.key, node.value
            current = stack[-1]
            if key in self.countries:
                matches = self.conditions(children(node), stack + [self.countries[key]])
            elif key == 'OR':
                matches = any(self.conditions([n], stack) for n in children(node))
            elif key == 'exists':
                matches = current.exists == (value == 'yes')
            elif key == 'tag':
                matches = current.tag == value
            elif key == 'has_full_control_of_state':
                state = self.states[int(value)]
                matches = state.controller == current.tag and not state.partial_control
            else:
                matches = super().conditions([node], stack)
            if not matches:
                return False
        return True

    def effects(self, nodes, stack=None):
        stack = stack or [self.root]
        previous_if = None
        for node in nodes:
            key, value = node.key, node.value
            current = stack[-1]
            if key == 'if':
                previous_if = self.conditions(children(block(node, 'limit')), stack)
                if previous_if:
                    self.effects([n for n in children(node) if n.key != 'limit'], stack)
            elif key == 'else_if':
                if previous_if is False:
                    previous_if = self.conditions(children(block(node, 'limit')), stack)
                    if previous_if:
                        self.effects([n for n in children(node) if n.key != 'limit'], stack)
            elif key == 'else':
                if previous_if is False:
                    self.effects(children(node), stack)
            elif key in self.countries:
                self.effects(children(node), stack + [self.countries[key]])
            elif key == 'clr_country_flag':
                current.flags.discard(value)
            elif key == 'country_event':
                self.scheduled.append((current.tag, field(node, 'id'),
                                       field(node, 'days') or field(node, 'hours')))
            elif key == 'transfer_state':
                state = self.states[int(value)]
                state.owner = state.controller = current.tag
            elif key == 'add_core_of':
                current.cores.add(value)
            else:
                super().effects([node], stack)

    def available(self, decision_id):
        decision = self.decisions[decision_id]
        return (decision_id not in self.used_decisions
                and self.conditions(children(block(decision, 'visible')), [self.root])
                and self.conditions(children(block(decision, 'available')), [self.root])
                and self.political_power >= int(field(decision, 'cost')))

    def request(self, decision_id):
        if not self.available(decision_id):
            return False
        decision = self.decisions[decision_id]
        self.used_decisions.add(decision_id)
        self.political_power -= int(field(decision, 'cost'))
        self.effects(children(block(decision, 'complete_effect')))
        return True

    def event(self, event_id, recipient='WFL', choice=None):
        current = self.countries[recipient]
        self.root = current
        event = self.events[event_id]
        if not self.conditions(children(block(event, 'trigger')), [current]):
            return False
        for node in children(event):
            if node.key == 'immediate':
                self.effects(children(node), [current])
        if choice is not None:
            self.option(event_id, recipient, choice)
        return True

    def option(self, event_id, recipient, choice):
        # Deliberately apply an old clicked option without its event/option UI
        # triggers: the effect's own guards must still protect the live chain.
        self.root = self.countries[recipient]
        option = [n for n in children(self.events[event_id]) if n.key == 'option'][choice]
        self.effects([n for n in children(option) if n.key not in ('name', 'trigger', 'ai_chance')])

    def as_wfl(self):
        self.root = self.countries['WFL']


class ReferendumAttemptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = {field(n, 'id'): n for n in parse((ROOT / 'events/WFL_referendums.txt')
                                                     .read_text(encoding='utf-8-sig'))
                      if n.key == 'country_event'}
        cls.decisions = {n.key: n for group in parse((ROOT / 'common/decisions/WFL_referendums.txt')
                                                    .read_text(encoding='utf-8-sig')) for n in children(group)}

    def world(self, state):
        world = ReferendumWorld(self.events, self.decisions)
        world.countries['WFL'].flags.add(f'WFL_ref_{state}_campaign_done')
        return world

    def test_first_refusal_unlocks_second_once_at_same_price_but_never_a_third(self):
        for state, first_consent, second_consent in ((51, 1, 21), (57, 11, 31)):
            with self.subTest(state=state):
                world = self.world(state)
                first = f'WFL_referendum_beantragen_{state}'
                second = f'WFL_referendum_zweiter_versuch_{state}'
                self.assertFalse(world.available(second))
                self.assertTrue(world.request(first))
                self.assertFalse(world.available(second))
                world.event(f'wfl_referendum.{first_consent}', 'GER', 1)
                world.as_wfl()
                self.assertTrue(world.request(second))
                self.assertEqual(world.political_power, 800)
                world.event(f'wfl_referendum.{second_consent}', 'GER', 1)
                world.as_wfl()
                self.assertFalse(world.available(first))
                self.assertFalse(world.available(second))
                self.assertEqual(world.states[state].owner, 'GER')
                self.assertNotIn('WFL', world.states[state].cores)

    def test_final_no_unlocks_second_and_second_yes_transfers_and_cores_once(self):
        for state, consent, ballot, second_consent, second_ballot in ((51, 1, 2, 21, 22), (57, 11, 12, 31, 32)):
            with self.subTest(state=state):
                world = self.world(state)
                world.request(f'WFL_referendum_beantragen_{state}')
                world.event(f'wfl_referendum.{consent}', 'GER', 0)
                world.event(f'wfl_referendum.{ballot}', 'GER', 1)
                world.as_wfl()
                self.assertTrue(world.request(f'WFL_referendum_zweiter_versuch_{state}'))
                world.event(f'wfl_referendum.{second_consent}', 'GER', 0)
                world.event(f'wfl_referendum.{second_ballot}', 'GER', 0)
                self.assertEqual(world.states[state].owner, 'WFL')
                self.assertIn('WFL', world.states[state].cores)
                self.assertIn(f'WFL_ref_{state}_joined', world.countries['WFL'].flags)
                world.as_wfl()
                self.assertFalse(world.available(f'WFL_referendum_zweiter_versuch_{state}'))

    def test_first_success_permanently_excludes_second_request(self):
        for state, consent, ballot in ((51, 1, 2), (57, 11, 12)):
            world = self.world(state)
            world.request(f'WFL_referendum_beantragen_{state}')
            world.event(f'wfl_referendum.{consent}', 'GER', 0)
            world.event(f'wfl_referendum.{ballot}', 'GER', 0)
            world.as_wfl()
            self.assertFalse(world.available(f'WFL_referendum_zweiter_versuch_{state}'))
            # Even later loss of the region does not revive a successful chain.
            world.states[state].owner = world.states[state].controller = 'GER'
            world.states[state].cores.discard('WFL')
            self.assertFalse(world.available(f'WFL_referendum_zweiter_versuch_{state}'))

    def test_old_watchdogs_and_old_options_cannot_touch_second_attempt(self):
        for state, consent, ballot, watchdog, second_consent, second_ballot in ((51, 1, 2, 6, 21, 22), (57, 11, 12, 16, 31, 32)):
            with self.subTest(state=state):
                world = self.world(state)
                world.request(f'WFL_referendum_beantragen_{state}')
                world.event(f'wfl_referendum.{consent}', 'GER', 0)
                # The first ballot is left unresolved until its timeout.
                self.assertTrue(world.event(f'wfl_referendum.{watchdog}'))
                world.as_wfl()
                self.assertTrue(world.request(f'WFL_referendum_zweiter_versuch_{state}'))
                world.event(f'wfl_referendum.{second_consent}', 'GER', 0)
                # A stale ballot may clean up its own expired first-host flag,
                # but every live second-round flag must be untouched.
                own_cleanup = f'WFL_ref_{state}_host'
                flags = {tag: c.flags - {own_cleanup} for tag, c in world.countries.items()}
                queue = list(world.scheduled)
                self.assertFalse(world.event(f'wfl_referendum.{watchdog}'))
                for stale_event in (consent, ballot):
                    for option in (0, 1, 2):
                        world.option(f'wfl_referendum.{stale_event}', 'GER', option)
                self.assertEqual(flags, {tag: c.flags - {own_cleanup} for tag, c in world.countries.items()})
                self.assertEqual(queue, world.scheduled)
                self.assertEqual(world.states[state].owner, 'GER')
                self.assertTrue(world.event(f'wfl_referendum.{second_ballot}', 'GER', 0))
                self.assertEqual(world.states[state].owner, 'WFL')

    def test_first_abort_allows_retry_after_conditions_recover_and_second_timeout_is_final(self):
        for state, consent, ballot, watchdog in ((51, 1, 2, 26), (57, 11, 12, 36)):
            with self.subTest(state=state):
                world = self.world(state)
                world.request(f'WFL_referendum_beantragen_{state}')
                world.event(f'wfl_referendum.{consent}', 'GER', 0)
                world.states[state].partial_control = True
                world.option(f'wfl_referendum.{ballot}', 'GER', 0)
                world.as_wfl()
                self.assertFalse(world.available(f'WFL_referendum_zweiter_versuch_{state}'))
                world.states[state].partial_control = False
                self.assertTrue(world.request(f'WFL_referendum_zweiter_versuch_{state}'))
                self.assertTrue(world.event(f'wfl_referendum.{watchdog}'))
                world.as_wfl()
                self.assertFalse(world.available(f'WFL_referendum_zweiter_versuch_{state}'))
                self.assertNotIn(f'WFL_ref_{state}_second_pending', world.countries['WFL'].flags)
                self.assertIn(f'WFL_ref_{state}_second_resolved', world.countries['WFL'].flags)
                self.assertEqual(world.states[state].owner, 'GER')

    def test_second_attempt_rechecks_ownership_control_and_sovereignty(self):
        for state, consent, second_consent, second_ballot in ((51, 1, 21, 22), (57, 11, 31, 32)):
            for failure in ('war', 'partial_control', 'ownership_change', 'subject', 'capitulated'):
                with self.subTest(state=state, failure=failure):
                    world = self.world(state)
                    world.request(f'WFL_referendum_beantragen_{state}')
                    world.event(f'wfl_referendum.{consent}', 'GER', 1)
                    world.as_wfl()
                    world.request(f'WFL_referendum_zweiter_versuch_{state}')
                    world.event(f'wfl_referendum.{second_consent}', 'GER', 0)
                    if failure == 'war': world.countries['WFL'].wars.add('GER')
                    elif failure == 'partial_control': world.states[state].partial_control = True
                    elif failure == 'ownership_change': world.states[state].owner = 'HOL'
                    elif failure == 'subject': world.countries['GER'].overlord = 'HOL'
                    elif failure == 'capitulated': world.countries['WFL'].capitulated = True
                    world.option(f'wfl_referendum.{second_ballot}', 'GER', 0)
                    self.assertNotEqual(world.states[state].owner, 'WFL')
                    self.assertNotIn('WFL', world.states[state].cores)
                    self.assertIn(f'WFL_ref_{state}_second_resolved', world.countries['WFL'].flags)

    def test_both_rounds_have_improved_base_chances_and_original_modifiers(self):
        for consent, ballot in ((1, 2), (11, 12), (21, 22), (31, 32)):
            accept, reject = [n for n in children(self.events[f'wfl_referendum.{consent}']) if n.key == 'option'][:2]
            yes, no = [n for n in children(self.events[f'wfl_referendum.{ballot}']) if n.key == 'option'][:2]
            chances = [block(n, 'ai_chance') for n in (accept, reject, yes, no)]
            factors = [float(field(n, 'factor')) for n in chances]
            self.assertEqual(factors, [25, 75, 60, 40])
            p = factors[0] / sum(factors[:2]) * factors[2] / sum(factors[2:])
            self.assertAlmostEqual(p, .15)
            self.assertAlmostEqual(1 - (1 - p) ** 2, .2775)
            self.assertEqual([field(n, 'factor') for n in children(chances[0]) if n.key == 'modifier'], ['2', '2', '1.5', '0.5'])
            self.assertEqual([field(n, 'factor') for n in children(chances[2]) if n.key == 'modifier'], ['1.5'])


if __name__ == '__main__':
    unittest.main()
