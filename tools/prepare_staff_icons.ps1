# Format/size conversion only. Background removal is already done by Imagegen.
[CmdletBinding()]
param([string]$ProjectRoot)
$ErrorActionPreference = 'Stop'
if (-not $ProjectRoot) { $ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path) }
Add-Type -AssemblyName System.Drawing
$folder = Join-Path $ProjectRoot 'gfx/interface/beraterstab'
function Save-Dds([Drawing.Bitmap]$Bitmap, [string]$Path) {
    $writer = [IO.BinaryWriter]::new([IO.File]::Create($Path))
    try {
        $writer.Write([Text.Encoding]::ASCII.GetBytes('DDS '))
        $header = @([uint32]124, 0x100F, $Bitmap.Height, $Bitmap.Width, ($Bitmap.Width * 4), 0, 0)
        $header += @(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        $header += @(32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, [uint32]4278190080)
        $header += @(0x1000, 0, 0, 0, 0)
        foreach ($number in $header) { $writer.Write([uint32]$number) }
        for ($y = 0; $y -lt $Bitmap.Height; $y++) {
            for ($x = 0; $x -lt $Bitmap.Width; $x++) {
                $c = $Bitmap.GetPixel($x, $y)
                $writer.Write([byte]$c.B); $writer.Write([byte]$c.G)
                $writer.Write([byte]$c.R); $writer.Write([byte]$c.A)
            }
        }
    } finally { $writer.Dispose() }
}
foreach ($id in @('dante_grossy', 'neal_foerster', 'max_heinsch', 'max_mueller', 'till_hoehne')) {
    $source = [Drawing.Image]::FromFile((Join-Path $folder "source/$id.png"))
    try {
        foreach ($variant in @(@('focus',102,90), @('ui',128,128))) {
            $name = $variant[0]; $width = [int]$variant[1]; $height = [int]$variant[2]
            $bitmap = [Drawing.Bitmap]::new($width,$height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
            $g = [Drawing.Graphics]::FromImage($bitmap)
            try {
                $g.Clear([Drawing.Color]::Transparent)
                $g.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
                $size = [Math]::Min($width,$height)-6
                $g.DrawImage($source,[Drawing.Rectangle]::new([int](($width-$size)/2),[int](($height-$size)/2),$size,$size))
                $bitmap.Save((Join-Path $folder "$($id)_$name.png"),[Drawing.Imaging.ImageFormat]::Png)
                Save-Dds $bitmap (Join-Path $folder "$($id)_$name.dds")
            } finally { $g.Dispose(); $bitmap.Dispose() }
        }
    } finally { $source.Dispose() }
}
$empty = [Drawing.Bitmap]::new(128,128,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
try { Save-Dds $empty (Join-Path $folder 'empty.dds') } finally { $empty.Dispose() }
Write-Output 'Exported five alpha-preserving focus/UI badges and an empty slot.'
