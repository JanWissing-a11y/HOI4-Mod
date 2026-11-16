#!/usr/bin/env python3
"""Render a schematic WFL focus layout, including the reserved continuous panel.

SVG is portable; the optional PNG uses Windows System.Drawing, without image
generation or external libraries. This is a diagram, not an engine screenshot.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import subprocess
import textwrap

try:
    from .validate_mod import children, field, parse
except ImportError:
    from validate_mod import children, field, parse

SPACING = (96, 130)
ITEM = (165, 128)
PANEL = (770, 380)
GRID_ORIGIN = (50, 50)
CANVAS_ORIGIN = (60, 100)


def layout(root):
    tree = parse((root / 'common/national_focus/WFL_focus.txt').read_text(encoding='utf-8-sig'))[0]
    labels = {}
    for path in (root / 'localisation/german').glob('*.yml'):
        labels.update(dict(re.findall(r'^ ([\w.]+):\d* "(.*)"$', path.read_text(encoding='utf-8-sig'), re.M)))
    focuses = []
    for node in children(tree):
        if node.key != 'focus':
            continue
        key = field(node, 'id')
        x, y = int(field(node, 'x')), int(field(node, 'y'))
        group = 'economy' if x <= 6 else 'military' if x <= 12 else 'politics' if x <= 24 else 'diplomacy'
        focuses.append({'id': key, 'label': labels[key], 'x': x, 'y': y, 'group': group,
                        'px': CANVAS_ORIGIN[0] + GRID_ORIGIN[0] + x * SPACING[0],
                        'py': CANVAS_ORIGIN[1] + GRID_ORIGIN[1] + y * SPACING[1],
                        'parents': [v.value for p in children(node) if p.key == 'prerequisite'
                                    for v in children(p) if v.key == 'focus']})
    panel = next(n for n in children(tree) if n.key == 'continuous_focus_position')
    panel = {'x': CANVAS_ORIGIN[0] + int(field(panel, 'x')),
             'y': CANVAS_ORIGIN[1] + int(field(panel, 'y')),
             'width': PANEL[0], 'height': PANEL[1]}
    windows = {}
    for path in (root / 'interface').glob('*.gui'):
        for group in parse(path.read_text(encoding='utf-8-sig')):
            for window in children(group):
                if window.key == 'containerWindowType':
                    windows[field(window, 'name')] = window
    definitions = {}
    for path in (root / 'common/focus_inlay_windows').glob('*.txt'):
        definitions.update((node.key, node) for node in parse(path.read_text(encoding='utf-8-sig')))
    inlays = []
    for binding in children(tree):
        if binding.key != 'inlay_window':
            continue
        key = field(binding, 'id')
        position = next(n for n in children(binding) if n.key == 'position')
        window = windows[field(definitions[key], 'window_name')]
        size = next(n for n in children(window) if n.key == 'size')
        inlays.append({'id': key, 'x': CANVAS_ORIGIN[0] + int(field(position, 'x')),
                       'y': CANVAS_ORIGIN[1] + int(field(position, 'y')),
                       'width': int(field(size, 'width')), 'height': int(field(size, 'height'))})
    width = max([f['px'] + ITEM[0] for f in focuses] + [i['x'] + i['width'] for i in inlays]) + 60
    height = max([f['py'] + ITEM[1] for f in focuses] + [panel['y'] + panel['height']]
                 + [i['y'] + i['height'] for i in inlays]) + 60
    return {'width': width, 'height': height, 'focuses': focuses, 'panel': panel, 'inlays': inlays}


def render(root, output, png=False):
    data = layout(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'layout.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    colors = {'economy': '#e4bd70', 'military': '#91b6ce', 'politics': '#9fc49c', 'diplomacy': '#c1a6d4'}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{data["width"]}" height="{data["height"]}" viewBox="0 0 {data["width"]} {data["height"]}">',
           '<rect width="100%" height="100%" fill="#171e25"/>',
           '<text x="60" y="37" fill="#f2ede1" font-family="Segoe UI, sans-serif" font-size="25">Wesel-Flüren – Fokusbaum und freier Bereich für kontinuierliche Fokusse</text>',
           '<text x="60" y="65" fill="#acb8c1" font-family="Segoe UI, sans-serif" font-size="16">Schematische Vorschau aus den Spielkoordinaten; keine Engine-Aufnahme.</text>']
    by_id = {f['id']: f for f in data['focuses']}
    for focus in data['focuses']:
        for parent in focus['parents']:
            p = by_id[parent]
            x1, y1 = p['px'] + ITEM[0] / 2, p['py'] + 100
            x2, y2 = focus['px'] + ITEM[0] / 2, focus['py'] + 8
            middle = (y1 + y2) / 2
            svg.append(f'<path d="M{x1},{y1} V{middle} H{x2} V{y2}" fill="none" stroke="#6c7c85" stroke-width="3"/>')
    for f in data['focuses']:
        color = colors[f['group']]
        svg.append(f'<rect x="{f["px"]}" y="{f["py"]+8}" width="165" height="100" rx="9" fill="#29343d" stroke="{color}" stroke-width="2"/>')
        lines = textwrap.wrap(f['label'], width=21, break_long_words=False)
        font_size = 13 if max(map(len, f['label'].split())) > 20 else 15
        for i, line in enumerate(lines):
            svg.append(f'<text x="{f["px"]+82.5}" y="{f["py"]+35+i*19}" text-anchor="middle" fill="#f2ede1" font-family="Segoe UI, sans-serif" font-size="{font_size}">{html.escape(line)}</text>')
    p = data['panel']
    svg.extend([f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["width"]}" height="{p["height"]}" rx="10" fill="#243e3b" stroke="#79c2a5" stroke-width="4"/>',
                f'<text x="{p["x"]+30}" y="{p["y"]+48}" fill="#c0e6d6" font-family="Segoe UI, sans-serif" font-size="28">Kontinuierliche Fokusse</text>',
                f'<text x="{p["x"]+30}" y="{p["y"]+82}" fill="#c0e6d6" font-family="Segoe UI, sans-serif" font-size="18">Reserviert: 770 × 380 Pixel – keine normalen Fokusse oder Verbindungen.</text>'])
    for row in range(2):
        for col in range(4):
            svg.append(f'<rect x="{p["x"]+30+col*180}" y="{p["y"]+112+row*120}" width="160" height="100" rx="5" fill="#2d4e48" stroke="#609885"/>')
    for i in data['inlays']:
        svg.append(f'<rect x="{i["x"]}" y="{i["y"]}" width="{i["width"]}" height="{i["height"]}" rx="10" fill="#24362e" stroke="#b99a57" stroke-width="4"/>')
        svg.append(f'<text x="{i["x"]+30}" y="{i["y"]+48}" fill="#e5d5aa" font-family="Segoe UI, sans-serif" font-size="28">Beraterstab: drei Sitze, fünf Kandidaten</text>')
    svg.append('</svg>')
    (output / 'WFL_focus_layout.svg').write_text('\n'.join(svg), encoding='utf-8')
    if png:
        def q(value):
            return "'" + str(value).replace("'", "''") + "'"
        script = r'''
Add-Type -AssemblyName System.Drawing
$d = Get-Content -Raw -Encoding UTF8 -LiteralPath JSONPATH | ConvertFrom-Json
$bmp = [Drawing.Bitmap]::new([int]$d.width,[int]$d.height)
$g = [Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([Drawing.ColorTranslator]::FromHtml('#171e25'))
$font = [Drawing.Font]::new('Segoe UI',15,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$title = [Drawing.Font]::new('Segoe UI',25,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
$brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#f2ede1'))
$muted = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#acb8c1'))
$pen = [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#6c7c85'),3)
$fill = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#29343d'))
$map = @{}
foreach ($f in $d.focuses) {$map[$f.id]=$f}
$g.DrawString('Wesel-Flüren – schematische Fokusübersicht',$title,$brush,60,20)
$g.DrawString('Keine Engine-Aufnahme. Panel und Fokuspositionen stammen direkt aus dem Skript.',$font,$muted,60,60)
foreach ($f in $d.focuses) {
 foreach ($parent in $f.parents) {
  $p=$map[$parent]; $x1=[single]($p.px+82); $y1=[single]($p.py+100)
  $x2=[single]($f.px+82); $y2=[single]($f.py+8); $m=[single](($y1+$y2)/2)
  $g.DrawLine($pen,$x1,$y1,$x1,$m);$g.DrawLine($pen,$x1,$m,$x2,$m);$g.DrawLine($pen,$x2,$m,$x2,$y2)
 }
}
$colors = @{economy='#e4bd70';military='#91b6ce';politics='#9fc49c';diplomacy='#c1a6d4'}
$format=[Drawing.StringFormat]::new();$format.Alignment=[Drawing.StringAlignment]::Center;$format.LineAlignment=[Drawing.StringAlignment]::Center
foreach ($f in $d.focuses) {
 $outline=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($colors[$f.group]),2)
 $rect=[Drawing.RectangleF]::new($f.px,($f.py+8),165,100)
 $g.FillRectangle($fill,$rect);$g.DrawRectangle($outline,$f.px,($f.py+8),165,100)
 $labelFont=$font;$ownedFont=$null
 foreach($word in ($f.label -split '\s+')) {
  while($g.MeasureString($word,$labelFont).Width -gt 155 -and $labelFont.Size -gt 10) {
   $nextSize=$labelFont.Size-1
   if($ownedFont){$ownedFont.Dispose()}
   $ownedFont=[Drawing.Font]::new('Segoe UI',$nextSize,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
   $labelFont=$ownedFont
  }
 }
 $g.DrawString($f.label,$labelFont,$brush,$rect,$format);$outline.Dispose()
 if($ownedFont){$ownedFont.Dispose()}
}
$p=$d.panel;$panelFill=[Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#243e3b'))
$panelPen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#79c2a5'),4)
$g.FillRectangle($panelFill,$p.x,$p.y,$p.width,$p.height);$g.DrawRectangle($panelPen,$p.x,$p.y,$p.width,$p.height)
$g.DrawString('Kontinuierliche Fokusse',$title,$brush,($p.x+30),($p.y+24))
$g.DrawString('770 × 380 Pixel: frei von normalen Fokussen und Verbindungen',$font,$brush,($p.x+30),($p.y+70))
for($row=0;$row-lt2;$row++){for($col=0;$col-lt4;$col++){$g.DrawRectangle($panelPen,($p.x+30+$col*180),($p.y+112+$row*120),160,100)}}
foreach($inlay in $d.inlays) {
 $g.FillRectangle($panelFill,$inlay.x,$inlay.y,$inlay.width,$inlay.height)
 $g.DrawRectangle($panelPen,$inlay.x,$inlay.y,$inlay.width,$inlay.height)
 $g.DrawString('Beraterstab: drei Sitze, fuenf Kandidaten',$title,$brush,($inlay.x+20),($inlay.y+20))
}
$bmp.Save(PNGPATH,[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose();$bmp.Dispose();$font.Dispose();$title.Dispose();$brush.Dispose();$muted.Dispose();$pen.Dispose();$fill.Dispose();$format.Dispose();$panelFill.Dispose();$panelPen.Dispose()
'''.replace('JSONPATH', q((output / 'layout.json').resolve())).replace('PNGPATH', q((output / 'WFL_focus_layout.png').resolve()))
        subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script], check=True)
    return output / 'WFL_focus_layout.svg'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--png', action='store_true')
    args = parser.parse_args()
    print(render(args.root, args.output or args.root / '.local-test/focus-layout', args.png))
