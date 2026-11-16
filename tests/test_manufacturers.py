"""Manufacturer inventory, DLC/progression behavior and local Vanilla parity."""

from collections import Counter, defaultdict
import os
from pathlib import Path
import re
import unittest

from tools.validate_mod import children, field, parse, walk


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = Path(os.environ.get(
    'HOI4_GAME_ROOT',
    r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV',
))
SECTIONS = {
    'tank_manufacturer': 12,
    'naval_manufacturer': 12,
    'aircraft_manufacturer': 15,
    'materiel_manufacturer': 10,
    'industrial_concern': 18,
}
EXTRA_LEGACY = {
    'CZE_skoda_works_german_manufacturer',
    'CZE_bohmische_mahrische_maschinenfabrik_ag_german_manufacturer',
    'CZE_zlin_aircraft',
    'CZE_ceska_zbrojovka_uhersky_brod',
    'CZE_anglo_czechoslovak_bank',
}
EXTRA_MIOS = {
    'CZE_skoda_works_german_organization',
    'CZE_bohmische_mahrische_maschinenfabrik_ag_german_organization',
    'CZE_avia_german_organization',
    'CZE_ceska_zbrojovka_uhersky_brod_organization',
}
BASE_MIOS = {
    'porsche', 'henschel', 'man', 'alkett', 'daimler_benz',
    'deschimag', 'germaniawerft', 'blohm_und_voss', 'hdw', 'deutsche_werke',
    'kriegsmarinewerft_wilhelmshaven', 'messerschmitt', 'junkers', 'focke_wulf',
    'heinkel', 'dornier', 'arado_flugzeugwerke', 'fieseler', 'focke_achgelis',
    'rheinmetall', 'mauser', 'opel', 'carl_walther', 'auto_union', 'henschel_kassel',
}
ALL_DLCS = {
    'Arms Against Tyranny', 'La Resistance', 'Gotterdammerung',
    'Peace For Our Time',
}


def block(node, key):
    matches = [part for part in children(node) if part.key == key]
    if len(matches) != 1:
        raise AssertionError(f'Expected one {key} in {node.key}, found {len(matches)}')
    return matches[0]


def canonical(node):
    return node.key, (tuple(canonical(n) for n in children(node))
                      if isinstance(node.value, list) else node.value)


def suffix(key):
    return (key[4:] if key.startswith('GER_') else key).lower()


def classic_profiles(nodes):
    return {
        item.key: (section.key, item)
        for group in nodes if group.key == 'ideas'
        for section in children(group) if section.key in SECTIONS
        for item in children(section) if isinstance(item.value, list)
    }


def matches(nodes, tag='WFL', dlcs=frozenset(), focuses=frozenset()):
    """Small, strict evaluator of the actual country-level offering conditions."""
    previous_if = None
    for node in nodes:
        if node.key == 'NOT':
            value = not matches(children(node), tag, dlcs, focuses)
        elif node.key == 'OR':
            value = any(matches([part], tag, dlcs, focuses) for part in children(node))
        elif node.key in ('AND', 'ROOT'):
            value = matches(children(node), tag, dlcs, focuses)
        elif node.key in ('original_tag', 'tag'):
            value = tag == node.value
        elif node.key == 'has_dlc':
            value = node.value in dlcs
        elif node.key == 'has_completed_focus':
            value = node.value in focuses
        elif node.key == 'has_war_with':
            value = False
        elif node.key == 'always':
            value = node.value == 'yes'
        elif node.key == 'if':
            condition = block(node, 'limit')
            previous_if = matches(children(condition), tag, dlcs, focuses)
            value = (not previous_if or matches(
                [part for part in children(node) if part.key != 'limit'],
                tag, dlcs, focuses,
            ))
        elif node.key == 'else':
            value = previous_if is not False or matches(children(node), tag, dlcs, focuses)
        else:
            raise AssertionError(f'Unsupported condition in manufacturer fixture: {node.key}')
        if not value:
            return False
    return True


class ManufacturerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ideas = classic_profiles(parse(
            (ROOT / 'common/ideas/WFL_manufacturers.txt').read_text(encoding='utf-8-sig')
        ))
        cls.mios = parse((ROOT / (
            'common/military_industrial_organization/organizations/WFL_organization.txt'
        )).read_text(encoding='utf-8-sig'))

    def test_complete_inventory_has_independent_wfl_ids(self):
        self.assertEqual(len(self.ideas), 67)
        self.assertEqual(Counter(section for section, _ in self.ideas.values()), SECTIONS)
        self.assertTrue(all(key.startswith('WFL_mfr_') for key in self.ideas))
        self.assertEqual(len(self.mios), 29)
        expected = {f'GER_{company}_organization' for company in BASE_MIOS} | EXTRA_MIOS
        self.assertEqual({field(node, 'include') for node in self.mios}, expected)
        self.assertEqual(len({node.key for node in self.mios}), 29)
        self.assertTrue(all(node.key.startswith('WFL_mio_') for node in self.mios))

    def test_dlc_modes_do_not_offer_both_designer_systems(self):
        for key, (section, idea) in self.ideas.items():
            allowed = children(block(idea, 'allowed'))
            for aat in (False, True):
                dlcs = ALL_DLCS - (set() if aat else {'Arms Against Tyranny'})
                should_offer = section == 'industrial_concern' or not aat
                if key.endswith('_improved_2_no_aat'):
                    should_offer = not aat
                elif key == 'WFL_mfr_philipp_holzmann_improved_2':
                    should_offer = aat
                with self.subTest(idea=key, aat=aat):
                    self.assertEqual(matches(allowed, dlcs=dlcs), should_offer)
                    self.assertFalse(matches(allowed, tag='GER', dlcs=dlcs))
        for mio in self.mios:
            allowed = children(block(mio, 'allowed'))
            self.assertFalse(matches(allowed, dlcs=ALL_DLCS - {'Arms Against Tyranny'}))
            self.assertTrue(matches(allowed, dlcs=ALL_DLCS))
            self.assertFalse(matches(allowed, tag='GER', dlcs=ALL_DLCS))

    def test_optional_dlc_companies_stay_hidden_without_their_dlc(self):
        for mio in self.mios:
            requirements = {
                node.value for node in walk(children(block(mio, 'allowed')))
                if node.key == 'has_dlc'
            }
            for dlc in requirements:
                with self.subTest(mio=mio.key, missing_dlc=dlc):
                    self.assertFalse(matches(
                        children(block(mio, 'allowed')), dlcs=ALL_DLCS - {dlc},
                    ))
        for key, (_, idea) in self.ideas.items():
            allowed = children(block(idea, 'allowed'))
            if key.startswith('WFL_mfr_cze_'):
                self.assertFalse(matches(allowed, dlcs=ALL_DLCS - {'Peace For Our Time'}))

    def test_upgrade_profiles_never_overlap_and_remain_reachable(self):
        groups = defaultdict(list)
        for key, (section, idea) in self.ideas.items():
            base = re.sub(r'_improved(?:_2(?:_no_aat)?)?$', '', key)
            groups[(section, base)].append(idea)
        common = {'WFL_werkbank_am_niederrhein', 'WFL_gewerbehoefe'}
        stages = [set(), common, common | {'WFL_ruestungswerkstatt'},
                  common | {'WFL_technikschule'},
                  common | {'WFL_ruestungswerkstatt', 'WFL_technikschule'}]
        for aat in (False, True):
            dlcs = ALL_DLCS - (set() if aat else {'Arms Against Tyranny'})
            for (section, base), variants in groups.items():
                for stage in stages:
                    offered = []
                    for idea in variants:
                        parts = [part for part in children(idea)
                                 if part.key in ('allowed', 'visible', 'available')]
                        if all(matches(children(part), dlcs=dlcs, focuses=stage) for part in parts):
                            offered.append(idea.key)
                    with self.subTest(company=base, aat=aat, focuses=stage):
                        self.assertLessEqual(len(offered), 1, offered)
                        if stage == stages[-1] and (section == 'industrial_concern' or not aat):
                            self.assertEqual(len(offered), 1, variants)

    def test_mio_bonus_payloads_and_trait_graphs_are_not_overwritten(self):
        permitted = {'token', 'visible', 'available', 'on_complete', 'ai_will_do'}
        for mio in self.mios:
            self.assertEqual(
                {part.key for part in children(mio)} - {'override_trait'},
                {'include', 'name', 'icon', 'allowed', 'visible', 'available'},
            )
            for part in children(mio):
                if part.key == 'override_trait':
                    if (mio.key == 'WFL_mio_blohm_und_voss' and field(part, 'token') ==
                            'generic_mio_trait_high_speed_operation_stores_no_mtg'):
                        self.assertEqual({node.key for node in children(part)}, {'token', 'position'})
                        self.assertEqual(field(block(part, 'position'), 'x'), '1')
                        self.assertEqual(field(block(part, 'position'), 'y'), '0')
                    else:
                        self.assertLessEqual({node.key for node in children(part)}, permitted)

    def test_own_guards_and_callbacks_do_not_depend_on_german_state(self):
        nodes = list(walk(self.mios))
        for _, idea in self.ideas.values():
            nodes.extend(walk([idea]))
        own_mios = {mio.key for mio in self.mios}
        for node in nodes:
            if node.key in ('original_tag', 'tag'):
                self.assertEqual(node.value, 'WFL')
            if node.key == 'has_completed_focus':
                self.assertTrue(node.value.startswith('WFL_'), node)
            if node.key in ('has_country_flag', 'set_country_flag'):
                self.assertTrue(node.value.startswith('WFL_mio_'), node)
            if node.key.startswith('mio:'):
                self.assertIn(node.key[4:], own_mios)
            if node.key == 'CHARACTER':
                self.assertTrue(node.value.startswith('WFL_manufacturer_'), node)

    def test_manufacturer_scientists_keep_skills_and_use_owned_unlocks(self):
        groups = parse((ROOT / 'common/characters/WFL_manufacturer_scientists.txt')
                       .read_text(encoding='utf-8-sig'))
        scientists = {node.key: node for group in groups for node in children(group)}
        self.assertEqual(set(scientists), {
            'WFL_manufacturer_porsche_scientist', 'WFL_manufacturer_henschel_scientist',
        })
        for key, char in scientists.items():
            scientist = block(char, 'scientist')
            self.assertEqual(field(block(scientist, 'skills'), 'specialization_land'), '3')
            traits = {part.key for part in children(block(scientist, 'traits'))}
            second = ('scientist_trait_gifted_engineer' if 'porsche' in key
                      else 'scientist_trait_brilliant_theorist')
            self.assertEqual(traits, {'scientist_trait_armored_specialist', second})
            for node in walk(children(block(scientist, 'visible'))):
                if node.key == 'has_idea':
                    self.assertIn(node.value, self.ideas)
                if node.key.startswith('mio:'):
                    self.assertIn(node.key[4:], {mio.key for mio in self.mios})


@unittest.skipUnless((GAME_ROOT / 'common/ideas/GER.txt').is_file(),
                     'Local HOI4 required for source parity checks')
class InstalledVanillaParityTests(unittest.TestCase):
    def test_blohm_voss_inherited_layout_has_no_duplicate_cells(self):
        folder = GAME_ROOT / 'common/military_industrial_organization/organizations'
        organizations = {}
        for source in (folder / '00_generic_organization.txt', folder / 'GER_organization.txt',
                       ROOT / 'common/military_industrial_organization/organizations/WFL_organization.txt'):
            organizations.update({node.key: node for node in parse(source.read_text(encoding='utf-8-sig'))
                                  if isinstance(node.value, list)})

        def inherited_traits(token):
            organization = organizations[token]
            included = field(organization, 'include')
            traits = inherited_traits(included) if included else {}
            for node in children(organization):
                if node.key in ('trait', 'add_trait'):
                    traits[field(node, 'token')] = {part.key: part for part in children(node)}
                elif node.key == 'override_trait':
                    traits[field(node, 'token')].update({part.key: part for part in children(node)})
            return traits

        original = inherited_traits('GER_blohm_und_voss_organization')
        own = inherited_traits('WFL_mio_blohm_und_voss')

        def positions(traits):
            resolved = {}

            def position(token):
                if token in resolved:
                    return resolved[token]
                parts = traits[token]
                offset = parts['position']
                x, y = int(field(offset, 'x')), int(field(offset, 'y'))
                relative = parts.get('relative_position_id')
                if relative:
                    rx, ry = position(relative.value)
                    x, y = x + rx, y + ry
                resolved[token] = x, y
                return x, y

            return {token: position(token) for token, parts in traits.items() if 'position' in parts}

        corrected = 'generic_mio_trait_high_speed_operation_stores_no_mtg'
        source_positions, own_positions = positions(original), positions(own)
        self.assertEqual(source_positions[corrected], (8, 1))
        self.assertEqual(own_positions[corrected], (9, 1))
        self.assertEqual(len(set(own_positions.values())), len(own_positions))
        for token in original:
            for key in ('equipment_bonus', 'production_bonus', 'organization_modifier', 'any_parent',
                        'all_parents', 'parent', 'mutually_exclusive', 'relative_position_id'):
                self.assertEqual(
                    canonical(original[token][key]) if key in original[token] else None,
                    canonical(own[token][key]) if key in own[token] else None,
                    (token, key),
                )
        # Both DLC alternatives retain their original complementary visibility.
        for token in (corrected, 'generic_mio_trait_high_speed_operation_stores'):
            self.assertEqual(canonical(original[token]['visible']), canonical(own[token]['visible']))

    def test_every_requested_logo_exists_in_the_installed_vanilla_interface(self):
        sprites = set()
        for path in (GAME_ROOT / 'interface').rglob('*.gfx'):
            sprites.update(re.findall(
                r'\bname\s*=\s*"?(GFX_[\w.]+)',
                path.read_text(encoding='utf-8-sig'),
            ))
        ideas = classic_profiles(parse((ROOT / 'common/ideas/WFL_manufacturers.txt')
                                       .read_text(encoding='utf-8-sig')))
        requested = {'GFX_idea_' + field(node, 'picture') for _, node in ideas.values()}
        mios = parse((ROOT / (
            'common/military_industrial_organization/organizations/WFL_organization.txt'
        )).read_text(encoding='utf-8-sig'))
        requested.update(field(node, 'icon') for node in mios)
        self.assertEqual(requested - sprites, set())

    def test_all_original_research_equipment_modifiers_traits_and_costs_match(self):
        own = classic_profiles(parse((ROOT / 'common/ideas/WFL_manufacturers.txt')
                                     .read_text(encoding='utf-8-sig')))
        sources = classic_profiles(parse((GAME_ROOT / 'common/ideas/GER.txt')
                                         .read_text(encoding='utf-8-sig')))
        sources.update({key: value for key, value in classic_profiles(parse(
            (GAME_ROOT / 'common/ideas/czechoslovakia.txt').read_text(encoding='utf-8-sig')
        )).items() if key in EXTRA_LEGACY})
        self.assertEqual(len(sources), 67)
        for source_key, (section, source) in sources.items():
            key = 'WFL_mfr_' + suffix(source_key)
            with self.subTest(manufacturer=source_key):
                self.assertIn(key, own)
                self.assertEqual(own[key][0], section)
                for payload in ('research_bonus', 'equipment_bonus', 'modifier', 'traits', 'cost'):
                    original = [canonical(part) for part in children(source) if part.key == payload]
                    copied = [canonical(part) for part in children(own[key][1]) if part.key == payload]
                    self.assertEqual(copied, original, payload)
                expected_picture = field(source, 'picture') or source_key
                expected_picture = expected_picture.removeprefix('GFX_idea_')
                self.assertEqual(field(own[key][1], 'picture'), expected_picture)


if __name__ == '__main__':
    unittest.main()
