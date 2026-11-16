"""Execute assembly scripts against a small deterministic clock and RNG fixture.

The fixture retains actual comparison operators and forces every material RNG
branch. It does not emulate the Clausewitz renderer or prove engine semantics.
"""
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
import json
import struct
import unittest

from tests.test_beraterstab import block, parse_script
from tools.validate_mod import children, field


ROOT = Path(__file__).resolve().parents[1]
MEMBERS = ('nils_meyer', 'jannik_altenschmidt', 'tobias_gaertner',
           'finn_bielig', 'max_gerwers', 'tim_wissing')


def read(relative):
    return parse_script((ROOT / relative).read_text(encoding='utf-8-sig'))


def walk(nodes):
    for node in nodes:
        yield node
        yield from walk(children(node))


class AssemblyWorld:
    def __init__(self):
        self.effects_by_name = {n.key: children(n) for f in ('WFL_assembly_effects.txt', 'WFL_board_mood_effects.txt') for n in read('common/scripted_effects/' + f)}
        self.triggers = {n.key: children(n) for n in read('common/scripted_triggers/WFL_assembly_triggers.txt')}
        self.hooks = {n.key: children(block(n, 'effect')) for n in children(read('common/on_actions/WFL_assembly_on_actions.txt')[0])}
        self.variables = {}
        self.flags = set()
        self.flag_dates = {}
        self.ideas = set()
        self.scheduled = []
        self.now = date(1936, 1, 1)
        self.tag = 'WFL'
        self.exists = True
        self.capitulated = False
        self.choices = []
        self.random_trace = []

    def number(self, value):
        try:
            return Decimal(str(value))
        except Exception:
            return self.variables.get(value.removeprefix('var:'), Decimal(0))

    def pair(self, node):
        if field(node, 'var'):
            return field(node, 'var'), field(node, 'value')
        first = children(node)[0]
        return first.key, first.value

    @staticmethod
    def compare(left, operator, right):
        operator = {'greater_than': '>', 'greater_than_or_equals': '>=', 'less_than': '<', 'less_than_or_equals': '<=', 'equals': '='}.get(operator, operator)
        return {'=': left == right, '>': left > right, '<': left < right,
                '>=': left >= right, '<=': left <= right, '!=': left != right}[operator]

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
            elif key == 'tag':
                result = self.tag == value
            elif key == 'exists':
                result = self.exists == (value == 'yes')
            elif key == 'has_capitulated':
                result = self.capitulated == (value == 'yes')
            elif key == 'always':
                result = value == 'yes'
            elif key == 'has_idea':
                result = value in self.ideas
            elif key == 'has_country_flag':
                if isinstance(value, str):
                    result = value in self.flags
                else:
                    flag = field(node, 'flag')
                    result = flag in self.flags
                    for part in children(node):
                        if part.key == 'days' and result:
                            elapsed = (self.now - self.flag_dates[flag]).days
                            result = self.compare(elapsed, part.op, int(part.value))
                        elif part.key not in ('flag', 'days'):
                            raise AssertionError('Unsupported dated flag field: ' + part.key)
            elif key == 'check_variable':
                name, target = self.pair(node)
                part = next(n for n in children(node) if n.key in (name, 'value'))
                result = self.compare(self.number(name), field(node, 'compare') or part.op, self.number(target))
            else:
                raise AssertionError('Unsupported assembly condition: ' + key)
            if not result:
                return False
        return True

    def run(self, name):
        self.effects(self.effects_by_name[name])

    def hook(self, name):
        self.effects(self.hooks[name])

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
                    raise AssertionError('Unpaired else_if')
                if not branch_taken and self.matches(children(block(node, 'limit'))):
                    branch_taken = True
                    self.effects([n for n in children(node) if n.key != 'limit'])
            elif key == 'else':
                if branch_taken is None:
                    raise AssertionError('Unpaired else')
                if not branch_taken:
                    self.effects(children(node))
                branch_taken = None
            elif key in self.effects_by_name:
                self.run(key)
            elif key in ('hidden_effect', 'effect', 'WFL'):
                if key != 'WFL' or self.exists:
                    self.effects(children(node))
            elif key in ('custom_effect_tooltip', 'show_ideas_tooltip', 'log'):
                pass
            elif key == 'set_country_flag':
                if not isinstance(value, str):
                    raise AssertionError('Unexpected timed country flag')
                self.flags.add(value)
                self.flag_dates[value] = self.now
            elif key == 'clr_country_flag':
                self.flags.discard(value)
                self.flag_dates.pop(value, None)
            elif key in ('set_variable', 'add_to_variable', 'subtract_from_variable'):
                name, amount = self.pair(node)
                amount, old = self.number(amount), self.number(name)
                self.variables[name] = {'set_variable': amount,
                                        'add_to_variable': old + amount,
                                        'subtract_from_variable': old - amount}[key]
            elif key in ('add_ideas', 'remove_ideas'):
                ideas = [value] if isinstance(value, str) else [n.key for n in children(node)]
                for idea in ideas:
                    if key == 'add_ideas':
                        self.ideas.add(idea)
                    else:
                        self.ideas.discard(idea)
            elif key == 'random_list':
                branches = children(node)
                weights = tuple(int(n.key) for n in branches)
                self.random_trace.append(weights)
                index = self.choices.pop(0) if self.choices else 0
                if not 0 <= index < len(branches):
                    raise AssertionError('RNG fixture branch outside script')
                self.effects(children(branches[index]))
            elif key in ('news_event', 'country_event'):
                self.scheduled.append((key, value if isinstance(value, str) else field(node, 'id')))
            else:
                raise AssertionError('Unsupported assembly effect: ' + key)

    def advance(self, days):
        for _ in range(days):
            self.now += timedelta(days=1)
            self.hook('on_daily_WFL')
            if self.now.day == 1:
                self.hook('on_monthly_WFL')


class AssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.group = read('common/decisions/WFL_assembly.txt')[0]
        cls.decisions = {n.key: n for n in children(cls.group)}

    def world(self):
        world = AssemblyWorld()
        world.hook('on_startup')
        return world

    def lobby(self, world, member):
        decision = self.decisions[f'WFL_board_lobby_{member}']
        self.assertTrue(world.matches(children(block(decision, 'available'))))
        world.effects(children(block(decision, 'complete_effect')))

    def test_calendar_first_meeting_is_july_then_january_without_january_double_count(self):
        world = self.world()
        world.hook('on_monthly_WFL')
        self.assertEqual(world.number('WFL_assembly_months_left'), 6)
        world.advance(181)
        self.assertEqual(world.now, date(1936, 6, 30))
        self.assertEqual(world.number('WFL_assembly_number'), 0)
        self.assertFalse(world.scheduled)
        world.advance(1)
        self.assertEqual(world.number('WFL_assembly_number'), 1)
        self.assertEqual(world.number('WFL_assembly_months_left'), 6)
        self.assertEqual(world.scheduled, [('news_event', 'wfl_assembly.1')])
        world.advance(184)
        self.assertEqual(world.now, date(1937, 1, 1))
        self.assertEqual(world.number('WFL_assembly_number'), 2)
        self.assertEqual(world.scheduled, [('news_event', 'wfl_assembly.1')] * 2)

    def test_reinitialization_preserves_existing_clock_and_campaign(self):
        world = self.world()
        world.advance(35)
        self.lobby(world, MEMBERS[0])
        before = dict(world.variables), set(world.flags), dict(world.flag_dates)
        for _ in range(2):
            world.hook('on_startup')
            world.hook('on_daily_WFL')
        self.assertEqual((world.variables, world.flags, world.flag_dates), before)

    def test_old_save_initializes_once_on_daily_hook_without_immediate_meeting(self):
        world = AssemblyWorld()
        world.now = date(1938, 3, 15)
        world.hook('on_daily_WFL')
        self.assertIn('WFL_assembly_initialized', world.flags)
        self.assertEqual(world.number('WFL_assembly_months_left'), 6)
        self.assertEqual(world.number('WFL_assembly_number'), 0)
        self.assertFalse(world.scheduled)
        world.advance((date(1938, 8, 31) - world.now).days)
        self.assertFalse(world.scheduled)
        world.advance(1)
        self.assertEqual(world.now, date(1938, 9, 1))
        self.assertEqual(world.number('WFL_assembly_number'), 1)

    def test_lobby_success_has_actual_cost_once_per_cycle_and_does_not_clear_anger(self):
        self.assertEqual(set(self.decisions), {f'WFL_board_lobby_{m}' for m in MEMBERS})
        for member in MEMBERS:
            with self.subTest(member=member):
                world = self.world()
                decision = self.decisions[f'WFL_board_lobby_{member}']
                self.assertEqual(field(decision, 'cost'), '35')
                self.lobby(world, member)
                self.assertEqual(world.random_trace, [(85, 10, 5)])
                self.assertIn(f'WFL_board_{member}_backed', world.flags)
                self.assertIn(f'WFL_board_{member}_used', world.flags)
                self.assertFalse(world.matches(children(block(decision, 'available'))))
                # A repeated/raced effect cannot reroll the result.
                before = set(world.flags), list(world.random_trace)
                world.effects(children(block(decision, 'complete_effect')))
                self.assertEqual((world.flags, world.random_trace), before)
                angry = self.world()
                angry.flags.add(f'WFL_board_{member}_angry')
                self.assertFalse(angry.matches(children(block(decision, 'available'))))
                angry.effects(children(block(decision, 'complete_effect')))
                self.assertIn(f'WFL_board_{member}_angry', angry.flags)
                self.assertFalse(angry.random_trace)

    def test_every_collateral_branch_angers_exactly_one_other_member_uniformly(self):
        for member in MEMBERS:
            victims = set()
            for index in range(5):
                world = self.world()
                world.choices = [1, index]
                self.lobby(world, member)
                self.assertEqual(world.random_trace[0], (85, 10, 5))
                weights = world.random_trace[1]
                self.assertEqual(len(weights), 5)
                self.assertEqual(len(set(weights)), 1)
                self.assertTrue(all(weight > 0 for weight in weights))
                angry = {m for m in MEMBERS if f'WFL_board_{m}_angry' in world.flags}
                self.assertEqual(len(angry), 1)
                self.assertNotIn(member, angry)
                self.assertIn(f'WFL_board_{member}_backed', world.flags)
                victims |= angry
            self.assertEqual(victims, set(MEMBERS) - {member})

    def test_failed_lobby_angers_only_its_own_member_and_awards_no_backing(self):
        for member in MEMBERS:
            world = self.world()
            world.choices = [2]
            self.lobby(world, member)
            self.assertIn(f'WFL_board_{member}_angry', world.flags)
            self.assertNotIn(f'WFL_board_{member}_backed', world.flags)
            self.assertEqual({m for m in MEMBERS if f'WFL_board_{m}_angry' in world.flags}, {member})

    def test_news_and_six_portraits_use_the_supplied_artwork(self):
        events = [n for n in read('events/WFL_assembly.txt') if n.key == 'news_event']
        self.assertTrue(events)
        for event in events:
            self.assertEqual(field(event, 'picture'), 'GFX_WFL_assembly_hall')
            self.assertEqual(field(event, 'major'), 'no')
        gfx = {field(n, 'name'): field(n, 'texturefile')
               for n in walk(read('interface/WFL_assembly_assets.gfx'))
               if n.key == 'spriteType' and isinstance(n.value, list)}
        expected = [(f'GFX_WFL_board_{m}', (128, 128)) for m in MEMBERS]
        expected.append(('GFX_WFL_assembly_hall', (397, 153)))
        for name, (width, height) in expected:
            raw = (ROOT / gfx[name]).read_bytes()
            self.assertEqual(raw[:4], b'DDS ')
            self.assertEqual(struct.unpack_from('<II', raw, 12), (height, width))
        recipe = json.loads((ROOT / 'tools/data/WFL_assembly_art.json').read_text(encoding='utf-8-sig'))
        self.assertEqual({m['id'] for m in recipe['members']}, set(MEMBERS))
        self.assertEqual(recipe['news'], 'Sch\u00fctzenversammlung im gro\u00dfen Vereinssaal.png')

    def test_vote_weights_and_anger_override_a_previous_promise(self):
        for member in MEMBERS:
            for backed, expected in ((False, (35, 65)), (True, (85, 15))):
                for branch in (0, 1):
                    world = self.world()
                    if backed:
                        world.flags.add(f'WFL_board_{member}_backed')
                    world.choices = [branch]
                    world.run(f'WFL_assembly_vote_{member}')
                    self.assertEqual(world.random_trace, [expected])
                    self.assertEqual(f'WFL_assembly_{member}_idea' in world.ideas, branch == 0)
                    self.assertIn(f'WFL_board_{member}_last_' + ('approved' if branch == 0 else 'rejected'), world.flags)
            angry = self.world()
            angry.flags.update((f'WFL_board_{member}_angry', f'WFL_board_{member}_backed'))
            angry.run(f'WFL_assembly_vote_{member}')
            self.assertFalse(angry.random_trace)
            self.assertFalse(angry.ideas)
            self.assertIn(f'WFL_board_{member}_last_angry', angry.flags)

    def test_quarrel_threshold_all_branches_and_severe_cancellation(self):
        for count in (0, 1):
            world = self.world()
            world.flags.update(f'WFL_board_{m}_angry' for m in MEMBERS[:count])
            world.run('WFL_assembly_resolve')
            self.assertNotIn((70, 20, 10), world.random_trace)
        for branch in range(3):
            world = self.world()
            world.flags.update(f'WFL_board_{m}_angry' for m in MEMBERS[:2])
            world.choices = [branch]  # All remaining normal votes approve.
            world.run('WFL_assembly_resolve')
            self.assertEqual(world.random_trace[0], (70, 20, 10))
            self.assertEqual('WFL_assembly_blockade_idea' in world.ideas, branch == 1)
            self.assertEqual('WFL_assembly_eklat_idea' in world.ideas, branch == 2)
            for member in MEMBERS:
                positive = f'WFL_assembly_{member}_idea' in world.ideas
                self.assertEqual(positive, branch != 2 and member not in MEMBERS[:2])
                self.assertIn(f'WFL_board_{member}_last_' + ('approved' if positive else 'rejected'), world.flags)
            if branch == 2:
                self.assertEqual(world.random_trace, [(70, 20, 10)])

    def test_results_replace_old_ideas_reset_lobby_and_never_stack(self):
        world = self.world()
        world.ideas = {'WFL_rheinhandel', 'WFL_assembly_eklat_idea', 'WFL_assembly_blockade_idea'}
        world.ideas.update(f'WFL_assembly_{m}_idea' for m in MEMBERS)
        world.flags.update(f'WFL_board_{m}_used' for m in MEMBERS)
        world.choices = [1] * 6  # All six untouched motions fail this time.
        world.run('WFL_assembly_resolve')
        self.assertEqual(world.ideas, {'WFL_rheinhandel'})
        for member in MEMBERS:
            self.assertNotIn(f'WFL_board_{member}_used', world.flags)
            self.assertNotIn(f'WFL_board_{member}_backed', world.flags)
            self.assertNotIn(f'WFL_board_{member}_angry', world.flags)
            self.assertTrue(world.matches(children(block(self.decisions[f'WFL_board_lobby_{member}'], 'available'))))
        self.assertEqual(world.scheduled, [('news_event', 'wfl_assembly.1')])
        event = next(n for n in read('events/WFL_assembly.txt') if n.key == 'news_event')
        self.assertEqual({n.key for n in children(block(event, 'option'))}, {'name'})

    def test_capitulation_pauses_calendar_removes_capacity_and_blocks_lobby(self):
        world = self.world()
        world.ideas = {'WFL_rheinhandel', 'WFL_assembly_eklat_idea'}
        world.ideas.update(f'WFL_assembly_{m}_idea' for m in MEMBERS)
        world.advance(35)
        before = world.number('WFL_assembly_months_left')
        world.capitulated = True
        world.advance(190)
        self.assertEqual(world.number('WFL_assembly_months_left'), before)
        self.assertEqual(world.ideas, {'WFL_rheinhandel'})
        self.assertFalse(world.scheduled)
        for decision in self.decisions.values():
            self.assertFalse(world.matches(children(block(decision, 'available'))))
        world.run('WFL_assembly_resolve')
        self.assertFalse(world.scheduled)
        world.capitulated = False
        world.advance(190)
        self.assertTrue(world.scheduled)

    def test_all_eight_modifier_profiles_match_published_contract(self):
        group = read('common/ideas/WFL_assembly_ideas.txt')[0]
        ideas = {n.key: children(block(n, 'modifier')) for n in children(block(group, 'country'))}
        expected = {
            'nils_meyer': {'industrial_capacity_factory': '.15', 'industrial_capacity_dockyard': '.15'},
            'jannik_altenschmidt': {'production_speed_industrial_complex_factor': '.15', 'production_speed_arms_factory_factor': '.15'},
            'tobias_gaertner': {'army_attack_factor': '.05', 'army_defence_factor': '.05', 'army_org_factor': '.05'},
            'finn_bielig': {'supply_consumption_factor': '-.10', 'training_time_army_factor': '-.10'},
            'max_gerwers': {'research_speed_factor': '.05', 'production_factory_efficiency_gain_factor': '.10'},
            'tim_wissing': {'political_power_gain': '.15', 'stability_factor': '.05'},
            'blockade': {'stability_factor': '-.05', 'political_power_factor': '-.10'},
            'eklat': {'industrial_capacity_factory': '-.10', 'production_speed_buildings_factor': '-.10', 'army_org_factor': '-.05'},
        }
        self.assertEqual(len(ideas), 8)
        for key, profile in expected.items():
            actual = {n.key: Decimal(n.value) for n in ideas[f'WFL_assembly_{key}_idea']}
            self.assertEqual(actual, {k: Decimal(v) for k, v in profile.items()})

    def test_decision_ui_has_six_bounded_portrait_cards_with_distinct_names(self):
        root = read('interface/WFL_assembly.gui')[0]
        window = block(root, 'containerWindowType')
        window_height = int(field(block(window, 'size'), 'height'))
        cards = [n for n in children(window) if n.key == 'containerWindowType']
        self.assertEqual(len(cards), 6)
        self.assertEqual({field(n, 'name') for n in cards}, {f'WFL_board_{m}_card' for m in MEMBERS})
        for card in cards:
            y = int(field(block(card, 'position'), 'y'))
            h = int(field(block(card, 'size'), 'height'))
            self.assertLessEqual(y + h, window_height)
            self.assertEqual(field(card, 'clipping'), 'no')
            for node in children(card):
                if node.key == 'instantTextBoxType':
                    self.assertLessEqual(int(field(block(node, 'position'), 'y')) + int(field(node, 'maxHeight')), h)

    def test_decision_labels_expose_bonuses_and_use_supported_normal_text_bindings(self):
        gui = read('interface/WFL_assembly.gui')
        widgets = {field(n, 'name'): n for n in walk(gui) if n.key == 'instantTextBoxType'}
        for member in MEMBERS:
            self.assertEqual(field(widgets[f'WFL_board_{member}_bonus'], 'text'), f'WFL_board_ui_{member}_bonus')
            status = widgets[f'WFL_board_{member}_status']
            self.assertEqual(field(status, 'text'), f'WFL_board_ui_{member}_status')
            self.assertIsNone(field(status, 'context_aware_text'))
        for key in ('clock', 'mood'):
            node = widgets[f'WFL_board_ui_{key}']
            self.assertEqual(field(node, 'text'), f'WFL_board_ui_{key}')
            self.assertIsNone(field(node, 'context_aware_text'))
        for language in ('german', 'english'):
            text = (ROOT / f'localisation/{language}/WFL_assembly_ui_l_{language}.yml').read_text(encoding='utf-8-sig')
            self.assertIn(' WFL_board_ui_clock:0 "[WFLBoardClock]"', text)
            self.assertIn('[?WFL_board_mood|0]/100', text)
            self.assertIn('[WFLBoardMoodLabel]', text)


if __name__ == '__main__':
    unittest.main()
