# Reproducible size/format conversion only; the supplied paintings are preserved.
[CmdletBinding()]
param([string]$ProjectRoot, [string]$InputFolder = 'C:/Users/jan_w/Downloads')
$ErrorActionPreference = 'Stop'
if (-not $ProjectRoot) { $ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path) }
Add-Type -AssemblyName System.Drawing
$recipe = Get-Content -LiteralPath (Join-Path $ProjectRoot 'tools/data/WFL_assembly_art.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$folder = Join-Path $ProjectRoot 'gfx/interface/assembly'
$sources = Join-Path $folder 'source'
New-Item -ItemType Directory -Force -Path $sources | Out-Null
function Write-Dds([Drawing.Bitmap]$Bitmap,[string]$Path) {
    $writer = [IO.BinaryWriter]::new([IO.File]::Create($Path))
    try {
        $writer.Write([Text.Encoding]::ASCII.GetBytes('DDS '))
        $header = @(124,0x100F,$Bitmap.Height,$Bitmap.Width,($Bitmap.Width*4),0,0) + @(0,0,0,0,0,0,0,0,0,0,0) + @(32,0x41,0,32,0x00FF0000,0x0000FF00,0x000000FF,[uint32]4278190080) + @(0x1000,0,0,0,0)
        foreach ($number in $header) { $writer.Write([uint32]$number) }
        $rect = [Drawing.Rectangle]::new(0,0,$Bitmap.Width,$Bitmap.Height)
        $data = $Bitmap.LockBits($rect,[Drawing.Imaging.ImageLockMode]::ReadOnly,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
        try {
            $bytes = [byte[]]::new($Bitmap.Width*$Bitmap.Height*4)
            [Runtime.InteropServices.Marshal]::Copy($data.Scan0,$bytes,0,$bytes.Length)
            $writer.Write($bytes)
        } finally { $Bitmap.UnlockBits($data) }
    } finally { $writer.Dispose() }
}
function Convert-Art([string]$Name,[string]$Id,[int]$Width,[int]$Height,[bool]$News) {
    $saved = Join-Path $sources "$Id.png"
    $inputPath = Join-Path $InputFolder $Name
    if (Test-Path -LiteralPath $inputPath) { Copy-Item -LiteralPath $inputPath -Destination $saved -Force }
    $source = [Drawing.Image]::FromFile($saved)
    $bitmap = [Drawing.Bitmap]::new($Width,$Height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [Drawing.Graphics]::FromImage($bitmap)
    try {
        if ($News) { $g.Clear([Drawing.Color]::FromArgb(32,38,32)) } else { $g.Clear([Drawing.Color]::Transparent) }
        $g.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $scale = [Math]::Min($Width/$source.Width,$Height/$source.Height)
        $w = [int][Math]::Round($source.Width*$scale); $h = [int][Math]::Round($source.Height*$scale)
        # Contain the entire image: no faces or people are cropped out.
        $g.DrawImage($source,[Drawing.Rectangle]::new([int](($Width-$w)/2),[int](($Height-$h)/2),$w,$h))
        $bitmap.Save((Join-Path $folder "$Id.png"),[Drawing.Imaging.ImageFormat]::Png)
        Write-Dds $bitmap (Join-Path $folder "$Id.dds")
    } finally { $g.Dispose(); $bitmap.Dispose(); $source.Dispose() }
}
foreach ($member in $recipe.members) { Convert-Art $member.file $member.id 128 128 $false }
Convert-Art $recipe.news 'assembly_hall' 397 153 $true
$card = [Drawing.Bitmap]::new(160,240,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [Drawing.Graphics]::FromImage($card)
$rect = [Drawing.Rectangle]::new(0,0,160,240)
$brush = [Drawing.Drawing2D.LinearGradientBrush]::new($rect,[Drawing.Color]::FromArgb(43,68,52),[Drawing.Color]::FromArgb(20,37,28),90.0)
$gold = [Drawing.Pen]::new([Drawing.Color]::FromArgb(157,135,85))
try {
    $g.FillRectangle($brush,$rect)
    $g.DrawRectangle($gold,1,1,157,237)
    $g.DrawLine($gold,12,129,148,129)
    $card.Save((Join-Path $folder 'board_card.png'),[Drawing.Imaging.ImageFormat]::Png)
    Write-Dds $card (Join-Path $folder 'board_card.dds')
} finally { $gold.Dispose(); $brush.Dispose(); $g.Dispose(); $card.Dispose() }
Write-Output 'Converted six full portraits and the full assembly image to game DDS textures.'
