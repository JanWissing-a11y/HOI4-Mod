# Neue Vereins- und Gemeinschaftsevents

Stand: 9. November 2026. Fiktive humorvolle Erweiterung für Wesel-Flüren.
Die vier Wahlereignisse ergänzen den Fokusbaum. Das Atom-/Flugzeugprogramm
bleibt eigenständig. Das frühere Alaska-Ereignis `.3` wurde mit seinem Zweig
entfernt; die übrigen Ereignis-IDs bleiben erhalten.

| Event | Auslösender Fokus | Erste Wahl | Zweite Wahl |
| --- | --- | --- | --- |
| `wfl_community.1` | `WFL_brauereiverbund` | +5 Prozentpunkte Stabilität, +50 PP | Festkasse: täglich +0,05 PP, +2 Prozentpunkte Stabilität |
| `wfl_community.2` | `WFL_schuetzenolympiade` | +30 Armeeerfahrung, +5 Prozentpunkte Kriegsunterstützung | +0,5 Prozentpunkte rekrutierbare Bevölkerung, -5 % Heeresausbildungszeit |
| `wfl_community.4` | `WFL_tag_der_offenen_labortuer` | Einmal +100 % Industrieforschungsbonus | +100 PP, +5 Prozentpunkte Stabilität |
| `wfl_community.5` | `WFL_weltkongress_des_schuetzenwesens` | +10 Prozentpunkte Stabilität, -5 Prozentpunkte Kriegsunterstützung | +1 Prozentpunkt rekrutierbare Bevölkerung, +5 Prozentpunkte Nichtkern-Mannstärke |

Wahlgeister sind dauerhaft. Die Industriebonus-Kategorie heißt in der lokalen
Vanilla-Version `industry`. Für rekrutierbare Bevölkerung verwenden Länderideen
`conscription`; `recruitable_population` gehört laut Engine-Dokumentation zum
Staatsscope. Schnellere Ausbildung verwendet den negativen Wert von
`training_time_army_factor`.

Jedes Ereignis ist auf WFL und seinen abgeschlossenen Fokus beschränkt,
`fire_only_once = yes` und eine eigene `WFL_community_<n>_resolved`-Flag sichern
die einmalige Nutzung. Jede Option prüft die Verbrauchsflag vor sämtlichen
Belohnungen und setzt sie vor der Auszahlung. Das verhindert auch bei einer
erneuten Optionsausführung zusätzliche Belohnungen oder beide Wahlgeister.

Die Ereignistrigger verlangen bewusst nicht Jan: Veränderte
Voraussetzungen zwischen Fokusabschluss und Auswahl dürfen den Abschluss nicht
verschlucken. Die Optionen der Ereignisse 1, 2 und 5 prüfen erneut, dass Jan
als autoritärer Anführer regiert. Andernfalls gewähren sie einmalig 50 PP.
Das offene Labor steht allen Regierungswegen offen.

Es gibt weder Gebietsübertragungen noch neue Kerne oder automatisch erzeugte
Truppen.

Zusätzliche Fokusgeister: Brauereiverbund (+10 % Zivilfabrikbau), Festlogistik
(-8 % Versorgungsverbrauch), Vereinsdiplomatie (-15 % laufende Kosten für
Beziehungsverbesserung), Schützenakademie (+5 % Heeresorganisation) und
Rheinischer Forschungsbund (+5 % Forschung).

Modifier und Forschungskategorie wurden gegen lokale Vanilla-Skripte und die
Engine-Dokumentation von HoI4 1.19.4.1 geprüft. Darstellung, Wahloptionen und
tatsächliche Boni benötigen zusätzlich eine Prüfung in einer laufenden Partie.

## Rheinblockade und Englandbesuch

`events/WFL_beer_diplomacy.txt` ergänzt sechs sichtbare Ereignisse und zwei
unsichtbare 30-Tage-Abrechnungen im Namespace `wfl_beer`. Der Rheinblockade-Fokus
gewährt seinen dauerhaften Baugeist unabhängig von den Antworten Deutschlands
und der Niederlande (+10 % Zivilfabrikbau und +10 % Militärfabrikbau).

Die Geschichte über Klappstühle, eine Wäscheleine und Forderungen auf Bierdeckeln
verändert weder Schiffsverkehr noch Handelssperren. Deutschland und die
Niederlande dürfen jeweils einen symbolischen Beitrag akzeptieren oder ablehnen.
Bei Annahme kosten sie nur dann 25 PP, wenn sie noch existieren, nicht kapituliert
haben, mehr als 25 PP besitzen und keinen Krieg mit WFL führen; WFL muss ebenfalls
existieren und darf nicht kapituliert haben. Dann erhalten beide Seiten +15
gegenseitige Meinung. Eine Ablehnung erzeugt für zwölf Monate -20 Meinung des
betroffenen Landes gegenüber WFL. WFL erhält pro Partnerantwort einmalig 50 PP,
auch bei Ablehnung, ungültig gewordener Zahlung oder ausbleibender Antwort.
Geschichtenbegründung bei Ablehnung sind die Einnahmen aus Protest-Bierdeckeln.

Der Englandbesuch führt über `wfl_beer.4` (WFL), `.5` (ENG) und `.6` (Abschluss
in WFL). Bei weiterhin existierenden, nicht kapitulierten Ländern ohne
gegenseitigen Krieg entstehen dauerhaft +100 gegenseitige Meinung und +50
gegenseitige Handelsmeinung. WFL erhält zusätzlich 75 PP. Die Handelsmeinung ist
ein separater Vanilla-Meinungsmodifier mit `trade = yes`, kein Fabrik- oder
Ressourcengeschenk. Wenn die Voraussetzungen wegfallen oder die Antwort ausbleibt,
erhält WFL stattdessen einmalig 50 PP. Das Abschlussereignis berichtet je nach
Ergebnis Erfolg oder Abwicklung. Die Texte verwenden die aktuellen Anführer über
`[GER.GetLeader]`, `[HOL.GetLeader]`, `[ENG.GetLeader]` und `[WFL.GetLeader]`.

Beide Ketten sperren bereits abgewickelte Antworten über eigene Flags. Die
unsichtbaren Ereignisse `.7` und `.8` schließen offene Vorgänge nach 30 Tagen;
spätere Antworten erzeugen keine zweite Belohnung. Kein Ereignis erklärt einen
Krieg, überträgt einen Staat/eine Fabrik, erzeugt einen Kern oder tritt einem
Bündnis bei. `tests/test_beer_diplomacy.py` prüft sieben Verhaltensgruppen:
Annahme/Ablehnung, geänderte Teilnehmer, die strikte 25-PP-Grenze, Einmaligkeit,
Abrechnung ausbleibender Antworten, verspätete Antworten sowie dauerhafte,
gegenseitige Freundschaft ohne erzwungene militärische Effekte. Alle sieben Tests
bestanden am 4. November. Die Engine-Abnahme steht aus.
