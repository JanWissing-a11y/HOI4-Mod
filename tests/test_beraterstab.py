"""Bounded execution of the staff scripts, including daily counters and swaps.

This checks the mod's state transitions; it is not an engine/UI simulation.
Unlike the project validator's structural AST, this parser keeps comparison
operators because counter thresholds are material to these behaviour tests.
"""
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import unittest

from tools.validate_mod import TOKEN, children, field

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = ('dante_grossy', 'neal_foerster', 'max_heinsch', 'max_mueller', 'till_hoehne')


@dataclass
class Statement:
    key: str
    value: object = None
    op: str = '='


def parse_script(text):
    tokens = []
    pos = 0
    while pos < len(text):
        match = TOKEN.match(text, pos)
        if match is None:
            raise AssertionError('Unsupported script token')
        kind, value = match.lastgroup, match.group()
        if kind not in ('space', 'comment'):
            tokens.append((kind, value[1:-1] if kind == 'string' else value))
        pos = match.end()
    index = 0

    def group(nested=False):
        nonlocal index
        nodes = []
        while index < len(tokens):
            kind, key = tokens[index]
            index += 1
            if kind == 'brace' and key == '}':
                if not nested:
                    raise AssertionError('Unexpected closing brace')
                return nodes
            if kind not in ('word', 'string'):
                raise AssertionError('Expected statement')
            value, op = None, '='
            if index < len(tokens) and tokens[index][0] == 'operator':
                op = tokens[index][1]
                index += 1
                value_kind, value = tokens[index]
                index += 1
                if value_kind == 'brace' and value == '{':
                    value = group(True)
                elif value_kind not in ('word', 'string'):
                    raise AssertionError('Expected statement value')
            nodes.append(Statement(key, value, op))
        if nested:
            raise AssertionError('Unclosed script block')
        return nodes

    return group()


def read(relative):
    return parse_script((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return next(part for part in children(node) if part.key == key)


class StaffWorld:
    def __init__(self):
        self.effects_by_name = {n.key: children(n) for n in read('common/scripted_effects/WFL_beraterstab_effects.txt')}
        self.triggers = {n.key: children(n) for n in read('common/scripted_triggers/WFL_beraterstab_triggers.txt')}
        tree = read('common/national_focus/WFL_focus.txt')[0]
        self.focuses = {field(n, 'id'): n for n in children(tree) if n.key == 'focus'}
        self.events = {field(n, 'id'): n for n in read('events/WFL_beraterstab.txt') if n.key == 'country_event'}
        self.variables = {}
        self.flags = set()
        self.ideas = set()
        self.completed = set()
        self.shining = set()
        self.completion_calls = []
        self.scheduled = []
        self.government = 'neutrality'
        self.leader = 'WFL_schuetzenkoenig'
        self.tag = 'WFL'
        self.capitulated = False
        self.exists = True
        self.normal_focus = 'WFL_werkbank_am_niederrhein'
        self.random_wait = 75
        self.pp = Decimal(0)
        self.stability = Decimal(0)
        self.war_support = Decimal(0)
        self.army_experience = Decimal(0)

    def number(self, value):
        try:
            return Decimal(str(value))
        except Exception:
            return self.variables.get(value.removeprefix('var:'), Decimal(0))

    def variable_pair(self, node):
        parts = children(node)
        if field(node, 'var'):
            return field(node, 'var'), field(node, 'value')
        first = next(n for n in parts if n.key not in ('tooltip', 'compare', 'type'))
        return first.key, first.value

    def matches(self, nodes):
        for node in nodes:
            key, value = node.key, node.value
            if key in self.triggers:
                result = self.matches(self.triggers[key]) == (value == 'yes')
            elif key in ('AND', 'hidden_trigger', 'custom_trigger_tooltip'):
                result = self.matches([n for n in children(node) if n.key != 'tooltip'])
            elif key == 'OR':
                result = any(self.matches([n]) for n in children(node))
            elif key == 'NOT':
                result = not self.matches(children(node))
            elif key == 'always':
                result = value == 'yes'
            elif key == 'tag':
                result = self.tag == value
            elif key == 'exists':
                result = self.exists == (value == 'yes')
            elif key == 'has_capitulated':
                result = self.capitulated == (value == 'yes')
            elif key == 'has_government':
                result = self.government == value
            elif key == 'has_country_leader':
                result = self.leader == field(node, 'character')
            elif key == 'has_country_flag':
                result = value in self.flags
            elif key == 'has_idea':
                result = value in self.ideas
            elif key == 'has_completed_focus':
                result = value in self.completed
            elif key == 'has_shine_effect_on_focus':
                result = value in self.shining
            elif key == 'check_variable':
                name, target = self.variable_pair(node)
                first = next(n for n in children(node) if n.key == name or n.key == 'value')
                compare = field(node, 'compare') or first.op
                left, right = self.variables.get(name, Decimal(0)), self.number(target)
                operators = {'=': left == right, 'equals': left == right,
                             'not_equals': left != right, '!=': left != right,
                             '>': left > right, 'greater_than': left > right,
                             '<': left < right, 'less_than': left < right,
                             '>=': left >= right, 'greater_than_or_equals': left >= right,
                             '<=': left <= right, 'less_than_or_equals': left <= right}
                if compare not in operators:
                    raise AssertionError('Unknown comparison: ' + compare)
                result = operators[compare]
            elif key == 'if':
                condition = self.matches(children(block(node, 'limit')))
                result = not condition or self.matches([n for n in children(node) if n.key != 'limit'])
            else:
                raise AssertionError('Unsupported staff condition: ' + key)
            if not result:
                return False
        return True

    def run(self, name):
        self.effects(self.effects_by_name[name])

    def effects(self, nodes):
        branch_taken = None
        for node in nodes:
            key, value = node.key, node.value
            if key == 'if':
                branch_taken = self.matches(children(block(node, 'limit')))
                if branch_taken:
                    self.effects([n for n in children(node) if n.key != 'limit'])
            elif key == 'else_if':
                if branch_taken is None:
                    raise AssertionError('else_if without if')
                if not branch_taken and self.matches(children(block(node, 'limit'))):
                    self.effects([n for n in children(node) if n.key != 'limit'])
                    branch_taken = True
            elif key == 'else':
                if branch_taken is None:
                    raise AssertionError('else without if')
                if not branch_taken:
                    self.effects(children(node))
                branch_taken = None
            elif key in self.effects_by_name:
                self.run(key)
            elif key in ('hidden_effect', 'effect'):
                self.effects(children(node))
            elif key in ('custom_effect_tooltip', 'show_ideas_tooltip', 'log'):
                pass
            elif key == 'set_country_flag':
                if not isinstance(value, str):
                    raise AssertionError('Timed flags are not part of the counter fixture')
                self.flags.add(value)
            elif key == 'clr_country_flag':
                self.flags.discard(value)
            elif key in ('set_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable', 'divide_variable'):
                name, amount = self.variable_pair(node)
                amount = self.number(amount)
                old = self.variables.get(name, Decimal(0))
                self.variables[name] = {'set_variable': lambda: amount,
                                       'add_to_variable': lambda: old + amount,
                                       'subtract_from_variable': lambda: old - amount,
                                       'multiply_variable': lambda: old * amount,
                                       'divide_variable': lambda: old / amount}[key]()
            elif key == 'clamp_variable':
                name = field(node, 'var')
                self.variables[name] = max(self.number(field(node, 'min')), min(self.number(field(node, 'max')), self.number(name)))
            elif key == 'set_variable_to_random':
                minimum, maximum = self.number(field(node, 'min')), self.number(field(node, 'max'))
                if not minimum <= self.random_wait < maximum:
                    raise AssertionError('Fixture random value outside the scripted half-open range')
                self.variables[field(node, 'var')] = Decimal(self.random_wait)
            elif key == 'clear_variable':
                self.variables.pop(value, None)
            elif key in ('add_ideas', 'remove_ideas'):
                ideas = [value] if isinstance(value, str) else [n.key for n in children(node)]
                for idea in ideas:
                    if key == 'add_ideas':
                        self.ideas.add(idea)
                    else:
                        self.ideas.discard(idea)
            elif key == 'country_event':
                self.scheduled.append((value, 0) if isinstance(value, str) else (field(node, 'id'), field(node, 'days')))
            elif key == 'complete_national_focus':
                focus_id = value if isinstance(value, str) else field(node, 'focus')
                self.completion_calls.append(focus_id)
                if focus_id not in self.completed:
                    self.completed.add(focus_id)
                    self.effects(children(block(self.focuses[focus_id], 'completion_reward')))
            elif key == 'uncomplete_national_focus':
                focus_id = value if isinstance(value, str) else field(node, 'focus')
                self.completed.discard(focus_id)
            elif key in ('activate_shine_on_focus', 'deactivate_shine_on_focus'):
                focus_id = value if isinstance(value, str) else field(node, 'focus')
                if key == 'activate_shine_on_focus':
                    self.shining.add(focus_id)
                else:
                    self.shining.discard(focus_id)
            elif key in ('add_political_power', 'add_stability', 'add_war_support', 'army_experience'):
                attr = {'add_political_power': 'pp', 'add_stability': 'stability',
                        'add_war_support': 'war_support', 'army_experience': 'army_experience'}[key]
                setattr(self, attr, getattr(self, attr) + self.number(value))
            else:
                raise AssertionError('Unsupported staff effect: ' + key)

    def tick(self, days=1):
        for _ in range(days):
            self.run('WFL_staff_daily_tick')

    def seats(self):
        return tuple(int(self.variables.get(f'WFL_staff_slot_{n}', 0)) for n in (1, 2, 3))

    def choose_replacement(self, suffix):
        event = self.events['wfl_staff.2']
        option = next(n for n in children(event) if n.key == 'option'
                      and field(n, 'name') == f'wfl_staff.2.{suffix}')
        gates = [n for n in children(option) if n.key == 'trigger']
        if gates and not self.matches(children(gates[0])):
            return False
        self.effects([n for n in children(option) if n.key not in ('name', 'trigger', 'ai_chance')])
        return True

    def snapshot(self):
        return (self.seats(), frozenset(self.ideas), frozenset(self.flags), frozenset(self.completed))


class StaffBehaviourTests(unittest.TestCase):
    def world(self):
        world = StaffWorld()
        world.completed.add('WFL_beraterstab_gruenden')
        world.effects(children(block(world.focuses['WFL_beraterstab_gruenden'], 'completion_reward')))
        world.scheduled.clear()
        return world

    def nominate(self, world, member):
        focus = world.focuses['WFL_staff_appoint_' + member]
        if world.matches(children(block(focus, 'available'))):
            world.completed.add(field(focus, 'id'))
            world.effects(children(block(focus, 'completion_reward')))

    def fill(self, world):
        for member in MEMBERS[:3]:
            world.variables['WFL_staff_cooldown'] = Decimal(0)
            self.nominate(world, member)
        self.assertEqual(world.seats(), (1, 2, 3))

    def test_initialization_is_safe_for_old_saves_and_cannot_reset_an_active_staff(self):
        world = self.world()
        self.assertEqual(world.seats(), (0, 0, 0))
        self.nominate(world, MEMBERS[0])
        world.tick(20)
        before = (dict(world.variables), world.snapshot())
        world.run('WFL_staff_initialize')
        self.assertEqual((world.variables, world.snapshot()), before)

    def test_three_special_seats_are_separate_from_ordinary_political_advisors(self):
        world = self.world()
        world.ideas.add('existing_ordinary_advisor')
        self.fill(world)
        self.assertEqual(sum(f'WFL_staff_{member}_active' in world.flags for member in MEMBERS), 3)
        self.assertIn('existing_ordinary_advisor', world.ideas)
        self.assertEqual(len(world.ideas), 4)

    def test_real_cooldown_blocks_new_appointments_for_175_daily_ticks(self):
        world = self.world()
        self.nominate(world, MEMBERS[0])
        self.assertEqual(world.variables['WFL_staff_cooldown'], 175)
        before = world.snapshot()
        self.nominate(world, MEMBERS[1])
        self.assertEqual(world.snapshot(), before)
        world.tick(174)
        self.assertEqual(world.variables['WFL_staff_cooldown'], 1)
        self.assertFalse(world.matches([Statement('WFL_staff_can_appoint', 'yes')]))
        world.tick()
        self.assertEqual(world.variables['WFL_staff_cooldown'], 0)
        self.assertTrue(world.matches([Statement('WFL_staff_can_appoint', 'yes')]))
        self.nominate(world, MEMBERS[1])
        self.assertEqual(world.seats(), (1, 2, 0))

    def test_full_staff_requires_an_explicit_replacement_and_cancel_keeps_incumbents(self):
        world = self.world()
        self.fill(world)
        world.variables['WFL_staff_cooldown'] = Decimal(0)
        before = world.snapshot()
        self.nominate(world, MEMBERS[3])
        self.assertEqual(world.seats(), before[0])
        self.assertEqual(world.ideas, set(before[1]))
        self.assertIn('WFL_staff_replacement_pending', world.flags)
        self.assertEqual(world.variables['WFL_staff_nominee'], 4)
        self.assertEqual(len(world.scheduled), 1)
        self.assertFalse(world.matches([Statement('WFL_staff_can_appoint', 'yes')]))
        self.assertTrue(world.choose_replacement('d'))
        self.assertEqual(world.snapshot(), before)
        self.assertEqual(world.variables['WFL_staff_nominee'], 0)
        world.run('WFL_staff_cancel_nomination')
        self.assertEqual(world.snapshot(), before)

    def test_replacement_removes_only_the_selected_members_bonus_and_stops_his_work(self):
        for slot in (1, 2, 3):
            with self.subTest(slot=slot):
                world = self.world()
                self.fill(world)
                world.tick(80)
                old_member = MEMBERS[slot - 1]
                old_ideas = {idea for idea in world.ideas if old_member in idea}
                other_ideas = world.ideas - old_ideas
                world.variables['WFL_staff_cooldown'] = Decimal(0)
                self.nominate(world, MEMBERS[3])
                self.assertTrue(world.choose_replacement('abc'[slot - 1]))
                expected = [1, 2, 3]
                expected[slot - 1] = 4
                self.assertEqual(world.seats(), tuple(expected))
                self.assertNotIn(f'WFL_staff_{old_member}_active', world.flags)
                self.assertIn(f'WFL_staff_{MEMBERS[3]}_active', world.flags)
                self.assertFalse(old_ideas & world.ideas)
                self.assertTrue(other_ideas <= world.ideas)
                self.assertEqual(world.variables[f'WFL_staff_{old_member}_phase'], 0)
                self.assertEqual(world.variables[f'WFL_staff_{old_member}_days'], 0)
                self.assertFalse(any(old_member in focus for focus in world.shining))
                self.assertEqual(world.variables['WFL_staff_cooldown'], 175)
                after = world.snapshot()
                world.run(f'WFL_staff_replace_slot_{slot}')
                self.assertEqual(world.snapshot(), after)

    def test_all_five_members_complete_three_autonomous_stages_with_exact_work_durations(self):
        for member in MEMBERS:
            with self.subTest(member=member):
                world = self.world()
                self.nominate(world, member)
                for stage, duration in ((1, 140), (2, 140), (3, 280)):
                    phase = f'WFL_staff_{member}_phase'
                    days = f'WFL_staff_{member}_days'
                    rank = f'WFL_staff_{member}_rank'
                    focus_id = f'WFL_staff_{member}_{stage}'
                    self.assertEqual(world.variables[phase], 1)
                    wait = int(world.variables[days])
                    self.assertGreaterEqual(wait, 75)
                    self.assertLessEqual(wait, 120)
                    world.tick(wait)
                    self.assertEqual(world.variables[phase], 2)
                    self.assertEqual(world.variables[days], duration)
                    self.assertIn(focus_id, world.shining)
                    self.assertNotIn(focus_id, world.completed)
                    world.tick(duration - 1)
                    self.assertEqual(world.variables[rank], stage - 1)
                    self.assertNotIn(focus_id, world.completed)
                    world.tick()
                    self.assertEqual(world.variables[rank], stage)
                    self.assertIn(focus_id, world.completed)
                    self.assertNotIn(focus_id, world.shining)
                    self.assertEqual(world.completion_calls.count(focus_id), 1)
                    self.assertEqual(len(world.ideas), 1, 'Base and upgraded bonus must never stack')
                self.assertEqual(world.variables[phase], 0)
                self.assertEqual(world.variables[days], 0)
                completed_calls = list(world.completion_calls)
                world.tick(600)
                self.assertEqual(world.completion_calls, completed_calls)
                self.assertEqual(world.normal_focus, 'WFL_werkbank_am_niederrhein')

    def test_three_members_work_in_parallel_without_occupying_the_normal_focus(self):
        world = self.world()
        self.fill(world)
        waits = {member: int(world.variables[f'WFL_staff_{member}_days']) for member in MEMBERS[:3]}
        world.tick(max(waits.values()) + 140)
        for member in MEMBERS[:3]:
            self.assertGreaterEqual(world.variables[f'WFL_staff_{member}_rank'], 1)
            self.assertIn(f'WFL_staff_{member}_1', world.completed)
        self.assertEqual(world.normal_focus, 'WFL_werkbank_am_niederrhein')

    def test_reappointment_preserves_rank_but_discards_old_partial_work(self):
        world = self.world()
        member = MEMBERS[0]
        self.nominate(world, member)
        wait = int(world.variables[f'WFL_staff_{member}_days'])
        world.tick(wait + 140)
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 1)
        first_focus = f'WFL_staff_{member}_1'
        world.tick(int(world.variables[f'WFL_staff_{member}_days']) + 100)
        world.run(f'WFL_staff_remove_{member}')
        world.variables['WFL_staff_slot_1'] = Decimal(0)
        self.assertEqual(world.variables[f'WFL_staff_{member}_days'], 0)
        self.assertIn(first_focus, world.completed)
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 1)
        world.variables['WFL_staff_cooldown'] = Decimal(0)
        self.nominate(world, member)
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 1)
        self.assertEqual(world.variables[f'WFL_staff_{member}_phase'], 1)
        new_wait = int(world.variables[f'WFL_staff_{member}_days'])
        self.assertGreaterEqual(new_wait, 75)
        world.tick(new_wait + 139)
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 1)
        world.tick()
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 2)
        self.assertEqual(world.completion_calls.count(first_focus), 1)

    def test_changed_government_or_leader_clears_all_live_bonuses_and_stops_counters(self):
        for change in ('government', 'leader', 'capitulated'):
            with self.subTest(change=change):
                world = self.world()
                self.fill(world)
                world.ideas.add('existing_ordinary_advisor')
                world.tick(250)
                completed = {focus for focus in world.completed if not focus.startswith('WFL_staff_appoint_')}
                ranks = {m: world.variables[f'WFL_staff_{m}_rank'] for m in MEMBERS}
                setattr(world, change, {'government': 'democratic', 'leader': 'another_leader', 'capitulated': True}[change])
                world.tick()
                self.assertEqual(world.seats(), (0, 0, 0))
                self.assertEqual(world.ideas, {'existing_ordinary_advisor'})
                self.assertEqual(world.completed, completed)
                self.assertEqual(world.shining, set())
                for member in MEMBERS:
                    self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], ranks[member])
                    self.assertEqual(world.variables[f'WFL_staff_{member}_phase'], 0)
                    self.assertEqual(world.variables[f'WFL_staff_{member}_days'], 0)
                calls = list(world.completion_calls)
                world.tick(800)
                self.assertEqual(world.completion_calls, calls)

    def test_pending_old_dialog_cannot_replace_a_member_after_governance_changes(self):
        world = self.world()
        self.fill(world)
        world.variables['WFL_staff_cooldown'] = Decimal(0)
        self.nominate(world, MEMBERS[3])
        world.government = 'democratic'
        world.tick()
        world.run('WFL_staff_replace_slot_1')
        self.assertEqual(world.seats(), (0, 0, 0))
        self.assertEqual(world.ideas, set())
        world.government = 'neutrality'
        world.run('WFL_staff_replace_slot_1')
        self.assertEqual(world.seats(), (0, 0, 0), 'A stale dialog must stay invalid after Jan returns')
        self.assertFalse(world.matches([Statement('WFL_staff_can_appoint', 'yes')]))
        world.run('WFL_staff_cancel_nomination')
        world.variables['WFL_staff_cooldown'] = Decimal(0)
        self.assertTrue(world.matches([Statement('WFL_staff_can_appoint', 'yes')]))

    def test_auto_focuses_are_manually_blocked_and_appointment_length_matches_vanilla(self):
        world = self.world()
        for member in MEMBERS:
            appointment = world.focuses[f'WFL_staff_appoint_{member}']
            self.assertEqual(field(appointment, 'cost'), '2')
            for stage, cost in ((1, '20'), (2, '20'), (3, '40')):
                focus = world.focuses[f'WFL_staff_{member}_{stage}']
                self.assertEqual(field(focus, 'cost'), cost)
                self.assertFalse(world.matches(children(block(focus, 'available'))))

    def test_inactive_members_cannot_be_completed_by_a_stale_direct_finish_call(self):
        world = self.world()
        self.nominate(world, MEMBERS[0])
        world.run(f'WFL_staff_remove_{MEMBERS[0]}')
        for stage in (1, 2, 3):
            world.run(f'WFL_staff_finish_{MEMBERS[0]}_{stage}')
        self.assertEqual(world.variables[f'WFL_staff_{MEMBERS[0]}_rank'], 0)
        self.assertEqual(world.ideas, set())
        self.assertEqual(world.completion_calls, [])

    def test_premature_or_repeated_finish_calls_never_skip_work_or_stack_rewards(self):
        world = self.world()
        member = MEMBERS[0]
        self.nominate(world, member)
        initial = (dict(world.variables), world.snapshot())
        world.run(f'WFL_staff_finish_{member}_1')
        self.assertEqual((world.variables, world.snapshot()), initial)
        world.tick(int(world.variables[f'WFL_staff_{member}_days']) + 139)
        working = (dict(world.variables), world.snapshot())
        world.run(f'WFL_staff_finish_{member}_1')
        self.assertEqual((world.variables, world.snapshot()), working)
        world.tick()
        finished = (dict(world.variables), world.snapshot())
        world.run(f'WFL_staff_finish_{member}_1')
        self.assertEqual((world.variables, world.snapshot()), finished)

    def test_longest_preparation_and_fully_developed_reappointment_do_not_restart_old_stages(self):
        world = self.world()
        world.random_wait = 120
        member = MEMBERS[4]
        self.nominate(world, member)
        for duration in (140, 140, 280):
            self.assertEqual(world.variables[f'WFL_staff_{member}_days'], 120)
            world.tick(120 + duration)
        self.assertEqual(world.variables[f'WFL_staff_{member}_rank'], 3)
        world.run(f'WFL_staff_remove_{member}')
        world.variables['WFL_staff_cooldown'] = Decimal(0)
        self.nominate(world, member)
        self.assertEqual(world.ideas, {f'WFL_staff_{member}_3_idea'})
        self.assertEqual(world.variables[f'WFL_staff_{member}_phase'], 0)
        self.assertEqual(world.variables[f'WFL_staff_{member}_progress'], 1)
        calls = list(world.completion_calls)
        world.tick(1000)
        self.assertEqual(world.completion_calls, calls)

    def test_fixture_rejects_unknown_conditions_and_effects(self):
        world = self.world()
        with self.assertRaises(AssertionError):
            world.matches([Statement('unknown_staff_trigger', 'yes')])
        with self.assertRaises(AssertionError):
            world.effects([Statement('unknown_staff_effect', 'yes')])


if __name__ == '__main__':
    unittest.main()
