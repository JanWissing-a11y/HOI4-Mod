# Kartenprüfung: Wesel-Flüren

Stand: 3. November 2026. Ausschließlich lesende Prüfung der lokalen Steam-
Installation unter `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`.
`launcher-settings.json` meldet **1.19.4.1**, Steam-Build **26282552**.
Die Prüfung umfasst Dateien und Kartenpixel, keinen Ingame- oder Nudge-Test.

## Hauptstadt als Kartenannäherung

Für die erste Umsetzung wird **Provinz 3512** als regionale Annäherung an
Wesel/Flüren verwendet. Die Vanilla-Karte bildet Flüren nicht als eigenständige
Provinz ab. Die Zuordnung ist eine geografische Interpretation der verifizierten
Kartenlage; die Vanilla-Dateien benennen Provinz 3512 nicht ausdrücklich „Wesel“.
Sie darf deshalb nicht als exakt nachgewiesene Stadt- oder Ortsteilgrenze gelten.

Folgende Befunde stammen direkt aus der installierten Version:

- `map/definition.csv`: Provinz 3512 besitzt RGB **44,114,13**, ist Land,
  Binnenland und ebenes Gelände auf Kontinent 1.
- `history/states/51-Moselland.txt`: Provinz 3512 gehört zu Staat 51. Dessen
  Provinzen sind 529, 587, 3444, 3512, 3547, 6469, 6570, 9482 und 9522.
  Staat 57 ist `57-Westfalen.txt`; er enthält Provinz 3512 nicht.
- `map/unitstacks.txt`, Platzierungstyp 0: Provinz 3512 liegt bei Kartenkoordinate
  **x=2908, z=1552**. Nachbaranker sind Essen 6469 bei 2914/1544 und Arnhem
  9363 bei 2904/1559. Die Städtenamen stehen in
  `localisation/english/victory_points_l_english.yml`.
- `map/railways.txt`: Die bestehende Bahnstrecke lautet
  `2 4 6469 3512 9363 6241`, also Essen – Provinz 3512 – Arnhem – Utrecht.
- `map/provinces.bmp`: Die Karte misst **5632 × 2048**, 24-Bit-BGR. Die Pixel
  an den von unten gezählten Koordinaten 2908/1552, 2909/1550, 2910/1550,
  2910/1551 und 2909/1551 besitzen sämtlich die Farbe von Provinz 3512.
  Beim Vergleich mit von oben gezählten Bildkoordinaten gilt
  `Bildzeile = 2047 - z`.
- Provinz 529 liegt bei ungefähr 2923/1529 südöstlich von Köln und scheidet
  als sinnvolle Wesel-Annäherung aus. Ihr Geländetyp ist Wald.

Die Provinzlage zwischen Essen und Arnhem am unteren Rhein stützt die Wahl
3512. Die abstrahierte Vanilla-Geografie erlaubt keine Vermessung des tatsächlichen
Gemeindegebiets. Für genauere Grenzen wäre eine eigene Provinzkarte erforderlich.

## Gewählte staatliche Abgrenzung

Der erste Stand trennt **nur Provinz 3512** aus Staat 51 ab und bildet
den neuen Staat **1082**. Die Länderhistorie verwendet `capital = 1082`;
der neue Hauptstadt-Siegpunkt liegt in Provinz 3512. Die höchste vorhandene Vanilla-ID ist 1081
(`1081 - Otago.txt`); alle Staatsdateien wurden dafür nach ihrem tatsächlichen
`id`-Feld geprüft. Provinz 3512 kommt in den Staatsdefinitionen ausschließlich
in Staat 51 vor. Dort existieren keine eigenen Siegpunkte, provinziellen Gebäude
oder datierten Gebäudeeinträge für 3512.

Dadurch bleibt das übrige Rheinland bei Deutschland. Ein Transfer des gesamten
Vanilla-Staates 51 wäre deutlich größer als Wesel/Flüren: Er umfasst unter anderem
Essen und Köln sowie 6.144.743 Einwohner in den ursprünglichen Startdaten.

Die bestehenden `map/strategicregions/7-Western Germany.txt`, Bahnstrecken und
provinzbasierten Einheitenpositionen benötigen durch diesen Split keine neue
Provinz-ID oder neue Grenzgeometrie. Die Provinzpartition der Staatsdateien muss
anschließend auf Vollständigkeit und Eindeutigkeit geprüft werden.

## Gebäude, Flugplätze und Versorgung

`map/buildings.txt` ordnet Gebäudeplätze Staaten zu. Sieben bisherige Plätze
von Staat 51 liegen innerhalb von Provinz 3512 und müssen zum neuen Staat gehören:

| Typ | x | Höhe | z |
| --- | ---: | ---: | ---: |
| arms_factory | 2912.00 | 9.70 | 1550.00 |
| arms_factory | 2914.00 | 9.70 | 1550.00 |
| bunker | 2909.00 | 9.73 | 1550.00 |
| anti_air_building | 2914.00 | 9.70 | 1550.00 |
| supply_node | 2908.00 | 10.00 | 1552.00 |
| special_project_facility_spawn | 2912.00 | 9.70 | 1549.00 |
| stronghold_network | 2906.00 | 10.00 | 1553.00 |

Das Rezept `tools/data/building_overrides.json` verschiebt diese sieben Plätze
und ergänzt weitere Gebäudeplätze des neuen Staates auf sechs bereits vorhandenen,
gegen die Provinzfarbe geprüften Punkten innerhalb 3512. Die Höhen werden von
den vorhandenen Vanilla-Plätzen übernommen. Als Typ- und Anzahlreferenz dient
der Binnenstaat Luxemburg 8: sechs Militär- und sechs Zivilfabrikplätze,
drei Flugabwehrplätze, je zwei Versorgungs-, Bunker- und Spezialprojektplätze
sowie je ein Flugplatz-, Festungsnetz-, Raffinerie-, Treibstoffsilo-, Radar-,
Reaktor- und Raketenplatz. Diese Positionen schaffen keine entsprechenden Gebäude;
sie legen deren grafische Darstellung bei tatsächlichem Bau fest.

Das einzige ursprüngliche `stronghold_network` von Staat 51 liegt in 3512.
Das Rezept ergänzt dafür einen Ersatzplatz im verbleibenden Staat an der
bekannten Essen-Position 2914.00/9.70/1544.00. Insgesamt entfernt es sieben
Originalzeilen und fügt 29 Zeilen hinzu. Die Originaldatei wird vor Anwendung
anhand ihres SHA-256 geprüft:
`0e50dac6146589200105b212cc489c9e68457d0d1e2087bb5211146679374934`.

Der bestehende Flugplatz von Staat 51 liegt bei 2914.92/9.80/1538.32 und bleibt
im bisherigen Staat. Die deutschen 1936-Luft-OOB-Dateien enthalten keinen
expliziten Flugplatzstandort 51. `map/supply_nodes.txt` enthält für das Gebiet
einen festen Knoten in Köln 587, aber keinen festen Knoten in 3512. Die neue
Hauptstadt liegt bereits an der obigen Eisenbahn; tatsächliche Hauptstadtsversorgung
und Gebäudeanzeige müssen trotzdem im Spiel geprüft werden.

Die aus dem lokal installierten `map/buildings.txt` erzeugte Mod-Datei vermeidet,
eine vollständige fremde Spieldatei ins Repository aufzunehmen. Das Spieloriginal
bleibt dabei unverändert. Mehrere Platzierungstypen teilen sich gültige Punkte;
die grafische Entzerrung im Nudge-Werkzeug bleibt eine spätere gestalterische
Aufgabe. Positionen, Höhendarstellung und Versorgung sind nicht in der Engine geprüft.

## Deutschland und das Rheinland

Die beiden geprüften deutschen Heer-OOBs `history/units/GER_1936.txt` und
`GER_1936_nsb.txt` enthalten jeweils 30 Divisionsstandorte. Keiner liegt in einer
der neun ursprünglichen Provinzen von Staat 51. Auch die geprüften deutschen
1936-Marine-OOB-Standorte betreffen diese Provinzen nicht.

Ein Transfer des gesamten Staates 51 würde den historischen deutschen Einstieg
blockieren: `GER_remilitarize_the_rhineland` in
`common/national_focus/germany.txt` verlangt die vollständige deutsche Kontrolle
über die Staaten 42, 51 und 978. Sein Bypass verlangt, dass alle drei bereits
entmilitarisiert sind. Nur die DMZ in Staat 51 zu entfernen reicht dafür nicht.

Der Split von Provinz 3512 vermeidet diesen konkreten Kontrollkonflikt: Deutschland
kann den verbleibenden Staat 51 weiterhin vollständig kontrollieren, dessen DMZ
und datierte Vanilla-Einträge erhalten bleiben. Ein wirklicher historischer
KI-Lauf ist weiterhin erforderlich, bevor die Kompatibilität bestätigt werden kann.
