# Florian Klaus und zusätzliche Rekruten

Stand: 5. November 2026.

## Wirtschaftsberater Florian Klaus

Der vom Nutzer benannte Charakter ist ab Spielstart für regulär 150 politische
Macht als politischer Berater einstellbar. Er belegt einen normalen Beraterplatz.
Die Boni wirken während seiner Anstellung:

| Wirkung | Bonus |
| --- | ---: |
| Zivilfabriken bauen | +20 % |
| Militärfabriken bauen | +20 % |
| Fabrikleistung | +15 % |
| Stabilität | +10 Prozentpunkte |

Sein eigener Trait `WFL_wirtschaftsstratege_mit_ruhiger_hand` verwendet die
lokalen Vanilla-Modifier für diese Wirkungen. Das Nutzerporträt `image.png`
(758 × 827 Pixel) wurde nur zugeschnitten und skaliert. Der Ausschnitt
`(110,15,600,807)` bewahrt Gesicht, Brille, Pfeife und Anzug; die große
Vorschau wurde visuell geprüft. Die Ausgaben sind große DDS (156 × 210), kleine
DDS (65 × 67) und eine PNG-Vorschau. Das Original wird ausschließlich gelesen.
`tools/data/florian_klaus_portrait.json` dokumentiert Quelle und Ausschnitt.

## Staatsgeist: Ein Volk unter dem Schützenhut

Der Staatsgeist ist ab Beginn einer neuen Partie aktiv und nicht regulär
entfernbar. `conscription = 0.20` erhöht die rekrutierbare Bevölkerungsquote
um **20 Prozentpunkte** zusätzlich zum Wehrpflichtgesetz. Es ist kein
relativer Faktor von +20 % auf die bisherige Quote. Die Freiwilligenarmee
liefert lokal 1,5 %; mit dem Staatsgeist sind es vor weiteren Faktoren 21,5 %.

Bei 240.000 Kernbevölkerung erhöht das die potenziell rekrutierbare Bevölkerung
rechnerisch um 48.000 Menschen. Bereits verwendete Rekruten und die normale
Mobilisierung bestimmen, wann und wie viel davon als freie Mannstärke erscheint.
Die Nichtkern-Abzüge und die bestehenden vier Anwerbefeste bleiben wirksam.
Das Wehrpflichtgesetz wird nicht geändert; zusätzliche Gesetzesnachteile werden
durch den Staatsgeist nicht eingeführt.

Beide Ergänzungen verwenden die Länderhistorie. Vorhandene Spielstände
übernehmen ihre Startrekrutierung beziehungsweise den Startgeist nicht
automatisch. Anzeige und tatsächliche Wirkung sind noch in der Engine zu prüfen.
