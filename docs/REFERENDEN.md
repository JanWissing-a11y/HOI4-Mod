# Zwei Referendumsversuche pro Gebiet

Stand: 5. November 2026. Gilt für Rheinland (Staat 51) und Westfalen (57).

Nach „Schützen zu Soldaten“ beginnt einmalig die Überzeugungskampagne für
75 politische Macht und 90 Tage. Ein erfolgreicher Abschluss schaltet den
ersten Referendumsantrag für 100 politische Macht frei. Nach Ablehnung,
Nein-Ergebnis oder Abbruch dieses Antrags wird ein zweiter und letzter Antrag
für weitere 100 politische Macht sichtbar. Die Werbekampagne muss dafür nicht
wiederholt werden. Maximal werden damit 275 politische Macht je Gebiet bezahlt.
Eine abgebrochene Werbekampagne ohne Abschluss schaltet keine Anträge frei.

Vor dem zweiten Antrag müssen das erste Verfahren beendet und sämtliche
Friedens-, Souveränitäts-, Besitz- und Kontrollbedingungen wieder erfüllt sein.
Nach einem erfolgreichen Beitritt entfällt der zweite Antrag dauerhaft, auch
wenn das Gebiet später wieder verloren geht. Kosten werden nicht erstattet.
Die einzelnen Antragsentscheidungen sind jeweils einmalig. Es gibt keinen
dritten Versuch und keine zusätzliche Wartefrist zwischen beendeten Anträgen.

## Verbesserte KI-Chancen

Die Grundgewichte der Zulassung sind jetzt 25 zu 75, die der anschließenden
Abstimmung 60 zu 40. Beide Versuche haben dieselben Chancen. Bestehende
Multiplikatoren bleiben erhalten: Meinung über +25 und über +50 verdoppeln
jeweils das Zulassungsgewicht; demokratische Eigentümer multiplizieren es
zusätzlich mit 1,5, negative Meinung halbiert es. Meinung über +50
multipliziert außerdem das Ja-Gewicht mit 1,5. Gewichte werden anschließend
gegen die jeweilige Nein-/Ablehnungsoption normalisiert.

Für einen nicht demokratischen KI-Eigentümer wie das Deutsche Reich ergeben
sich bei stabilen Beziehungen und fortbestehenden gültigen Bedingungen:

| Meinung des Eigentümers über WFL | Zulassung | Ja nach Zulassung | Beitritt je Versuch | Beitritt über bis zu zwei Versuche |
| --- | ---: | ---: | ---: | ---: |
| Unter 0 | 14,29 % | 60 % | 8,57 % | 16,41 % |
| 0 bis einschließlich +25 | 25 % | 60 % | 15 % | 27,75 % |
| Über +25 bis einschließlich +50 | 40 % | 60 % | 24 % | 42,24 % |
| Über +50 | 57,14 % | 69,23 % | 39,56 % | 63,47 % |

Ein Versuch hat `p = P(Zulassung) × P(Ja | Zulassung)`. Für zwei unabhängige
Versuche mit derselben Erfolgswahrscheinlichkeit ist die Chance mindestens
eines Erfolgs `1 − (1 − p)²`. Änderungen von Beziehungen oder Regierung zwischen
den Ereignissen ändern diese Werte. Menschliche Eigentümer wählen selbst;
die KI-Gewichte sind dann keine Zufallsgarantie.

## Zeit und technische Absicherung

Der Eigentümer erhält den Antrag nach einem Tag. Erst nach seiner Zustimmung
folgt 30 Tage später die Abstimmung. Ein gültiges anerkanntes Ja überträgt
den Staat und gibt WFL einen Kern. Eigentümerwechsel, Teilbesetzung, Krieg,
Kapitulation oder Unterwerfung verhindern die Übertragung und werden beim
Optionsklick erneut geprüft. Unerledigte Verfahren enden nach 120 Tagen.

Die zweite Runde verwendet eigene `second_requested`, `second_pending`,
`second_approved`, `second_resolved` und `second_host`-Flags sowie eigene
Antrags-, Abstimmungs- und Zeitablaufereignisse. Die erste Runde bleibt mit
ihren bisherigen IDs bestehen. Alte 120-Tage-Zeitgeber können die neue Runde
nicht beenden; verspätet angeklickte Erstoptionen können keine neue Runde
auszahlen oder deren Flags löschen. Nur die gültige Schlussoption überträgt
Land und Kernrechte. Das gemeinsame `joined`-Flag sperrt weitere Anträge
nach einem Erfolg. Die Meldungen und Entscheidungstexte nennen beide Versuche.

Gezielte Tests führen die tatsächlichen Skriptblöcke mit einer begrenzten
Scope-Fixture aus: Ablehnung, Nein, Erfolg, Abbruch, Eigentümerwechsel,
Teilkontrolle, verspätete Erstoptionen und alte Zeitgeber werden geprüft.
Das ersetzt keine Abnahme der Ereignisketten in der HoI4-Engine.
