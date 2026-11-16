# Luftfahrtzweig Römerwardt

Stand: 10. November 2026, lokale Referenz HoI4 1.19.4.2.

WFL beginnt eine neue Partie jetzt mit dem leichten Flugzeug des Jahres 1936
und leichter Flugzeugbewaffnung: Mit **By Blood Alone** sind
`iw_small_airframe`, `basic_small_airframe` (einfache kleine Flugzeugzelle)
und `aa_lmg` (Leichtes MG) erforscht. Dazu kommen `engines_1` und `engines_2`,
damit passende Triebwerke für den Flugzeugentwurf verfügbar sind. Ohne das
Designer-DLC stehen stattdessen `early_fighter` und `fighter1` bereit.
Die Zuordnung folgt den Technologien und DLC-Zweigen der lokalen deutschen
Länderhistorie. Es werden keine kostenlosen Flugzeuge oder fortgeschrittenen
schweren Waffen vergeben. Fallschirmjäger I bleiben ebenfalls erforscht.
Diese Startdaten gelten für neue Partien; laufende Spielstände erhalten die
Technologien durch diese Änderung nicht rückwirkend.

Vier zusammenhängende Fokusse entwickeln den Flugplatz zum Ausbildungs- und
Wartungszentrum. Der Kartenstandort ist eine regionale Abbildung auf der
vorhandenen HoI4-Karte; es wird keine neue historische Flugplatzprovinz angelegt.

| Fokus | Luftwaffenerfahrung | Dauerhafte Förderung |
| --- | ---: | --- |
| Den Römerwardt ausbauen | 10 | Sofort Flugplatz auf mindestens Stufe 5 bei gültigem Standort |
| Die Flugschule Römerwardt | 35 | +20 % Erfahrungsgewinn der Luftgeschwader während der Ausbildung |
| Luftfahrtwerkstätten an der Startbahn | 25 | −20 % Flugunfälle, +10 % Flugzeugreichweite |
| Die Luftwaffenakademie Römerwardt | 50 | +10 % Luftmissionseffizienz |

Die drei nationalen Geister gelten nur für WFL. Ihre Effekte nutzen dieselben
Ländermodifier wie lokale Vanilla-Ideen:

- `air_training_xp_gain_factor`: `common/ideas/air_spirits.txt`,
  `effective_training_programs_spirit`.
- `air_accidents_factor`: dieselbe Datei, `air_crew_surveys_spirit`.
- `air_range_factor`: `common/ideas/belgium.txt`.
- `air_mission_efficiency`: `common/ideas/air_spirits.txt`,
  `centralized_control_spirit`.

Der Flugplatz-Ausbau verlangt beim Abschluss weiterhin eigenen Besitz und
vollständige Kontrolle über Staat 1082, einen nicht entmilitarisierten Standort
und keine Kapitulation. Ein Flugplatz unter Stufe 5 wird unmittelbar auf Stufe 5
gesetzt; Stufe 5 oder höher bleibt erhalten. Bei ungültig gewordenem
Standort erhält WFL 50 politische Macht; die 10 Luftwaffenerfahrung bleiben.
Die vier Fokusse gewähren zusammen 120 Punkte Luftwaffenerfahrung.

Der Ausbildungsbonus erhöht den Erfahrungsgewinn der übenden Luftgeschwader.
Er ist kein zusätzlicher Multiplikator für die jeweils einmalig gewährten
10/35/25/50 Punkte nationaler Luftwaffenerfahrung. Eigene Ideen setzen keine
Luftwaffengeister-DLC-Freischaltung voraus. Die Zahlen verändern die regulären
jeweiligen Modifiersummen im Spiel.

Dieser Zweig fügt keine weiteren Produktionskostenrabatte hinzu. Der bestehende
Fokus „Das Flürener Flugzeugwunder“ mit einem Drittel der normalen Flugzeug-IC
bleibt für die gewünschte dreifache Grundproduktion zuständig.

Der Sofortausbau nutzt `set_building_level` mit `instant_build = yes`, wie in
`common/national_focus/china_nationalist.txt` der lokalen Installation. Der
Stufenschutz nutzt den in `events/NSB_Soviet.txt` verwendeten Vergleich `air_base < ...`.

Die Tests vergleichen die Modifier gegen tatsächlich vorhandene Vanilla-Ideen,
prüfen die WFL-Bindung, die linearen Voraussetzungen der vier Fokusse und das
Fehlen zusätzlicher Flugzeugkostenrabatte. Die Darstellung und die tatsächlichen
Werte im laufenden Spiel müssen weiterhin in der Engine abgenommen werden.
