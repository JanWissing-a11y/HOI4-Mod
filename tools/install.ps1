#requires -Version 5.1
<#
.SYNOPSIS
Installiert ausschließlich diese Mod; Originalspiel und Playsets bleiben unverändert.
.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1
.EXAMPLE
.\tools\install.ps1 -Destination 'C:\Tests mit Umlauten\Mods'
.EXAMPLE
.\tools\install.ps1 -Destination 'C:\Tests\Mods' -RestoreBackup '20261103-123456-abcdef12'
#>
[CmdletBinding()]
param(
    [string]$Destination = (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Paradox Interactive\Hearts of Iron IV\mod'),
    [string]$SourceRoot,
    [string]$GameRoot,
    [string]$RestoreBackup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$projectId = 'HOI4-Wesel-Flueren'
$markerName = '.wesel_flueren_install.json'
$descriptorMarker = '# Managed by HOI4-Wesel-Flueren'
$utf8 = New-Object System.Text.UTF8Encoding($false)
if (-not $SourceRoot) { $SourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path) }

function Assert-ChildPath([string]$Path, [string]$Parent) {
    $resolved = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($Parent).TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
    if (-not $resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Ziel liegt außerhalb des erlaubten Mod-Verzeichnisses: $resolved"
    }
}

function Assert-NoReparsePoint([string]$Path) {
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Verknüpfte Verzeichnisse/Dateien werden aus Sicherheitsgründen nicht verändert: $cursor"
            }
        }
        $parent = Split-Path -Parent $cursor
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}

function Assert-OwnedInstallation([string]$Path) {
    Assert-NoReparsePoint $Path
    $markerPath = Join-Path $Path $markerName
    Assert-NoReparsePoint $markerPath
    if (-not (Test-Path -LiteralPath $markerPath -PathType Leaf)) {
        throw "Vorhandenes Verzeichnis gehört nicht nachweisbar zu dieser Mod: $Path"
    }
    $manifest = Get-Content -LiteralPath $markerPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($manifest.project -ne $projectId -or $manifest.schema -ne 1) {
        throw "Unbekannte Installationsmarkierung: $markerPath"
    }
    $known = @{}
    foreach ($entry in $manifest.files) { $known[$entry] = $true }
    $known[$markerName] = $true
    foreach ($entry in Get-ChildItem -LiteralPath $Path -Recurse -Force) {
        if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Verknüpfung in vorhandener Installation: $($entry.FullName)"
        }
        if (-not $entry.PSIsContainer) {
            $relative = $entry.FullName.Substring($Path.Length + 1).Replace('\', '/')
            if (-not $known.ContainsKey($relative)) {
                throw "Fremde Datei in der Mod-Installation; bitte separat sichern: $relative"
            }
        }
    }
}

function Assert-OwnedDescriptor([string]$Path) {
    if (Test-Path -LiteralPath $Path) {
        Assert-NoReparsePoint $Path
        $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
        if (-not $text.StartsWith($descriptorMarker)) {
            # Paradox Launcher rewrites descriptors and strips comments. Accept
            # that form only alongside a verified owned installation, with the
            # exact live target and the installed descriptor's identity fields.
            $ownedDirectory = Join-Path (Split-Path -Parent $Path) 'wesel_flueren'
            $ownedDescriptor = Join-Path $ownedDirectory 'descriptor.mod'
            $recognized = $false
            if ((Test-Path -LiteralPath $ownedDirectory -PathType Container) -and
                (Test-Path -LiteralPath $ownedDescriptor -PathType Leaf)) {
                Assert-OwnedInstallation $ownedDirectory
                $installedText = Get-Content -LiteralPath $ownedDescriptor -Raw -Encoding UTF8
                $pathMatches = [regex]::Matches($text, '(?m)^\s*path\s*=\s*"([^"\r\n]+)"\s*$')
                if ($pathMatches.Count -eq 1 -and $text -notmatch '(?m)^\s*(archive|replace_path)\s*=') {
                    $referencedPath = [IO.Path]::GetFullPath($pathMatches[0].Groups[1].Value.Replace('/', '\')).TrimEnd('\')
                    $recognized = $referencedPath.Equals([IO.Path]::GetFullPath($target).TrimEnd('\'), [StringComparison]::OrdinalIgnoreCase)
                    foreach ($identityField in @('name', 'version')) {
                        $pattern = '(?m)^\s*' + $identityField + '\s*=\s*"([^"\r\n]+)"\s*$'
                        $actual = [regex]::Matches($text, $pattern)
                        $expected = [regex]::Matches($installedText, $pattern)
                        if ($actual.Count -ne 1 -or $expected.Count -ne 1 -or
                            $actual[0].Groups[1].Value -cne $expected[0].Groups[1].Value) {
                            $recognized = $false
                        }
                    }
                }
            }
            if (-not $recognized) { throw "Launcher-Descriptor gehört nicht nachweisbar zu dieser Mod: $Path" }
        }
    }
}

function Find-GameRoot {
    $libraries = New-Object 'System.Collections.Generic.List[string]'
    $steamSetting = Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -Name SteamPath -ErrorAction SilentlyContinue
    if ($steamSetting) { $libraries.Add($steamSetting.SteamPath) }
    if (${env:ProgramFiles(x86)}) { $libraries.Add((Join-Path ${env:ProgramFiles(x86)} 'Steam')) }
    foreach ($library in @($libraries.ToArray())) {
        $vdf = Join-Path $library 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf) {
            $contents = Get-Content -LiteralPath $vdf -Raw
            foreach ($match in [regex]::Matches($contents, '"path"\s+"([^"]+)"')) {
                $libraries.Add($match.Groups[1].Value.Replace('\\', '\'))
            }
        }
    }
    foreach ($library in $libraries) {
        $candidate = Join-Path $library 'steamapps\common\Hearts of Iron IV'
        if (Test-Path -LiteralPath (Join-Path $candidate 'map\buildings.txt') -PathType Leaf) { return $candidate }
    }
    throw 'HoI4 wurde nicht automatisch gefunden. Bitte -GameRoot mit dem Steam-Spielordner angeben.'
}

function Build-LocalMap([string]$RecipePath, [string]$InstalledGame) {
    $recipe = Get-Content -LiteralPath $RecipePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($recipe.source_state -ne 51 -or $recipe.target_state -ne 1082) { throw 'Unbekanntes Kartenrezept.' }
    $original = Join-Path $InstalledGame 'map\buildings.txt'
    $hashAlgorithm = [Security.Cryptography.SHA256]::Create()
    $stream = [IO.File]::OpenRead($original)
    try { $originalHash = [BitConverter]::ToString($hashAlgorithm.ComputeHash($stream)).Replace('-', '').ToLowerInvariant() }
    finally { $stream.Dispose(); $hashAlgorithm.Dispose() }
    if ($originalHash -ne $recipe.source_sha256.ToLowerInvariant()) {
        throw 'Die Gebäudeplatzierungen passen nicht zur geprüften Spielversion. Installation vor Änderungen abgebrochen.'
    }
    $lines = New-Object 'System.Collections.Generic.List[string]'
    foreach ($line in [IO.File]::ReadAllLines($original)) { $lines.Add($line) }
    foreach ($line in $recipe.remove_lines) {
        if (-not $line.StartsWith('51;')) { throw 'Ungültige Ausgangszeile im Kartenrezept.' }
        $matches = @($lines | Where-Object { $_ -ceq $line })
        if ($matches.Count -ne 1) { throw "Ausgangszeile nicht genau einmal vorhanden: $line" }
        $lines.Remove($line) | Out-Null
    }
    foreach ($line in $recipe.add_lines) {
        if ($line -notmatch '^(51|1082);[^;]+;[^;]+;[^;]+;[^;]+;[^;]+;[^;]+$') { throw 'Ungültige Zielzeile im Kartenrezept.' }
        $lines.Add($line)
    }
    # HoI4's buildings parser treats a final empty line as an invalid record.
    # ReadAllLines already separates the original EOF from appended records,
    # including vanilla files which intentionally have no trailing newline.
    return ($lines -join "`n")
}

function Build-LocalColors([string]$RecipePath, [string]$InstalledGame) {
    $recipe = Get-Content -LiteralPath $RecipePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($recipe.base_tag -ne 'WFL' -or $recipe.cosmetic_tag -ne 'WFL_KINGDOM') { throw 'Unbekanntes Farbrezept.' }
    foreach ($values in @($recipe.map_color, $recipe.ui_color)) {
        if ($values.Count -ne 3) { throw 'Farben benoetigen drei RGB-Werte.' }
        foreach ($value in $values) {
            if (($value -isnot [int] -and $value -isnot [long]) -or $value -lt 0 -or $value -gt 255) { throw 'RGB-Werte muessen ganze Zahlen von 0 bis 255 sein.' }
        }
    }
    $result = @{}
    foreach ($name in @('colors', 'cosmetic')) {
        $relative = "common/countries/$name.txt"
        $original = Join-Path $InstalledGame $relative
        if (-not (Test-Path -LiteralPath $original -PathType Leaf)) { throw "Vanilla-Farbdatei fehlt: $relative" }
        $text = [IO.File]::ReadAllText($original)
        $tag = if ($name -eq 'colors') { $recipe.base_tag } else { $recipe.cosmetic_tag }
        if ($text -match "(?m)^\s*$tag\s*=") { throw "Vanilla definiert bereits den Mod-Farbtag $tag." }
        # These special filenames replace the whole vanilla registry. Preserve
        # every other tag from the installed version and append only our entry.
        $result[$relative] = $text + "`n# Wesel-Flueren: generated from the local vanilla registry.`n$tag = {`n    color = rgb { $($recipe.map_color -join ' ') }`n    color_ui = rgb { $($recipe.ui_color -join ' ') }`n}`n"
    }
    return $result
}

if ([string]::IsNullOrWhiteSpace($Destination)) { throw 'Destination darf nicht leer sein.' }
$destinationRoot = [IO.Path]::GetFullPath($Destination).TrimEnd('\', '/')
Assert-NoReparsePoint $destinationRoot
$cursor = $destinationRoot
while ($cursor) {
    if (Test-Path -LiteralPath (Join-Path $cursor 'hoi4.exe')) {
        throw 'Installationen innerhalb des Originalspiel-Verzeichnisses sind nicht erlaubt.'
    }
    $parent = Split-Path -Parent $cursor
    if ($parent -eq $cursor) { break }
    $cursor = $parent
}
$target = Join-Path $destinationRoot 'wesel_flueren'
$launcher = Join-Path $destinationRoot 'wesel_flueren.mod'
$backupRoot = Join-Path $destinationRoot '.wesel_flueren-backups'
foreach ($entry in @($target, $launcher, $backupRoot)) { Assert-ChildPath $entry $destinationRoot }
if (Test-Path -LiteralPath $target) { Assert-OwnedInstallation $target }
Assert-OwnedDescriptor $launcher

if ($RestoreBackup) {
    if ($RestoreBackup -notmatch '^[a-zA-Z0-9-]+$') { throw 'RestoreBackup muss der angezeigte Sicherungsname sein.' }
    $restorePath = Join-Path $backupRoot $RestoreBackup
    Assert-ChildPath $restorePath $backupRoot
    Assert-NoReparsePoint $restorePath
    Assert-OwnedInstallation (Join-Path $restorePath 'wesel_flueren')
    if (-not (Test-Path -LiteralPath (Join-Path $restorePath 'wesel_flueren.mod') -PathType Leaf)) {
        throw 'Die Sicherung enthält keinen Launcher-Descriptor.'
    }
    Assert-OwnedDescriptor (Join-Path $restorePath 'wesel_flueren.mod')
    $descriptor = Get-Content -LiteralPath (Join-Path $restorePath 'wesel_flueren\descriptor.mod') -Raw -Encoding UTF8
} else {
    $source = (Resolve-Path -LiteralPath $SourceRoot).Path.TrimEnd('\', '/')
    Assert-NoReparsePoint $source
    if ($source -eq $target -or $source.StartsWith($target + '\', [StringComparison]::OrdinalIgnoreCase) -or
        $destinationRoot -eq $source) {
        throw 'Quelle und Installationsziel müssen getrennte Verzeichnisse sein.'
    }
    foreach ($folder in @('common', 'history', 'events', 'localisation', 'gfx', 'interface', 'portraits', 'map')) {
        $payloadFolder = Join-Path $source $folder
        if ($destinationRoot -eq $payloadFolder -or $destinationRoot.StartsWith($payloadFolder + '\', [StringComparison]::OrdinalIgnoreCase)) {
            throw 'Das Installationsziel darf nicht innerhalb der zu kopierenden Mod-Dateien liegen.'
        }
    }
    $descriptorSource = Join-Path $source 'descriptor.mod'
    if (-not (Test-Path -LiteralPath $descriptorSource -PathType Leaf)) { throw 'descriptor.mod fehlt in der Quelle.' }
    $descriptor = Get-Content -LiteralPath $descriptorSource -Raw -Encoding UTF8
    foreach ($required in @('common', 'history', 'events', 'localisation', 'gfx')) {
        if (-not (Test-Path -LiteralPath (Join-Path $source $required) -PathType Container)) {
            throw "Mod-Verzeichnis fehlt: $required"
        }
    }
    $buildingText = $null
    $colorFiles = @{}
    $recipePath = Join-Path $source 'tools\data\building_overrides.json'
    if (Test-Path -LiteralPath $recipePath -PathType Leaf) {
        if (-not $GameRoot) { $GameRoot = Find-GameRoot }
        $GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
        if (Test-Path -LiteralPath (Join-Path $source 'map\buildings.txt')) { throw 'Quelle enthält bereits map/buildings.txt neben dem lokalen Kartenrezept.' }
        $buildingText = Build-LocalMap $recipePath $GameRoot
    }
    $colorRecipePath = Join-Path $source 'tools\data\WFL_country_colors.json'
    if (Test-Path -LiteralPath $colorRecipePath -PathType Leaf) {
        if (-not $GameRoot) { $GameRoot = Find-GameRoot }
        $GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
        foreach ($name in @('colors', 'cosmetic')) {
            if (Test-Path -LiteralPath (Join-Path $source "common/countries/$name.txt")) { throw 'Quelle enthaelt bereits abgeleitete Farbregister neben dem Farbrezept.' }
        }
        $colorFiles = Build-LocalColors $colorRecipePath $GameRoot
    }
}
if ($descriptor -match '(?m)^\s*(path|archive|replace_path)\s*=') {
    throw 'Der Quelldescriptor darf keine path-, archive- oder replace_path-Einträge enthalten.'
}

[IO.Directory]::CreateDirectory($destinationRoot) | Out-Null
$stage = Join-Path $destinationRoot ('.wesel_flueren-stage-' + [guid]::NewGuid().ToString('N'))
Assert-ChildPath $stage $destinationRoot
[IO.Directory]::CreateDirectory($stage) | Out-Null
$stageTarget = Join-Path $stage 'wesel_flueren'
$stageLauncher = Join-Path $stage 'wesel_flueren.mod'
if ($RestoreBackup) {
    Copy-Item -LiteralPath (Join-Path $restorePath 'wesel_flueren') -Destination $stageTarget -Recurse
    $descriptor = Get-Content -LiteralPath (Join-Path $stageTarget 'descriptor.mod') -Raw -Encoding UTF8
} else {
    [IO.Directory]::CreateDirectory($stageTarget) | Out-Null
    $files = New-Object 'System.Collections.Generic.List[string]'
    foreach ($folder in @('common', 'history', 'events', 'localisation', 'gfx', 'interface', 'portraits', 'map')) {
        $sourceFolder = Join-Path $source $folder
        if (-not (Test-Path -LiteralPath $sourceFolder -PathType Container)) { continue }
        Assert-NoReparsePoint $sourceFolder
        foreach ($entry in Get-ChildItem -LiteralPath $sourceFolder -Recurse -Force) {
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Verknüpfung in Mod-Quelle: $($entry.FullName)" }
            if ($entry.PSIsContainer -or $entry.Name -eq '.gitkeep') { continue }
            $relative = $entry.FullName.Substring($source.Length + 1)
            $output = Join-Path $stageTarget $relative
            Assert-ChildPath $output $stageTarget
            [IO.Directory]::CreateDirectory((Split-Path -Parent $output)) | Out-Null
            Copy-Item -LiteralPath $entry.FullName -Destination $output
            $files.Add($relative.Replace('\', '/'))
        }
    }
    Copy-Item -LiteralPath $descriptorSource -Destination (Join-Path $stageTarget 'descriptor.mod')
    $files.Add('descriptor.mod')
    if ($buildingText) {
        [IO.Directory]::CreateDirectory((Join-Path $stageTarget 'map')) | Out-Null
        [IO.File]::WriteAllText((Join-Path $stageTarget 'map\buildings.txt'), $buildingText, $utf8)
        $files.Add('map/buildings.txt')
    }
    foreach ($relative in $colorFiles.Keys) {
        $output = Join-Path $stageTarget $relative
        Assert-ChildPath $output $stageTarget
        [IO.Directory]::CreateDirectory((Split-Path -Parent $output)) | Out-Null
        [IO.File]::WriteAllText($output, $colorFiles[$relative], $utf8)
        $files.Add($relative)
    }
    $manifest = @{ project = $projectId; schema = 1; files = @($files.ToArray()); installedAt = [DateTime]::UtcNow.ToString('o') }
    [IO.File]::WriteAllText((Join-Path $stageTarget $markerName), ($manifest | ConvertTo-Json -Depth 4), $utf8)
}
$escapedPath = $target.Replace('\', '/')
if ($escapedPath.Contains('"')) { throw 'Anführungszeichen im Installationspfad werden nicht unterstützt.' }
[IO.File]::WriteAllText($stageLauncher, ($descriptorMarker + "`n" + $descriptor.TrimEnd() + "`npath=`"$escapedPath`"`n"), $utf8)

$backup = $null
$publishedTarget = $false
$publishedLauncher = $false
try {
    if ((Test-Path -LiteralPath $target) -or (Test-Path -LiteralPath $launcher)) {
        $backupName = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
        $backup = Join-Path $backupRoot $backupName
        Assert-ChildPath $backup $backupRoot
        Assert-NoReparsePoint $backupRoot
        [IO.Directory]::CreateDirectory($backup) | Out-Null
        # Alle zu verschiebenden absoluten Pfade wurden auf die Zielgrenze geprüft.
        if (Test-Path -LiteralPath $target) { [IO.Directory]::Move($target, (Join-Path $backup 'wesel_flueren')) }
        if (Test-Path -LiteralPath $launcher) { [IO.File]::Move($launcher, (Join-Path $backup 'wesel_flueren.mod')) }
    }
    [IO.Directory]::Move($stageTarget, $target)
    $publishedTarget = $true
    [IO.File]::Move($stageLauncher, $launcher)
    $publishedLauncher = $true
} catch {
    if ($publishedLauncher) { [IO.File]::Move($launcher, $stageLauncher) }
    if ($publishedTarget) { [IO.Directory]::Move($target, $stageTarget) }
    if ($backup) {
        if (-not (Test-Path -LiteralPath $target) -and (Test-Path -LiteralPath (Join-Path $backup 'wesel_flueren'))) {
            [IO.Directory]::Move((Join-Path $backup 'wesel_flueren'), $target)
        }
        if (-not (Test-Path -LiteralPath $launcher) -and (Test-Path -LiteralPath (Join-Path $backup 'wesel_flueren.mod'))) {
            [IO.File]::Move((Join-Path $backup 'wesel_flueren.mod'), $launcher)
        }
    }
    throw
}
Remove-Item -LiteralPath $stage
Write-Output "Installiert: $target"
Write-Output "Launcher-Descriptor: $launcher"
if ($backup) { Write-Output "Sicherung: $backup" }
Write-Output 'Im Launcher einem eigenen Playset hinzufügen und aktivieren. Es wurde kein Playset geändert.'
