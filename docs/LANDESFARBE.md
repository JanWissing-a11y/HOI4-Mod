# Schützengrün auf der politischen Karte

Stand: 9. November 2026. Die gewünschte Grundfarbe ist **#236B3B**,
RGB **35, 107, 59**. Die hellere UI-Farbe ist RGB **57, 153, 86**.

Die Länderdefinition verwendet jetzt ausdrücklich `color = rgb { 35 107 59 }`.
Zusätzlich hinterlegt `tools/data/WFL_country_colors.json` dieselbe Kartenfarbe
für den echten Tag `WFL` und den bei der Krönung gesetzten kosmetischen Tag
`WFL_KINGDOM`.

`colors.txt` und `cosmetic.txt` sind spezielle Vanilla-Register. Der Installer
liest deshalb beide Dateien aus der vorhandenen Spielversion und ergänzt nur
den jeweiligen Flürener Eintrag in der Modinstallation. Alle vorhandenen
Ländereinträge bleiben erhalten. Die Originalspiel-Dateien werden nicht
verändert; die abgeleiteten Register werden nicht ins Quellpaket aufgenommen.
Das Paket enthält stattdessen das Farbrezept und den Installer.

Zwei Installerprüfungen sichern Grundtag, Königreichsfarbe, UI-Farbe, Erhalt
der ursprünglichen Register, Wiederinstallation und ungültige RGB-Werte ab.
Die Spielaufnahme des Nutzers belegt noch den vorherigen Stand. Die neue
Kartenfarbe benötigt eine erneute Prüfung nach einem vollständigen Spielneustart.
