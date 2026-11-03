#!/usr/bin/env python3
"""Statische Prüfung eigener Mod-Dateien; kein Ersatz für die HOI4-Engine."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


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


def validate(root: Path) -> Result:
    errors: list[str] = []
    documents: dict[Path, list[Node]] = {}
    registries: dict[str, dict[str, Node]] = {
        kind: {} for kind in ('tag', 'character', 'idea', 'focus', 'event', 'category', 'decision')
    }
    required_text: set[str] = set()

    def problem(path: Path, message: str):
        errors.append(f'{path.relative_to(root)}: {message}')

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
    for folder in ('common', 'events', 'history'):
        paths.extend(sorted((root / folder).rglob('*.txt')))
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
        elif relative.startswith('common/ideas/'):
            for group in nodes:
                for section in children(group):
                    if group.key == 'ideas' and section.key == 'country':
                        for node in children(section):
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
                if node.key == 'country_event':
                    register('event', field(node, 'id'), node, path, description=False)
                    for part in walk(children(node)):
                        if part.key in ('title', 'desc', 'name') and isinstance(part.value, str):
                            required_text.add(part.value)
        elif relative.startswith('common/decisions/categories/'):
            for node in nodes:
                register('category', node.key, node, path)
        elif relative.startswith('common/decisions/'):
            for category in nodes:
                for node in children(category):
                    register('decision', node.key, node, path)

    reference_fields = {
        'focus': 'focus', 'has_completed_focus': 'focus',
        'recruit_character': 'character', 'retire_character': 'character',
        'add_ideas': 'idea', 'remove_ideas': 'idea', 'has_idea': 'idea',
    }
    for path, nodes in documents.items():
        for node in walk(nodes):
            kind = reference_fields.get(node.key)
            if kind:
                references = [node.value] if isinstance(node.value, str) else [n.key for n in children(node)]
                for key in references:
                    if key.startswith('WFL_') and key not in registries[kind]:
                        problem(path, f'unknown {kind} reference: {key}')
            if node.key == 'country_event' and isinstance(node.value, list):
                key = field(node, 'id')
                if key and key.startswith('wfl.') and key not in registries['event']:
                    problem(path, f'unknown event reference: {key}')
        if path.relative_to(root).parent == Path('common/decisions'):
            for node in nodes:
                if node.key not in registries['category']:
                    problem(path, f'unknown decision category: {node.key}')

    edges: dict[str, set[str]] = {}
    exclusions: dict[str, set[str]] = {}
    for key, node in registries['focus'].items():
        edges[key] = {n.value for group in children(node) if group.key == 'prerequisite'
                      for n in children(group) if n.key == 'focus' and isinstance(n.value, str)}
        exclusions[key] = {n.value for group in children(node) if group.key == 'mutually_exclusive'
                           for n in children(group) if n.key == 'focus' and isinstance(n.value, str)}
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

    counts = {kind: len(items) for kind, items in registries.items()}
    counts['script_files'] = len(documents)
    return Result(errors, counts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = validate(args.root.resolve())
    for error in result.errors:
        print('ERROR:', error)
    print('Checked:', ', '.join(f'{value} {key}' for key, value in result.counts.items()))
    if result.errors:
        return 1
    print('PASS: project syntax, own references, focus graph and DE/EN localisation.')
    print('NOT CHECKED: vanilla compatibility, map, graphics, game startup and gameplay.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
