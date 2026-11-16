#requires -Version 5.1
<#
.SYNOPSIS
Converts the approved PNG flag into forty-five uncompressed 32-bit TGAs.
.DESCRIPTION
All political variants of WFL and its two cosmetic names use the same design. No other flag files
are changed. Run with Python's generate_flags.py bridge or supply -Source and
-FlagsRoot explicitly. An optional contact sheet is saved through -Preview.
#>
[CmdletBinding()]
param(
    [string]$Source,
    [string]$FlagsRoot,
    [string]$Preview
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$repositoryRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $FlagsRoot) { $FlagsRoot = Join-Path $repositoryRoot 'gfx\flags' }
if (-not $Source) { $Source = Join-Path $FlagsRoot 'source\WFL_flag.png' }
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$flagsPath = [IO.Path]::GetFullPath($FlagsRoot)
$sourceImage = [Drawing.Image]::FromFile($sourcePath)

function Resize-Flag([Drawing.Image]$Image, [int]$Width, [int]$Height) {
    $bitmap = [Drawing.Bitmap]::new($Width, $Height, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $attributes = [Drawing.Imaging.ImageAttributes]::new()
    try {
        $graphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceCopy
        $graphics.CompositingQuality = [Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $attributes.SetWrapMode([Drawing.Drawing2D.WrapMode]::TileFlipXY)
        # Preserve the full approved design, matching each size's HoI4 ratio.
        $graphics.DrawImage($Image, [Drawing.Rectangle]::new(0, 0, $Width, $Height),
            0, 0, $Image.Width, $Image.Height, [Drawing.GraphicsUnit]::Pixel, $attributes)
    } catch {
        $bitmap.Dispose()
        throw
    } finally {
        $attributes.Dispose()
        $graphics.Dispose()
    }
    return $bitmap
}

function Encode-Tga([Drawing.Bitmap]$Bitmap) {
    $stream = [IO.MemoryStream]::new()
    $writer = [IO.BinaryWriter]::new($stream)
    try {
        # HoI4 flags use bottom-left raster order, like the local vanilla TGAs.
        # Write matching header AND bottom-to-top rows: top-left TGAs display
        # upside down in-game even though ordinary image viewers honour them.
        # Image type 2; no palette; BGRA pixels; eight alpha bits.
        $writer.Write([byte[]]@(0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        $writer.Write([uint16]$Bitmap.Width)
        $writer.Write([uint16]$Bitmap.Height)
        $writer.Write([byte]32)
        $writer.Write([byte]0x08)
        for ($row = $Bitmap.Height - 1; $row -ge 0; $row--) {
            for ($column = 0; $column -lt $Bitmap.Width; $column++) {
                $color = $Bitmap.GetPixel($column, $row)
                $writer.Write([byte]$color.B)
                $writer.Write([byte]$color.G)
                $writer.Write([byte]$color.R)
                $writer.Write([byte]$color.A)
            }
        }
        $writer.Flush()
        return ,$stream.ToArray()
    } finally {
        $writer.Dispose()
    }
}

$bitmaps = [Collections.Generic.List[Drawing.Bitmap]]::new()
$sizes = @(
    @{ Folder = ''; Width = 82; Height = 52 },
    @{ Folder = 'medium'; Width = 41; Height = 26 },
    @{ Folder = 'small'; Width = 10; Height = 7 }
)
try {
    foreach ($size in $sizes) {
        $bitmap = Resize-Flag $sourceImage $size.Width $size.Height
        $bitmaps.Add($bitmap)
        $bytes = Encode-Tga $bitmap
        $directory = $flagsPath
        if ($size.Folder) { $directory = Join-Path $flagsPath $size.Folder }
        [IO.Directory]::CreateDirectory($directory) | Out-Null
        foreach ($tag in @('WFL', 'WFL_KINGDOM', 'WFL_GREATER_REICH')) {
            foreach ($suffix in @('', '_democratic', '_neutrality', '_fascism', '_communism')) {
                [IO.File]::WriteAllBytes((Join-Path $directory ($tag + $suffix + '.tga')), $bytes)
            }
        }
    }
    if ($Preview) {
        $previewPath = [IO.Path]::GetFullPath($Preview)
        [IO.Directory]::CreateDirectory((Split-Path -Parent $previewPath)) | Out-Null
        $sheet = [Drawing.Bitmap]::new(980, 460, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $graphics = [Drawing.Graphics]::FromImage($sheet)
        $font = [Drawing.Font]::new('Segoe UI', 13)
        $brush = [Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(32, 38, 46))
        $border = [Drawing.Pen]::new([Drawing.Color]::FromArgb(185, 192, 202))
        try {
            $graphics.Clear([Drawing.Color]::FromArgb(240, 243, 247))
            $graphics.DrawString('Flueren - approved green bell flag', $font, $brush, 22, 15)
            $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
            $graphics.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::Half
            $panels = @(
                @{ X = 22; Y = 85; Width = 492; Height = 312; Label = '82 x 52 - enlarged 6x' },
                @{ X = 548; Y = 85; Width = 246; Height = 156; Label = '41 x 26 - enlarged 6x' },
                @{ X = 824; Y = 85; Width = 120; Height = 84; Label = '10 x 7 - 12x' }
            )
            for ($index = 0; $index -lt $panels.Count; $index++) {
                $panel = $panels[$index]
                $graphics.DrawString($panel.Label, $font, $brush, $panel.X, $panel.Y - 28)
                $graphics.DrawImage($bitmaps[$index], [Drawing.Rectangle]::new($panel.X, $panel.Y, $panel.Width, $panel.Height))
                $graphics.DrawRectangle($border, $panel.X, $panel.Y, $panel.Width, $panel.Height)
                $graphics.DrawImageUnscaled($bitmaps[$index], $panel.X, $panel.Y + $panel.Height + 10)
            }
            $sheet.Save($previewPath, [Drawing.Imaging.ImageFormat]::Png)
        } finally {
            $border.Dispose(); $brush.Dispose(); $font.Dispose(); $graphics.Dispose(); $sheet.Dispose()
        }
        Write-Output "Preview: $previewPath"
    }
    Write-Output "Source: $sourcePath ($($sourceImage.Width)x$($sourceImage.Height))"
    Write-Output 'Generated 45 flags for WFL, WFL_KINGDOM and WFL_GREATER_REICH: 82x52, 41x26 and 10x7; uncompressed 32-bit BGRA TGA.'
} finally {
    foreach ($bitmap in $bitmaps) { $bitmap.Dispose() }
    $sourceImage.Dispose()
}
