"""Execute Iran's actual AST rewards in a deliberately limited scope fixture.

The interpreter rejects unknown commands. It models the local engine docs, but
cannot replace an in-game check of war cleanup, factions or character promotion.
"""
from dataclasses import dataclass, field as data_field
import json
from pathlib import Path
import struct
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
EFFECT = 'WFL_establish_iranian_puppet_effect'
SHAH = 'WFL_PER_al_hoehne'
SHAH_TRAIT = 'WFL_PER_fluerentreuer_schah'
COMPLETED = 'WFL_iran_treaty_completed'
FOCI = ('WFL_iran_erbfolgekrise', 'WFL_iran_gesandtschaft',
        'WFL_iran_hochzeit', 'WFL_iran_treuevertrag')


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return next(n for n in children(node) if n.key == key)


@dataclass
class Country:
    tag: str
    overlord: str | None = None
    faction: str | None = None
    capitulated: bool = False
    wars: set[str] = data_field(default_factory=set)
    flags: set[str] = data_field(default_factory=set)
    characters: list[str] = data_field(default_factory=list)
    leader: str = 'original_ruler'
    government: str = 'neutrality'
    elections: str = 'no'
    power: int = 0
    stability: float = 0.5


@dataclass
class State:
    id: int
    owner: str
    controller: str
    cores: set[str]


@dataclass
class RuntimeCharacter:
    identity: str
    name: str
    owner: str
    traits: set[str]


class IranWorld:
    def __init__(self, autonomy_dlc=False):
        self.countries = {tag: Country(tag) for tag in ('WFL', 'PER', 'GER', 'HOL')}
        self.root = self.countries['WFL']
        self.root.leader = 'WFL_schuetzenkoenig'
        self.root.characters = ['WFL_schuetzenkoenig', 'WFL_lukas_hoehne_i']
        self.countries['PER'].leader = 'PER_reza_shah'
        self.countries['GER'].leader = 'unchanged_german_leader'
        self.states = {
            1082: State(1082, 'WFL', 'WFL', {'WFL'}),
            266: State(266, 'PER', 'PER', {'PER'}),
            410: State(410, 'PER', 'PER', {'PER'}),
            51: State(51, 'GER', 'GER', {'GER'}),
            7: State(7, 'HOL', 'HOL', {'HOL'}),
        }
        self.faction_leaders = {}
        self.autonomy_dlc = autonomy_dlc
        self.autonomy = {}
        self.scheduled = []
        self.transfers = []
        self.detachments = []
        self.puppet_calls = []
        self.created = []
        self.portraits = {}
        self.character_data = {}
        self.add_character('PER', 'PER_reza_shah', 'PER_reza_shah', {'original_shah'})
        self.scripted = {n.key: children(n)
                         for n in read('common/scripted_effects/WFL_iran_succession_effects.txt')}

    def add_character(self, owner, identity, name, traits):
        self.countries[owner].characters.append(identity)
        self.character_data[identity] = RuntimeCharacter(identity, name, owner, set(traits))
        return identity

    def scope(self, key, stack):
        if key == 'ROOT':
            return self.root
        if key == 'PREV':
            return stack[-2]
        if key == 'overlord':
            return self.countries[stack[-1].overlord]
        if key.isdigit():
            return self.states[int(key)]
        return self.countries[key]

    def conditions(self, nodes, stack):
        current = stack[-1]
        for node in nodes:
            key, value = node.key, node.value
            if key == 'NOT':
                matches = not self.conditions(children(node), stack)
            elif key in self.countries or key.isdigit():
                matches = self.conditions(children(node), stack + [self.scope(key, stack)])
            elif key == 'tag':
                matches = current.tag == value
            elif key == 'exists':
                matches = any(s.owner == current.tag for s in self.states.values()) == (value == 'yes')
            elif key == 'is_subject':
                matches = (current.overlord is not None) == (value == 'yes')
            elif key == 'is_subject_of':
                matches = current.overlord == self.scope(value, stack).tag
            elif key == 'has_capitulated':
                matches = current.capitulated == (value == 'yes')
            elif key == 'has_country_flag':
                matches = value in current.flags
            elif key == 'has_character':
                matches = value in current.characters
            elif key == 'any_character':
                matches = any(self.conditions(children(node), stack + [self.character_data[identity]])
                              for identity in current.characters)
            elif key == 'has_trait':
                assert isinstance(current, RuntimeCharacter), 'has_trait requires character scope'
                matches = value in current.traits
            elif key == 'is_core_of':
                matches = self.scope(value, stack).tag in current.cores
            elif key == 'is_faction_leader':
                matches = (current.faction is not None and
                           self.faction_leaders[current.faction] == current.tag) == (value == 'yes')
            elif key == 'is_in_faction':
                matches = (current.faction is not None) == (value == 'yes')
            elif key == 'is_in_faction_with':
                matches = current.faction is not None and current.faction == self.scope(value, stack).faction
            elif key == 'has_dlc':
                assert value == 'Together for Victory', value
                matches = self.autonomy_dlc
            else:
                raise AssertionError(f'unsupported condition: {key}')
            if not matches:
                return False
        return True

    def end_wars(self, target):
        target.wars.clear()
        for country in self.countries.values():
            country.wars.discard(target.tag)

    def effects(self, nodes, stack=None):
        stack = stack or [self.root]
        preceding_if = None
        for node in nodes:
            current = stack[-1]
            key, value = node.key, node.value
            if key == 'if':
                preceding_if = self.conditions(children(block(node, 'limit')), stack)
                if preceding_if:
                    self.effects([n for n in children(node) if n.key != 'limit'], stack)
            elif key == 'else':
                if preceding_if is False:
                    self.effects(children(node), stack)
            elif key in self.countries or key.isdigit() or key == 'overlord':
                self.effects(children(node), stack + [self.scope(key, stack)])
            elif key in self.scripted:
                self.effects(self.scripted[key], stack)
            elif key == 'hidden_effect':
                self.effects(children(node), stack)
            elif key in ('every_state', 'every_owned_state'):
                limit = next((n for n in children(node) if n.key == 'limit'), None)
                selected = [s for s in self.states.values()
                            if (key == 'every_state' or s.owner == current.tag)
                            and (limit is None or self.conditions(children(limit), stack + [s]))]
                for state in selected:
                    self.effects([n for n in children(node) if n.key != 'limit'], stack + [state])
            elif key == 'transfer_state':
                state = self.scope(value, stack)
                self.transfers.append((state.id, state.owner, current.tag))
                state.owner = state.controller = current.tag
            elif key == 'set_state_controller_to':
                current.controller = self.scope(value, stack).tag
            elif key == 'add_core_of':
                current.cores.add(self.scope(value, stack).tag)
            elif key == 'end_puppet':
                subject = self.scope(value, stack)
                assert subject.overlord == current.tag, (current.tag, subject)
                self.detachments.append((current.tag, subject.tag))
                subject.overlord = None
            elif key == 'puppet':
                target = self.scope(field(node, 'target'), stack)
                assert target.overlord in (None, current.tag), target.overlord
                assert field(node, 'end_wars') == field(node, 'end_civil_wars') == 'yes'
                assert current.overlord is None, 'a subject cannot be an overlord in this supported path'
                target.overlord = current.tag
                self.end_wars(target)
                self.puppet_calls.append((current.tag, target.tag))
            elif key == 'set_autonomy':
                target = self.scope(field(node, 'target'), stack)
                assert self.autonomy_dlc
                assert target.overlord == current.tag
                assert field(node, 'end_wars') == field(node, 'end_civil_wars') == 'yes'
                self.autonomy[target.tag] = (field(node, 'autonomy_state'), field(node, 'freedom_level'))
                self.end_wars(target)
            elif key == 'set_faction_leader':
                assert current.faction is not None
                self.faction_leaders[current.faction] = current.tag
            elif key == 'dismantle_faction':
                faction = current.faction
                assert self.faction_leaders[faction] == current.tag
                for country in self.countries.values():
                    if country.faction == faction:
                        country.faction = None
                del self.faction_leaders[faction]
            elif key == 'leave_faction':
                assert self.faction_leaders[current.faction] != current.tag
                current.faction = None
            elif key == 'create_country_leader':
                assert current.tag == 'PER'
                # The real engine did NOT register the static name token when
                # creating this previously unrecruited character. IDs are opaque.
                identity = f'runtime-{current.tag}-{len(self.created) + 901}'
                self.add_character(current.tag, identity, field(node, 'name'),
                                   {n.key for n in children(block(node, 'traits'))})
                self.created.append(identity)
            elif key == 'every_character':
                assert isinstance(current, Country)
                selected = [self.character_data[identity] for identity in current.characters
                            if self.conditions(children(block(node, 'limit')),
                                               stack + [self.character_data[identity]])]
                for character in selected:
                    self.effects([n for n in children(node)
                                  if n.key != 'limit'], stack + [character])
            elif key == 'set_portraits':
                assert isinstance(current, RuntimeCharacter), 'use the actual character scope'
                assert field(node, 'character') is None, 'do not resolve the display name as an ID'
                self.portraits[current.identity] = {
                    n.key: n.value for n in children(block(node, 'civilian'))}
            elif key == 'promote_character':
                assert isinstance(current, RuntimeCharacter), 'use the actual character scope'
                assert value == 'yes'
                self.countries[current.owner].leader = current.identity
            elif key == 'set_politics':
                current.government = field(node, 'ruling_party')
                current.elections = field(node, 'elections_allowed')
            elif key == 'set_country_flag':
                current.flags.add(value)
            elif key == 'country_event':
                self.scheduled.append((current.tag, field(node, 'id')))
            elif key == 'add_political_power':
                current.power += int(value)
            elif key == 'add_stability':
                current.stability += float(value)
            elif key == 'custom_effect_tooltip':
                pass
            else:
                raise AssertionError(f'unsupported effect: {key}')


class IranSuccessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focuses = {field(n, 'id'): n for tree in read('common/national_focus/WFL_focus.txt')
                       for n in children(tree) if n.key == 'focus' and field(n, 'id') in FOCI}
        cls.reward = children(block(cls.focuses[FOCI[-1]], 'completion_reward'))

    def assert_treaty(self, world):
        iran = world.countries['PER']
        self.assertTrue(any(s.owner == 'PER' for s in world.states.values()))
        self.assertEqual(iran.overlord, 'WFL')
        self.assertEqual((world.character_data[iran.leader].name, iran.government, iran.elections),
                         (SHAH, 'neutrality', 'no'))
        self.assertNotEqual(iran.leader, SHAH)
        self.assertEqual(sum(SHAH_TRAIT in world.character_data[identity].traits
                             for identity in iran.characters), 1)
        self.assertEqual(world.portraits[iran.leader], {
            'large': 'GFX_portrait_WFL_PER_al_hoehne',
            'small': 'GFX_portrait_WFL_PER_al_hoehne_small'})
        self.assertIn(COMPLETED, world.root.flags)
        self.assertIn('WFL_iran_al_hoehne_crowned', iran.flags)
        self.assertEqual(world.scheduled.count(('WFL', 'wfl_iran_succession.4')), 1)
        self.assertTrue(all(s.controller == 'PER' for s in world.states.values() if s.owner == 'PER'))
        self.assertEqual(world.root.leader, 'WFL_schuetzenkoenig')
        self.assertEqual(world.root.characters, ['WFL_schuetzenkoenig', 'WFL_lukas_hoehne_i'])
        self.assertEqual(world.countries['GER'].leader, 'unchanged_german_leader')
        self.assertEqual((world.states[51].owner, world.states[7].owner), ('GER', 'HOL'))
        if world.autonomy_dlc:
            self.assertEqual(world.autonomy['PER'], ('autonomy_puppet', '0'))
        else:
            self.assertEqual(world.autonomy, {})

    def test_full_focus_chain_resolves_without_clicking_any_event_and_under_either_dlc_setting(self):
        self.assertEqual(set(self.focuses), set(FOCI))
        for autonomy_dlc in (False, True):
            with self.subTest(autonomy_dlc=autonomy_dlc):
                world = IranWorld(autonomy_dlc)
                parent = 'WFL_vereinsdiplomatie'
                for focus_id in FOCI:
                    focus = self.focuses[focus_id]
                    self.assertEqual(field(block(focus, 'prerequisite'), 'focus'), parent)
                    self.assertEqual(field(focus, 'cost'), '5')
                    self.assertTrue(world.conditions(children(block(focus, 'available')), [world.root]))
                    world.effects(children(block(focus, 'completion_reward')))
                    parent = focus_id
                self.assert_treaty(world)
                self.assertEqual(len(world.scheduled), 4)
                self.assertEqual(world.transfers, [])

    def test_foreign_overlord_and_enemy_war_are_removed_without_changing_unrelated_countries(self):
        world = IranWorld(True)
        world.countries['PER'].overlord = 'GER'
        world.countries['PER'].faction = world.countries['GER'].faction = 'german_faction'
        world.faction_leaders['german_faction'] = 'GER'
        world.countries['PER'].wars = {'WFL', 'HOL'}
        world.root.wars = {'PER', 'HOL'}
        world.countries['HOL'].wars = {'PER', 'WFL'}
        world.states[266].controller = 'WFL'
        world.states[410].controller = 'GER'
        world.effects(self.reward)
        self.assert_treaty(world)
        self.assertEqual(world.detachments, [('GER', 'PER')])
        self.assertEqual(world.countries['PER'].wars, set())
        self.assertEqual(world.root.wars, {'HOL'})
        self.assertEqual(world.countries['HOL'].wars, {'WFL'})
        self.assertEqual(world.countries['GER'].faction, 'german_faction')
        self.assertIsNone(world.countries['PER'].faction)
        self.assertEqual(world.transfers, [])

    def test_annexed_iran_split_between_owners_is_restored_with_actual_control(self):
        for autonomy_dlc in (False, True):
            for owners in [('GER', 'HOL'), ('WFL', 'WFL')]:
                with self.subTest(autonomy_dlc=autonomy_dlc, owners=owners):
                    world = IranWorld(autonomy_dlc)
                    world.states[266].owner, world.states[410].owner = owners
                    world.states[266].controller = 'HOL'
                    world.states[410].controller = 'GER'
                    world.countries['PER'].overlord = 'GER'  # retained after annexation
                    world.effects(self.reward)
                    self.assert_treaty(world)
                    self.assertEqual({s[0] for s in world.transfers}, {266, 410})
                    self.assertEqual(world.detachments, [('GER', 'PER')])

    def test_historical_capital_anchor_restores_iran_even_if_all_cores_were_removed(self):
        world = IranWorld()
        for state in (world.states[266], world.states[410]):
            state.owner = state.controller = 'GER'
            state.cores.clear()
        world.effects(self.reward)
        self.assert_treaty(world)
        self.assertEqual(world.transfers, [(266, 'GER', 'PER')])
        self.assertIn('PER', world.states[266].cores)
        self.assertEqual(world.states[410].owner, 'GER')

    def test_existing_wfl_puppet_and_pre_recruited_ruler_need_no_second_recruitment(self):
        world = IranWorld()
        world.countries['PER'].overlord = 'WFL'
        world.add_character('PER', 'loaded-save-character-478', SHAH, {SHAH_TRAIT})
        world.effects(self.reward)
        self.assert_treaty(world)
        self.assertEqual(world.detachments, [])
        self.assertEqual(world.puppet_calls, [('WFL', 'PER')])
        self.assertEqual(world.created, [])

    def test_iranian_faction_leadership_is_resolved_without_replacing_other_rulers(self):
        for shared_with_wfl in (False, True):
            with self.subTest(shared_with_wfl=shared_with_wfl):
                world = IranWorld()
                world.countries['PER'].faction = world.countries['HOL'].faction = 'iranian_faction'
                world.faction_leaders['iranian_faction'] = 'PER'
                if shared_with_wfl:
                    world.root.faction = 'iranian_faction'
                world.effects(self.reward)
                self.assert_treaty(world)
                if shared_with_wfl:
                    self.assertEqual(world.faction_leaders['iranian_faction'], 'WFL')
                    self.assertEqual(world.countries['HOL'].faction, 'iranian_faction')
                else:
                    self.assertEqual(world.faction_leaders, {})
                    self.assertIsNone(world.countries['HOL'].faction)

    def test_repeat_reward_does_not_undo_a_later_government_or_trigger_duplicate_events(self):
        world = IranWorld(True)
        world.effects(self.reward)
        world.countries['PER'].leader = 'later_ruler'
        world.countries['PER'].overlord = None
        world.states[266].owner = world.states[266].controller = 'HOL'
        world.effects(self.reward)
        self.assertEqual(world.countries['PER'].leader, 'later_ruler')
        self.assertIsNone(world.countries['PER'].overlord)
        self.assertEqual(world.states[266].owner, 'HOL')
        self.assertEqual(world.puppet_calls, [('WFL', 'PER')])
        self.assertEqual(len(world.scheduled), 1)

    def test_wfl_sovereignty_and_non_capitulation_are_required_transparently(self):
        for invalid in ('subject', 'capitulated'):
            with self.subTest(invalid=invalid):
                world = IranWorld()
                if invalid == 'subject':
                    world.root.overlord = 'GER'
                else:
                    world.root.capitulated = True
                for focus in self.focuses.values():
                    self.assertFalse(world.conditions(children(block(focus, 'available')), [world.root]))
                world.effects(self.reward)
                self.assertEqual(world.countries['PER'].leader, 'PER_reza_shah')
                self.assertNotIn(COMPLETED, world.root.flags)
                self.assertEqual(world.puppet_calls, [])

    def test_story_has_no_rng_or_foreign_veto_and_does_not_move_the_wfl_field_marshal(self):
        events = [n for n in read('events/WFL_iran_succession.txt') if n.key == 'country_event']
        self.assertEqual({field(n, 'id') for n in events},
                         {f'wfl_iran_succession.{n}' for n in range(1, 5)})
        for event in events:
            self.assertEqual(field(event, 'is_triggered_only'), 'yes')
            self.assertEqual(field(event, 'fire_only_once'), 'yes')
            self.assertEqual(field(block(event, 'trigger'), 'tag'), 'WFL')
            options = [n for n in children(event) if n.key == 'option']
            self.assertEqual(len(options), 1)
            self.assertEqual([n.key for n in children(options[0])], ['name'])
        scripted = read('common/scripted_effects/WFL_iran_succession_effects.txt')
        all_nodes = list(walk(scripted + events + list(self.focuses.values())))
        self.assertFalse(any(n.key == 'recruit_character' for n in all_nodes))
        self.assertFalse(any(n.key.startswith('random') or n.key == 'ai_chance' for n in all_nodes))
        self.assertFalse(any(n.value in ('WFL_lukas_hoehne_i', 'WFL_schuetzenkoenig') for n in all_nodes))

    def test_character_portrait_traits_and_localised_name_use_the_supplied_cigar_portrait(self):
        character = next(n for group in read('common/characters/WFL_iran.txt')
                         for n in children(group) if n.key == SHAH)
        self.assertEqual(field(character, 'name'), SHAH)
        self.assertEqual(field(block(character, 'country_leader'), 'ideology'), 'despotism')
        creation = next(n for n in walk(read('common/scripted_effects/WFL_iran_succession_effects.txt'))
                        if n.key == 'create_country_leader')
        selection = next(n for n in walk(read('common/scripted_effects/WFL_iran_succession_effects.txt'))
                         if n.key == 'every_character')
        self.assertIsNone(field(selection, 'include_invisible'))
        declared = block(character, 'country_leader')
        self.assertEqual(field(creation, 'name'), SHAH)
        self.assertEqual(field(creation, 'picture'), 'GFX_portrait_WFL_PER_al_hoehne')
        for key in ('ideology', 'traits', 'expire'):
            self.assertEqual(block(creation, key).value, block(declared, key).value)
        self.assertEqual({n.key for n in children(character)}, {'name', 'portraits', 'country_leader'})
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(read('interface/WFL_iran.gfx')) if n.key == 'spriteType'}
        civilian = block(block(character, 'portraits'), 'civilian')
        manifest = json.loads((ROOT / 'tools/data/al_hoehne_portrait.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(manifest['source_file'], 'Selbstbewusster Offizier mit Zigarre.png')
        for size, dimensions in [('large', (156, 210)), ('small', (65, 67))]:
            texture = sprites[field(civilian, size)]
            self.assertEqual(texture, manifest['output' if size == 'large' else 'small_output'])
            raw = (ROOT / texture).read_bytes()
            self.assertEqual(raw[:4], b'DDS ')
            height, width = struct.unpack_from('<II', raw, 12)
            self.assertEqual((width, height), dimensions)
        trait = children(read('common/country_leader/WFL_iran_traits.txt')[0])[0]
        self.assertEqual(field(trait, 'political_power_factor'), '0.05')
        self.assertEqual(field(trait, 'stability_factor'), '0.05')
        for language in ('german', 'english'):
            raw = (ROOT / f'localisation/{language}/WFL_iran_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            source = raw.decode('utf-8-sig')
            self.assertIn(f' {SHAH}:0 "Al Höhne"', source)
            for focus_id in FOCI:
                self.assertIn(f' {focus_id}:0 "', source)
                self.assertIn(f' {focus_id}_desc:0 "', source)


if __name__ == '__main__':
    unittest.main()
