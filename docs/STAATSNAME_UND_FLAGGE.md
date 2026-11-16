# Flüren und Groß Flürener Reich

Stand: 16. November 2026.

Der Staat heißt in allen politischen Varianten **Flüren**. Auch Krönung,
Staat 1082 und Hauptstadtprovinz 3512 verwenden diesen Namen. Technische
Kennung WFL und Dateipfade bleiben für bestehende Spielstände erhalten.

Die erfolgreiche Entscheidung zur deutschen Einigung setzt nach Vergabe
der Kerne und Ansprüche den kosmetischen Tag `WFL_GREATER_REICH` mit dem
Namen **Groß Flürener Reich**. Sie entfernt weiterhin den Mobilisierungsgeist.
Ein fehlgeschlagener Entscheidungsabschluss vergibt den Namen nicht.

Für bestehende Spielstände mit `WFL_deutschland_vereint_done` zieht eine
Start-/Tagesaktion den kosmetischen Namen nach, ohne Belohnungen erneut
zu vergeben. Eine spätere Krönung kann den Reichsnamen nicht überschreiben.

Die neue Flagge stammt unverändert aus der vom Nutzer gelieferten Datei
„Waldgrüne Flagge mit goldenem Glockenwappen.png“. Das Original liegt unter
`gfx/flags/source/WFL_flag.png`. Die Umrechnung durch
`python tools/generate_flags.py` erzeugt 45 unkomprimierte 32-Bit-TGAs:

- Größen: 82×52, 41×26 und 10×7 Pixel.
- Kennungen: WFL, WFL_KINGDOM und WFL_GREATER_REICH.
- Jeweils Grundflagge und vier Ideologievarianten, alle mit demselben Motiv.
- Ursprung unten links und passende Rasterreihenfolge gegen die frühere
  verkehrte Darstellung; keine zusätzliche Drehung des gelieferten Motivs.

Der Installer erhält die vollständigen lokalen Vanilla-Farbregister und
ergänzt beide kosmetischen Tags mit dem bisherigen Schützengrün.
Vorhandene eigene Namens- und Porträtpools gelten auch nach der Einigung.

Die Konvertierungsvorschau wurde visuell geprüft. Neue Engine-Sichtprüfung
nach vollständigem Neustart und Laden des Spielstands steht noch aus.
