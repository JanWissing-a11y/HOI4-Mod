#requires -Version 5.1
<#
.SYNOPSIS
Creates game portraits from explicitly selected rectangles in the supplied photos.
.DESCRIPTION
Only crops and resizes the source photos. No faces are identified or synthesized.
Original photos are read only. DDS dimensions match the local vanilla assets.
#>
[CmdletBinding()]
param([string]$SourceDirectory, [string]$Preview)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.Drawing
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $SourceDirectory) { $SourceDirectory = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads' }
if (-not $Preview) { $Preview = Join-Path $repoRoot '.local-test\advisor-portraits.png' }
$outputDir = Join-Path $repoRoot 'gfx\leaders\WFL\advisors'
[IO.Directory]::CreateDirectory($outputDir) | Out-Null
$spec = Get-Content -LiteralPath (Join-Path $repoRoot 'tools\data\advisor_portraits.json') -Raw -Encoding UTF8 | ConvertFrom-Json

function Resize-Portrait([Drawing.Image]$Source, [Drawing.Rectangle]$Crop, [int]$Width, [int]$Height) {
    $bitmap = [Drawing.Bitmap]::new($Width, $Height, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $attributes = [Drawing.Imaging.ImageAttributes]::new()
    try {
        $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $attributes.SetWrapMode([Drawing.Drawing2D.WrapMode]::TileFlipXY)
        $graphics.Clear([Drawing.Color]::FromArgb(31, 36, 29))
        $graphics.DrawImage($Source, [Drawing.Rectangle]::new(0, 0, $Width, $Height),
            $Crop.X, $Crop.Y, $Crop.Width, $Crop.Height, [Drawing.GraphicsUnit]::Pixel, $attributes)
    } finally { $attributes.Dispose(); $graphics.Dispose() }
    return $bitmap
}

function Save-Dds([Drawing.Bitmap]$Bitmap, [string]$Path) {
    $writer = [IO.BinaryWriter]::new([IO.File]::Create($Path))
    try {
        $writer.Write([Text.Encoding]::ASCII.GetBytes('DDS '))
        $header = @([uint32]124, 0x100F, $Bitmap.Height, $Bitmap.Width, ($Bitmap.Width * 4), 0, 0)
        $header += @(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        $header += @(32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, [uint32]4278190080)
        $header += @(0x1000, 0, 0, 0, 0)
        foreach ($number in $header) { $writer.Write([uint32]$number) }
        for ($row = 0; $row -lt $Bitmap.Height; $row++) {
            for ($column = 0; $column -lt $Bitmap.Width; $column++) {
                $color = $Bitmap.GetPixel($column, $row)
                $writer.Write([byte]$color.B); $writer.Write([byte]$color.G)
                $writer.Write([byte]$color.R); $writer.Write([byte]255)
            }
        }
    } finally { $writer.Dispose() }
}

$sheet = [Drawing.Bitmap]::new(904, (12 + [int][Math]::Ceiling($spec.portraits.Count / 4.0) * 332))
$sheetGraphics = [Drawing.Graphics]::FromImage($sheet)
$font = [Drawing.Font]::new('Segoe UI', 11)
try {
    $sheetGraphics.Clear([Drawing.Color]::FromArgb(230, 234, 229))
    $index = 0
    foreach ($entry in $spec.portraits) {
        $sourcePath = Join-Path $SourceDirectory $entry.file
        $source = [Drawing.Image]::FromFile($sourcePath)
        $crop = [Drawing.Rectangle]::new($entry.crop[0], $entry.crop[1], $entry.crop[2], $entry.crop[3])
        try {
            if ($crop.X -lt 0 -or $crop.Y -lt 0 -or $crop.Right -gt $source.Width -or $crop.Bottom -gt $source.Height) {
                throw "Crop outside original photo: $($entry.file)"
            }
            $large = Resize-Portrait $source $crop 156 210
            $small = Resize-Portrait $large ([Drawing.Rectangle]::new(0, 20, 156, 161)) 65 67
            try {
                $stem = 'WFL_advisor_' + $entry.id
                Save-Dds $large (Join-Path $outputDir ($stem + '.dds'))
                Save-Dds $small (Join-Path $outputDir ($stem + '_small.dds'))
                # The cropped PNG is a portable, non-synthesized preview/source.
                $large.Save((Join-Path $outputDir ($stem + '.png')), [Drawing.Imaging.ImageFormat]::Png)
                $x = 20 + ($index % 4) * 224
                $y = 12 + [Math]::Floor($index / 4) * 332
                $sheetGraphics.DrawString(('Portrait ' + $entry.id), $font, [Drawing.Brushes]::Black, $x, $y)
                $sheetGraphics.DrawImageUnscaled($large, $x, ($y + 25))
                $sheetGraphics.DrawImageUnscaled($small, $x, ($y + 243))
                $index++
            } finally { $large.Dispose(); $small.Dispose() }
        } finally { $source.Dispose() }
    }
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($Preview))) | Out-Null
    $sheet.Save($Preview, [Drawing.Imaging.ImageFormat]::Png)
    Write-Output "Created $($spec.portraits.Count) large and small DDS portraits; original photos unchanged."
    Write-Output "Preview: $Preview"
} finally { $sheetGraphics.Dispose(); $sheet.Dispose(); $font.Dispose() }
