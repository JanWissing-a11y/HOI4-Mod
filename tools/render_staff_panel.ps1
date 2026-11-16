# Code-drawn interface decoration. No changes to the supplied portrait artwork.
[CmdletBinding()]
param([string]$ProjectRoot)
$ErrorActionPreference = 'Stop'
if (-not $ProjectRoot) { $ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path) }
Add-Type -AssemblyName System.Drawing
$folder = Join-Path $ProjectRoot 'gfx/interface/beraterstab'
$bitmap = [Drawing.Bitmap]::new(960,590,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [Drawing.Graphics]::FromImage($bitmap)
function Panel-Gradient([int]$x,[int]$y,[int]$w,[int]$h,[string]$top,[string]$bottom) {
    $rect = [Drawing.Rectangle]::new($x,$y,$w,$h)
    $brush = [Drawing.Drawing2D.LinearGradientBrush]::new($rect,[Drawing.ColorTranslator]::FromHtml($top),[Drawing.ColorTranslator]::FromHtml($bottom),90.0)
    try { $g.FillRectangle($brush,$rect) } finally { $brush.Dispose() }
}
$gold = [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#9d8755'),1)
$dim = [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#405346'),1)
try {
    $g.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
    Panel-Gradient 0 0 960 590 '#243b2f' '#111e18'
    Panel-Gradient 5 5 950 96 '#304d3b' '#1b3025'
    $g.DrawRectangle($gold,2,2,955,585)
    $g.DrawRectangle($dim,6,6,947,577)
    # Header flourishes leave room for the localized title and status.
    $g.DrawLine($gold,26,34,222,34); $g.DrawLine($gold,738,34,934,34)
    $g.DrawLine($dim,26,39,180,39); $g.DrawLine($dim,780,39,934,39)
    foreach ($x in @(20,337,654)) {
        Panel-Gradient $x 107 286 285 '#263e30' '#15251c'
        $g.DrawRectangle($gold,$x,107,286,285)
        $g.DrawRectangle($dim,($x+4),111,278,277)
        $g.DrawLine($dim,($x+18),247,($x+268),247)
        $g.DrawLine($dim,($x+18),354,($x+268),354)
        # Quiet seal under the dynamic medallion; also marks an empty seat.
        $g.DrawEllipse($dim,($x+94),118,98,98)
        $g.DrawEllipse($gold,($x+100),124,86,86)
    }
    foreach ($x in @(20,208,396,584,772)) {
        Panel-Gradient $x 431 168 142 '#2c4435' '#1a2b21'
        $g.DrawRectangle($gold,$x,431,168,142)
        $g.DrawLine($dim,($x+12),544,($x+156),544)
    }
    $g.DrawLine($gold,28,417,118,417); $g.DrawLine($gold,842,417,932,417)
    $bitmap.Save((Join-Path $folder 'staff_panel.png'),[Drawing.Imaging.ImageFormat]::Png)
    # Uncompressed BGRA DDS, matching the project's existing UI textures.
    $writer = [IO.BinaryWriter]::new([IO.File]::Create((Join-Path $folder 'staff_panel.dds')))
    try {
        $writer.Write([Text.Encoding]::ASCII.GetBytes('DDS '))
        $header = @(124,0x100F,590,960,3840,0,0) + @(0,0,0,0,0,0,0,0,0,0,0) + @(32,0x41,0,32,0x00FF0000,0x0000FF00,0x000000FF,[uint32]4278190080) + @(0x1000,0,0,0,0)
        foreach ($number in $header) { $writer.Write([uint32]$number) }
        $rect = [Drawing.Rectangle]::new(0,0,960,590)
        $data = $bitmap.LockBits($rect,[Drawing.Imaging.ImageLockMode]::ReadOnly,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
        try {
            $bytes = [byte[]]::new(960*590*4)
            [Runtime.InteropServices.Marshal]::Copy($data.Scan0,$bytes,0,$bytes.Length)
            $writer.Write($bytes)
        } finally { $bitmap.UnlockBits($data) }
    } finally { $writer.Dispose() }
} finally { $gold.Dispose(); $dim.Dispose(); $g.Dispose(); $bitmap.Dispose() }
Write-Output 'Rendered green/gold staff panel (960 x 590 PNG and DDS).'
