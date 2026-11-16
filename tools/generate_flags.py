"""Convert the approved PNG flag to HoI4's three 32-bit TGA flag sizes.

The PNG in gfx/flags/source is the editable design source. This bridge uses
Windows PowerShell and System.Drawing; it never redraws the coat of arms and
requires no third-party Python image library.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'gfx/flags/source/WFL_flag.png')
    parser.add_argument('--preview', type=Path, default=ROOT / '.local-test/flag-preview.png')
    parser.add_argument('--no-preview', action='store_true')
    args = parser.parse_args()
    powershell = shutil.which('powershell.exe') or shutil.which('pwsh')
    if powershell is None:
        raise SystemExit('Windows PowerShell with System.Drawing is required to convert the flag PNG.')
    command = [powershell, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
               '-File', str(ROOT / 'tools/generate_flags.ps1'),
               '-Source', str(args.source.resolve()), '-FlagsRoot', str(ROOT / 'gfx/flags')]
    if not args.no_preview:
        command.extend(['-Preview', str(args.preview.resolve())])
    subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
