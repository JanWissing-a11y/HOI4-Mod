#!/usr/bin/env python3
"""Rebuild WFL's fictional political advisors from an installed vanilla catalog.

Only scalar trait effects and base prices are imported. German story/AI gates
are deliberately replaced; original files and original photos remain read only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .validate_mod import Node, children, field, parse, walk
except ImportError:
    from validate_mod import Node, children, field, parse, walk


NAMES = [
    'Arne Rabenau', 'Friedrich Ufermann', 'Ludwig Dornbach', 'Johann Auenfeld',
    'Emil Werkhausen', 'Benedikt Torberg', 'Heinrich Rechenberg', 'Rudolf Stahlbach',
    'Karl Lauterfeld', 'Wilhelm Ratsburg', 'Konrad Wachtmann', 'Oskar Binnenhof',
    'Marlene Rheinfeld', 'Theodor Werksdorf', 'Paul Kirchhain', 'Ernst Sicherau',
    'Adrian Falkenried', 'Leonhard Freihagen', 'Hermann Kronwald', 'Georg Maßfeld',
    'Matthias Bürgering', 'Daniel Wiesenbrück', 'Felix Blattmann', 'Anton Münzberg',
    'Otmar Freimarkt', 'Kurt Schützenwald', 'August Fernbach', 'Rainer Rechtfeld',
    'Wendelin Kornau', 'Martin Friedenshain', 'Jakob Rotacker', 'Viktor Ordnau',
    'Richard Nachrichtenau', 'Eduard Denkfeld', 'Lorenz Lehrmann',
    'Alfred Gemeinschaft', 'Samuel Standhaft',
]

# One label per source trait, including the two pairs of DLC alternatives.
LABELS = [
    ('Nationaler Agitator', 'National agitator'),
    ('Planungsbeauftragter', 'Planning commissioner'),
    ('Entschlossener Außenpolitiker', 'Determined diplomat'),
    ('Ausgleichender Außenpolitiker', 'Conciliatory diplomat'),
    ('Infrastrukturingenieur', 'Infrastructure engineer'),
    ('Staatsarchitekt', 'State architect'),
    ('Rüstungsfinanzier', 'Armaments financier'),
    ('Wirtschaftsverwalter', 'Economic administrator'),
    ('Nationaler Rundfunkredner', 'National radio speaker'),
    ('Politischer Vermittler', 'Political mediator'),
    ('Strenger Sicherheitsverwalter', 'Strict security administrator'),
    ('Kabinettssekretär', 'Cabinet secretary'),
    ('Filmregisseurin', 'Film director'),
    ('Arbeitsorganisator', 'Labour organiser'),
    ('Gemeindevermittler', 'Community mediator'),
    ('Sicherheitskoordinator', 'Security coordinator'),
    ('Sicherheitskoordinator', 'Security coordinator'),
    ('Nachrichtendienstleiter', 'Intelligence chief'),
    ('Demokratischer Agent', 'Democratic agent'),
    ('Königstreuer Medienunternehmer', 'Royalist media magnate'),
    ('Preiskommissar', 'Price commissioner'),
    ('Vernetzter Bürger', 'Connected citizen'),
    ('Demokratischer Reformer', 'Democratic reformer'),
    ('Liberaler Journalist', 'Liberal journalist'),
    ('Zentralbankfachmann', 'Central bank expert'),
    ('Wirtschaftsreformer', 'Economic reformer'),
    ('Freiwilligenkommandeur', 'Volunteer commander'),
    ('Überseeverwalter', 'Overseas administrator'),
    ('Königstreuer Jurist', 'Royalist jurist'),
    ('Landwirtschaftsfachmann', 'Agricultural expert'),
    ('Einflussreicher Gemeindepfarrer', 'Influential pastor'),
    ('Kommunistischer Agitator', 'Communist agitator'),
    ('Arbeiterpolitiker', 'Labour politician'),
    ('Kommunistischer Organisator', 'Communist organiser'),
    ('Geheimdienstkoordinator', 'Intelligence coordinator'),
    ('Sozialistischer Philosoph', 'Socialist philosopher'),
    ('Arbeiterbildner', 'Workers educator'),
    ('Kollektiver Produktionsplaner', 'Collective production planner'),
    ('Erfahrener Widerstandsorganisator', 'Experienced resistance organiser'),
]


def block(node: Node, key: str) -> list[Node]:
    return children(next((n for n in children(node) if n.key == key), Node(key)))


def emit(node: Node, depth: int = 0) -> str:
    """Used only for equality-based DLC/role blocks, never source comparisons."""
    pad = '    ' * depth
    if isinstance(node.value, list):
        return pad + node.key + ' = {\n' + ''.join(emit(n, depth + 1) for n in node.value) + pad + '}\n'
    if node.value is None:
        return pad + node.key + '\n'
    value = json.dumps(node.value, ensure_ascii=False) if any(c.isspace() for c in node.value) else node.value
    return pad + node.key + ' = ' + value + '\n'


def build(root: Path, game: Path) -> dict:
    source_paths = ['common/characters/GER.txt', 'common/country_leader/00_traits.txt', 'common/defines/00_defines.lua']
    chars = children(parse((game / source_paths[0]).read_text(encoding='utf-8-sig'))[0])
    traits = {n.key: n for group in parse((game / source_paths[1]).read_text(encoding='utf-8-sig'))
              if group.key == 'leader_traits' for n in children(group)}
    selected = [c for c in chars if any(n.key == 'advisor' and field(n, 'slot') == 'political_advisor'
                                       for n in walk(children(c)))]
    if len(selected) != len(NAMES):
        raise ValueError('Vanilla political advisor catalog changed; review the import mapping first.')
    id_map = {c.key: f'WFL_advisor_{i:02}' for i, c in enumerate(selected, 1)}
    excludes = {7: [8], 8: [7, 25], 25: [8], 10: [12], 12: [10]}
    photo_ids = [i for i in range(1, 19) if i != 12]
    localized = {'german': [], 'english': []}
    character_lines = ['# Fictional characters; numerical profiles from the installed German catalog.\ncharacters = {\n']
    trait_lines = ['# Imported numerical effects; German event and AI hooks are not imported.\nleader_traits = {\n']
    manifest = {'source_version': '1.19.4.1', 'sources': {
        p: hashlib.sha256((game / p).read_bytes()).hexdigest() for p in source_paths}, 'advisors': []}
    trait_index = 0
    for number, char in enumerate(selected, 1):
        own_id = id_map[char.key]
        photo = 12 if field(char, 'gender') == 'female' else photo_ids[(number - 1) % len(photo_ids)]
        portraits = Node('portraits', [Node('civilian', [Node('large', f'GFX_portrait_WFL_advisor_{photo:02}'),
                                                      Node('small', f'GFX_portrait_WFL_advisor_{photo:02}_small')])])
        metadata = [Node('name', own_id), portraits]
        if field(char, 'gender'):
            metadata.append(Node('gender', field(char, 'gender')))
        # The engine chooses either one plain character body or DLC instance
        # bodies. Mixing metadata outside the instance blocks makes it parse
        # this as a plain character and reject each later `instance` token.
        source_instances = [n for n in children(char) if n.key == 'instance']
        if source_instances and any(n.key == 'advisor' for n in children(char)):
            raise ValueError(f'Review mixed plain/instance character: {char.key}')
        own_char = Node(own_id, [] if source_instances else metadata)
        record = {'id': own_id, 'source_character': char.key, 'name': NAMES[number - 1],
                  'portrait': f'{photo:02}', 'roles': []}
        for language in localized:
            localized[language].append((own_id, NAMES[number - 1]))

        def import_role(source_role: Node) -> Node:
            nonlocal trait_index
            trait_index += 1
            trait_id = f'WFL_advisor_skill_{trait_index:02}'
            source_trait_names = [n.key for n in block(source_role, 'traits')]
            if len(source_trait_names) != 1:
                raise ValueError(f'Unexpected trait list for {char.key}')
            source_trait = traits[source_trait_names[0]]
            if any(isinstance(n.value, list) and n.key != 'ai_will_do' for n in children(source_trait)):
                raise ValueError(f'Review non-scalar trait effects: {source_trait.key}')
            scalar = [n for n in children(source_trait) if isinstance(n.value, str)]
            if not any(n.key == 'random' for n in scalar):
                scalar.append(Node('random', 'no'))
            trait_lines.append(emit(Node(trait_id, scalar), 1))
            cost = field(source_role, 'cost') or '150'
            dlc = [n for n in block(source_role, 'allowed') if n.key == 'has_dlc']
            role = Node('advisor', [Node('slot', 'political_advisor'), Node('idea_token', own_id),
                                   Node('allowed', [Node('original_tag', 'WFL'), *dlc]),
                                   Node('cost', cost), Node('traits', [Node(trait_id)])])
            available = [Node(f'WFL_advisor_{n:02}', [Node('is_hired_as_advisor', 'no')])
                         for n in excludes.get(number, [])]
            if char.key == 'GER_wilhelm_canaris':
                available.append(Node('has_intelligence_agency', 'yes'))
            if available:
                role.value.append(Node('available', available))
            # Preserve drift activation semantics and the generic supervised-state restriction.
            do_effect = next((n for n in children(source_role) if n.key == 'do_effect'), None)
            if do_effect:
                role.value.append(do_effect)
            if char.key in ('GER_joseph_goebbels', 'GER_ernst_thalmann') and do_effect:
                role.value.append(Node('available', [Node('if', [Node('limit', [Node('has_dlc', 'Man the Guns')]),
                    Node('NOT', [Node('has_autonomy_state', 'autonomy_supervised_state')])])]))
            role.value.append(Node('ai_will_do', [Node('factor', '1')]))
            modifiers = {n.key: n.value for n in scalar if n.key not in ('sprite', 'random')}
            record['roles'].append({'source_trait': source_trait.key, 'trait': trait_id,
                                    'base_cost': int(cost), 'modifiers': modifiers,
                                    'required_dlc': [n.value for n in dlc]})
            de, en = LABELS[trait_index - 1]
            localized['german'].extend([(trait_id, de), (trait_id + '_desc',
                'Fiktive Flürener Beraterrolle. Die Fähigkeiten entsprechen der deutschen Vorlage, einschließlich ihrer Nachteile.')])
            localized['english'].extend([(trait_id, en), (trait_id + '_desc',
                'Fictional Flüren advisor role. Effects match the German template, including its drawbacks.')])
            return role

        for child in children(char):
            if child.key == 'advisor' and field(child, 'slot') == 'political_advisor':
                own_char.value.append(import_role(child))
            elif child.key == 'instance':
                roles = [n for n in children(child) if n.key == 'advisor' and field(n, 'slot') == 'political_advisor']
                if roles:
                    first_role_index = len(record['roles'])
                    own_char.value.append(Node('instance', [Node('allowed', block(child, 'allowed')), *metadata,
                                                           *(import_role(n) for n in roles)]))
                    for variant in record['roles'][first_role_index:]:
                        variant['instance_allowed'] = emit(Node('allowed', block(child, 'allowed'))).strip()
        character_lines.append(emit(own_char, 1))
        manifest['advisors'].append(record)
    if trait_index != len(LABELS):
        raise ValueError('Vanilla role variants changed; review labels.')
    character_lines.append('}\n')
    trait_lines.append('}\n')
    (root / 'common/characters/WFL_advisors.txt').write_text(''.join(character_lines), encoding='utf-8')
    (root / 'common/country_leader/WFL_advisor_traits.txt').write_text(''.join(trait_lines), encoding='utf-8')
    for language, entries in localized.items():
        text = f'l_{language}:\n' + ''.join(f' {key}:0 {json.dumps(value, ensure_ascii=False)}\n' for key, value in entries)
        (root / f'localisation/{language}/WFL_advisors_l_{language}.yml').write_text(text, encoding='utf-8-sig')
    (root / 'tools/data/WFL_advisors.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    history = root / 'history/countries/WFL - Wesel-Flueren.txt'
    before, separator, after = history.read_text(encoding='utf-8-sig').partition('# BEGIN WFL POLITICAL ADVISORS')
    tail = after.partition('# END WFL POLITICAL ADVISORS')[2] if separator else ''
    history_text = before.rstrip()
    history_text += '\n\n# BEGIN WFL POLITICAL ADVISORS\n# Available for normal paid hiring; no advisors are hired for free.\n'
    history_text += ''.join(f'recruit_character = {id_map[c.key]}\n' for c in selected)
    history_text += '# END WFL POLITICAL ADVISORS\n' + tail.lstrip('\n')
    history.write_text(history_text, encoding='utf-8')
    return manifest


def write_sprites(root: Path):
    entries = json.loads((root / 'tools/data/advisor_portraits.json').read_text(encoding='utf-8'))['portraits']
    text = 'spriteTypes = {\n'
    for entry in entries:
        for suffix in ('', '_small'):
            stem = 'WFL_advisor_' + entry['id'] + suffix
            text += f'    spriteType = {{\n        name = "GFX_portrait_{stem}"\n        texturefile = "gfx/leaders/WFL/advisors/{stem}.dds"\n    }}\n'
    (root / 'interface/WFL_advisor_portraits.gfx').write_text(text + '}\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    manifest = build(args.root, args.game_root)
    write_sprites(args.root)
    print(f"Imported {len(manifest['advisors'])} advisors / {sum(len(a['roles']) for a in manifest['advisors'])} variants.")


if __name__ == '__main__':
    main()
