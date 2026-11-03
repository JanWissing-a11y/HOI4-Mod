# HOI4-Mod

Grundgerüst für eine Mod für **Hearts of Iron IV**. Es enthält noch keine
Spieländerungen. Name, Thema und Inhalte können darauf aufbauend entwickelt werden.

## Entwicklung in der Cloud

Die Mod besteht aus Daten- und Skriptdateien. Für dieses Grundgerüst sind weder
Paketinstallation noch Build oder Serverstart erforderlich. Git ist bereits in
der Cloud-Umgebung vorhanden.

Das bestehende Checkout unter `/workspace/HOI4-Mod` verwenden. Ein zusätzliches
Git-Worktree ist nicht erforderlich.

```sh
cd /workspace/HOI4-Mod
git status --short --branch
git diff --check
```

`git diff --check` prüft die Änderungen auf Whitespace-Fehler. Es ersetzt keine
Prüfung durch die Spielengine. Automatisierte Spieltests sind noch nicht vorhanden.

## Struktur

| Pfad | Zweck |
| --- | --- |
| `descriptor.mod` | Gemeinsame Metadaten der Mod |
| `common/` | Beispielsweise nationale Fokusse, Ideen und Entscheidungen |
| `events/` | Ereignisse |
| `history/` | Historische Startdaten, beispielsweise Länder und Staaten |
| `localisation/german/` | Deutsche Texte |
| `localisation/english/` | Englische Texte |
| `gfx/` | Grafiken |

Die `.gitkeep`-Dateien halten zunächst leere Ordner in Git. Sobald ein Ordner
Inhalte enthält, kann seine Platzhalterdatei entfernt werden.

Lokalisierungsdateien benötigen UTF-8 **mit BOM**. Ihre Dateinamen enden zum
Beispiel auf `_l_german.yml` oder `_l_english.yml`; die erste Zeile lautet
entsprechend `l_german:` oder `l_english:`. Andere Textdateien als UTF-8 speichern.

## Lokal in HOI4 laden

Voraussetzung ist eine eigene Installation von Hearts of Iron IV einschließlich
Paradox Launcher. Spieldateien und Zugangsdaten gehören nicht in dieses Repository.

1. Im Paradox Launcher unter den Mod-Werkzeugen eine lokale Mod mit dem Namen
   `HOI4-Mod` und dem Verzeichnis `HOI4-Mod` anlegen. Die Bezeichnungen der
   Menüpunkte können je nach Launcher-Version abweichen.
2. Den Inhalt dieses Repositorys in das erzeugte Mod-Verzeichnis kopieren.
   `descriptor.mod` muss direkt in diesem Verzeichnis liegen. Der Launcher legt
   daneben eine zusätzliche `.mod`-Datei mit dem lokalen Pfad an. Diese
   rechnerabhängige Datei nicht ins Repository übernehmen.
3. Die Mod einem Playset hinzufügen, aktivieren und HOI4 mit `-debug` starten.
4. Ein neues Spiel starten und `logs/error.log` im HOI4-Benutzerdatenverzeichnis
   auf neue, durch die Mod verursachte Meldungen prüfen. Dieses Grundgerüst
   verändert das Spiel noch nicht.

Das Benutzerdatenverzeichnis liegt unter Windows üblicherweise in
`Dokumente/Paradox Interactive/Hearts of Iron IV`, unter Linux in
`~/.local/share/Paradox Interactive/Hearts of Iron IV` und unter macOS in
`~/Documents/Paradox Interactive/Hearts of Iron IV`.

Eine unterstützte Spielversion ist noch nicht deklariert. Nach einem erfolgreichen
Spieltest `supported_version` in `descriptor.mod` passend zur getesteten
HOI4-Version ergänzen. Die Cloud-Umgebung enthält keine HOI4-Installation;
Spielstart und Kompatibilität sind daher hier nicht geprüft.
