# Drei Generäle für Wesel-Flüren

Stand: 4. November 2026. Die Namen wurden vom Nutzer anhand der Bildmotive
bestätigt, nachdem sich die Reihenfolge der Chat-Anlagen als unzuverlässig
erwiesen hatte.

| Name | Bestätigtes Porträt | Stufe | Angriff | Verteidigung | Planung | Logistik |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Ian Jannis Foerster | Wuschelige braune Haare, schwarze Brille, ohne Hut | 8 | 8 | 7 | 9 | 8 |
| Nils Schapfeld I. | Grüner Schützenhut, schwarze Brille, viele Orden | 8 | 7 | 9 | 8 | 9 |
| Lars Stüwe | Kurze braune Haare, ohne Brille und ohne Hut | 8 | 9 | 8 | 8 | 7 |

Alle drei werden als `corps_commander` in der Länderhistorie rekrutiert.
Die militärischen Schwerpunkte sind Spielgestaltung auf Wunsch nach starken
Generälen; sie behaupten keine Eigenschaften der abgebildeten Personen.
Lukas Höhne I. bleibt der Feldmarschall, Jan der Regierungschef.

Die sechs Eigenschaften pro General stammen aus den lokalen Vanilla-Tabellen:

- Ian: `brilliant_strategist`, `organizer`, `trait_engineer`,
  `fortress_buster`, `infantry_leader`, `infantry_expert`.
- Nils: `inflexible_strategist`, `infantry_leader`, `ambusher`, `ranger`,
  `commando`, `organizer`.
- Lars: `brilliant_strategist`, `panzer_leader`, `panzer_expert`, `trickster`,
  `organizer`, `commando`.

Die Auswahl wurde auf Generalrollen, Elternvoraussetzungen und gegenseitige
Ausschlüsse geprüft. Alle fünf gesetzten Fähigkeitswerte sind in den lokalen
Tabellen für `corps_commander` definiert.

Die Quellbilder stammen aus dem Nutzerordner `Desktop/Hoi4mod`:

- Ian: `Porträt eines festlichen Uniformträgers.png`.
- Nils: `Feierliches Porträt im grünen Ordensornat.png`.
- Lars: `Lächelnder Offizier im grünen Ehrenuniform-Look.png`.

Die Motive werden nur zugeschnitten und skaliert. Originale werden ausschließlich
gelesen. Das Manifest `tools/data/commander_portraits.json` hält die bestätigte
Zuordnung, Quellnamen, Ausschnitte und Ausgabepfade fest. Alle Quellen haben
1075 × 1463 Pixel. Ian und Nils verwenden den Ausschnitt `(190,20,720,969)`,
Lars `(230,80,720,969)`. Das vorhandene Werkzeug `tools/prepare_portrait.ps1`
erzeugt je eine große DDS (156 × 210), eine kleine DDS (65 × 67) und eine
PNG-Vorschau. Beide DDS sind unkomprimiertes BGRA.

Die Rekrutierung aus der Länderhistorie wirkt regulär beim Beginn einer neuen
Partie. Eine bereits gespeicherte Partie erhält diese Startcharaktere nicht
automatisch. Porträtanzeige und Fähigkeiten sind noch in der Engine abzunehmen.
