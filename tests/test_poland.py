"""Country-scoped startup for Poland's user-named neutral king."""
from pathlib import Path
from dataclasses import dataclass
import struct
import unittest

from tests.test_expansion_safety import Country, ScopeFixture
from tools.validate_mod import children, field, parse, walk

ROOT = Path(__file__).resolve().parents[1]
KING = 'WFL_POL_kevin_von_beverungen_i'
INITIALIZED = 'WFL_POL_kevin_initialized'
KING_TRAIT = 'WFL_POL_pragmatischer_koenig'


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8-sig'))


def block(node, key):
    return next(n for n in children(node) if n.key == key)


@dataclass
class RuntimeCharacter:
    identity: str
    name: str
    owner: str
    traits: set[str]


class PolishStartupWorld(ScopeFixture):
    def __init__(self):
        super().__init__()
        self.countries['POL'] = Country('POL')
        for country in self.countries.values():
            country.exists = True
        self.created = {tag: [] for tag in self.countries}
        self.characters = {tag: [] for tag in self.countries}
        self.character_data = {}
        self.portraits = {}
        self.leaders = {'WFL': 'WFL_schuetzenkoenig', 'POL': 'POL_ignacy_moscicki'}
        self.politics = {'POL': {'ruling_party': 'neutrality', 'elections_allowed': 'no'}}

    def conditions(self, nodes, stack):
        for node in nodes:
            if node.key == 'exists':
                valid = stack[-1].exists == (node.value == 'yes')
            elif node.key == 'has_trait':
                assert isinstance(stack[-1], RuntimeCharacter)
                valid = node.value in stack[-1].traits
            else:
                valid = super().conditions([node], stack)
            if not valid:
                return False
        return True

    def effects(self, nodes, stack=None):
        stack = stack or [self.root]
        for node in nodes:
            current = stack[-1]
            tag = current.owner if isinstance(current, RuntimeCharacter) else current.tag
            if node.key in self.countries:
                self.effects(children(node), stack + [self.countries[node.key]])
            elif node.key == 'create_country_leader':
                # Display-name tokens do not identify newly created runtime
                # instances; the actual engine exposed that old assumption.
                identity = f'runtime-{tag}-{len(self.created[tag]) + 731}'
                self.created[tag].append(identity)
                self.characters[tag].append(identity)
                self.character_data[identity] = RuntimeCharacter(
                    identity, field(node, 'name'), tag,
                    {n.key for n in children(block(node, 'traits'))})
            elif node.key == 'every_character':
                for identity in self.characters[tag]:
                    character = self.character_data[identity]
                    if self.conditions(children(block(node, 'limit')), stack + [character]):
                        self.effects([n for n in children(node)
                                      if n.key != 'limit'], stack + [character])
            elif node.key == 'set_portraits':
                assert isinstance(current, RuntimeCharacter), 'requires actual character scope'
                assert field(node, 'character') is None, 'a name token is not a character ID'
                self.portraits[current.identity] = {
                    n.key: n.value for n in children(block(node, 'civilian'))}
            elif node.key == 'promote_character':
                assert isinstance(current, RuntimeCharacter), 'requires actual character scope'
                assert node.value == 'yes'
                self.leaders[tag] = current.identity
            elif node.key == 'set_politics':
                self.politics[tag] = {n.key: n.value for n in children(node)}
            else:
                super().effects([node], stack)


class PolishKingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.character = children(read('common/characters/WFL_poland.txt')[0])[0]
        actions = read('common/on_actions/zz_WFL_poland.txt')[0]
        cls.startup = children(block(block(actions, 'on_startup'), 'effect'))

    def test_startup_selects_a_neutral_king_in_poland_once_and_leaves_other_countries_alone(self):
        self.assertEqual([n.key for n in self.startup], ['POL'])
        world = PolishStartupWorld()
        world.effects(self.startup)
        self.assertEqual(len(world.created['POL']), 1)
        identity = world.created['POL'][0]
        self.assertNotEqual(identity, KING)
        self.assertEqual(world.character_data[identity].name, KING)
        self.assertEqual(world.leaders['POL'], identity)
        self.assertEqual(world.politics['POL'], {'ruling_party': 'neutrality', 'elections_allowed': 'no'})
        self.assertIn(INITIALIZED, world.countries['POL'].flags)
        self.assertEqual(world.leaders['WFL'], 'WFL_schuetzenkoenig')
        self.assertTrue(all(not created for tag, created in world.created.items() if tag != 'POL'))
        self.assertEqual(world.portraits[identity], {
            'large': 'GFX_portrait_WFL_POL_kevin_von_beverungen_i',
            'small': 'GFX_portrait_WFL_POL_kevin_von_beverungen_i_small'})
        # Re-running a startup must not undo a legitimate later government change.
        world.leaders['POL'] = 'later_polish_leader'
        world.politics['POL']['ruling_party'] = 'democratic'
        world.effects(self.startup)
        self.assertEqual(world.created['POL'], [identity])
        self.assertEqual(world.leaders['POL'], 'later_polish_leader')
        self.assertEqual(world.politics['POL']['ruling_party'], 'democratic')

    def test_absent_poland_is_skipped_and_no_vanilla_history_is_overridden(self):
        world = PolishStartupWorld()
        world.countries['POL'].exists = False
        world.effects(self.startup)
        self.assertEqual(world.created['POL'], [])
        self.assertNotIn(INITIALIZED, world.countries['POL'].flags)
        self.assertEqual(world.leaders['POL'], 'POL_ignacy_moscicki')
        self.assertFalse((ROOT / 'history/countries/POL - Poland.txt').exists())
        self.assertEqual({n.key for n in children(self.character)}, {'name', 'portraits', 'country_leader'})
        role = block(self.character, 'country_leader')
        self.assertEqual(field(role, 'ideology'), 'despotism')
        traits = {t.key: t for t in children(read('common/country_leader/WFL_poland_traits.txt')[0])}
        selected = {n.key for n in children(block(role, 'traits'))}
        self.assertEqual(selected, set(traits))
        effects = {n.key: n.value for t in traits.values() for n in children(t) if n.key != 'random'}
        self.assertEqual(effects, {'political_power_factor': '0.05', 'stability_factor': '0.05'})

    def test_runtime_creation_keeps_the_declared_role_and_avoids_history_only_recruitment(self):
        self.assertFalse(any(n.key == 'recruit_character' for n in walk(self.startup)))
        creation = next(n for n in walk(self.startup) if n.key == 'create_country_leader')
        declared = block(self.character, 'country_leader')
        self.assertEqual(field(creation, 'name'), KING)
        self.assertEqual(field(creation, 'picture'), 'GFX_portrait_WFL_POL_kevin_von_beverungen_i')
        for key in ('ideology', 'traits', 'expire'):
            self.assertEqual(block(creation, key).value, block(declared, key).value)
        selection = next(n for n in walk(self.startup) if n.key == 'every_character')
        self.assertEqual(field(block(selection, 'limit'), 'has_trait'), KING_TRAIT)
        # The shipped engine rejects this option in every_character despite
        # the generated docs showing a copied every_unit_leader example.
        self.assertIsNone(field(selection, 'include_invisible'))
        self.assertEqual(field(selection, 'promote_character'), 'yes')
        self.assertIsNone(field(block(selection, 'set_portraits'), 'character'))

    def test_supplied_royal_portrait_and_confirmed_name_are_connected(self):
        sprites = {field(n, 'name'): field(n, 'texturefile')
                   for n in walk(read('interface/WFL_poland.gfx')) if n.key == 'spriteType'}
        civilian = block(block(self.character, 'portraits'), 'civilian')
        for size, dimensions in [('large', (156, 210)), ('small', (65, 67))]:
            texture = sprites[field(civilian, size)]
            self.assertTrue(texture.startswith('gfx/leaders/POL/Portrait_POL_kevin_'))
            raw = (ROOT / texture).read_bytes()
            self.assertEqual(raw[:4], b'DDS ')
            height, width = struct.unpack_from('<II', raw, 12)
            self.assertEqual((width, height), dimensions)
        for language in ('german', 'english'):
            raw = (ROOT / f'localisation/{language}/WFL_poland_l_{language}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertIn(f' {KING}:0 "Kevin von Beverungen I."', raw.decode('utf-8-sig'))


if __name__ == '__main__':
    unittest.main()
