# Bataillonsversammlung und Vorstand

Stand: 10. November 2026. WFL erhält eine automatische Versammlung und die
Entscheidungskategorie **Vorstand** mit sechs Porträts. Das System funktioniert
unter jeder Regierung. Ein vorgeschalteter Fokus ist nicht erforderlich.

## Termine und Beschlüsse

Die erste Versammlung einer neuen Partie findet am **1. Juli 1936**, die nächste
am **1. Januar 1937** statt; danach folgen jeweils sechs Monatswechsel.
Ein alter Spielstand wird einmalig initialisiert und erhält die erste Sitzung
nach sechs folgenden Monatswechseln. Laden setzt den gespeicherten Zähler nicht
zurück. Während einer Kapitulation pausiert der Zähler; alle Versammlungsboni
und -mali werden entfernt. Nach der Befreiung läuft der Restzähler weiter.

Bei jeder Sitzung erscheint für WFL ein **Nachrichtenfenster mit demselben
gelieferten Saalbild**. Die Abstimmung wird vor dem Öffnen durchgeführt; der
Bestätigungsknopf vergibt keine zweite Belohnung. Drei reguläre Geschichten
wechseln sich ab: verkürzte Tagesordnung, Grillzange als Rednerstab und eine
Handyübertragung der Kasse. Blockade und Eklat erhalten eigene Geschichten.

Jeder der sechs Anträge wird getrennt ausgewürfelt. Unbeeinflusst hat er **35 %**
Zustimmung, mit Zusage **85 %**, bei verärgertem Antragsteller **0 %**. Beschlüsse
gelten bis zur nächsten Sitzung, werden dort zuerst entfernt und neu bewertet.
Sie stapeln sich nicht über mehrere Halbjahre.

| Vorstandsmitglied | Ressort | Beschlossener Bonus |
| --- | --- | --- |
| Nils Meyer | Industrie | +15 % Fabrik- und Werftleistung |
| Jannik Altenschmidt | Bauwesen | +15 % Baugeschwindigkeit für Zivil- und Militärfabriken |
| Tobias Gärtner | Heer | +5 % Heeresangriff, Verteidigung und Organisation |
| Finn Bielig | Versorgung | −10 % Nachschubverbrauch und Heeresausbildungszeit |
| Max Gerwers | Forschung | +5 % Forschung, +10 % Produktionseffizienz-Zuwachs |
| Tim Wissing | Zusammenhalt | +0,15 politische Macht täglich, +5 Prozentpunkte Stabilität |

## Einflussnahme und Streit

Jedes Mitglied kann für **35 politische Macht einmal je Sitzungsperiode**
beeinflusst werden. Die Entscheidung beschreibt seinen Antrag und eine kleine
Geschichte. Das Ergebnis ist sofort in seiner Porträtkarte erkennbar:

- **85 %:** Zusage ohne Nebenwirkung.
- **10 %:** Zusage, aber eines der fünf anderen Mitglieder wird gleichverteilt
  verärgert. Dies kann auch einen bereits unterstützten Kollegen treffen.
- **5 %:** Der angesprochene Schütze wird selbst verärgert und erteilt keine Zusage.

Verärgerte Mitglieder lassen sich in dieser Periode nicht erneut beeinflussen.
Eine spätere Zusage heilt keinen bestehenden Streit. Nach der Versammlung werden
Einflussnahme, Zusagen und Verärgerung für die nächste Runde zurückgesetzt;
die letzten Abstimmungsergebnisse bleiben in den Tooltips sichtbar.

Bei **mindestens zwei verärgerten Mitgliedern** wird zusätzlich ausgewürfelt:

| Wahrscheinlichkeit | Ergebnis |
| --- | --- |
| 70 % | Kein zusätzlicher Malus; normale Einzelabstimmungen |
| 20 % | Blockade: −5 Prozentpunkte Stabilität, −10 % politischer Machtgewinn; Einzelabstimmungen finden statt |
| 10 % | Eklat: alle positiven Anträge scheitern; −10 % Fabrikleistung, −10 % allgemeine Baugeschwindigkeit, −5 % Heeresorganisation |

Auch diese Abzüge gelten nur bis zur nächsten Versammlung. Bei weniger als zwei
verärgerten Mitgliedern wird kein allgemeiner Streitmalus ausgewürfelt.

## Allgemeine Stimmung im Vorstand

Die Porträtkarten zeigen die möglichen Boni jetzt direkt unter ihrem Ressort.
Eine gemeinsame Anzeige ergänzt die Stimmung auf einer Skala von **0 bis 100**;
sie startet bei **75**. Der Wert bleibt über Versammlungen und Spielstände hinweg
erhalten. Auch alte Spielstände mit bereits laufender Bataillonsversammlung
erhalten ihn einmalig, ohne ihren Termin oder ihre Zusagen zurückzusetzen.

| Stimmung | Einordnung | Zusätzlicher Staatsmalus |
| --- | --- | --- |
| 80–100 | Harmonisch | keiner |
| 60–79 | Sachlich | keiner |
| 40–59 | Angespannt | keiner |
| 20–39 | Gespalten | −5 Prozentpunkte Stabilität |
| 0–19 | Feindselig | −10 Prozentpunkte Stabilität |

Diese zwei Stimmungsgeister schließen sich gegenseitig aus; sie stapeln sich
nicht. Sie können zusätzlich zu einer bestehenden Versammlungsblockade wirken.
Während einer Kapitulation sind sie ausgesetzt. Nach der Befreiung gilt wieder
die dem gespeicherten Stimmungswert entsprechende Stufe.

Jede Einflussnahme kostet zusätzlich **12 Stimmungspunkte**. Verärgert sie einen
anderen Schützen, sinkt die Stimmung um weitere **6 Punkte**; eine eigene
Verärgerung kostet weitere **8 Punkte**. Drei erfolgreiche Zusagen ohne
Nebenwirkung senken den Anfangswert damit bereits von 75 auf 39 und lösen den
ersten Stabilitätsmalus aus. Eine erneute Ausführung einer bereits verbrauchten
Einflussentscheidung verändert den Wert nicht.

Eine beschlossene Blockade senkt die Stimmung sofort um **10 Punkte**, ein
Eklat um **20 Punkte**. An jedem aktiven Monatswechsel gilt genau eine der
folgenden Veränderungen, in dieser Reihenfolge:

1. Bei bestehendem Eklat: **−5** Stimmung.
2. Sonst bei bestehender Blockade: **−3** Stimmung.
3. Sonst bei Stimmung unter 40: **−2** Stimmung.
4. Andernfalls: **+2** Stimmung.

Dadurch kann schlechte Stimmung ohne Versöhnung weiter kippen. Werte werden
nach jeder Änderung auf 0–100 begrenzt und der Staatsmalus sofort neu bewertet.
Die halbjährliche Versammlung setzt diesen allgemeinen Stimmungswert nicht
zurück. Der Monatswechsel vor einer Abstimmung berücksichtigt noch die bis
dahin geltenden Beschlüsse.

Drei wiederholbare Entscheidungen helfen beim Gegensteuern:

| Entscheidung | Kosten | Stimmung | Abklingzeit |
| --- | --- | --- | --- |
| Kameradschaftsabend | 35 politische Macht | +15 | 30 Tage |
| Gemeinsamer Kassensturz | 50 politische Macht | +25 | 60 Tage |
| Versöhnungsgrillen | 70 politische Macht | +35 | 90 Tage |

Bei Stimmung 100 oder während einer Kapitulation sind sie nicht verfügbar.
Sie verbessern das gemeinsame Klima, beseitigen aber keine individuelle
Verärgerung und vergeben keine Zusage für einen Antrag. Die Abklingzeiten
werden durch die normalen Entscheidungsregeln der Engine verwaltet.

## Zwei Fokusse für geordnete Verhandlungen

**Geschäftsordnung auf Bierdeckeln** folgt auf den Rat der Bürgerhalle und
dauert **35 Tage**. Nach Abschluss kosten alle drei durch Einflussnahme
verursachten Stimmungsverluste dauerhaft **25 % weniger**:

| Einflussnahme | Bisher | Mit Geschäftsordnung |
| --- | --- | --- |
| Grundverlust bei jedem Versuch | −12 | −9 |
| Zusätzlicher Verlust bei Ärger eines anderen Mitglieds | −6 | −4,5 |
| Zusätzlicher Verlust bei eigener Verärgerung | −8 | −6 |

Die politischen Kosten und Zufallswahrscheinlichkeiten bleiben gleich.
Versammlungsblockaden, Eklats und der monatliche Stimmungsabzug werden durch
die Geschäftsordnung nicht abgeschwächt.

**Der Ältestenrat am Tresen** folgt auf diese Geschäftsordnung und dauert weitere
**35 Tage**. Der Fokus schaltet eine zusätzliche Entscheidung frei:

- **Ältestenrat vermitteln lassen:** 50 politische Macht, 30 Tage Abklingzeit.
- Beruhigt genau **ein** verärgertes Vorstandsmitglied und gibt **+10 Stimmung**.
- Der Beschreibungstext nennt das aktuelle Ziel. Bei mehreren Verärgerten
  vermittelt der Rat in Porträtreihenfolge: Nils, Jannik, Tobias, Finn, Max, Tim.
- Bereits verbrauchte Einflussversuche bleiben verbraucht. Bestehende Zusagen
  bleiben erhalten, der Rat vergibt selbst keine Zusage und würfelt nichts neu.
- Ohne verärgertes Mitglied oder während einer Kapitulation ist die Entscheidung
  gesperrt. Stimmung 100 verhindert die persönliche Aussöhnung nicht; der
  Stimmungszuwachs wird dann auf 100 begrenzt.

Auch bei Ausführung wird erneut geprüft, ob noch ein Mitglied verärgert ist.
Sieben weitere Skripttests prüfen die Fokusbelohnungen, die genauen reduzierten
Kosten in allen sechs Lobbyeffekten, unveränderte Streitfolgen, die Auswahl
genau eines Mitglieds, erneute Guards und den Erhalt von Zusagen/Verbrauchsflags.

Zehn zusätzliche deterministische Skripttests prüfen Migration, Grenzen,
Stabilitätsstufen, sämtliche Einflusszweige, den monatlichen Abwärtseffekt,
schlechte Versammlungen, Erholung, Kapitulation und persistente Werte. Die
Tests führen die tatsächlichen Skripte aus; sie ersetzen weder die Engine
noch eine erneute Sichtprüfung der Vorstandsansicht.

## Grafik und Umsetzung

Die Zuordnung der sechs gelieferten Dateien steht in
`tools/data/WFL_assembly_art.json`; die unveränderten PNGs liegen unter
`gfx/interface/assembly/source/`. `tools/prepare_assembly_art.ps1` erzeugt daraus
128×128-Porträts und das Nachrichtenbild im Vanilla-Format **397×153**. Die
gesamten Motive bleiben durch proportionale Einpassung erhalten; beim Saalbild
entstehen seitliche Randflächen. Es werden keine Personen abgeschnitten.
Die Kartenrahmen sind als einfache grün-goldene UI-Flächen gezeichnet.

Primäre lokale Vorbilder: `00_on_actions.txt` (`on_monthly_GER`), die generische
Decision-Category-Scripted-GUI der australischen/indischen Vanilla-Inhalte,
`eventwindow.gui`, `eventpictures.gfx` und `ideas.gfx`. Verwendete Hooks und
Variablen sind WFL-eigen; bestehender Schützenrat und andere Entscheidungen
werden nicht verändert.

Begrenzte Tests führen die echten Skripte mit Kalender und vorgegebenen
Zufallszweigen aus. Sie prüfen die Termine, alte Spielstände, alle Einfluss-
und Streitfälle, Ersatz alter Beschlüsse, Kapitulation, Porträtzuordnung und
Fensterbindungen. Die Darstellung im Spiel und die tatsächliche Engine-Ausführung
müssen nach einem vollständigen Neustart noch geprüft werden.
