# Reichspfandministerium und Zapfhahnkrise

Stand: 5. November 2026, lokale HoI4-Version 1.19.4.1.

Das Reichspfandministerium folgt auf „Rheinhandel beleben“ und dauert 35 Tage.
Der permanente Wirtschaftsgeist gewährt +15 % Ressourcengewinnung,
−10 % Rohstoffmangelmalus und +5 % Fabrikleistung. Der vorgeschlagene Modifier
`production_factory_resource_factor` wurde in den lokalen Vanilla-Skripten und
englischen Modifiertexten nicht gefunden. Deshalb wird ausdrücklich die
Alternative aus geringerem Rohstoffmangelmalus und höherer Fabrikleistung
verwendet, keine behauptete Verringerung des tatsächlichen Rohstoffverbrauchs.
Alle verwendeten Modifier kommen in lokalen Vanilla-Ideen/Traits vor.

„Die Zapfhahnkrise“ folgt auf „Anglo Bier Diplomatie“ und dauert ebenfalls
35 Tage. Beim Staatsbankett löst britisches Warmbier eine diplomatische
Temperaturdebatte aus. Drei sichtbare Ereignisse führen vom Flürener Protest
über die britische Antwort zum gemeinsamen Kommuniqué. Die Flürener wählen:

- Kühlhandelsvertrag: dauerhaft +10 % Zivilfabrikbau, +5 % Fabrikleistung,
  beidseitig +35 Meinung und +30 Handelsmeinung.
- Freundschaftliches Trinkduell: dauerhaft +5 Prozentpunkte Stabilität,
  +10 % Organisationserholung der Armee und beidseitig +50 Meinung.

Die Krönung oder ein bestimmter britischer Regierungschef wird nicht benötigt;
die Geschichte nennt die Delegationen und den Grafen. Die Folgeboni sind
alternativ und schließen sich durch eine einmalige Wahl aus. Es gibt keine
Kriegserklärung, Kriegsziele, Gebietsübertragung oder aufgezwungene britische
Ausgaben. Die britische Antwort erkennt den gewählten friedlichen Ausgang an.
Antwort und Abschluss besitzen wahlabhängige Beschreibungen: ein konkreter
Eiswürfelvertrag mit Fabriklieferungen oder das unentschiedene Duell zwischen
Jan und `[ENG.GetLeader]` mit verschwundenem Punktestand. Der britische
Regierungschef wird zur Laufzeit aus dem Spielstand eingesetzt.

Bei fehlendem, kapitulierendem oder mit WFL im Krieg befindlichem Großbritannien
greift ein einmaliger Ersatz von 50 politischer Macht. Ein nach 45 Tagen
ausstehender Abschluss wird ebenfalls einmalig durch diesen Ersatz abgegolten.
Pending-/Resolved-/Choice-Flags verhindern doppelte Auszahlung durch späte
Optionen, erneute Ereignisaufrufe oder den Zeitgeber. Die Voraussetzungen
werden sowohl beim Fokusabschluss als auch in der Antwort erneut geprüft.

Eigene Dateien enthalten Ideen, Meinungsmodifier, Ereignisse und DE/EN-Texte.
Gezielte Tests führen die tatsächlichen Belohnungen durch eine begrenzte
Scope-Fixture aus und prüfen beide Zweige, fehlende Partner, Krieg, Zeitablauf
und verspätete Antworten. Eine Prüfung im laufenden Spiel steht noch aus.
