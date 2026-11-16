# Übergabe: Flüren – Die Macht am Niederrhein

**Stand: 16. November 2026.** Dieses Dokument übergibt die bisherige Zusammenarbeit mit Jan und den überprüften Repository-Stand an den nächsten KI-Assistenten.

- Repository: <https://github.com/JanWissing-a11y/HOI4-Mod>, Branch `main`.
- Spielcode-Basis dieser Übergabe: `5a4cde4bcc8f7156424df120bee168db2ec74970` – „Rename country to Flueren and add unified Reich identity with new flag“. Der anschließende Dokumentationscommit enthält diese Übergabe.
- Arbeitsverzeichnis: `C:/Users/jan_w/Documents/ChatGPT/Hoi4 Mod`.
- Statusbegriffe: **umgesetzt** bedeutet vorhandener Code/Assets; **geprüft** nennt jeweils die konkrete Prüfart. Statische Tests, Vorschaurender und Installation ersetzen keine Sicht- und Funktionsprüfung durch die Spielengine.

## 1. Projektziel

Eine eigenständige alternative Geschichtsmod für **Hearts of Iron IV**, beginnend am **1. Januar 1936**. Ein unabhängiger Kleinstaat am Niederrhein entwickelt sich vom örtlichen Schützenwesen zur wirtschaftlichen, militärischen und diplomatischen Großmacht. Der Staat heißt inzwischen ausschließlich **Flüren**. Nach erfolgreicher deutscher Einigung heißt er **Groß Flürener Reich**. „Wesel-Flüren“ in technischen Pfaden ist ein historischer Projektname.

Der Ton ist bewusst überzeichnet: Schützenfeste, Bier, Vereinsbürokratie, persönliche Bekannte und absurde Diplomatie. Sehr starke Boni sind überwiegend ausdrücklich gewünscht. Historische Glaubwürdigkeit und ausgewogene Mehrspielerbalance sind keine Leitziele. Die übrige Welt bleibt weitgehend Vanilla; Polen und Iran erhalten gezielte eigene Herrscher.

### Länder und Start

- Echtes Ländertag **`WFL`**. Staat **1082** enthält nur Provinz **3512**, abgetrennt von Vanilla-Staat 51. Der restliche Staat 51 bleibt deutsch. Die Provinz ist eine regionale Annäherung, keine exakte Stadtgrenze.
- 240.000 Kernbevölkerung, zwei Startdivisionen, drei Divisionsvorlagen und zwei Forschungsplätze. Fallschirmjäger und die vorgesehenen frühen leichten Flugzeug-/Bewaffnungstechnologien sind zu Beginn erforscht, mit DLC-abhängigen Technologievarianten.
- **Jan Graf von Insel I.** führt das autoritäre **Schützenwesen**. Technisch verwendet dieses die vorhandene Hauptideologie `neutrality`; keine neue fünfte Hauptideologie.
- Alternative politische Wege: Bürgerrepublik, königliche Route und Schützenverwaltung. Nicht sämtliche Wege gleichzeitig verfügbar machen.
- **Polen (`POL`)**: neutraler König **Kevin von Beverungen I.**, durchschnittliche Boni.
- **Iran (`PER`)**: besondere Fokusreihe setzt **Al Höhne** ein und macht Iran zur Flürener Marionette.
- Großbritannien und die tatsächlichen Alliierten sind Ziel der Bier-/Dorfkeller-Diplomatie. Deutschland und Niederlande spielen unter anderem bei der Rheinblockade eine Rolle.

Die zwei großen eigenen Verwaltungsmechaniken sind getrennt: **Stab des Grafen** im Fokusbaum und **Vorstand/Bataillonsversammlung** im Entscheidungsfenster. Dazu existieren die normalen politischen Berater, der Militärstab und Hersteller.

## 2. Aktueller Stand

### 2.1 Umfang und belastbare Prüfung

Aktueller statischer Umfang: **78 Fokusse, 48 Events, 38 Entscheidungen in sechs Kategorien, 133 Ideendefinitionen einschließlich 46 sichtbarer Staatsgeister**, 86 Charakterdefinitionen, 52 Traits, 77 Sprites und 45 Flaggen-TGAs. 20 Ideen sind verborgene Rangboni des besonderen Stabs; die Gesamtzahl enthält auch klassische Herstellerprofile. Daher sind Ideenanzahl und sichtbare Staatsgeister nicht gleichzusetzen.

Alle eigenen Texte liegen auf Deutsch und Englisch vor. Die Mod ist installiert und paketierbar. Beim letzten Installationsvergleich waren **328 direkte Quelldateien bytegleich** zur installierten Fassung; abgeleitete Vanilla-Karten-/Farbdateien werden zusätzlich erzeugt. Letzte dokumentierte Installationssicherung: `20261116-175213-38e5bb4e`. Letztes Paket vor diesem Dokument: `dist/wesel_flueren-0.1.0-dev.zip`, 417 Dateien; die Dateizahl ändert sich durch neue Dokumente.

Letzter großer Testlauf: **288 Tests, zunächst zwei Fehler**. Beide Ursachen wurden korrigiert, anschließend bestanden **29 betroffene Tests** sowie **sechs zusätzliche Installertests**. Es wurde danach kein vollständig grüner neuer 288er-Gesamtlauf dokumentiert. Nicht pauschal „288 Tests bestanden“ behaupten. Ausführliche Chronologie: [TESTPROTOKOLL.md](TESTPROTOKOLL.md).

### 2.2 Umgesetzt: Name, Flagge, Farbe und Personen

- Alle Grundideologien und `WFL_KINGDOM` zeigen **Flüren**. Erfolgreiche Einigungsentscheidung setzt `WFL_GREATER_REICH` → **Groß Flürener Reich**.
- Bestehende Einigungssaves werden über Start-/Tagesaktionen nachgezogen. Eine spätere Krönung überschreibt den Reichsnamen nicht. Technisches Tag bleibt `WFL`.
- Neue Nutzerflagge: waldgrün, schwarz-goldenes Kreuz, goldenes Glockenwappen mit Zielscheibe/Eichenlaub. Original: `gfx/flags/source/WFL_flag.png`. Alle drei Identitäten und alle vier Ideologien nutzen dasselbe Motiv.
- Kartenfarbe **RGB 35/107/59, `#236B3B`**; zusätzliche UI-Farbe RGB 57/153/86. Kosmetische Farbregister werden beim Installieren vollständig aus Vanilla übernommen und um die eigenen Tags ergänzt.
- Jan: +15 % politischer Machtgewinn, +10 % Fabrikleistung; eigenes geliefertes Herrscherporträt.
- Feldmarschall **Lukas Höhne I.**: Stufe 9, Angriff/Verteidigung/Planung/Logistik jeweils 9, sieben starke kompatible Eigenschaften. Motiv: grüne Uniform, Schirmmütze, Sonnenbrille.
- Drei Generäle auf Stufe 8, starke spezialisierte Werte. **Verbindliche korrigierte Bildzuordnung:**

| Person | Motiv | Ursprüngliche Bilddatei |
|---|---|---|
| Ian Jannis Foerster | Wuschelige braune Haare, schwarze Brille, ohne Hut | `Porträt eines festlichen Uniformträgers.png` |
| Nils Schapfeld I. | Grüner Schützenhut, schwarze Brille, viele Orden | `Feierliches Porträt im grünen Ordensornat.png` |
| Lars Stüwe | Kurze braune Haare, ohne Brille und Hut | `Lächelnder Offizier im grünen Ehrenuniform-Look.png` |

Die ursprüngliche Chat-Anlagenreihenfolge war missverständlich; die später ausdrücklich bestätigte Motivzuordnung gilt.

- Politischer Berater **Florian Klaus**, Pfeifenporträt: 150 PP, +20 % Zivilfabrikbau, +20 % Militärfabrikbau, +15 % Fabrikleistung, +10 Prozentpunkte Stabilität während seiner Anstellung.
- 37 aus Deutschland übernommene politische Berater mit 39 DLC-Grundvarianten; einschließlich Florian insgesamt **38 Personen/40 Varianten**, dazu acht Aufwertungen. Eigene Namen/Fotos, deutsche Fähigkeiten einschließlich vorhandener Nachteile.
- Deutscher Militärstab: **36 Personen/37 Rollen**, Originalwerte und Kosten; einschließlich zweier auch Deutschland zugänglicher österreichischer Profile. Nicht mit den fünf besonderen Stabsmitgliedern verwechseln.
- **67 klassische Herstellerprofile, 29 MIOs**, ergänzende Herstellerspezialisten. Deutsche Vorbilder mit DLC-Verzweigungen.
- Kevin von Beverungen I.: neutral, +5 % politischer Machtgewinn und +5 Prozentpunkte Stabilität, eigenes Königsporträt. Laufzeitbehandlung ist implementiert, tatsächliches Porträt/Herrscherauswahl noch sichtbar bestätigen.

### 2.3 Umgesetzt: Fokusbaum und Erweiterungen

| Zweig | Verhalten |
|---|---|
| Berufskolleg Wesel | Umbenennung von „Die Technikschule Wesel“, +5 % Forschung und zwei Industrie-Forschungsboni von je 100 %. Technische Fokus-ID bleibt `WFL_technikschule`. |
| Forschungsplätze | Zwei zusätzliche Plätze über Fokusse, bei zwei Startplätzen normalerweise vier insgesamt. |
| Rheinhandel beleben | Dauerhaft je +15 % Baugeschwindigkeit für Zivil- und Militärfabriken. |
| Rheinblockade | Betrunkene Schützen kassieren Durchfahrtsgebühren von Deutschland/Niederlanden; positive wirtschaftliche Wirkung unabhängig von deren Antwort. |
| Alkoholfreies Bier verbieten | +10 % Erholung der Armeeorganisation; dies setzt den Wunsch „Armeemoral“ technisch um. |
| Flachglas zur Rüstungsproduktion umbauen | Drei Militärfabriken samt nötigen Bauplätzen im gültigen eigenen kontrollierten Gebiet; abgesicherter Ersatz von 150 PP, falls die Bauwirkung nicht ausführbar ist. |
| Kriegswirtschaft | Eigener sinnvoll eingeordneter Fokus setzt `war_economy`; eine vorhandene Totalmobilisierung wird nicht verschlechtert. |
| Römerwardt | Vier Fokusse, zusammen 120 Lufterfahrung und Luftfahrtboni. Der erste setzt den Flugplatz auf mindestens Stufe 5; er addiert nicht pauschal fünf Stufen. |
| Atomprogramm | +300 % nukleare Technologieforschung, +400 % Geschwindigkeit für vier benannte Atom-Spezialprojekte, +300 % Reaktor-/Anlagenbau und +200 % Bombenproduktion; Labor in Provinz 3512 sowie Wissenschaftler Stufe 5 mit fünf Durchbruchspunkten. Sehr stark auf Nutzerwunsch. |
| Flugzeugwunder | Alle 20 erfassten Flugzeug-Grund-/Rollenklassen kosten ein Drittel Basis-IC (`build_cost_ic = -0.666666667`). Dadurch ungefähr dreifache Stückzahl bei gleicher IC/Effizienz; weitere Kostenrabatte können additiv wirken. Kein globaler Fabrikleistungsbonus. |
| Reichspfandministerium | +15 % Ressourcen, -10 % Rohstoffmangelmalus, +5 % Fabrikleistung. |
| Anglo Bier Diplomatie | Drei humorvolle Events, gegenseitig +100 Meinung und +50 Handelsmeinung. |
| Zapfhahnkrise | Drei sichtbare Events mit unterschiedlichen Lösungen und Timeout gegen festhängende Ketten. |
| Dorfkeller Diplomatie | 35 Tage nach abgeschlossenem Vorgängerfokus der Zapfhahnkrise; direkter Beitritt zu den tatsächlichen Alliierten unter deren aktueller Führung. Details unten. |
| Iran | Vier Fokusse à 35 Tage: dubiose Erbfolgeunfälle, Höhnes Gesandtschaft, Romanze/Hochzeit mit Prinzessin Shirin, Treuevertrag. Abschluss garantiert Marionetten-Iran mit neutralem **Al Höhne** und Zigarrenporträt, ohne fremdes Zufallsveto. Auch annektierter Iran wird wiederhergestellt; andere Oberherrschaft/Bündnisse/Kriege sind berücksichtigt. Der vorhandene WFL-Feldmarschall bleibt erhalten. |

**Alaska ist ausdrücklich entfernt.** Die früher gewünschte USA-Trinkreise mit Alaska-Geschenk wurde auf späteren Nutzerwunsch vollständig gestrichen. Alte Dokumentationsstellen dazu sind historisch, keine offene Aufgabe.

**Dorfkeller heute:** `common/scripted_triggers/WFL_dorfkeller_triggers.txt` ist maßgeblich. WFL muss unabhängig, nicht kapituliert und bündnislos sein. ENG muss existieren und einem Bündnis mit `faction_template_allies` angehören; dessen tatsächlicher Führer muss existieren, unabhängig und nicht kapituliert sein. Kein Krieg WFLs gegen ENG oder ein anderes Mitglied. **Keine demokratische britische Regierung, keine britische Führungsrolle und keine versteckte Erfolgsflagge erforderlich.** Beim Abschluss wird erneut geprüft; bei inzwischen ungültiger Lage gibt es den vorgesehenen PP-Ersatz statt fehlerhafter Aufnahme.

### 2.4 Umgesetzt: Expansion, Einigung und Rekrutierung

- Rheinland 51 und Westfalen 57: je einmalige Kampagne für 75 PP/90 Tage, danach Referendumsantrag für 100 PP. Genau **ein zweiter Antrag** nach Ablehnung/Abbruch, erneut 100 PP. Bei Zulassung folgt nach 30 Tagen die Abstimmung; Timeouts und Rundenkennungen verhindern verspätete Resultate aus Runde eins in Runde zwei.
- KI-Grundgewichte: Zulassung 25:75, anschließendes Ja 60:40 → **15 % Gesamterfolg pro Versuch**, bei unveränderten Grundchancen **27,75 % über höchstens zwei Versuche**. Beziehungen und Regierungsform verändern Gewichte; menschliche Empfänger wählen selbst. Das ist keine garantierte Anschlusswahrscheinlichkeit.
- Zulassungsgewicht steigt bei Meinung über 25 und über 50 jeweils um Faktor 2, bei demokratischem Besitzer zusätzlich um 1,5; negative Meinung senkt es um Faktor 0,5. Bei Meinung über 50 steigt das Ja-Gewicht der Abstimmung um Faktor 1,5. Gewichte anschließend normalisieren, nicht als direkte Prozentaufschläge lesen.
- Militärische Fokusse vergeben Ansprüche/Kriegsziele gegen den tatsächlichen Besitzer, kein kostenloses Land. Integration nach Besitz, vollständiger Kontrolle und Frieden: 100/150 PP; bereits vorhandene Kerne verhindern Doppelbezahlung.
- Startgeist `WFL_volk_unter_schuetzenhut`: **`conscription = 0.20`**, also **20 zusätzliche Prozentpunkte rekrutierbarer Bevölkerung**, nicht 20 % relative Erhöhung und keine sofortige einmalige Mannstärke. Auf ausdrücklichen Wunsch von 30 auf 20 reduziert. Mit 1,5 % Grundgesetz beispielsweise 21,5 %; bei 240.000 Einwohnern 48.000 zusätzliches Potenzial gegenüber dem Grundgesetz, tatsächliche Mobilisierung nach Spielregeln.
- Vier einmalige humorvolle Anwerbefeste in besetzten Nichtkerngebieten: je `non_core_manpower = 0.05`, zusammen +20 Prozentpunkte. Voraussetzungen prüfen Jan und passende besetzte Gebiete.
- Kostenlose Entscheidung **`WFL_deutschland_unter_schuetzenhut_vereinen`** benötigt die deutschen **Startgebiete von 1936** plus Flüren in eigenem Besitz und vollständig kontrolliert:

  `5, 42, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 763, 909, 978, 1082`.

  Danzig 85, Memel 188, Gdynia 807, Posen 86 und Kattowitz 762 sind **keine zusätzliche Voraussetzung**. Die vorgesehenen östlichen Ansprüche bleiben erhalten. Weitere bereits eigene vollständig kontrollierte deutsche Kerne werden ebenfalls gekernt. Nur erfolgreicher Abschluss entfernt den Mobilisierungsgeist, setzt `WFL_deutschland_vereint_done` und vergibt den Reichsnamen; fehlgeschlagener Abschluss bleibt erneut ausführbar.

### 2.5 Umgesetzt: Stab des Grafen

Inspiriert vom deutschen Beraterstab nach Götterdämmerung, aber mit eigenen WFL-Skripten/Variablen und eigener Fokus-Inlay-GUI. **Fünf Kandidaten, drei besondere Sitze**, getrennt von normalen Beraterplätzen. Voraussetzung: Jan an der Macht, Neutralität, nicht kapituliert.

| Kandidat | Ursprüngliches Porträtabzeichen | Boni vom Grundrang bis Höchstrang |
|---|---|---|
| Dante Grossy | `Militärmedaillon mit goldener Ehrenlaurbe.png` | Organisation +5→15 %, Rekrutierung +1→3 Prozentpunkte, Ausbildungszeit -5→-20 % |
| Neal Foerster | `Goldenes Koch-Abzeichen mit Wasserglas.png` | Versorgung -8→-20 %, Konsumgüterfaktor -3→-6 %, Stabilität +3→10 Prozentpunkte |
| Max Heinsch | `Bronzenes Medaillon mit grünem Uniformporträt.png` | Fabrikleistung +10→25 %, Militärfabrikbau +10→25 %, Effizienzwachstum +5→20 % |
| Max Müller | `Militärisches Porträt mit Lorbeerwappen.png` | Planung +10→25 %, Maximalplanung +5→15 Prozentpunkte, Heeres-XP +10→25 %, Doktrinkosten -5→-20 % |
| Till Hoehne | `Militärisches Porträt mit Lorbeeremblem.png` | Tägliche PP +0,25→0,60, Zivilfabrikbau +10→25 %, Stabilität +3→10 Prozentpunkte |

- Einführungsfokus 35 Tage, Ernennung 14 Tage, 175 Tage Abstand zwischen Ernennungen; bei drei besetzten Sitzen ersetzt ein Dialog einen bisherigen Kandidaten.
- Drei persönliche Projekte pro Kandidat: Vorbereitung 75–120 Tage, Arbeit 140/140/280 Tage. Sie laufen **parallel zum nationalen Fokus**, über gespeicherte Tageszähler.
- Rang 0→3 ersetzt verborgene Ideen; Boni nicht stapeln. Regierungsverlust entlässt den Stab und beendet laufende Arbeit/Boni, abgeschlossene Ränge bleiben gespeichert.
- Alte Ersatzdialoge dürfen nach Regierungsverlust und Rückkehr Jans keine frische unberechtigte Ernennung ermöglichen; abgesichert.
- Fünf freigestellte Abzeichen vorhanden. Nutzer bestätigte die Mechanik, meldete aber Zoomdarstellungsfehler. Fix im Code, neue Engine-Sichtprüfung offen.

### 2.6 Umgesetzt: Vorstand und Bataillonsversammlung

Unabhängig vom Stab: sechs Mitglieder im Entscheidungsfenster, automatische Versammlung **alle sechs Monatswechsel**, erster regulärer Termin 1. Juli 1936, dann 1. Januar 1937 usw. Alte Saves beginnen nach Initialisierung mit sechs weiteren Monatswechseln. Bei Kapitulation pausiert der Kalender; Versammlungsboni und -mali entfallen.

| Mitglied | Fachgebiet | Möglicher Halbjahresbonus |
|---|---|---|
| Nils Meyer | Industrie | +15 % Fabrik- und Werftleistung |
| Jannik Altenschmidt | Bauwesen | Je +15 % Zivil-/Militärfabrikbau |
| Tobias Gärtner | Heer | Je +5 % Angriff, Verteidigung und Organisation |
| Finn Bielig | Versorgung | -10 % Nachschubverbrauch und Ausbildungszeit |
| Max Gerwers | Forschung | +5 % Forschung, +10 % Produktionseffizienzwachstum |
| Tim Wissing | Zusammenhalt | +0,15 tägliche PP, +5 Prozentpunkte Stabilität |

- Eigene Nutzerporträts, Fachgebietsboni und Abstimmungsstatus auf den Karten. Immer Nachrichtenfenster `wfl_assembly.1` mit dem gelieferten Bild **„Schützenversammlung im großen Vereinssaal.png“**; Eventbild 397×153, vollständiges Motiv mit Rand statt unkontrolliertem Beschnitt. Resolution vor dem Fenster, keine erneute Belohnung durch dessen Option.
- Einflussnahme: 35 PP, einmal pro Mitglied/Halbjahr. 85 % Zusage; 10 % Zusage plus Ärger bei einem zufälligen anderen Mitglied; 5 % eigener Ärger.
- Normale Abstimmung: ohne Zusage 35 %, mit Zusage 85 %, verärgert 0 %. Ab zwei verärgerten Mitgliedern: 70 % normaler Ablauf, 20 % Blockade, 10 % Eklat.
- Blockade: -5 Prozentpunkte Stabilität, -10 % PP-Faktor. Eklat: positive Beschlüsse scheitern, -10 % Fabrikleistung/Bautempo, -5 % Organisation. Beschlüsse gelten bis zur nächsten Versammlung.
- Stimmung `WFL_board_mood`: Start 75, begrenzt auf 0–100. Unter 40: -5 Prozentpunkte Stabilität, unter 20 stattdessen -10. Einflussnahme -12 Stimmung; zusätzliche Fremdverärgerung -6, eigene Verärgerung -8. Blockade sofort -10, Eklat -20.
- Monatsänderung nach Priorität: Eklat -5, sonst Blockade -3, sonst Stimmung unter 40 weitere -2, sonst +2. Diese Monatsabzüge werden nicht miteinander gestapelt.
- Erholung: Kameradschaftsabend +15 für 35 PP/30 Tage Abklingzeit, Kassensturz +25 für 50 PP/60 Tage, Versöhnungsgrillen +35 für 70 PP/90 Tage. Diese Entscheidungen beseitigen persönlichen Ärger nicht automatisch.
- Fokus **Geschäftsordnung auf Bierdeckeln**: 35 Tage, Einfluss-Stimmungsverluste -25 % → 9/4,5/6. Folgefokus **Der Ältestenrat am Tresen**: 35 Tage, schaltet Vermittlung für 50 PP/30 Tage frei; beruhigt das erste verärgerte Mitglied in UI-Reihenfolge und gibt +10 Stimmung. Bereits verwendete Einflussnahme/Zusagen bleiben markiert, kein Gratis-Neuwürfeln.

### 2.7 Halb fertig oder noch nicht abgenommen

Der angeforderte Inhalt ist überwiegend implementiert. Hauptlücke ist **Engine-Abnahme**, nicht ein noch leerer Fokusbaum: Zoom-Inlay, Vorstandsanzeige nach Glyphenfix, Dorfkeller im betroffenen Save, Polen-/Iran-Herrscher, Atomprojekte, Flugzeugkosten, Hersteller-/DLC-Varianten, länger laufende Versammlungen sowie neue Flagge/Farbe/Reichsname. Details und Priorität unter 6 und 7.

## 3. Dateistruktur und Zuständigkeiten

Alle folgenden Pfade sind relativ zur Repository-Wurzel; keine gleichnamigen Dateien im installierten Mod-Ordner als primäre Quelle bearbeiten.

| Pfad | Zweck / wichtige Beispiele |
|---|---|
| `descriptor.mod` | Modname, `0.1.0-dev`, Zielversion `1.19.5.*`. Installierbarer externer Descriptor wird vom Installer erzeugt. |
| `common/country_tags/WFL_tags.txt` | Echtes Tag `WFL` → Länderdefinition. |
| `common/countries/Wesel-Flueren.txt` | Ländergrunddaten. Vollständige `colors.txt`/`cosmetic.txt` entstehen lokal beim Installieren, nicht als Vanilla-Kopien ins Repo aufnehmen. |
| `history/countries/WFL - Wesel-Flueren.txt` | Startregierung, Forschung, Geister, Charakterrekrutierung usw. |
| `history/states/51-Moselland.txt`, `1082-Wesel-Flueren.txt` | Bestehenden Vanilla-Staat korrekt überschreiben und neue Provinzpartition anlegen. Exakter Vanilla-Dateiname des Overrides ist wichtig. |
| `history/units/WFL_1936.txt` | Zwei Startdivisionen und drei Vorlagen. |
| `common/bookmarks/WFL_1936.txt` | Eigenes Startlesezeichen „Die Macht am Niederrhein“. |
| `common/national_focus/WFL_focus.txt` | Gesamter Fokusbaum, Voraussetzungen, Positionen, Belohnungen, Inlay und Position kontinuierlicher Fokusse. |
| `common/characters/` | `WFL_characters.txt`, `WFL_generals.txt`, `WFL_lukas_hoehne.txt`, `WFL_florian_klaus.txt`, `WFL_advisors.txt`, `WFL_military_staff.txt`, `WFL_poland.txt`, `WFL_iran.txt`, `WFL_manufacturer_scientists.txt`. |
| `common/country_leader/` | Anführer-/Beratertraits; z. B. `WFL_traits.txt`, `WFL_poland_traits.txt`, `WFL_iran_traits.txt`, `WFL_advisor_upgrade_traits.txt`. |
| `common/ideas/` | Staatsgeister und Hersteller: besonders `WFL_mobilisation.txt`, `WFL_focus_expansion_ideas.txt`, `WFL_beraterstab_ideas.txt`, `WFL_assembly_ideas.txt`, `WFL_board_mood_ideas.txt`. |
| `common/decisions/` | `WFL_referendums.txt`, `WFL_german_integration.txt`, `WFL_recruitment_festivals.txt`, `WFL_advisor_development.txt`, `WFL_assembly.txt`, `WFL_board_mood_decisions.txt`, `WFL_board_elders_decisions.txt`. |
| `common/decisions/categories/` | Sichtbarkeit/Kategoriebeschreibungen, unter anderem Vorstand und deutsche Einigung. |
| `events/` | Hauptdatei `WFL_events.txt`, dazu Referenden, Bierdiplomatie, Zapfhahnkrise, Dorfkeller, Iran, Stab, Versammlung und Gemeinschaftsereignisse in eigenen `WFL_*.txt`. |
| `common/scripted_effects/` | Wiederverwendbare Wirkungen: `WFL_country_name_effects.txt`, `WFL_iran_succession_effects.txt`, `WFL_beraterstab_effects.txt`, `WFL_assembly_effects.txt`, `WFL_board_mood_effects.txt`. |
| `common/scripted_triggers/` | Zentralisierte Bedingungen: besonders `WFL_dorfkeller_triggers.txt`, `WFL_german_integration_triggers.txt`, `WFL_beraterstab_triggers.txt`, `WFL_assembly_triggers.txt`, `WFL_board_elders_triggers.txt`. |
| `common/on_actions/` | Start-/Tages-/Monatshooks: `WFL_country_name_on_actions.txt`, `WFL_assembly_on_actions.txt`, `WFL_beraterstab_on_actions.txt`, `zz_WFL_poland.txt`. Polen gezielt ergänzen statt gesamte Vanilla-Länderhistorie zu ersetzen. |
| `common/scripted_localisation/` | Dynamische Texte für Stab, Vorstand und Versammlungsnachrichten. |
| `common/scripted_guis/WFL_assembly_ui.txt` | Dynamische Entscheidungs-GUI des Vorstands. |
| `common/focus_inlay_windows/WFL_beraterstab.txt` | Bindet den besonderen Stab in den Fokusbaum ein. |
| `interface/WFL_beraterstab.gui`, `WFL_assembly.gui` | Fenster, Karten und Textpositionen. `*.gfx` daneben definiert Sprites/Assets. |
| `common/military_industrial_organization/organizations/WFL_organization.txt` | Eigene Herstellerorganisationen und geerbte Traitbäume. |
| `common/opinion_modifiers/` | Meinungs-/Handelsboni aus Bierdiplomatie und Zapfhahnkrise. |
| `common/names/WFL_names.txt`, `portraits/WFL_portraits.txt` | Namens-/Porträtpools einschließlich beider kosmetischen Tags. |
| `localisation/german/`, `localisation/english/` | Fachweise `WFL_*_l_german.yml` / `_l_english.yml`, identische Schlüsselabdeckung. |
| `gfx/flags/` | 45 TGAs in drei Größen, dazu `source/WFL_flag.png`. |
| `gfx/leaders/` | Spielporträts als DDS, kleine Varianten und vorhandene PNG-Ausgaben. |
| `gfx/interface/assembly/`, `gfx/interface/beraterstab/` | Sechs Vorstandsmitglieder, Saalbild, fünf transparente Stabsabzeichen und Panelgrafik; Quellen/Rezepte soweit vorhanden erhalten. |
| `tools/data/` | JSON-Rezepte/Importmanifeste: Gebäudepositionen, Farben, Berater/Militärstab, Porträtzuschnitte und Versammlungsbilder. |
| `tools/` | Validierung, Installation, Paketbau, Flaggenkonvertierung, Bildaufbereitung, Vanilla-Importer und Layoutvorschauen. |
| `tests/` | Fachbezogene Python-Unittests, begrenzte Skriptausführung, Validator-/Paket-/Installer-Regressionen. |
| `docs/` | Featureverträge, Status, Fehlerhistorie, Testchronik und diese Übergabe. |
| `.local-test/`, `dist/` | Lokale Vorschauen/Testartefakte und ZIP; üblicherweise ignoriert. Keine Spielprotokolle, Dumps oder abgeleiteten vollständigen Vanilla-Dateien veröffentlichen. |

Wichtige vertiefende Dokumente: [BATAILLONSVERSAMMLUNG.md](BATAILLONSVERSAMMLUNG.md), [BERATERSTAB.md](BERATERSTAB.md), [DORFKELLER_DIPLOMATIE.md](DORFKELLER_DIPLOMATIE.md), [DEUTSCHE_EINIGUNG.md](DEUTSCHE_EINIGUNG.md), [STAATSNAME_UND_FLAGGE.md](STAATSNAME_UND_FLAGGE.md), [IRAN_ERBFOLGE.md](IRAN_ERBFOLGE.md), [FOKUS_LAYOUT.md](FOKUS_LAYOUT.md), [LAUFZEITKORREKTUREN.md](LAUFZEITKORREKTUREN.md), [TESTPROTOKOLL.md](TESTPROTOKOLL.md).

**Dokumentationsfallen:** Das ursprüngliche `HOI4_Wesel_Flueren_Codex_Briefing.md` beschreibt teilweise noch einen nicht implementierten Entwurf. `LOKAL_WEITERARBEITEN.md` enthält alte Versions-/Fokuszahlen. `STATUS.md` hat bei Dorfkeller noch frühere strengere Bedingungen; `BERATERSTAB.md` nennt stellenweise ältere Gesamtzahlen 123 Ideen/36 Geister. Das Testprotokoll ist chronologisch: alte Zahlen/Alaska-Abnahmepunkte nicht als aktuellen Vertrag übernehmen. Bei Widerspruch gelten aktuelle Skripte und spätere ausdrückliche Nutzerentscheidungen.

## 4. Konventionen

### IDs, Zustände und Texte

- Tag `WFL` beibehalten; `WFL_KINGDOM` und `WFL_GREATER_REICH` sind nur kosmetische Identitäten. Nicht alle Dateinamen nach „Flüren“ umbenennen: Stabilität bestehender Referenzen/Saves geht vor.
- Fokus-/Entscheidungs-/Ideen-/Trait-/Effekt-IDs überwiegend `WFL_` plus sprechender ASCII-Name in `snake_case`, Umlaute ausgeschrieben: `WFL_geschaeftsordnung_bierdeckel`, `WFL_deutschland_unter_schuetzenhut_vereinen`, `WFL_refresh_country_name`.
- Angezeigte Umbenennung muss keine technische ID ändern: Berufskolleg verwendet weiter `WFL_technikschule`.
- Eventnamespaces klein: `wfl`, `wfl_referendum`, `wfl_beer`, `wfl_zapfhahn`, `wfl_dorfkeller`, `wfl_iran_succession`, `wfl_staff`, `wfl_assembly`, `wfl_community`. Beispiel `add_namespace = wfl_assembly`, Event-ID `wfl_assembly.1`.
- Lokalisierung üblicherweise gleiche ID, Beschreibungen `_desc`, Events beispielsweise `wfl_assembly.1.t` / `.d` / `.a`. Bestehenden Schlüsselstil der jeweiligen Datei fortführen; keine doppelten Schlüssel.
- Country-Flags für dauerhafte Einmalzustände, beispielsweise `WFL_deutschland_vereint_done`; Variablen für Zähler/Stimmung, beispielsweise `WFL_board_mood`. Runde/Zustand vor verspäteten Eventantworten prüfen.
- `ROOT`, `FROM`, Länder-, Staats- und Charakterscopes ausdrücklich beachten. Bedingungen sowohl bei Verfügbarkeit als auch im Abschlusseffekt prüfen, weil sich Weltzustände während Wartezeiten ändern können.
- Runtime-Charakter-ID nicht mit sichtbarem Namen oder Lokalisierungsschlüssel gleichsetzen. Polen/Iran suchen erzeugte Figuren über eindeutige Traits und arbeiten dann im gefundenen Charakterscope.

### Format und Grafik

- Paradox-Skripte: vier Leerzeichen pro Ebene, geschweifte Klammern, `#`-Kommentare, sprechende IDs; kurze einfache Blöcke dürfen einzeilig sein. Bestehenden Dateistil erhalten.
- Lokalisierung: **UTF-8 mit BOM**, `l_german:` beziehungsweise `l_english:`, ein führendes Leerzeichen vor Schlüsseln, z. B. ` WFL_technikschule:0 "Das Berufskolleg Wesel"`. Zeilenumbrüche als `\n`, Farbmarkierung etwa `§G...§!`.
- Im betroffenen GUI-Font **ASCII-Minus `-` verwenden**, nicht U+2212 `−`: Letzteres wurde als Fragezeichen angezeigt.
- Entscheidungs-GUI nutzt normale dynamische Textbindungen. `context_aware_text` aus dem Fokus-Inlay nicht ungeprüft dort übernehmen.
- DDS-/Spritepfade case-/dateigenau referenzieren. Bestehende Nutzerbilder aufbereiten und deren Zuordnung erhalten; keine ersatzweisen KI-Motive erfinden.
- Flaggen: unkomprimierte **32-Bit-BGRA-TGA**, Größen 82×52, 41×26, 10×7. Ursprung unten links, Descriptor `0x08`, dazu von unten nach oben geschriebene Rasterzeilen. Eine scheinbar richtige Desktopvorschau garantiert keine korrekte Ingame-Ausrichtung.
- Fokuslayout: Rasterabstand 96×130; Fokusfläche 165×128. Kontinuierliche Fokusse bei `x = 0, y = 1650`, reserviert 770×380. Letzte normale Reihe y=9 mit etwa 302 Pixeln Abstand zum Panel. Stab rechts: Fokusspalten 34–42, Inlay ungefähr (3300,1000), 960×590; Vorstandsfokusse rechts bei x=44. Keine neuen Inhalte über das linke untere Dauerfokusfeld legen.

## 5. Designentscheidungen und Balancing

1. **Starker Kleinstaat auf Wunsch:** Atomforschung, Flugzeugfertigung, Generäle und Wirtschaftsboni sind bewusst außergewöhnlich stark. Nicht ungefragt auf Vanilla-Niveau abschwächen. Die Reduzierung von 30 auf 20 Prozentpunkte Rekrutierung ist dagegen ausdrücklich beschlossen.
2. **Garantierte Erzählresultate, wo gewünscht:** Iran wird nach vollständiger Fokusreihe Marionette; Rheinblockade bringt immer wirtschaftlichen Nutzen. Vorstand/Referenden haben dagegen offengelegte Zufallsrisiken und Gegenmaßnahmen.
3. **Rekrutierungsgeist endet bei deutscher Einigung:** Der Kleinstaat erhält viel Personalpotenzial, soll dieses aber nach dem Gewinn großer Kernbevölkerung verlieren. Einigung prüft feste 1936-Gebiete, damit spätere deutsche Ansprüche nicht zum unerfüllbaren Pflichtkatalog werden.
4. **Technische Namen stabil halten:** Sichtbarer Landesname ändert sich, echtes Tag und historische Dateipfade bleiben. Start-/Tagesmigration korrigiert alte Einigungssaves ohne erneute Belohnungen.
5. **Flugzeugleistung über Stückkosten:** Ein Drittel IC trifft alle vorgesehenen Flugzeugarten gezielt, ohne sämtliche Rüstung zu verdreifachen. Zusätzliche Rabatte können starke Wechselwirkungen haben; im Spiel prüfen.
6. **Kein Gratisland durch gewöhnliche Kriegszielfokusse:** Rheinland/Westfalen erfordern Krieg oder erfolgreichen friedlichen Prozess. Die ausdrücklich garantierte Iran-Erzählung ist eine eigene Ausnahme.
7. **Stab und Vorstand haben verschiedene Rollen:** Stab = langfristige Auswahl/Entwicklung von drei aus fünf Personen unter Jan. Vorstand = sechs parallele Ressorts mit Halbjahrespolitik, Stimmung und Streit, auch ohne vorherigen Fokus freigeschaltet.
8. **Stimmung erzeugt Kosten für Einflussnahme:** Viele Zusagen sollen nicht kostenlos alle Boni sichern. Vermittlung und Erholungsentscheidungen geben Handlungsspielraum; global bessere Stimmung löscht persönlichen Ärger nicht pauschal.
9. **Gezielte Vanilla-Ergänzung:** Deutsche Berater/Hersteller übernehmen Fähigkeiten und DLC-Unterschiede. Polen wird über eigenen Hook ergänzt; vollständige Vanilla-Länderhistorien nicht unnötig überschreiben. Installer erzeugt große Karten-/Farbdateien aus lokalen Originalen.
10. **UI und Lesbarkeit sind Teil der Funktion:** Alle Boni, Abstimmungszustände, Stimmung und Wartezeiten sichtbar. Nutzer legt besonderen Wert auf Zoom und das freie Feld kontinuierlicher Fokusse.

## 6. Bekannte Bugs, Protokolle und bisherige Versuche

### 6.1 Neuester echter Spielprotokollstand

Pfad: `C:/Users/jan_w/Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log`, zuletzt geändert **13.11.2026, 17:11:40**, 2.845 Bytes. `system.log` bestätigt **1.19.5.0.7c6c** und genau **eine aktive Mod**, damals noch unter dem Namen „Wesel-Flüren – Die Macht am Niederrhein“. `game.log` zeigt eine Partie bis **1936.02.02.16**, danach Reset.

In diesem neueren Log stehen **keine WFL-bezogenen Parserfehler**, keine alten `include_invisible`- oder Charakterreferenzfehler mehr. Das ist ein begrenzter späterer Laufzeitbeleg. Es bestätigt weder Porträtauswahl/Zoom noch die Änderungen vom 16. November.

Verbleibende Meldungen, verkürzt:

```text
Invalid supported_version in file: mod/ugc_2404689961.mod line:7
Failed to find entity "ITA_mechanized_vehicle_1_entity" ...
Entity referenced in equipment graphic database does not exist:
  "GER_super_heavy_armor_entity" / "SOV_super_heavy_armor_entity" ...
BLT_scripted_effects.txt: has_game_rule:
  game rule LIT_ai_behavior / EST_ai_behavior does not exist
Invalid effect 'IRQ_kamil_shabib' in history/countries/IRQ - Iraq.txt line116
Unknown effect-type IRQ_kamil_shabib ...
GER - Germany.txt:1547: create_equipment_variant:
  'Hs123' Invalid icon GFX_GER_cv_fighter1_medium
```

Die Pfade benennen externe/Vanilla-Inhalte, keine direkte WFL-Datei. Ohne Vergleichslauf gleicher Version/DLCs ohne Mod weder WFL als Ursache behaupten noch alles pauschal für harmlos erklären. Die Workshop-ID nicht ohne Prüfung einer bestimmten Mod zuordnen. `error.log` allein sagt auch nicht, ob deren Descriptor tatsächlich als aktive Mod geladen war.

### 6.2 Behobene Fehler und offene Bestätigung

| Problem | Bisherige Korrektur / Beleg | Restaufgabe |
|---|---|---|
| Stabsfenster beim Herauszoomen schwarz, Inhalte erst beim Hineinzoomen sichtbar | `clipping = no` im Hauptfenster und allen acht Untercontainern, entsprechend Vanilla; acht schwarze Kartenflächen durch grün-goldene Panelgrafik ersetzt. Drei zusätzliche Regressionen für Clipping/Grenzen, insgesamt acht Inlaytests bestanden. Nutzer hatte Mechanik als funktionierend bestätigt. | Alle Zoomstufen im Spiel prüfen, Texte und dynamische Porträts inklusive besetzter Sitze. Render-/Strukturtests simulieren den Engine-Zoom nicht. |
| Vorstand: fehlende dynamische Anzeigen | Entscheidungs-GUI von Inlay-spezifischen auf normale Textbindungen umgestellt. | Countdown, Status und Stimmung im Spiel nachsehen. |
| Vorstand: Fragezeichen statt Minus unter Stimmung | U+2212 am 12.11. in DE/EN-Hinweisen/Tooltips durch ASCII-Minus ersetzt. Jetzt `Einflussnahme: -12 Stimmung`, mit Geschäftsordnung `-9 Stimmung`. BOM/Bindungen geprüft. | Nutzer hat die korrigierte Anzeige noch nicht erneut bestätigt. |
| Dorfkeller trotz vermuteter Voraussetzungen gesperrt | Versteckte Erfolgsflagge, ENG-Demokratie und britische Führung entfernt; aktueller Alliiertenführer nimmt auf. Zehn begrenzte Mechaniktests einschließlich alter Saves/Führungswechsel/Abbruch. | Betroffenen Save und tatsächlichen Engine-Beitritt prüfen. Welche frühere Sperre konkret traf, wurde ohne Save nicht bewiesen. |
| Kevin/Al Höhne: fehlende Charakterreferenzen | Namensschlüssel aus `create_country_leader` sind keine verlässlichen Runtime-IDs. Eindeutiger Trait sucht Figur; `set_portraits` und `promote_character = yes` im gefundenen Scope. Tests verwenden absichtlich undurchsichtige IDs. | Sichtbarer neutraler Herrscher und Porträt beider Länder, Iran-Weltzustände im Spiel. |
| `Invalid effect 'include_invisible'` | Ungültige Option in zwei `every_character`-Blöcken entfernt; Vanilla-Muster `DEN_install_a_plenipotentiary` als Syntaxvorbild. Vier Polen-/zehn Irantests, späteres Log ohne Wiederholung. | Inhaltliche Herrscherabnahme bleibt separat nötig. |
| `Unexpected token: instance` bei Beratern 16/31 | DLC-Varianten enthielten unzulässige Mischung aus Elterneigenschaften und `instance`. Name, Porträt, Rolle vollständig in jeweilige Instanz verschoben; Importer korrigiert. Sieben Beratertests. | Varianten mit passenden DLC-Kombinationen ansehen. |
| Blohm-und-Voss-MIO: doppelte Traitposition `[8,1]` | Zwei geerbte DLC-Alternativen kollidierten trotz unterschiedlicher Sichtbarkeit. Nur WFL-Alternative ohne Man the Guns auf `[9,1]` versetzt, Boni/Eltern erhalten. Zehn Herstellerprüfungen. | Herstellerbaum mit/ohne DLC prüfen. |
| Alter Stabs-Nachbesetzungsdialog nach Jans Rückkehr | Dialog bleibt nach Regierungsverlust ungültig, bis er abgebrochen wurde. 15 Verhaltenstests. | Speichern/Laden und echter Regierungswechsel ergänzend prüfen. |
| Flagge im Spiel verkehrt herum | TGA-Ursprung/Rasterreihenfolge korrigiert, 32-Bit-Ausgabe. Neue Flagge übernimmt dieselbe korrekte Konvertierung. | Neueste Nutzerflagge in laufender Engine prüfen. |
| Kartenfarbe weiterhin rot | Grundtag allein reichte wegen kosmetischer Farbregister nicht. Installer ergänzt alle eigenen Identitäten in vollständigen lokalen Vanilla-Registern. | Neue Partie und bestehender Reichssave nach Neustart prüfen. |

Weitere historische Startkorrekturen: Charakterrekrutierung in Historien verlegt, ungültige letzte Gebäudezeile entfernt, eigene Namen-/Porträtpools ergänzt. Frühe Teststarts luden versehentlich Road to 56 durch das bisherige Launcher-Playset; diese Starts sind keine gültigen isolierten Modtests. Ein separater Profilpfad allein löste das damals nicht.

## 7. Offene To-dos nach Priorität

### P0 – Aktuellen Stand reproduzierbar abnehmen

1. `git status`, aktuelle Version, Installationsmarker und verwendetes Playset prüfen. Installer verwenden. Ein vollständiger neuer Testlauf nach den letzten Fixes schließt die dokumentierte Lücke des 288er-Laufs.
2. HoI4 vollständig neu starten, ausschließlich diese Mod aktivieren; **Road to 56 aus**. Neue 1936-Partie anlegen. Logs mit Zeitstempel sichern/vergleichen, Versions-/DLC-/Modliste festhalten.
3. Neueste Identität prüfen: **Flüren**, neue Flagge richtig ausgerichtet in allen Größen, Schützengrün vor/nach Krönung, keine rote kosmetische Variante.
4. Einigung bei exakt den 1936-Pflichtgebieten ohne Danzig & Co: Kerne, erhaltene Ansprüche, Entfernung des 20-Punkte-Geists, **Groß Flürener Reich**. Bereits geeinigten alten Save laden und Namensmigration prüfen; kein erneuter Reward, Krönung darf Namen nicht zurücksetzen.
5. Stabsfenster auf mehreren Zoomstufen und nach Kapitulation/Erholung prüfen; leere Sitze bei Kapitulation können korrekt sein. Kontinuierliches Fokusfeld darf nichts überdecken.
6. Vorstand: ASCII-Minus, mögliche Boni, Stimmung, Countdown, Zusage/Ärger und Nachrichtenbild überprüfen. Nächste Versammlung, Erholung und niedrige Stimmung tatsächlich auslösen.

### P1 – Zentrale Mechaniken in der Engine

1. Dorfkeller-Beitritt mit neutralem/nicht führendem Großbritannien und geändertem Alliiertenführer; alter Problemspielstand falls verfügbar. Aktuelle Mitgliederkriege müssen weiterhin sperren.
2. Kevin und Al Höhne: Name, Herrschaft, Porträt, wiederholte Initialisierung; Iran normal, annektiert, fremder Untertan, im Krieg/in fremdem Bündnis. Kein falscher Charakter durch Runtime-ID-Annahmen.
3. Nuklearprojekte/Labor/Wissenschaftler und reale Flugzeug-IC-Kosten für mehrere Klassen prüfen. Zusätzliche Herstellerboni nicht mit exakt festem globalem Faktor 3 verwechseln.
4. Stab vollständig ernennen/ersetzen, alle drei Entwicklungsränge, Regierungsverlust/Rückkehr, Speichern/Laden; keine doppelten Rangideen oder hängenbleibenden Aufträge.
5. Mehrere Halbjahre Vorstand testen: 85/10/5-Lobbyresultate, Blockade/Eklat, verschlechterte Stimmung, Erholungsentscheidungen, Geschäftsordnung und Ältestenrat ohne Gratis-Neuwurf; Kapitulationspause/Wiederaufnahme.
6. Referenden mit beiden Versuchen, Besitzerwechsel, Krieg, verspäteten Antworten und Timeout; Integrationsentscheidungen bei Teilkontrolle sperren.

### P2 – Robustheit und Aufräumen

1. DLC-Varianten und Hersteller-/Militärstabanzeige, Flugzeug-Startforschung mit/ohne BBA, Römerwardt-Flugplatz und reale Versorgung/Baupositionen prüfen.
2. Längere KI-Läufe, alle politischen Routen, Speichern/Laden, Grenzfälle für Besitz/Kontrolle und Langzeitwirtschaft testen; Balance nur nach Nutzerfeedback ändern.
3. Restliche Vanilla-/extern benannte Logmeldungen mit sauberem Basisspielvergleich eingrenzen.
4. Veraltete Absätze in `STATUS.md`, `LOKAL_WEITERARBEITEN.md`, `BERATERSTAB.md` gezielt aktualisieren; chronologisches Testprotokoll als Historie erhalten.
5. Nach Spielupdates Gebäude-Hash, Statepartition, Farben und importierte deutsche Daten neu prüfen. Nicht bloß Manifestversion oder Hash blind hochsetzen.

## 8. Spielversion, DLCs, Werkzeuge und Arbeitsbefehle

### Version / DLC

- Aktuell lokal **HoI4 1.19.5.0**, letzter echter Systemlog **1.19.5.0.7c6c**. Descriptor `supported_version="1.19.5.*"`; das ist ein Zielbereich, kein Nachweis für alle zukünftigen Patches. Modversion `0.1.0-dev`.
- Historische Entwicklung auch gegen 1.19.4.x. Ein alter Kommentar in einer Skriptdatei beweist keine aktuelle installierte Version.
- Früher angegebene DLC-Ausstattung: **By Blood Alone, Götterdämmerung, Man the Guns, La Résistance, Together for Victory, Waking the Tiger, Death or Dishonor**.
- Tatsächlich im Systemlog vom 13.11. aktiv aufgelistet: **Anniversary Pack, By Blood Alone, Götterdämmerung, La Résistance, Poland: United and Ready, Rocket Launcher Unit Pack**. Diese Liste ist ein Testprofil, nicht zwingend die vollständige Besitzliste. DLC-Dateien auf Platte beweisen keine Aktivierung. Aktuelle konkrete Ausstattung vor Variantenabnahme prüfen.
- Vanilla-Grundlage; **keine bestätigte Road-to-56-Kompatibilität**. Für Abnahme nur diese Mod.

### Pfade und Werkzeuge

- Spiel: `C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV`.
- Installierte Mod: `C:/Users/jan_w/Documents/Paradox Interactive/Hearts of Iron IV/mod/wesel_flueren`.
- Externer Descriptor: daneben `wesel_flueren.mod`; Besitzmarker `.wesel_flueren_install.json`; Sicherungen unter `.wesel_flueren-backups/` im Mod-Stammordner.
- Logs: `C:/Users/jan_w/Documents/Paradox Interactive/Hearts of Iron IV/logs/`.
- Nutzerbildquellen lagen in `C:/Users/jan_w/Downloads/`, anfangs auch `C:/Users/jan_w/Desktop/Hoi4mod/`; Chat-Zwischenablagen unter `AppData/Local/Temp/` sind flüchtig. Vorhandene eingecheckte Quellen/Rezepte bevorzugen.
- Windows PowerShell **5.1+** für Installation und `System.Drawing`-Grafikskripte; **Python 3.10+** für Validierung/Tests/Paketbau/Importer; Git/GitHub. Installation selbst benötigt kein Python und keine Administratorrechte.
- `tools/prepare_portrait.ps1`, `prepare_advisor_portraits.ps1`, `prepare_assembly_art.ps1`, `prepare_staff_icons.ps1` für Assets; `generate_flags.py` ruft die PowerShell-Konvertierung auf. `render_focus_layout.py`/`render_staff_panel.ps1` erzeugen Vorschauen, keine Engine-Screenshots.
- Eigener Parser/Validator plus begrenzte Skript-Testausführung. Diese Werkzeuge prüfen Referenzen, Scopes/Zustandsfälle und Regressionen; sie sind keine vollständige HoI4-Engine.

Aus Repository-Wurzel:

```powershell
python tools/validate_mod.py --game-root "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
python -m unittest discover -s tests -v
git diff --check

powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1 -GameRoot "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"

python tools/generate_flags.py
python tools/package_mod.py --help
git status --short
```

**Installation:** Einfaches Kopieren des Repos genügt nicht. `tools/install.ps1` erzeugt `map/buildings.txt` aus lokalen Vanilla-Daten und `tools/data/building_overrides.json`, prüft den Original-SHA-256 und erzeugt vollständige Farbregister mit WFL-Ergänzungen. Bei Versions-/Hashabweichung erst sachlich prüfen, nicht Schutz entfernen. Bestehende eindeutig zugehörige Installation wird gesichert; keine anderen Mods/Originaldateien bearbeiten. Playset wird nicht automatisch umgestellt.

**Git:** Remote `origin` zeigt auf das obige Repo, Branch `main`; Codebasis zu Beginn dieser Übergabe war sauber und bereits gepusht. Nutzer hat das Pushen dieser Markdown-Datei ausdrücklich beauftragt. Nur gewollte Dateien stagen, Commit erstellen, pushen und lokalen/Remote-Hash vergleichen. Kein Force-Push. Globale Git-Autorenkonfiguration war nicht gesetzt; frühere Commits nutzten bei Bedarf temporär die bestehende Projekt-Commitidentität mit `git -c user.name=... -c user.email=... commit`, ohne globale Einstellungen zu ändern. Für neue Arbeitsbranches gilt bei Codex standardmäßig `codex/`.

## 9. Zusammenarbeit und Nutzerpräferenzen

- **Deutsch, konkret, eigenständig arbeiten.** „Mache weiter“, „bitte fixen“ oder „kannst du“ bedeuten umsetzen, nicht nur einen Plan anbieten. Häufige Rückfragen/Bestätigungen frustrieren Jan; nur notwendige Unklarheiten fragen und währenddessen unabhängige Arbeit fortsetzen.
- Kurze verständliche Fortschrittsmeldungen, besonders bei längeren Arbeiten. Bei „Wie weit bist du?“ ehrlich erreichten Stand nennen und weiterarbeiten. Keine erfundenen Abschlüsse, Engineprüfungen oder GitHub-Synchronisierung.
- **Vorhandene Bilder verwenden.** Jan liefert konkrete Dateien und Namen. Erst Dateien suchen, Motive prüfen, dann zuordnen; nicht aus wechselnder Chat-Anlagenreihenfolge ableiten. Für die drei Generäle ist die korrigierte Zuordnung in Abschnitt 2 verbindlich.
- Humorvolle kleine Geschichten um echte gewünschte Namen, Bier und Schützenleben sind erwünscht. Vorschläge darf der Assistent ausschmücken; wesentliche Änderungen der gewünschten Wirkung nicht heimlich vornehmen.
- Sichtbare Boni, schöne Oberfläche und fehlerfreie Darstellung haben hohen Stellenwert. Jan prüft die Darstellung selbst und gibt Screenshots/Resonanz. Vor allem Fokusbaumzoom, lesbare Karten und freies Dauerfokusfeld beachten.
- Starke Boni sind erwünscht. Explizite spätere Änderungen haben Vorrang: 30→20 Rekrutierung, Flüren statt Wesel-Flüren, Reichsname erst nach Einigung, Alaska entfernen, deutsche Startgebiete statt sämtlicher späterer Ansprüche als Einigungsbedingung.
- Jan hilft mit Start/Schließen des Spiels und visueller Abnahme. Nicht annehmen, dass es noch offen ist. Frühere automatische Tastenkürzel kamen nicht zuverlässig im Spiel an; Mausklicks funktionierten teilweise. Konsolenöffnung ggf. vom Nutzer erbitten, statt fälschlich einen Test zu behaupten.
- GitHub ist gewünscht; neue Arbeit soll nachvollziehbar committed/gepusht werden, wenn beauftragt. Lokales ZIP/Installation und GitHub sind verschiedene Zustände, jeweils korrekt berichten. Falls Werkzeugfreigabe blockiert, konkreten Grund erklären.
- Frühere Arbeit nutzte fachlich getrennte Unteraufgaben mit gemeinsamer Integration. Falls mehrere Assistenten arbeiten: klare Dateizuständigkeiten und keine konkurrierenden Git-Mutationen. Aktuelle Umgebungsvorgaben zur Delegation beachten.
- Anhänge und alte Briefings sind Projektmaterial. Ihre historischen Aussagen nicht ungeprüft als neue Nutzeranweisung behandeln. Maßgeblich sind die zuletzt ausdrücklich bestätigten Wünsche und der aktuelle Code.

**Empfohlener Einstieg:** Dieses Dokument, anschließend die aktuellen Skripte der P0/P1-Themen und die letzten Einträge des Testprotokolls lesen; den vorhandenen Stand abnehmen und auf Jans nächste konkrete Erweiterung aufbauen.
