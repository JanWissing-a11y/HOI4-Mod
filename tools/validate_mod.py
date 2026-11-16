#!/usr/bin/env python3
"""Statische Prüfung eigener Mod-Dateien; kein Ersatz für die HOI4-Engine."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
import hashlib
from pathlib import Path
import re
import struct


class ParseError(ValueError):
    pass


@dataclass
class Node:
    key: str
    value: str | list[Node] | None = None


@dataclass
class Result:
    errors: list[str]
    counts: dict[str, int]


WFL_IDENTITIES = ('WFL', 'WFL_KINGDOM', 'WFL_GREATER_REICH')
FLAG_SUFFIXES = ('', '_democratic', '_neutrality', '_fascism', '_communism')


TOKEN = re.compile(
    r'(?P<space>\s+)|(?P<comment>\#[^\n]*)|'
    r'(?P<string>"(?:[^"\\]|\\.)*")|(?P<brace>[{}])|'
    r'(?P<operator>\?=|<=|>=|!=|=|<|>)|(?P<word>[^\s{}"=<>!?#]+)'
)


def parse(text: str) -> list[Node]:
    """Parse assignments, lists and nested blocks used by this project."""
    tokens: list[tuple[str, str]] = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if match is None:
            line = text.count('\n', 0, position) + 1
            raise ParseError(f'invalid token or unterminated string at line {line}')
        kind = match.lastgroup
        value = match.group()
        if kind not in ('space', 'comment'):
            tokens.append((kind, value[1:-1] if kind == 'string' else value))
        position = match.end()

    index = 0

    def block(nested: bool = False) -> list[Node]:
        nonlocal index
        nodes: list[Node] = []
        while index < len(tokens):
            kind, key = tokens[index]
            if kind == 'brace' and key == '}':
                if not nested:
                    raise ParseError('unexpected closing brace')
                index += 1
                return nodes
            if kind not in ('word', 'string'):
                raise ParseError(f'expected key or list item, got {key!r}')
            index += 1
            value = None
            if index < len(tokens) and tokens[index][0] == 'operator':
                index += 1
                if index == len(tokens):
                    raise ParseError(f'missing value for {key}')
                value_kind, value_text = tokens[index]
                index += 1
                if value_kind == 'brace' and value_text == '{':
                    value = block(nested=True)
                elif value_kind in ('word', 'string'):
                    value = value_text
                    if (value_kind == 'word' and value_text.lower() in ('rgb', 'hsv', 'hsv360')
                            and index < len(tokens) and tokens[index] == ('brace', '{')):
                        index += 1
                        value = [Node(value_text, block(nested=True))]
                else:
                    raise ParseError(f'invalid value for {key}')
            nodes.append(Node(key, value))
        if nested:
            raise ParseError('unclosed block')
        return nodes

    return block()


def children(node: Node) -> list[Node]:
    return node.value if isinstance(node.value, list) else []


def field(node: Node, key: str) -> str | None:
    return next((n.value for n in children(node) if n.key == key and isinstance(n.value, str)), None)


def walk(nodes: list[Node]):
    for node in nodes:
        yield node
        yield from walk(children(node))


def validate(root: Path, game_root: Path | None = None) -> Result:
    errors: list[str] = []
    documents: dict[Path, list[Node]] = {}
    registries: dict[str, dict[str, Node]] = {
        kind: {} for kind in ('tag', 'character', 'trait', 'sprite', 'idea', 'focus', 'event', 'category', 'decision')
    }
    required_text: set[str] = set()
    # Explicit names prevent cosmetic tags from inheriting a vanilla ideology name.
    required_text.update(tag + ideology + suffix
                         for tag in WFL_IDENTITIES for ideology in FLAG_SUFFIXES
                         for suffix in ('', '_DEF', '_ADJ'))
    opinion_modifiers: set[str] = set()

    def problem(path: Path, message: str):
        errors.append(f'{path.relative_to(root).as_posix()}: {message}')

    def register(kind: str, key: str | None, node: Node, path: Path, description: bool = True):
        if not key:
            problem(path, f'missing {kind} ID')
            return
        if key in registries[kind]:
            problem(path, f'duplicate {kind} ID: {key}')
        registries[kind][key] = node
        if description:
            required_text.update((key, key + '_desc'))

    paths = [root / 'descriptor.mod']
    for folder in ('common', 'events', 'history', 'portraits'):
        paths.extend(sorted((root / folder).rglob('*.txt')))
    paths.extend(sorted((root / 'interface').rglob('*.gfx')))
    paths.extend(sorted((root / 'interface').rglob('*.gui')))
    for path in paths:
        try:
            documents[path] = parse(path.read_text(encoding='utf-8-sig'))
        except (OSError, UnicodeError, ParseError) as exc:
            problem(path, str(exc))

    descriptor = Node('descriptor', documents.get(root / 'descriptor.mod', []))
    if not field(descriptor, 'name') or not field(descriptor, 'version'):
        errors.append('descriptor.mod: name and version are required')
    if any(n.key == 'replace_path' for n in children(descriptor)):
        errors.append('descriptor.mod: broad replace_path is not permitted by this project')

    for path, nodes in documents.items():
        relative = path.relative_to(root).as_posix()
        if relative.startswith('common/country_tags/'):
            for node in nodes:
                register('tag', node.key, node, path, description=False)
                required_text.update((node.key, node.key + '_DEF', node.key + '_ADJ'))
                if not isinstance(node.value, str) or not (root / 'common' / node.value).is_file():
                    problem(path, f'missing country definition for {node.key}')
        elif relative.startswith('common/characters/'):
            for group in nodes:
                if group.key == 'characters':
                    for node in children(group):
                        register('character', node.key, node, path, description=False)
                        required_text.add(field(node, 'name') or node.key)
        elif relative.startswith('common/country_leader/'):
            for group in nodes:
                if group.key == 'leader_traits':
                    for node in children(group):
                        register('trait', node.key, node, path)
        elif relative.startswith('common/ideas/'):
            for group in nodes:
                for section in children(group):
                    if group.key == 'ideas' and section.key in (
                            'country', 'hidden_ideas', 'tank_manufacturer', 'naval_manufacturer',
                            'aircraft_manufacturer', 'materiel_manufacturer', 'industrial_concern'):
                        for node in children(section):
                            # Section metadata such as designer = yes is not an
                            # idea ID and must not require localisation.
                            if isinstance(node.value, list):
                                register('idea', node.key, node, path)
        elif relative.startswith('common/national_focus/'):
            for tree in nodes:
                if tree.key != 'focus_tree':
                    continue
                binding = next((n for n in children(tree) if n.key == 'country'), Node('country'))
                if not any(n.key == 'tag' and n.value == 'WFL' for n in walk(children(binding))):
                    problem(path, 'focus tree must be bound to WFL')
                for node in children(tree):
                    if node.key == 'focus':
                        register('focus', field(node, 'id'), node, path)
        elif relative.startswith('events/'):
            for node in nodes:
                if node.key in ('country_event', 'news_event'):
                    register('event', field(node, 'id'), node, path, description=False)
                    for part in walk(children(node)):
                        if part.key in ('title', 'desc', 'name', 'text') and isinstance(part.value, str):
                            required_text.add(part.value)
        elif relative.startswith('common/opinion_modifiers/'):
            for group in nodes:
                if group.key == 'opinion_modifiers':
                    for node in children(group):
                        if node.key in opinion_modifiers:
                            problem(path, f'duplicate opinion modifier: {node.key}')
                        opinion_modifiers.add(node.key)
                        required_text.add(node.key)
        elif relative.startswith('common/decisions/categories/'):
            for node in nodes:
                register('category', node.key, node, path)
        elif relative.startswith('common/decisions/'):
            for category in nodes:
                for node in children(category):
                    register('decision', node.key, node, path)
        elif relative.startswith('interface/'):
            for node in walk(nodes):
                if node.key == 'spriteType' and isinstance(node.value, list):
                    register('sprite', field(node, 'name'), node, path, description=False)

    gui_windows = {}
    scripted_texts = set()
    inlays = {}
    scripted_guis = {}
    for path, nodes in documents.items():
        relative = path.relative_to(root).as_posix()
        if relative.startswith('interface/') and path.suffix == '.gui':
            for node in walk(nodes):
                if node.key == 'containerWindowType' and field(node, 'name'):
                    gui_windows[field(node, 'name')] = node
        if relative.startswith('common/scripted_localisation/'):
            scripted_texts.update(field(node, 'name') for node in nodes if node.key == 'defined_text')
        if relative.startswith('common/focus_inlay_windows/'):
            inlays.update((node.key, (node, path)) for node in nodes)
        if relative.startswith('common/scripted_guis/'):
            for group in nodes:
                if group.key == 'scripted_gui':
                    scripted_guis.update((node.key, (node, path)) for node in children(group))
    for key, (definition, path) in scripted_guis.items():
        if field(definition, 'window_name') not in gui_windows:
            problem(path, f'scripted GUI has unknown window: {key}')
    for key, category in registries['category'].items():
        binding = field(category, 'scripted_gui')
        if binding and binding.startswith('WFL_') and binding not in scripted_guis:
            errors.append(f'decision category {key}: unknown scripted GUI: {binding}')
    for inlay_id, (inlay, path) in inlays.items():
        window = gui_windows.get(field(inlay, 'window_name'))
        if window is None:
            problem(path, f'inlay has unknown GUI window: {inlay_id}')
            continue
        components = {field(node, 'name') for node in walk(children(window)) if isinstance(node.value, list)}
        for group in children(inlay):
            if group.key in ('scripted_images', 'scripted_buttons', 'scripted_progressbars'):
                for component in children(group):
                    if component.key not in components:
                        problem(path, f'inlay has unknown GUI component: {component.key}')
    for path, nodes in documents.items():
        for node in walk(nodes):
            if node.key == 'inlay_window':
                key = field(node, 'id')
                if key and key.startswith('WFL_') and key not in inlays:
                    problem(path, f'unknown focus inlay: {key}')
            if path.suffix == '.gui' and node.key in ('text', 'context_aware_text', 'context_aware_tooltip', 'pdx_tooltip') and isinstance(node.value, str):
                if node.value.startswith('WFL_'):
                    required_text.add(node.value)
                for key in re.findall(r'\[(WFL\w+)\]', node.value):
                    if key not in scripted_texts:
                        problem(path, f'unknown scripted UI text: {key}')
            if node.key in ('spriteType', 'quadTextureSprite', 'picture') and isinstance(node.value, str) and node.value.startswith(('GFX_WFL_', 'GFX_focus_WFL_')):
                if node.value not in registries['sprite']:
                    problem(path, f'unknown GUI sprite: {node.value}')
            if path.parent.name == 'focus_inlay_windows' and node.key.startswith(('GFX_WFL_', 'GFX_focus_WFL_')) and node.key not in registries['sprite']:
                problem(path, f'unknown inlay sprite: {node.key}')

    reference_fields = {
        'focus': 'focus', 'has_completed_focus': 'focus',
        'complete_national_focus': 'focus', 'uncomplete_national_focus': 'focus',
        'recruit_character': 'character', 'retire_character': 'character',
        'promote_character': 'character',
        'traits': 'trait', 'has_trait': 'trait',
        'add_country_leader_trait': 'trait', 'remove_country_leader_trait': 'trait',
        'add_ideas': 'idea', 'remove_ideas': 'idea', 'has_idea': 'idea',
    }
    portrait_references: dict[str, set[Path]] = {}
    for path, nodes in documents.items():
        is_portrait_pool = path.relative_to(root).parts[0] == 'portraits'
        for node in walk(nodes):
            if node.key == 'recruit_character' and path.relative_to(root).parts[0] != 'history':
                problem(path, 'recruit_character is restricted to history files; use a runtime character effect')
            kind = reference_fields.get(node.key)
            if kind:
                references = [node.value] if isinstance(node.value, str) else [n.key for n in children(node)]
                for key in references:
                    if key.startswith('WFL_') and key not in registries[kind]:
                        problem(path, f'unknown {kind} reference: {key}')
            if node.key in ('country_event', 'news_event') and isinstance(node.value, list):
                key = field(node, 'id')
                if key and key.lower().startswith(('wfl.', 'wfl_')) and key not in registries['event']:
                    problem(path, f'unknown event reference: {key}')
            if node.key == 'add_opinion_modifier' and isinstance(node.value, list):
                key = field(node, 'modifier')
                if key and key.startswith('WFL_') and key not in opinion_modifiers:
                    problem(path, f'unknown opinion modifier: {key}')
            if node.key == 'texturefile' and isinstance(node.value, str):
                asset = node.value.replace('\\', '/')
                if not ((root / asset).is_file() or (game_root and (game_root / asset).is_file())):
                    problem(path, f'missing referenced texture asset: {asset}')
            if is_portrait_pool:
                sprite = node.key if node.value is None else node.value
                if isinstance(sprite, str) and sprite.startswith('GFX_'):
                    portrait_references.setdefault(sprite, set()).add(path)
            elif node.key in ('large', 'small') and isinstance(node.value, str):
                if node.value.startswith('GFX_') and '_wfl_' in node.value.lower():
                    portrait_references.setdefault(node.value, set()).add(path)
        if path.relative_to(root).parent == Path('common/decisions'):
            for node in nodes:
                if node.key not in registries['category']:
                    problem(path, f'unknown decision category: {node.key}')

    unresolved = set(portrait_references) - set(registries['sprite'])
    if game_root and unresolved:
        # Only inspect vanilla files which mention an unresolved reference.
        # Other vanilla interface dialects need not be accepted by this parser.
        for path in sorted((game_root / 'interface').rglob('*.gfx')):
            try:
                source = path.read_text(encoding='utf-8-sig')
                if not any(sprite in source for sprite in unresolved):
                    continue
                names = {field(node, 'name') for node in walk(parse(source)) if node.key == 'spriteType'}
                unresolved -= names
                if not unresolved:
                    break
            except (OSError, UnicodeError, ParseError) as exc:
                errors.append(f'vanilla interface/{path.name}: cannot resolve portrait sprites: {exc}')
    for sprite in sorted(unresolved):
        for path in sorted(portrait_references[sprite]):
            problem(path, f'unknown portrait sprite reference: {sprite}')

    edges: dict[str, set[str]] = {}
    exclusions: dict[str, set[str]] = {}
    positions: dict[tuple[int, int], str] = {}
    for key, node in registries['focus'].items():
        edges[key] = {n.value for group in children(node) if group.key == 'prerequisite'
                      for n in children(group) if n.key == 'focus' and isinstance(n.value, str)}
        exclusions[key] = {n.value for group in children(node) if group.key == 'mutually_exclusive'
                           for n in children(group) if n.key == 'focus' and isinstance(n.value, str)}
        if field(node, 'relative_position_id') is None:
            try:
                position = (int(field(node, 'x')), int(field(node, 'y')))
            except (TypeError, ValueError):
                errors.append(f'focus requires integer coordinates: {key}')
                continue
            if position in positions:
                errors.append(f'overlapping focus positions: {positions[position]} / {key}')
            positions[position] = key
            for parent in edges[key]:
                other = registries['focus'].get(parent)
                if other is not None and field(other, 'relative_position_id') is None:
                    try:
                        if int(field(other, 'y')) >= position[1]:
                            errors.append(f'focus prerequisite must be above child: {parent} / {key}')
                    except (TypeError, ValueError):
                        pass  # Invalid coordinates are reported for that focus.
    active: set[str] = set()
    completed: set[str] = set()

    def visit(key: str):
        if key in active:
            errors.append(f'focus prerequisite cycle at {key}')
            return
        if key in completed:
            return
        active.add(key)
        for parent in edges.get(key, set()):
            visit(parent)
        active.remove(key)
        completed.add(key)

    for key in edges:
        visit(key)
        if key in exclusions[key]:
            errors.append(f'focus excludes itself: {key}')
        for other in exclusions[key]:
            if key not in exclusions.get(other, set()):
                errors.append(f'asymmetric focus exclusion: {key} / {other}')

    for language in ('german', 'english'):
        localized: set[str] = set()
        for path in sorted((root / 'localisation' / language).glob('*.yml')):
            try:
                raw = path.read_bytes()
                if not raw.startswith(b'\xef\xbb\xbf'):
                    problem(path, 'localisation requires UTF-8 BOM')
                lines = raw.decode('utf-8-sig').splitlines()
                if not path.name.endswith(f'_l_{language}.yml'):
                    problem(path, 'wrong localisation filename suffix')
                if not lines or lines[0] != f'l_{language}:':
                    problem(path, 'wrong localisation header')
                for line in lines[1:]:
                    if not line.strip() or line.lstrip().startswith('#'):
                        continue
                    match = re.fullmatch(r'\s+([\w.\-]+):\d*\s+"(?:[^"\\]|\\.)*"\s*(?:#.*)?', line)
                    if not match:
                        problem(path, f'invalid localisation line: {line}')
                        continue
                    key = match[1]
                    if key in localized:
                        problem(path, f'duplicate localisation key: {key}')
                    localized.add(key)
            except (OSError, UnicodeError) as exc:
                problem(path, str(exc))
        for key in sorted(required_text - localized):
            errors.append(f'{language}: missing localisation: {key}')

    validate_startup(root, documents, errors, game_root)
    counts = {kind: len(items) for kind, items in registries.items()}
    counts['script_files'] = len(documents)
    return Result(errors, counts)


def validate_startup(root: Path, documents: dict[Path, list[Node]],
                     errors: list[str], game_root: Path | None = None) -> None:
    """Check concrete 1936 startup data; this does not execute game scripts."""
    def report(message: str):
        errors.append('startup: ' + message)

    def read_state(path: Path) -> Node:
        nodes = documents.get(path)
        if nodes is None:
            nodes = parse(path.read_text(encoding='utf-8-sig'))
        states = [node for node in nodes if node.key == 'state']
        if len(states) != 1:
            raise ParseError('expected exactly one state block')
        return states[0]

    def state_provinces(state: Node) -> list[str]:
        return [p.key for n in children(state) if n.key == 'provinces' for p in children(n)]

    def state_history(state: Node) -> Node:
        return next((n for n in children(state) if n.key == 'history'), Node('history'))

    states: dict[str, tuple[Path, Node]] = {}
    for path in sorted((root / 'history/states').glob('*.txt')):
        try:
            state = read_state(path)
            key = field(state, 'id')
            if not key or not key.isdigit():
                report(f'invalid state ID in {path.name}')
                continue
            if key in states:
                report(f'duplicate state ID: {key}')
            states[key] = (path, state)
        except (OSError, UnicodeError, ParseError) as exc:
            report(f'{path.name}: {exc}')
    province_counts = Counter(p for _, state in states.values() for p in state_provinces(state))
    for province, count in province_counts.items():
        if count > 1:
            report(f'province assigned to multiple mod states: {province}')

    histories = [(path, nodes) for path, nodes in documents.items()
                 if path.parent == root / 'history/countries' and path.name.startswith('WFL - ')]
    if len(histories) != 1:
        report('expected exactly one WFL country history')
        return
    path, nodes = histories[0]
    country = Node('WFL', nodes)
    capital = field(country, 'capital')
    if capital not in states:
        report(f'capital must reference a supplied state: {capital}')
    elif field(state_history(states[capital][1]), 'owner') != 'WFL':
        report(f'capital state {capital} is not owned by WFL in 1936')
    owned: set[str] = set()
    for key, (_, state) in states.items():
        history = state_history(state)
        if field(history, 'owner') == 'WFL':
            owned.update(state_provinces(state))
            if not any(n.key == 'add_core_of' and n.value == 'WFL' for n in children(history)):
                report(f'WFL starting state {key} is not a WFL core')
            if field(history, 'set_demilitarized_zone') == 'yes':
                report(f'WFL starting state {key} is demilitarized')
    for setting in ('set_technology', 'set_politics', 'set_popularities'):
        if not any(n.key == setting for n in nodes):
            report(f'country history requires {setting}')
    oob = field(country, 'oob')
    oob_path = root / 'history/units' / ((oob or '') + '.txt')
    if not oob or oob_path not in documents:
        report(f'missing starting OOB: {oob}')
    else:
        oob_nodes = documents[oob_path]
        templates = {field(n, 'name') for n in oob_nodes if n.key == 'division_template'}
        divisions = [n for group in oob_nodes if group.key == 'units'
                     for n in children(group) if n.key == 'division']
        if not divisions:
            report('starting OOB contains no divisions')
        for division in divisions:
            location = field(division, 'location')
            if location not in owned:
                report(f'division location is outside WFL starting territory: {location}')
            if field(division, 'division_template') not in templates:
                report(f'unknown starting division template: {field(division, "division_template")}')

    for folder, expected in (('', (82, 52)), ('medium', (41, 26)), ('small', (10, 7))):
        base_data = None
        for tag in WFL_IDENTITIES:
            for suffix in FLAG_SUFFIXES:
                flag = root / 'gfx/flags' / folder / f'{tag}{suffix}.tga'
                try:
                    data = flag.read_bytes()
                    if tag == 'WFL' and not suffix:
                        base_data = data
                    elif base_data is not None and data != base_data:
                        report(f'{flag.relative_to(root)} must match WFL.tga in the same size')
                    if len(data) < 18:
                        raise ValueError('truncated TGA header')
                    width, height, depth = struct.unpack_from('<HHB', data, 12)
                    if (width, height) != expected:
                        report(f'{flag.relative_to(root)} requires dimensions {expected}, got {(width, height)}')
                    if data[1] != 0 or data[2] not in (2, 10) or depth not in (24, 32):
                        report(f'{flag.relative_to(root)} must be a true-color 24/32-bit TGA')
                    if data[17] & 0x30:
                        report(f'{flag.relative_to(root)} requires bottom-left TGA origin for HoI4')
                    if data[2] == 2 and len(data) < 18 + data[0] + width * height * (depth // 8):
                        report(f'{flag.relative_to(root)} has truncated pixel data')
                except (OSError, ValueError, struct.error) as exc:
                    report(f'{flag.relative_to(root)}: {exc}')

    if game_root is None:
        return
    try:
        settings = json.loads((game_root / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
        version = settings['rawVersion']
        descriptor = Node('descriptor', documents.get(root / 'descriptor.mod', []))
        supported = field(descriptor, 'supported_version')
        if supported and not re.fullmatch(re.escape(supported).replace(r'\*', '.*'), version):
            report(f'supported_version {supported} does not match installed {version}')
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        report(f'cannot read installed game version: {exc}')

    vanilla_states: dict[str, tuple[Path, Node]] = {}
    original_provinces: Counter[str] = Counter()
    for path in sorted((game_root / 'history/states').glob('*.txt')):
        try:
            state = read_state(path)
            key = field(state, 'id')
            if key in vanilla_states:
                report(f'duplicate vanilla state ID: {key}')
            vanilla_states[key] = (path, state)
            original_provinces.update(state_provinces(state))
        except (OSError, UnicodeError, ParseError) as exc:
            report(f'cannot read vanilla state {path.name}: {exc}')
    if not vanilla_states:
        report('no vanilla state files found under --game-root')
    effective = dict(vanilla_states)
    for key, (path, state) in states.items():
        if key in vanilla_states and path.name != vanilla_states[key][0].name:
            report(f'state {key} must override exact vanilla filename {vanilla_states[key][0].name}')
        effective[key] = (path, state)
    effective_provinces = Counter(p for _, state in effective.values() for p in state_provinces(state))
    for province in sorted(set(original_provinces) | set(effective_provinces)):
        if effective_provinces[province] != original_provinces[province]:
            report(f'effective map changes province assignment count: {province} '
                   f'({original_provinces[province]} -> {effective_provinces[province]})')
    for path in sorted((game_root / 'common/country_tags').glob('*.txt')):
        try:
            if any(n.key == 'WFL' for n in parse(path.read_text(encoding='utf-8-sig'))):
                report(f'WFL tag collides with installed game: {path.name}')
        except (OSError, UnicodeError, ParseError) as exc:
            report(f'cannot check vanilla tags {path.name}: {exc}')
    for path, nodes in documents.items():
        for node in walk(nodes):
            if node.key in ('large', 'small', 'texturefile') and isinstance(node.value, str):
                asset = node.value
                if asset.startswith(('gfx/', 'portraits/')) and not ((root / asset).is_file() or
                                                                        (game_root / asset).is_file()):
                    report(f'missing referenced asset: {asset}')

    recipe_path = root / 'tools/data/building_overrides.json'
    if recipe_path.is_file():
        try:
            recipe = json.loads(recipe_path.read_text(encoding='utf-8-sig'))
            original = (game_root / 'map/buildings.txt').read_bytes()
            if hashlib.sha256(original).hexdigest() != recipe['source_sha256'].lower():
                report('installed buildings map does not match the reviewed recipe SHA256')
            original_lines = original.decode('utf-8-sig').splitlines()
            removed = recipe['remove_lines']
            if len(set(removed)) != len(removed):
                report('building recipe contains duplicate removal lines')
            for line in removed:
                if original_lines.count(line) != 1:
                    report(f'building recipe removal line is not unique in vanilla: {line}')
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
            report(f'cannot validate building recipe: {exc}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--game-root', type=Path, help='Read-only installed vanilla files for map/version checks')
    args = parser.parse_args()
    result = validate(args.root.resolve(), args.game_root.resolve() if args.game_root else None)
    for error in result.errors:
        print('ERROR:', error)
    print('Checked:', ', '.join(f'{value} {key}' for key, value in result.counts.items()))
    if result.errors:
        return 1
    print('PASS: project syntax, own references, focus graph, startup data, flags and DE/EN localisation.')
    if args.game_root:
        print('PASS: installed game version, WFL tag, effective province partition and direct asset paths.')
    print('NOT CHECKED: engine script scopes, game startup, AI, DLC behavior and gameplay.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
