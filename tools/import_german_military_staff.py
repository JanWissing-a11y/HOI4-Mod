#!/usr/bin/env python3
"""Import Germany's military advisor profiles as independent WFL characters.

Vanilla traits remain referenced, preserving nested equipment bonuses, experience
gain and command power costs. German story locks are replaced by WFL eligibility;
DLC conditions and Fritsch's two mutually exclusive appointments are retained.
The importer never edits country history or any game-installation file.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re

try:
    from .import_german_advisors import emit
    from .validate_mod import Node, children, field, parse, walk
except ImportError:
    from import_german_advisors import emit
    from validate_mod import Node, children, field, parse, walk


SLOTS = {'army_chief', 'navy_chief', 'air_chief', 'high_command', 'theorist'}
LANGUAGES = ('german', 'english')


def military_roles(character: Node) -> list[Node]:
    """Only roles explicitly permitted for GER, including Germany/Hungary roles."""
    result = []
    for role in walk(children(character)):
        if role.key != 'advisor' or field(role, 'slot') not in SLOTS:
            continue
        allowed = next((n for n in children(role) if n.key == 'allowed'), Node('allowed'))
        if any(n.key == 'original_tag' and n.value == 'GER' for n in walk(children(allowed))):
            result.append(role)
    return result


def localisation_catalog(game: Path, language: str):
    values, paths = {}, {}
    pattern = re.compile(r'^\s*([\w.]+):\d*\s*"((?:[^"\\]|\\.)*)"', re.MULTILINE)
    for path in sorted((game / 'localisation' / language).rglob('*.yml')):
        for match in pattern.finditer(path.read_text(encoding='utf-8-sig')):
            key, value = match.groups()
            values[key], paths[key] = value, path
    return values, paths


def resolve_name(key: str, values: dict[str, str], paths: dict[str, Path], used: set[Path], stack=()) -> str:
    if key not in values or key in stack:
        raise ValueError(f'Cannot resolve vanilla character name: {key}')
    used.add(paths[key])
    text = re.sub(r'\$([\w.]+)\$', lambda m: resolve_name(m[1], values, paths, used, (*stack, key)), values[key])
    if '$' in text:
        raise ValueError(f'Unresolved dynamic name: {key}')
    return text.replace(r'\"', '"')


def recruitment_block(manifest: dict) -> str:
    return ('# BEGIN WFL MILITARY STAFF\n'
            '# Available for normal paid hiring; no military advisors are hired for free.\n'
            + ''.join(f'recruit_character = {item["id"]}\n' for item in manifest['staff'])
            + '# END WFL MILITARY STAFF\n')


def build(root: Path, game: Path) -> dict:
    source_character_paths = [game / f'common/characters/{tag}.txt' for tag in ('GER', 'AUS')]
    source_traits = game / 'common/country_leader/00_traits.txt'
    source_defines = game / 'common/defines/00_defines.lua'
    used_sources = {*source_character_paths, source_traits, source_defines}
    characters = [(c, p) for p in source_character_paths
                  for c in children(parse(p.read_text(encoding='utf-8-sig'))[0])]
    traits = {n.key: n for g in parse(source_traits.read_text(encoding='utf-8-sig'))
              if g.key == 'leader_traits' for n in children(g)}
    default_match = re.search(r'DEFAULT_PP_COST_FOR_MILITARY_ADVISOR\s*=\s*(\d+)',
                              source_defines.read_text(encoding='utf-8-sig'))
    if not default_match:
        raise ValueError('Missing vanilla military advisor default price')
    default_cost = default_match[1]
    catalogs = {lang: localisation_catalog(game, lang) for lang in LANGUAGES}
    localized = {lang: {} for lang in LANGUAGES}
    selected = [(c, military_roles(c), p) for c, p in characters if military_roles(c)]
    if len(selected) != 36 or sum(len(roles) for _, roles, _ in selected) != 37:
        raise ValueError('German military staff catalog changed; review before importing')
    manifest = {'source_version': json.loads((game / 'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
                'scope': 'Military advisor roles explicitly allowed for GER, including two Austrian profiles in AUS.txt; FIN-only Falkenhorst is excluded.',
                'default_military_advisor_cost': int(default_cost), 'staff': []}
    output = ['# German military advisor profiles; independent WFL characters with supplied photos.\ncharacters = {\n']
    photos = [i for i in range(1, 19) if i != 12]
    imported_ids = set()
    for index, (character, roles, source_path) in enumerate(selected):
        own_id = 'WFL_staff_' + character.key.split('_', 1)[1]
        if own_id in imported_ids:
            raise ValueError(f'Imported military staff ID collision: {own_id}')
        imported_ids.add(own_id)
        photo = f'{photos[index % len(photos)]:02}'
        portrait_roles = [Node(role, [Node('large', f'GFX_portrait_WFL_advisor_{photo}'),
                                     Node('small', f'GFX_portrait_WFL_advisor_{photo}_small')])
                          for role in ('army', 'civilian')]
        own_character = Node(own_id, [Node('name', own_id), Node('portraits', portrait_roles)])
        names = {}
        for language in LANGUAGES:
            values, name_paths = catalogs[language]
            names[language] = resolve_name(field(character, 'name') or character.key,
                                           values, name_paths, used_sources)
            localized[language][own_id] = names[language]
        record = {'id': own_id, 'source_character': character.key,
                  'source_file': source_path.relative_to(game).as_posix(), 'names': names,
                  'portrait': photo, 'roles': []}
        for source_role in roles:
            unknown = {n.key for n in children(source_role)} - {
                'slot', 'idea_token', 'ledger', 'cost', 'traits', 'allowed', 'visible', 'available', 'ai_will_do'}
            if unknown:
                raise ValueError(f'Review new advisor fields for {character.key}: {unknown}')
            slot = field(source_role, 'slot')
            token = own_id + '_' + slot if len(roles) > 1 else own_id
            source_trait_ids = [n.key for n in children(next(n for n in children(source_role) if n.key == 'traits'))]
            # Fail if a future trait gains a country/event hook: original traits
            # must remain safe to use on another country without global edits.
            for trait_id in source_trait_ids:
                definition = traits[trait_id]
                if any(n.key in {'on_add', 'on_remove', 'on_activate', 'on_deactivate'}
                       or (isinstance(n.value, str) and re.match(r'^(GER|FIN|HUN)\b', n.value))
                       for n in walk(children(definition))):
                    raise ValueError(f'Review country-sensitive military trait: {trait_id}')
            allowed_source = next(n for n in children(source_role) if n.key == 'allowed')
            instance_gates = [n for instance in children(character) if instance.key == 'instance'
                              and any(n is source_role for n in children(instance))
                              for n in children(instance) if n.key == 'allowed']
            # Beyer's GER-permitted role exists only in the positive DLC
            # instance. Carry that gate onto the independent WFL advisor role.
            # His negative-DLC instance is AUS-only and is excluded above.
            gates = [allowed_source, *instance_gates]
            if any(n.key == 'NOT' for gate in gates for n in walk(children(gate))):
                raise ValueError(f'Review negated advisor DLC condition: {character.key}')
            if any(n.key != 'has_dlc' for gate in instance_gates for n in children(gate)):
                raise ValueError(f'Review complex military instance condition: {character.key}')
            dlc_names = sorted({n.value for gate in gates for n in walk(children(gate)) if n.key == 'has_dlc'})
            allowed = Node('allowed', [Node('original_tag', 'WFL'), *[Node('has_dlc', dlc) for dlc in dlc_names]])
            own_role = Node('advisor', [Node('slot', slot), Node('idea_token', token), allowed])
            ledger = field(source_role, 'ledger')
            if ledger:
                own_role.value.append(Node('ledger', ledger))
            cost = field(source_role, 'cost') or default_cost
            own_role.value.extend([Node('cost', cost), Node('traits', [Node(t) for t in source_trait_ids])])
            if len(roles) > 1:
                # One person cannot occupy both of Fritsch's appointments.
                own_role.value.append(Node('available', [Node('not_already_hired_except_as', slot)]))
            own_role.value.append(Node('ai_will_do', [Node('factor', '1')]))
            own_character.value.append(own_role)
            for language in LANGUAGES:
                localized[language][token] = names[language]
            record['roles'].append({'slot': slot, 'idea_token': token,
                                    'source_idea_token': field(source_role, 'idea_token'),
                                    'ledger': ledger, 'base_cost': int(cost),
                                    'traits': source_trait_ids, 'required_dlc': dlc_names,
                                    'trait_definitions': {t: asdict(traits[t]) for t in source_trait_ids}})
        output.append(emit(own_character, 1))
        manifest['staff'].append(record)
    output.append('}\n')
    manifest['role_counts'] = dict(sorted(Counter(r['slot'] for s in manifest['staff'] for r in s['roles']).items()))
    manifest['sources'] = {p.relative_to(game).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(used_sources)}
    # No history side effect: the caller integrates recruitment after concurrent
    # commander edits are finished. This makes regeneration safe and reviewable.
    (root / 'common/characters').mkdir(parents=True, exist_ok=True)
    (root / 'common/characters/WFL_military_staff.txt').write_text(''.join(output), encoding='utf-8')
    for language, entries in localized.items():
        path = root / f'localisation/{language}/WFL_military_staff_l_{language}.yml'
        path.parent.mkdir(parents=True, exist_ok=True)
        text = f'l_{language}:\n' + ''.join(f' {key}:0 {json.dumps(value, ensure_ascii=False)}\n' for key, value in entries.items())
        path.write_text(text, encoding='utf-8-sig')
    (root / 'tools/data').mkdir(parents=True, exist_ok=True)
    (root / 'tools/data/WFL_military_staff.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    manifest = build(args.root, args.game_root)
    print(f'Imported {len(manifest["staff"])} military staff with {sum(manifest["role_counts"].values())} roles.')
    print(recruitment_block(manifest))


if __name__ == '__main__':
    main()
