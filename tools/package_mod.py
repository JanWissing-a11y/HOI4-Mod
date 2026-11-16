#!/usr/bin/env python3
"""Create an installable source package without local profiles or vanilla assets."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

try:
    from .validate_mod import Node, field, parse, validate
except ImportError:
    from validate_mod import Node, field, parse, validate


def package(root: Path, output: Path) -> int:
    result = validate(root)
    if result.errors:
        raise ValueError('\n'.join(result.errors))
    files = [root / 'descriptor.mod', root / 'README.md', root / 'tools/install.ps1']
    for folder in ('common', 'history', 'events', 'localisation', 'gfx', 'interface', 'portraits', 'map'):
        files.extend(path for path in (root / folder).rglob('*') if path.is_file() and path.name != '.gitkeep')
    files.extend(sorted((root / 'docs').glob('*.md')))
    files.extend(sorted((root / 'tools/data').glob('*.json')))
    for folder in ('tools', 'tests'):
        files.extend(path for path in (root / folder).glob('*')
                     if path.is_file() and path.suffix in ('.py', '.ps1'))
    if root / 'map/buildings.txt' in files:
        raise ValueError('Do not package locally derived vanilla map/buildings.txt; package the recipe instead.')
    if any(root / f'common/countries/{name}.txt' in files for name in ('colors', 'cosmetic')):
        raise ValueError('Do not package locally derived vanilla colour registries; package WFL_country_colors.json instead.')
    for path in files:
        if path.is_symlink():
            raise ValueError(f'Refusing symlink in package: {path}')
        if not path.is_file():
            raise ValueError(f'Missing package input: {path}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            info = ZipInfo(path.relative_to(root).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return len(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    descriptor = Node('descriptor', parse((root / 'descriptor.mod').read_text(encoding='utf-8-sig')))
    version = field(descriptor, 'version') or 'dev'
    if any(char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_' for char in version):
        raise ValueError('Descriptor version is unsuitable for a package filename')
    output = (args.output or root / 'dist' / f'wesel_flueren-{version}.zip').resolve()
    count = package(root, output)
    print(f'Created {output} ({count} files).')
    print('Install with tools/install.ps1 after extraction; the local vanilla buildings file is read at installation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
