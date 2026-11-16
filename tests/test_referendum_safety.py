"""Check territory-transfer safety invariants in the actual referendum scripts.

These are structural checks of high-impact guards, not an engine simulator.
"""
from pathlib import Path
import unittest

from tools.validate_mod import Node, children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]


def blocks(node: Node, key: str):
    return [part for part in children(node) if part.key == key]


def direct_pairs(node: Node):
    return {(part.key, part.value) for part in children(node) if isinstance(part.value, str)}


class ReferendumSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodes = parse((ROOT / 'events/WFL_referendums.txt').read_text(encoding='utf-8-sig'))
        cls.events = {field(node, 'id'): node for node in nodes if node.key == 'country_event'}
        decisions = parse((ROOT / 'common/decisions/WFL_referendums.txt').read_text(encoding='utf-8-sig'))
        cls.decisions = {node.key: node for category in decisions for node in children(category)}

    def assert_has_pairs(self, node, *pairs):
        self.assertTrue(set(pairs) <= direct_pairs(node), (node.key, pairs, direct_pairs(node)))

    def option(self, event_id, suffix):
        options = [option for option in blocks(self.events[event_id], 'option')
                   if field(option, 'name') == event_id + '.' + suffix]
        self.assertEqual(len(options), 1)
        return options[0]

    def test_transfers_only_in_guarded_final_yes_options(self):
        expected_events = {'wfl_referendum.2': ('51', ''), 'wfl_referendum.12': ('57', ''),
                           'wfl_referendum.22': ('51', 'second_'), 'wfl_referendum.32': ('57', 'second_')}
        found = set()
        for event_id, event in self.events.items():
            for option in blocks(event, 'option'):
                transfers = [node for node in walk(children(option)) if node.key == 'transfer_state']
                cores = [node for node in walk(children(option)) if node.key == 'add_core_of']
                if not transfers and not cores:
                    continue
                self.assertIn(event_id, expected_events)
                state, attempt = expected_events[event_id]
                found.add(event_id)
                self.assertEqual(field(option, 'name'), event_id + '.a')
                self.assertEqual([node.value for node in transfers], [state])
                self.assertEqual([node.value for node in cores], ['WFL'])
                branch = blocks(option, 'if')
                self.assertEqual(len(branch), 1)
                limit = blocks(branch[0], 'limit')
                self.assertEqual(len(limit), 1)
                self.assert_has_pairs(limit[0], ('exists', 'yes'), ('has_war', 'no'),
                                      ('is_subject', 'no'), ('has_capitulated', 'no'),
                                      ('has_country_flag', f'WFL_ref_{state}_{attempt}host'))
                wfl_scopes = blocks(limit[0], 'WFL')
                wfl_pairs = set().union(*(direct_pairs(scope) for scope in wfl_scopes))
                self.assertTrue({('exists', 'yes'), ('has_war', 'no'), ('is_subject', 'no'),
                                 ('has_capitulated', 'no'),
                                 ('has_country_flag', f'WFL_ref_{state}_{attempt}pending'),
                                 ('has_country_flag', f'WFL_ref_{state}_{attempt}approved')} <= wfl_pairs)
                self.assertTrue(any(('has_country_flag', f'WFL_ref_{state}_{attempt}resolved') in direct_pairs(negation)
                                    for scope in wfl_scopes for negation in blocks(scope, 'NOT')))
                state_scope = blocks(limit[0], state)
                self.assertEqual(len(state_scope), 1)
                self.assert_has_pairs(state_scope[0], ('is_owned_by', 'ROOT'), ('is_fully_controlled_by', 'ROOT'))
                # The transfer and core must both remain inside this guarded
                # branch and retain their respective country/state scopes.
                self.assertTrue(any(('transfer_state', state) in direct_pairs(scope)
                                    for scope in blocks(branch[0], 'WFL')))
                self.assertTrue(any(('add_core_of', 'WFL') in direct_pairs(scope)
                                    for scope in blocks(branch[0], state)))
        self.assertEqual(found, set(expected_events))

    def test_consent_and_rejections_never_transfer_territory(self):
        for consent, ballot in (('wfl_referendum.1', 'wfl_referendum.2'),
                                ('wfl_referendum.11', 'wfl_referendum.12'),
                                ('wfl_referendum.21', 'wfl_referendum.22'),
                                ('wfl_referendum.31', 'wfl_referendum.32')):
            for node in walk(children(self.events[consent])):
                self.assertNotIn(node.key, ('transfer_state', 'add_core_of'))
            for suffix in ('b', 'c'):
                for node in walk(children(self.option(ballot, suffix))):
                    self.assertNotIn(node.key, ('transfer_state', 'add_core_of'))

    def test_campaigns_are_paid_timed_and_once_only(self):
        for state in ('51', '57'):
            with self.subTest(state=state):
                campaign = self.decisions['WFL_schuetzenkampagne_' + state]
                self.assert_has_pairs(campaign, ('cost', '75'), ('days_remove', '90'), ('fire_only_once', 'yes'))
                available = blocks(campaign, 'available')[0]
                self.assert_has_pairs(available, ('has_war', 'no'), ('is_subject', 'no'))
                self.assert_has_pairs(blocks(campaign, 'complete_effect')[0],
                                      ('set_country_flag', f'WFL_ref_{state}_campaign_started'))

    def test_requests_require_completed_campaign_and_expire(self):
        for state, consent in (('51', 'wfl_referendum.1'), ('57', 'wfl_referendum.11')):
            with self.subTest(state=state):
                request = self.decisions['WFL_referendum_beantragen_' + state]
                self.assert_has_pairs(request, ('cost', '100'), ('fire_only_once', 'yes'))
                visible = blocks(request, 'visible')[0]
                self.assert_has_pairs(visible, ('has_country_flag', f'WFL_ref_{state}_campaign_done'))
                self.assertTrue(any(('has_country_flag', f'WFL_ref_{state}_requested') in direct_pairs(node)
                                    for node in blocks(visible, 'NOT')))
                effect = blocks(request, 'complete_effect')[0]
                self.assert_has_pairs(effect, ('set_country_flag', f'WFL_ref_{state}_requested'))
                events = [node for node in walk(children(effect)) if node.key == 'country_event']
                self.assertTrue(any(field(node, 'id') == consent and field(node, 'days') == '1' for node in events))
                watchdog = 'wfl_referendum.6' if state == '51' else 'wfl_referendum.16'
                self.assertTrue(any(field(node, 'id') == watchdog and field(node, 'days') == '120' for node in events))

    def test_campaign_rechecks_the_original_host(self):
        for state in ('51', '57'):
            with self.subTest(state=state):
                campaign = self.decisions['WFL_schuetzenkampagne_' + state]
                effect = blocks(campaign, 'complete_effect')[0]
                owner = blocks(blocks(effect, state)[0], 'owner')[0]
                self.assert_has_pairs(owner, ('set_country_flag', f'WFL_ref_{state}_campaign_host'))
                cancellation = blocks(blocks(campaign, 'cancel_trigger')[0], 'NOT')[0]
                owner = blocks(blocks(cancellation, state)[0], 'owner')[0]
                self.assert_has_pairs(owner, ('has_country_flag', f'WFL_ref_{state}_campaign_host'))
                timed = blocks(blocks(campaign, 'remove_effect')[0], 'if')[0]
                success = blocks(timed, 'if')[0]
                limit = blocks(success, 'limit')[0]
                owner = blocks(blocks(limit, state)[0], 'owner')[0]
                self.assert_has_pairs(owner, ('has_country_flag', f'WFL_ref_{state}_campaign_host'))

    def test_cancelled_campaign_cannot_grant_completion(self):
        for state in ('51', '57'):
            with self.subTest(state=state):
                campaign = self.decisions['WFL_schuetzenkampagne_' + state]
                cancelled = blocks(campaign, 'cancel_effect')[0]
                self.assert_has_pairs(cancelled, ('clr_country_flag', f'WFL_ref_{state}_campaign_active'))
                self.assertFalse(any(node.key == 'set_country_flag' and node.value == f'WFL_ref_{state}_campaign_done'
                                     for node in walk(children(cancelled))))
                removal = blocks(campaign, 'remove_effect')[0]
                active_branch = blocks(removal, 'if')[0]
                self.assert_has_pairs(blocks(active_branch, 'limit')[0],
                                      ('has_country_flag', f'WFL_ref_{state}_campaign_active'))
                completion = [node for node in walk(children(removal))
                              if node.key == 'set_country_flag' and node.value == f'WFL_ref_{state}_campaign_done']
                guarded_completion = [node for node in walk(children(active_branch))
                                      if node.key == 'set_country_flag' and node.value == f'WFL_ref_{state}_campaign_done']
                self.assertEqual(len(completion), 1)
                self.assertEqual(completion, guarded_completion)
                for terminal in (cancelled, removal):
                    cleanup = blocks(terminal, 'every_country')
                    self.assertEqual(len(cleanup), 1)
                    self.assert_has_pairs(blocks(cleanup[0], 'limit')[0],
                                          ('has_country_flag', f'WFL_ref_{state}_campaign_host'))
                    self.assert_has_pairs(cleanup[0], ('clr_country_flag', f'WFL_ref_{state}_campaign_host'))

    def test_ballot_is_delayed_after_consent(self):
        for consent, ballot in (('wfl_referendum.1', 'wfl_referendum.2'),
                                ('wfl_referendum.11', 'wfl_referendum.12'),
                                ('wfl_referendum.21', 'wfl_referendum.22'),
                                ('wfl_referendum.31', 'wfl_referendum.32')):
            scheduled = [node for node in walk(children(self.option(consent, 'a')))
                         if node.key == 'country_event' and field(node, 'id') == ballot]
            self.assertEqual(len(scheduled), 1)
            self.assertEqual(field(scheduled[0], 'days'), '30')


if __name__ == '__main__':
    unittest.main()
