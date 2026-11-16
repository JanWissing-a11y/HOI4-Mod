<#
.SYNOPSIS
Creates a 156x210 HOI4 portrait from an original PNG, preserving its image.
Defaults retain the original Jan portrait crop; pass Crop and ExpectedSize for
another supplied portrait. No synthesis or changes to the original image.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Source,
    [string]$Output,
    [string]$SmallOutput,
    [string]$Preview,
    [int[]]$Crop = @(340, 65, 480, 646),
    [int[]]$ExpectedSize = @(1199, 1312)
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Output) { $Output = Join-Path $scriptDirectory '..\gfx\leaders\WFL\Portrait_WFL_jan_graf_von_insel_i.dds' }
if (-not $SmallOutput) { $SmallOutput = Join-Path $scriptDirectory '..\gfx\leaders\WFL\Portrait_WFL_jan_graf_von_insel_i_small.dds' }
if (-not $Preview) { $Preview = Join-Path $scriptDirectory '..\.local-test\portrait-preview.png' }
$sourceImage = [System.Drawing.Image]::FromFile((Resolve-Path -LiteralPath $Source).Path)
$portrait = New-Object System.Drawing.Bitmap 156, 210
$graphics = [System.Drawing.Graphics]::FromImage($portrait)
try {
    if ($ExpectedSize.Count -ne 2 -or $sourceImage.Width -ne $ExpectedSize[0] -or $sourceImage.Height -ne $ExpectedSize[1]) {
        throw 'Original image dimensions do not match ExpectedSize; check the selected crop.'
    }
    if ($Crop.Count -ne 4 -or $Crop[0] -lt 0 -or $Crop[1] -lt 0 -or $Crop[2] -le 0 -or $Crop[3] -le 0 -or
        ($Crop[0] + $Crop[2]) -gt $sourceImage.Width -or ($Crop[1] + $Crop[3]) -gt $sourceImage.Height) {
        throw 'Crop must be a nonempty rectangle within the original image.'
    }
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($sourceImage, [System.Drawing.Rectangle]::new(0, 0, 156, 210),
        [System.Drawing.Rectangle]::new($Crop[0], $Crop[1], $Crop[2], $Crop[3]), [System.Drawing.GraphicsUnit]::Pixel)
    $outputPath = [IO.Path]::GetFullPath($Output)
    $previewPath = [IO.Path]::GetFullPath($Preview)
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($outputPath)) | Out-Null
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($previewPath)) | Out-Null
    $portrait.Save($previewPath, [System.Drawing.Imaging.ImageFormat]::Png)
    # Standard uncompressed DDS header, 32-bit BGRA, matching vanilla portrait dimensions.
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
                $color = $Bitmap.GetPixel($x, $y)
                $writer.Write([byte]$color.B); $writer.Write([byte]$color.G)
                $writer.Write([byte]$color.R); $writer.Write([byte]255)
            }
        }
      } finally { $writer.Dispose() }
    }
    Save-Dds $portrait $outputPath
    $small = [Drawing.Bitmap]::new(65, 67)
    $smallGraphics = [Drawing.Graphics]::FromImage($small)
    try {
        $smallGraphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $smallGraphics.DrawImage($portrait, [Drawing.Rectangle]::new(0, 0, 65, 67),
            [Drawing.Rectangle]::new(0, 20, 156, 161), [Drawing.GraphicsUnit]::Pixel)
        $smallPath = [IO.Path]::GetFullPath($SmallOutput)
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($smallPath)) | Out-Null
        Save-Dds $small $smallPath
    } finally { $smallGraphics.Dispose(); $small.Dispose() }
    Write-Output "Portrait: $outputPath"
    Write-Output "Preview: $previewPath"
} finally {
    $graphics.Dispose(); $portrait.Dispose(); $sourceImage.Dispose()
}
