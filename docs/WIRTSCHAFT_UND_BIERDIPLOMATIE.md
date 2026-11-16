# Wirtschaft, Bierdiplomatie und Römerwardt

Stand: 10. November 2026. Diese Erweiterung ergänzte am 4. November die damaligen
29 Fokusse um 23 auf insgesamt 52. Nach weiteren Ergänzungen, Entfernung des
Alaska-Zweigs und Ergänzung des Beraterstabs umfasst der aktuelle Baum 78 Fokusse. Der sichtbare Name der
Technikschule lautet jetzt **Das Berufskolleg Wesel**;
`WFL_technikschule` bleibt als interne ID für Hersteller und Berater erhalten.

## Gewünschte Wirtschafts- und Armeefokusse

| Fokus | Freischaltung | Belohnung |
| --- | --- | --- |
| Das Berufskolleg Wesel | Gewerbehöfe | Bisheriger Forschungsplatz, dauerhaft +5 % Forschung, zweimal +100 % Industrieforschung |
| Rheinhandel beleben | Werkbank am Niederrhein | Dauerhaft +15 % Baugeschwindigkeit für Zivilfabriken und +15 % für Militärfabriken |
| Rheinblockade | Brauereiverbund → Festlogistik | Dauerhaft weitere +10 % Zivil- und Militärfabrikbau; Deutschland/Niederlande erhalten humorvolle Beitragsforderungen |
| Alkoholfreies Bier verbieten | Übungsplatz am Auesee | Dauerhaft +10 % Armeemoral, im Spiel die Organisationserholung |
| Flachglas zur Rüstungsproduktion umbauen | Rüstungswerkstatt | Sofort +3 Militärfabriken und +3 zusätzliche Bauplätze in Staat 1082 |
| Alles für die Schützenwirtschaft | Flachglasumbau | Sofort das Wirtschaftsgesetz Kriegswirtschaft ohne PP-Kosten; bereits vorhandene Kriegswirtschaft oder totale Mobilmachung bleiben erhalten und geben stattdessen 100 PP |
| Anglo Bier Diplomatie | Vereinsdiplomatie | Drei sichtbare Events; dauerhaft +100 gegenseitige Meinung und +50 Handelsmeinung mit Großbritannien |

Die Rheinblockade ist eine fiktive Komödie um Schützenboote, eine Wäscheleine und
Durchfahrtsgebühren auf Bierdeckeln. Der Wirtschaftsgeist wird direkt durch den
Fokus gewährt, bevor ausländische Antworten eintreffen. Pro Antwort kommen
einmalig 50 PP hinzu; auch Ablehnung oder eine ausbleibende Antwort führen zu
dieser Belohnung. Eine echte Handelssperre wird nicht gesetzt. Einzelheiten und
Verzweigungen stehen in [GEMEINSCHAFT_EVENTS.md](GEMEINSCHAFT_EVENTS.md).

Bei einem regulären Start erhöht das Berufskolleg die Forschungsplätze von zwei
auf drei; der gesonderte Forschungsrat bringt den vierten Platz. Die alte
Technikschulregel bleibt erhalten: Bei bereits mindestens vier Plätzen gibt der
Kollegfokus statt seines Platzes 75 PP. Forschungsgeist und beide Industrieforschungsboni
werden trotzdem gewährt. Die zusätzliche Förderung des Forschungsbundes und das
starke bestehende Atomprogramm bleiben eigenständig.

Der Flachglasumbau prüft beim Abschluss erneut Besitz, volle Kontrolle,
Kapitulation, Entmilitarisierung und die Obergrenze von 20 Militärfabriken je
Staat. Nach drei zusätzlichen Bauplätzen werden tatsächlich drei freie Plätze
verlangt, bevor alle drei Fabriken gebaut werden. Falls das nicht möglich ist,
gibt es 150 PP als Ersatz. Fremde Gebiete werden nicht ausgebaut.

## Luftfahrt und weitere Zweige

**Den Römerwardt ausbauen** eröffnet eine lineare Folge aus Flugschule,
Luftfahrtwerkstätten und Luftwaffenakademie. Insgesamt gibt es 120
Luftwaffenerfahrung, sofort einen Flugplatz auf mindestens Stufe 5 und drei permanente Geister:
+20 % Ausbildungs-EP für Luftgeschwader, −20 % Flugunfälle, +10 % Reichweite und
+10 % Luftmissionseffizienz. Der Flugplatz entsteht ausschließlich im eigenen,
vollständig kontrollierten Staat 1082 außerhalb
einer entmilitarisierten Zone. Andernfalls gibt es 50 PP; die 10 Luftwaffen-EP
des Einstiegs bleiben erhalten. Details: [ROEMERWARDT.md](ROEMERWARDT.md).

Zusätzliche Fokusse vertiefen Vereinsdiplomatie, Brauereien, Versorgung,
Schützenausbildung und den Forschungsbund. Vier Wahlereignisse betreffen
Brauereifest, Schützenolympiade, offene Forschung und einen Weltkongress.
Jeder politische Weg erhält einen weiteren Abschluss.

Das Layout trennt den Forschungszweig seitlich von der Rüstungswerkstatt.
Alle 78 Positionen sind verschieden, alle Voraussetzungen liegen oberhalb der
jeweiligen Folgefokusse. Der Validator prüft diese Eigenschaften sowie eigene
Meinungsmodifier und bedingte Ereignisbeschreibungen.
Der Beraterstab erhält einen eigenen Bereich auf x=34 bis x=42 und y=1 bis y=5.
Das zugehörige Inlay bei x=3300, y=1000 misst 960 × 590 Pixel. Die vorhandenen
Wirtschafts- und Diplomatiepositionen bleiben erhalten; das kontinuierliche
Fokusfeld unten links bleibt frei. Details: [FOKUS_LAYOUT.md](FOKUS_LAYOUT.md)
und [BERATERSTAB.md](BERATERSTAB.md).

## Prüfung und Grenzen

Die neuen Verhaltenstests führen die tatsächlichen Skriptbäume für
Gebäudebelohnungen, Wirtschaftsgesetze, diplomatische Antworten und Wahloptionen
in begrenzten Testwelten aus. Sie prüfen unter anderem verlorene Kontrolle,
Regierungswechsel, bereits erreichte Gebäudegrenzen, spätere Antworten und
ausbleibende Antworten. Diese Tests ersetzen keine Spielengine.

Die zwei im letzten vorhandenen Spielprotokoll beobachteten Berater-/MIO-Fehler
wurden ebenfalls korrigiert; siehe [LAUFZEITKORREKTUREN.md](LAUFZEITKORREKTUREN.md).
Die neuen Inhalte und diese Fehlerkorrekturen benötigen noch einen erneuten
Engine-Lauf. Bestehende Spielstände können bereits abgeschlossene Fokusse nicht
erneut belohnen; für eine vollständige Abnahme ist ein neues Spiel vorgesehen.
