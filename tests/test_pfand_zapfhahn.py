"""Bounded execution of the deposit economy and tap-crisis event rewards."""
from pathlib import Path
import unittest

from tests.test_beer_diplomacy import DiplomacyWorld, block
from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]


class TapWorld(DiplomacyWorld):
    def __init__(self, events):
        super().__init__(events)
        self.ideas = {tag: [] for tag in self.countries}

    def effects(self, nodes, current, root):
        rest = []
        for node in nodes:
            if node.key == 'add_ideas':
                self.ideas[current.tag].append(node.value)
            else:
                rest.append(node)
        super().effects(rest, current, root)


class DepositAndTapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = {field(n, 'id'): n for n in parse((ROOT / 'events/WFL_zapfhahnkrise.txt').read_text())
                      if n.key == 'country_event'}
        cls.focuses = {field(n, 'id'): n for group in parse((ROOT / 'common/national_focus/WFL_focus.txt').read_text())
                       for n in children(group) if n.key == 'focus'}
        cls.ideas = {n.key: n for group in parse((ROOT / 'common/ideas/WFL_pfand_ideas.txt').read_text())
                     for category in children(group) for n in children(category)}

    def begin(self, world):
        world.effects(children(block(self.focuses['WFL_zapfhahnkrise'], 'completion_reward')),
                      world.countries['WFL'], world.countries['WFL'])

    def test_focuses_have_independent_economic_and_diplomatic_prerequisites(self):
        for own, parent in (('WFL_reichspfandministerium', 'WFL_rheinhandel_beleben'),
                            ('WFL_zapfhahnkrise', 'WFL_anglo_bier_diplomatie')):
            self.assertEqual(field(block(self.focuses[own], 'prerequisite'), 'focus'), parent)
            self.assertEqual(field(self.focuses[own], 'cost'), '5')
        spirit = self.ideas['WFL_reichspfandministerium_idee']
        modifiers = {n.key: n.value for n in children(block(spirit, 'modifier'))}
        self.assertEqual(modifiers, {'local_resources_factor': '0.15',
                                    'production_lack_of_resource_penalty_factor': '-0.10',
                                    'industrial_capacity_factory': '0.05'})
        self.assertEqual(field(spirit, 'removal_cost'), '-1')
        self.assertEqual(field(block(self.focuses['WFL_reichspfandministerium'], 'completion_reward'), 'add_ideas'),
                         'WFL_reichspfandministerium_idee')

    def test_both_choices_grant_distinct_rewards_once_and_never_war_or_territory(self):
        for choice, expected in ((0, 'WFL_kuehlkettenkompromiss'), (1, 'WFL_trinkduell_der_freundschaft')):
            with self.subTest(choice=choice):
                world = TapWorld(self.events)
                self.begin(world)
                self.assertTrue(world.event('wfl_zapfhahn.1', 'WFL', choice))
                world.option('wfl_zapfhahn.1', 'WFL', 1-choice)
                self.assertTrue(world.event('wfl_zapfhahn.2', 'ENG'))
                world.option('wfl_zapfhahn.2', 'ENG')
                self.assertFalse(world.event('wfl_zapfhahn.4', 'WFL'))
                self.begin(world)
                self.assertEqual(world.ideas['WFL'], [expected])
                self.assertTrue(world.countries['WFL'].opinions)
                self.assertEqual(world.countries['WFL'].pp, 0)
                route = 'trade' if choice == 0 else 'duel'
                for number, recipient in ((2, 'ENG'), (3, 'WFL')):
                    descriptions = [n for n in children(self.events[f'wfl_zapfhahn.{number}']) if n.key == 'desc']
                    matching = [field(n, 'text') for n in descriptions if world.matches(
                        children(block(n, 'trigger')), world.countries[recipient], world.countries[recipient])]
                    self.assertEqual(matching, [f'wfl_zapfhahn.{number}.{route}'])
        forbidden = {'declare_war_on', 'create_wargoal', 'transfer_state', 'annex_country', 'add_core_of'}
        self.assertFalse(forbidden & {n.key for e in self.events.values() for n in walk(children(e))})
        visible = [e for e in self.events.values() if field(e, 'hidden') != 'yes']
        self.assertEqual(len(visible), 3)

    def test_missing_partner_war_late_reply_and_timeout_pay_fallback_exactly_once(self):
        for stage in ('focus_missing', 'choice_missing', 'reply_missing', 'reply_war', 'timeout'):
            with self.subTest(stage=stage):
                world = TapWorld(self.events)
                if stage == 'focus_missing': world.countries['ENG'].exists = False
                self.begin(world)
                if stage != 'focus_missing':
                    if stage == 'choice_missing': world.countries['ENG'].exists = False
                    world.event('wfl_zapfhahn.1', 'WFL')
                    if stage == 'reply_missing': world.countries['ENG'].exists = False
                    if stage == 'reply_war': world.countries['ENG'].wars.add('WFL')
                    if stage == 'timeout': world.event('wfl_zapfhahn.4', 'WFL')
                    else: world.event('wfl_zapfhahn.2', 'ENG')
                world.option('wfl_zapfhahn.2', 'ENG')
                world.option('wfl_zapfhahn.1', 'WFL', 1)
                world.event('wfl_zapfhahn.4', 'WFL')
                self.begin(world)
                self.assertEqual(world.countries['WFL'].pp, 50)
                self.assertEqual(world.ideas['WFL'], [])


if __name__ == '__main__':
    unittest.main()
