# Anordnung des Fokusbaums

Stand: 10. November 2026. Der aktuelle Baum enthält **78 Fokusse**. Der komplette
Alaska-Zweig mit USA-Staatsbesuch und drei Folgefokussen wurde entfernt. Die
übrigen Positionen und der Abstand zum kontinuierlichen Fokusfeld bleiben erhalten.
Der Beraterstab ergänzt rechts einen eigenen Bereich mit 21 Fokussen und einem
Informationsfenster für seine drei Sondersitze.
**Dorfkeller Diplomatie** liegt auf x=28, y=5 unter der Zapfhahnkrise und links
neben der Iran-Hochzeit. Römerwardt baut sofort einen Flugplatz auf mindestens Stufe 5.

Historischer Ausgangspunkt: Bei der Layoutarbeit vom 5. November wurden die
damals 52 Fokusse ausschließlich neu angeordnet. IDs, Voraussetzungen,
gegenseitige Ausschlüsse, Icons, Laufzeiten und Belohnungen blieben dabei
unverändert. Reichspfandministerium, Zapfhahnkrise und die vier Iran-Fokusse
erhöhten den Umfang anschließend auf 58, die Dorfkeller Diplomatie zunächst
auf 59. Der Inhaltsvergleich unten belegt ausschließlich diesen früheren Stand.

## Lesefolge

Der Rat der Bürgerhalle bildet den gemeinsamen Einstieg oben. Eine freie Zeile
trennt ihn von den Einstiegen der einzelnen Bereiche. Von links nach rechts:

- Wirtschaft und Forschung: Brauereien links, Berufskolleg mit den beiden
  Forschungsfolgen daneben, Fabriken und Kriegswirtschaft rechts davon.
  Das Reichspfandministerium erhält einen eigenen freien Ast nach Rheinhandel.
- Heer und Luftfahrt: Römerwardt als durchgehende senkrechte Kette; Berliner
  Tor und Gewehre mittig, Festkultur und Schützenakademie rechts. Das
  Flugzeugwunder steht als gemeinsame Abschlussbelohnung darunter.
- Drei politische Wege: Bürgerverfassung, Krone und Schützenverwaltung stehen
  nebeneinander. Rheinland/Westfalen bilden eine symmetrische Gabel mit der
  Niederrheinunion darunter. Die freie Forschungsgemeinschaft bleibt mit ihren
  beiden unveränderten Voraussetzungen verbunden.
- Diplomatie rechts: Vereinsdiplomatie mit Olympiade/Kongress und Bierdiplomatie
  als benachbarte Zweige, Zapfhahnkrise und Dorfkeller Diplomatie unter der
  Bierdiplomatie. Die Iran-Erbfolge, Gesandtschaft, Hochzeit und der Treuevertrag
  bilden außen rechts eine eigene senkrechte Kette auf Spalte 30. Der Einstieg
  setzt Vereinsdiplomatie voraus.
- Beraterstab ganz rechts: Der Schützenrat des Grafen steht auf x=38, y=1.
  Die fünf Ernennungsfokusse verteilen sich auf x=34, 36, 38, 40 und 42 bei
  y=2; die persönlichen Vorhaben folgen jeweils senkrecht auf y=3 bis y=5.
  Unter diesen Reihen zeigt ein eigenes Inlay die drei Sitze, ihre Boni,
  Arbeitstage und die fünf Kandidaten. Einzelheiten: [BERATERSTAB.md](BERATERSTAB.md).
- Vorstand am rechten Rand: „Geschäftsordnung auf Bierdeckeln“ steht auf x=44,
  y=1, „Der Ältestenrat am Tresen“ darunter auf y=2. Beide bleiben oberhalb
  und außerhalb des Beraterstab-Inlays.

Normale Fokusse benutzen nur nichtnegative X-Werte, mit mindestens zwei
Rasterspalten zwischen gleichzeitig angeordneten Nachbarn. Die X-Spanne
beträgt mit den Vorstandsfokussen 44 Rastereinheiten. Der tiefste normale Fokus liegt
auf Zeile 9 statt zuvor 7. Die beiden bereichsübergreifenden Verknüpfungen
bleiben inhaltlich notwendig und wurden nicht durch andere Voraussetzungen
ersetzt. Der erste sichtbare Fokus bleibt der Rat der Bürgerhalle.

## Freie Fläche für kontinuierliche Fokusse

Das wichtige Feld unten links hatte bisher keine eigene Position im WFL-Baum.
Jetzt setzt die Baumdefinition ausdrücklich:

~~~text
continuous_focus_position = { x = 0 y = 1650 }
~~~

Diese Werte sind **Pixel**, während die einzelnen Fokuskoordinaten Rasterwerte
sind. Die lokale Vanilla-Datei `interface/nationalfocusview.gui` definiert:

| Element | Maße |
| --- | --- |
| `focus_spacing` | 96 × 130 Pixel pro Rastereinheit |
| `national_focus_item` | 165 × 128 Pixel |
| `continuous_focus_window` | 770 × 380 Pixel |

Bei der untersten normalen Zeile 9 liegt selbst die konservative Unterkante
mit 50 Pixel Rasterursprung und voller Containerhöhe bei 1348 Pixeln.
Das Panel beginnt bei y=1650, also **302 Pixel darunter**. Auch die gesamte
Verbindungsgeometrie zwischen normalen Fokuszeilen bleibt oberhalb des Panels.
Das Feld steht damit links unterhalb des vollständigen normalen Baumbereichs,
statt einen nur zufällig gerade leeren Zwischenraum zu benutzen. Keine globale
GUI-Datei und kein Vanilla-Panel werden überschrieben.

Das Beraterstabs-Inlay beginnt bei x=3300, y=1000 und misst 960 × 590 Pixel.
Sein Rechteck liegt damit bei x=3300–4260 und y=1000–1590 vollständig rechts
vom kontinuierlichen Fokusfeld. Es überdeckt keine persönlichen Vorhaben der
Zeilen 1–5 und lässt die wichtige Fläche unten links weiterhin frei.

## Prüfung und Vorschau

Ein historischer Vergleich des Skripttexts vor/nach der Layoutänderung vom
5. November ergab Identität,
nachdem ausschließlich die Fokus-X/Y-Zahlen und die neue Panelposition aus dem
Vergleich entfernt wurden. Ein zusätzlicher AST-Vergleich bestätigte die gleiche
Eigenschaft für alle 52 ursprünglichen Fokusse. Die sechs neuen Blöcke sind
zusätzlich unverändert mit den Vorlagen der Inhaltsagents verglichen worden.
Lokale Nachweise liegen unter `.local-test/focus-layout/content-parity.json`,
`content-parity-with-additions.json`, `content-parity-with-iran.json` und dem
vorherigen Skript dort. Diese lokalen Belege sind archivierte Vergleiche des
damaligen Layoutumbaus; sie bilden spätere Inhaltsänderungen und die Entfernung
des Alaska-Zweigs nicht ab.

Zwei Layoutprüfungen sichern mindestens 300 Pixel Abstand des Panels, die freien Fokusrechtecke
und die vollständig aufwärts liegenden Voraussetzungen. Die beiden bestehenden
Validator-Regressionen für Fokusüberlagerung und vertauschte Eltern/Kind-Zeilen
wurden an die neuen Koordinaten angepasst und bestanden ebenfalls.

Reproduzierbare Vorschau:

~~~powershell
python tools/render_focus_layout.py --png
~~~

Die SVG-/PNG-Übersicht wird unter `.local-test/focus-layout` erzeugt. Farben und
beschriftete Rechtecke dienen dort der graphischen Kontrolle; sie ändern keine
Spielgrafiken und sind keine Aufnahme aus der Engine. Die PNG-Vorschau wurde
visuell geprüft. Der Validator mit der lokalen Spielinstallation bestand.
Die abschließende Sichtprüfung bei verschiedenen Zoomstufen in HoI4 bleibt
zusätzlich erforderlich.
