# Forschung und Flugzeugbau

Stand: 9. November 2026. Vier Fokusse erweitern Forschung und Flugzeugfertigung,
dazu kommen zwei nationale Geister. Die Texte liegen vollständig auf Deutsch
und Englisch vor. Der frühere USA-Staatsbesuch samt Alaska-Schenkung wurde
zusammen mit den drei Alaska-Folgefokussen und ihren Ereignissen entfernt.

## Forschung und Atomprogramm

Nach dem Berufskolleg gewährt der **Forschungsrat von Flüren genau einen weiteren
Forschungsplatz**. Eine eigene Flagge sichert diesen zusätzlichen Platz gegen
wiederholte Anwendung derselben Belohnung ab.

Das **Atomprogramm am Auesee** gewährt ausschließlich WFL:

- dauerhaft +300 Prozent Geschwindigkeit nuklearer Technologieforschung;
- drei zusätzliche +300-Prozent-Technologieboni mit vier Jahren Vorlaufabbau;
- gezielt +400 Prozent Projektgeschwindigkeit für Forschungsreaktor,
  Atombombe, Wasserstoffbombe und nukleare Gefechtsköpfe;
- +300 Prozent Baugeschwindigkeit von Nuklearanlagen und beiden
  Forschungsreaktortypen;
- +200 Prozent Produktion von Atom- und Wasserstoffbomben.

Der Laborfokus errichtet eine Nuklearforschungsanlage in Provinz 3512 im eigenen,
vollständig kontrollierten Staat 1082. Bei verlorener Kontrolle, entmilitarisiertem
oder bereits belegtem Standort gibt es stattdessen 150 PP. Einmalig erhält WFL
außerdem einen Nuklearwissenschaftler der Stufe 5 und fünf nukleare Durchbruchpunkte.
Wissenschaftlerzuweisung, Technologien, Projekte und spätere Einsatzvoraussetzungen
bleiben Teil der regulären Spielmechanik. Andere Sonderprojekte erhalten keinen
allgemeinen Geschwindigkeitsbonus.

Die Werte sind aus den lokalen Kategorien nuclear, den Projekten
sp_nuclear_reactor, sp_nuclear_bomb, sp_thermo_nuclear_bomb und
sp_nuclear_warheads sowie der dokumentierten dynamischen Modifierfamilie
<SpecialProject>_speed_factor abgeleitet. Anlagenbau und Wissenschaftlererzeugung
verwenden die lokale Gebäude- und Effektdokumentation der Version 1.19.4.1.

## Dreifache Flugzeugfertigung

Das **Flürener Flugzeugwunder** senkt die IC-Kosten aller 20 vorhandenen
Flugzeug-Basis- und Rollentypen um 66,666667 Prozent auf ein Drittel.
Bei gleicher Fabrikleistung und Effizienz ergibt das ohne weitere Kostenrabatte
die dreifache Stückzahl. Andere Kostenmodifikatoren werden nach den üblichen
additiven Spielregeln verrechnet; Rohstoffmangel und Effizienz bleiben wirksam.

Erfasst sind auch Trägerflugzeuge, Transporter, Aufklärer, Marinevarianten,
Düsenflugzeuge, Raketenabfangjäger, Interkontinentalbomber und Mutterschiffflugzeuge.
Schiffe, Panzer, Infanteriewaffen und Raketenmunition werden nicht verbilligt.
Das Verfahren equipment_bonus/build_cost_ic folgt den vorhandenen SOV-/FIN-Ideen.
Die Ziele stammen aus plane_airframes.txt, x_plane_airframes.txt,
quad_engine_airframe.txt, intercontinental_bomber.txt und mothership.txt.

## Prüfung

tests/test_focus_expansion.py führt den tatsächlichen Forschungsplatz-Effekt
wiederholt aus. Mit lokaler Installation werden alle Flugzeugdefinitionen der
genannten Dateien über ihre Archetypen verfolgt
und auf den Produktionsbonus geprüft. Der Projektvalidator prüft zusätzlich
Referenzen, Lokalisierung und den gesamten Fokusgraph.

Die Tests sind statisch und simulieren nur den benötigten Ausschnitt. Anzeige,
Kostenverrechnung in echten Produktionslinien, Wissenschaftlerzuweisung und
Sonderprojekte benötigen weiterhin eine konkrete Engine-Abnahme.
Die starken Boni sind auf ausdrücklichen Nutzerwunsch gewählt
und keine abgeschlossene Balancebewertung.
