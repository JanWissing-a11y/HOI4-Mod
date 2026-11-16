"""Execute the new construction and economic-law rewards in bounded fixtures.

Only this subset is modelled; these tests do not execute the game engine.
"""
from pathlib import Path
import unittest

from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]


def child(node, key):
    return next(part for part in children(node) if part.key == key)


class EconomyWorld:
    def __init__(self):
        self.owner = self.controller = 'WFL'
        self.full_control = True
        self.capitulated = self.dmz = False
        self.factories = 1
        self.used_slots = 3
        self.slots = 4
        self.extra_slots = 0
        self.pp = 0
        self.law = 'civilian_economy'
        self.law_changes = []

    def conditions(self, nodes):
        for node in nodes:
            key, value = node.key, node.value
            if key == '1082':
                result = self.conditions(children(node))
            elif key == 'NOT':
                result = not self.conditions(children(node))
            elif key == 'is_owned_by':
                result = self.owner == 'WFL'
            elif key == 'is_fully_controlled_by':
                result = self.controller == 'WFL' and self.full_control
            elif key == 'has_capitulated':
                result = self.capitulated == (value == 'yes')
            elif key == 'is_demilitarized_zone':
                result = self.dmz == (value == 'yes')
            elif key == 'arms_factory':
                # The project parser stores comparison operands; assert the
                # actual operator separately where this fixture uses '<'.
                result = self.factories < int(value)
            elif key == 'free_building_slots':
                assert field(node, 'building') == 'arms_factory'
                result = (self.slots - self.used_slots > int(field(node, 'size'))
                          and 20 - self.factories > int(field(node, 'size')))
            elif key == 'has_idea':
                result = self.law == value
            else:
                raise AssertionError(f'Unmodelled condition: {key}')
            if not result:
                return False
        return True

    def effects(self, nodes):
        preceding_if = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                preceding_if = self.conditions(children(child(node, 'limit')))
                if preceding_if:
                    self.effects([part for part in children(node) if part.key != 'limit'])
            elif key == 'else':
                if preceding_if is False:
                    self.effects(children(node))
            elif key == '1082':
                self.effects(children(node))
            elif key == 'add_extra_state_shared_building_slots':
                self.extra_slots += int(value)
                self.slots = min(25, self.slots + int(value))
            elif key == 'add_building_construction':
                assert self.owner == self.controller == 'WFL' and self.full_control
                assert not self.dmz and field(node, 'instant_build') == 'yes'
                assert field(node, 'type') == 'arms_factory'
                amount = int(field(node, 'level'))
                assert amount <= self.slots - self.used_slots
                assert self.factories + amount <= 20
                self.factories += amount
                self.used_slots += amount
            elif key == 'add_political_power':
                self.pp += int(value)
            elif key == 'add_ideas':
                assert value == 'war_economy'
                self.law = value
                self.law_changes.append(value)
            else:
                raise AssertionError(f'Unmodelled effect: {key}')


class EconomyExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig')
        cls.source = source
        cls.focuses = {field(n, 'id'): n for n in children(parse(source)[0]) if n.key == 'focus'}

    def reward(self, focus):
        return children(child(self.focuses[focus], 'completion_reward'))

    def test_conversion_adds_three_factories_with_room(self):
        world = EconomyWorld()
        world.effects(self.reward('WFL_flachglas_ruestungsproduktion'))
        self.assertEqual((world.factories, world.extra_slots, world.pp), (4, 3, 0))

    def test_conversion_rechecks_owner_control_capitulation_and_dmz(self):
        cases = (('owner', 'GER'), ('controller', 'GER'), ('full_control', False),
                 ('capitulated', True), ('dmz', True), ('factories', 18))
        for attribute, value in cases:
            with self.subTest(attribute=attribute):
                world = EconomyWorld()
                setattr(world, attribute, value)
                before = world.factories
                world.effects(self.reward('WFL_flachglas_ruestungsproduktion'))
                self.assertEqual((world.factories, world.extra_slots, world.pp), (before, 0, 150))

    def test_conversion_at_shared_slot_cap_never_overbuilds(self):
        world = EconomyWorld()
        world.slots = world.used_slots = 24
        world.effects(self.reward('WFL_flachglas_ruestungsproduktion'))
        self.assertEqual((world.factories, world.slots, world.pp), (1, 25, 150))

    def test_war_economy_is_free_and_never_downgrades_total_mobilisation(self):
        for law in ('civilian_economy', 'low_economic_mobilisation', 'partial_economic_mobilisation',
                    'war_economy', 'tot_economic_mobilisation'):
            with self.subTest(law=law):
                world = EconomyWorld()
                world.law = law
                world.effects(self.reward('WFL_schuetzen_kriegswirtschaft'))
                if law in ('war_economy', 'tot_economic_mobilisation'):
                    self.assertEqual((world.law, world.law_changes, world.pp), (law, [], 100))
                else:
                    self.assertEqual((world.law, world.law_changes, world.pp),
                                     ('war_economy', ['war_economy'], 0))

    def test_rhine_trade_and_morale_have_exact_permanent_country_modifiers(self):
        ideas = {}
        for relative in ('common/ideas/WFL_ideas.txt', 'common/ideas/WFL_economy_expansion_ideas.txt'):
            group = parse((ROOT / relative).read_text(encoding='utf-8-sig'))[0]
            ideas.update({n.key: n for n in children(child(group, 'country'))})
        expected = {'WFL_rheinhandel': {'production_speed_industrial_complex_factor': '0.15',
                                       'production_speed_arms_factory_factor': '0.15'},
                    'WFL_alkoholfreies_bier_verbot_idee': {'army_morale_factor': '0.10'}}
        for ident, modifiers in expected.items():
            self.assertEqual({n.key: n.value for n in children(child(ideas[ident], 'modifier'))}, modifiers)
            self.assertEqual(field(child(ideas[ident], 'allowed'), 'tag'), 'WFL')
            self.assertEqual(field(ideas[ident], 'removal_cost'), '-1')
        self.assertIn('arms_factory < 18', self.source)

    def test_college_keeps_original_unlock_id_and_adds_research_support(self):
        reward = self.reward('WFL_technikschule')
        self.assertEqual(next(n.value for n in reward if n.key == 'add_ideas'), 'WFL_berufskolleg_idee')
        bonus = next(n for n in reward if n.key == 'add_tech_bonus')
        self.assertEqual((field(bonus, 'uses'), field(bonus, 'bonus'), field(bonus, 'category')),
                         ('2', '1.0', 'industry'))
        self.assertEqual(sum(int(n.value) for n in walk(reward) if n.key == 'add_research_slot'), 1)

    def test_blockade_positive_economy_does_not_depend_on_foreign_reply(self):
        reward = self.reward('WFL_rheinblockade')
        self.assertEqual(next(n.value for n in reward if n.key == 'add_ideas'), 'WFL_rheinblockade_idee')
        self.assertFalse(any(n.key in ('if', 'random', 'random_list') for n in reward))
        self.assertEqual(field(next(n for n in reward if n.key == 'country_event'), 'id'), 'wfl_beer.1')


if __name__ == '__main__':
    unittest.main()
