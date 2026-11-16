# Militärstab nach deutschen Vorlagen

Stand: 4. November 2026, lokale Steam-Installation HoI4 1.19.4.1.

Erneut mit HoI4 1.19.4.2 am 8. November verglichen: alle generierten Charakter-
und Lokalisierungsdateien sind unverändert. Im Quellenmanifest wurde nur die
Spielversion aktualisiert.

Wesel-Flüren erhält **36 eigenständige Berater mit 37 Rollen**: sechs Heerchefs,
drei Marinechefs, vier Luftwaffenchefs, 16 Oberkommandos und acht Theoretiker.
Die historischen Anzeigenamen und Fähigkeiten stammen aus Deutschland; die
Bilder sind die bereits vorhandenen, vom Nutzer gelieferten WFL-Fotoausschnitte.
Diese kosmetische Zuordnung behauptet keine Identität der abgebildeten Personen.

## Übernommene Werte

Alle Rollen referenzieren exakt dieselben Vanilla-Eigenschaften wie ihre
deutschen Vorlagen. Dadurch bleiben auch verschachtelte Ausrüstungsboni,
Doktrinbeherrschung, Erfahrungserzeugung, Befehlsmachtkosten und die Erhöhung
des Befehlsmachtlimits erhalten. Es werden keine globalen Traits überschrieben.
Die PP-Basispreise werden unverändert übernommen; nur Lettow-Vorbeck hat keinen
expliziten Preis und verwendet den lokalen Militärberater-Standard von **50 PP**.
Weitere Kostenmodifikatoren im Spiel wirken regulär.

Deutschland-spezifische Fokus-, Regierungs- und Ereignissperren werden durch
WFL-Verfügbarkeit ersetzt, damit der gesamte Katalog bei Flüren einstellbar ist.
Es erfolgt keine kostenlose Ernennung: Die Länderhistorie rekrutiert lediglich
die verfügbaren Charaktere. Die passende Stabsposition muss regulär bezahlt und
besetzt werden. Weder deutsche Charaktere noch deren Rekrutierung werden verändert.
Es werden keine deutschen Generals-, Feldmarschalls-, Admirals-, Wissenschaftler-
oder Regierungsrollen importiert.

Werner von Fritsch hat eine Logistikrolle im Oberkommando und mit Götterdämmerung
zusätzlich eine Heerchefrolle. Er kann nur eine der beiden Positionen gleichzeitig
besetzen. Die DLC-Bedingung der Heerchefrolle bleibt erhalten.
Zusätzlich zu den 34 Charakteren aus GER.txt sind Wilhelm Gebauer und Eugen Beyer
aus AUS.txt enthalten: Ihre Rollen erlauben ausdrücklich auch Deutschland.
Beyers Deutschland-Zulassung besteht nur in der Götterdämmerung-Instanz; diese
DLC-Bedingung wird beibehalten. Die alternative Instanz ohne DLC ist nur für
Österreich erlaubt und wird nicht importiert. Gebauer benötigt keinen DLC.
Nikolaus von Falkenhorsts Rolle in GER.txt ist ausdrücklich nur für Finnland
freigegeben und gehört deshalb nicht zum übernommenen deutschen Katalog.
Die auskommentierte alte Theoretikerrolle Wernher von Brauns ist ebenfalls keine
aktive militärische Beraterrolle und wird nicht übernommen.

## Profile

| Anzeigename | Rolle | Basis-PP | Unveränderte Vanilla-Eigenschaft |
| --- | --- | ---: | --- |
| Werner von Blomberg | Theoretiker | 150 | `grand_battle_plan_expert` |
| Gerd von Rundstedt | Oberkommando | 100 | `army_regrouping_2` |
| Werner von Fritsch | Oberkommando | 100 | `army_logistics_2` |
| Werner von Fritsch | Heerchef (Götterdämmerung) | 100 | `army_chief_army_high_command` |
| Erwin Rommel | Oberkommando | 200 | `army_armored_3` |
| Erich von Manstein | Theoretiker | 150 | `mobile_warfare_expert` |
| Heinz Guderian | Theoretiker | 200 | `blitzkrieg_theorist` |
| Kurt Student | Oberkommando | 100 | `air_airborne_2` |
| Albert Kesselring | Luftwaffenchef | 100 | `air_chief_reform_2` |
| Paul von Lettow-Vorbeck | Oberkommando | 50 | `army_concealment_2` |
| Karl Dönitz | Marinechef | 200 | `navy_chief_commerce_raiding_3` |
| Erich Raeder | Marinechef | 100 | `navy_chief_decisive_battle_2` |
| Alfred Saalwächter | Theoretiker | 150 | `submarine_specialist` |
| Günther Lütjens | Oberkommando | 100 | `navy_fleet_logistics_2` |
| W. von Richthofen | Theoretiker | 150 | `close_air_support_proponent` |
| Walther Wever | Theoretiker | 100 | `air_warfare_theorist` |
| Ernst Udet | Theoretiker | 100 | `dive_bomber` |
| Otto Ciliax | Theoretiker | 100 | `naval_theorist` |
| Ludwig Beck | Heerchef | 100 | `army_chief_organizational_2` |
| Wilhelm Keitel | Heerchef | 100 | `army_chief_drill_2` |
| Franz Halder | Heerchef | 100 | `army_chief_offensive_2` |
| W. von Brauchitsch | Heerchef | 100 | `army_chief_maneuver_2` |
| Rolf Carls | Marinechef | 100 | `navy_chief_maneuver_2` |
| Hermann Göring | Luftwaffenchef | 100 | `GER_reich_marshal` |
| Ritter von Greim | Luftwaffenchef | 100 | `air_chief_all_weather_2` |
| Helmuth Wilberg | Luftwaffenchef | 100 | `air_chief_ground_support_3` |
| Ferdinand Schörner | Oberkommando | 100 | `army_infantry_2` |
| Erich Bey | Oberkommando | 100 | `navy_naval_air_defense_2` |
| Viktor Schütze | Oberkommando | 50 | `navy_submarine_1` |
| Hugo Sperrle | Oberkommando | 100 | `air_close_air_support_2` |
| Erhard Milch | Oberkommando | 100 | `air_tactical_bombing_2` |
| Robert Knauss | Oberkommando | 100 | `air_strategic_bombing_2` |
| Josef Kammhuber | Oberkommando | 100 | `air_bomber_interception_2` |
| Alfred Becker | Oberkommando | 100 | `GER_adaptive_engineer` |
| Walter Dornberger | Oberkommando | 100 | `GER_head_of_the_missile_department` |
| Wilhelm Gebauer | Heerchef | 100 | `army_chief_morale_3` |
| Eugen Beyer | Oberkommando (Götterdämmerung) | 100 | `army_commando_2` |

## Reproduktion und Prüfung

`tools/import_german_military_staff.py --game-root <Spielordner>` erzeugt die
Charaktere, deutsche und englische Lokalisierung mit UTF-8-BOM und das Manifest
`tools/data/WFL_military_staff.json`. Das Manifest enthält die Quell-IDs,
Bildnummern, Preise, Traits samt verschachtelter Definitionen und SHA-256-Werte
der verwendeten Quelldateien. Die Suche nach `original_tag = GER` in sämtlichen
lokalen Charakterdateien ergab nur GER.txt und AUS.txt als einschlägige Quellen.
Der Importer schreibt keine Länderhistorie;
`recruitment_block()` liefert den separat zu integrierenden Rekrutierungsblock.

Die eigenen Charakter-IDs beginnen mit `WFL_staff_`. Ihre Porträts sind für
`army` und `civilian` auf große und kleine vorhandene DDS verbunden. Die
Namenslokalisierung löst auch Vanilla-Verweise wie `$donitz$` vollständig auf.

Die Tests vergleichen den gesamten aktiven GER-Katalog, Basispreise, Ressorts,
Trait-IDs und vollständige Traitdefinitionen mit den lokalen Spieldaten. Sie
prüfen außerdem bezahlte Einstellung, WFL-Scope, Fritschs Doppelrolle und
DLC-Bedingung, Porträtdateien, Namen und eine reproduzierbare Regenerierung.
Eine neue Partie ist für die Startrekrutierung erforderlich. Die Anzeige und
Wirkung aller Positionen müssen noch im laufenden Spiel abgenommen werden.
