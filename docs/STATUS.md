# Entwicklungsstand

Stand: 16. November 2026. Lokale Windows-Entwicklung gegen die Steam-Installation
von **HoI4 1.19.5.0**. Ziel dieses Schritts ist ein erster
lokaler Prototyp mit unabhängigem Flüren im Jahr 1936. Eine erfolgreiche
statische Prüfung allein bestätigt weder Spielbarkeit noch DLC-Kompatibilität.
Tatsächlich ausgeführte Prüfungen stehen im [Prüfprotokoll](TESTPROTOKOLL.md).

## Implementierter Umfang

- Land WFL mit eigener Definition, Regierung, Gesetzen, Technologien,
  zwei Forschungsplätzen und eigener Startaufstellung.
- Fallschirmjäger I sind ab Beginn einer neuen Partie erforscht (`paratroopers`).
- Leichtes Flugzeug und leichte Flugzeugbewaffnung sind ab neuer Partie
  erforscht; mit By Blood Alone kleines 1936-Flugzeugmodell, leichte MGs und
  passende Motoren, ohne DLC die entsprechenden Jagdflugzeugtechnologien.
- Staat **1082** mit genau einer Provinz **3512**, aus Vanilla-Staat 51
  abgetrennt. Hauptstadt und beide Startdivisionen liegen in dieser Provinz.
  Die übrigen Provinzen von Staat 51 bleiben bei Deutschland.
- Landesfarbe auf der politischen Karte: Schützengrün **#236B3B** (RGB 35, 107, 59).
- Eigenes 1936-Lesezeichen „Die Macht am Niederrhein“.
- Drei Divisionsvorlagen und zwei Startdivisionen; kein Flugzeug- oder
  Schiffsdesigner wird für die Startaufstellung vorausgesetzt.
- Eigene Flaggen mit dem gelieferten Wappen in den benötigten drei Größen.
- **Jan Graf von Insel I.** startet mit dem bereitgestellten Gemälde als alleiniger
  autoritärer Anführer. Die Partei heißt **Schützenwesen**. Das Bürgerpräsidium
  bleibt demokratische Alternative, die Schützenverwaltung arbeitet unter Jan.
- 18 Fotoausschnitte in großen und kleinen DDS ersetzen die übrigen WFL-Personen.
  Länderpools erfassen Heer, Marine, Politik, Agenten und Wissenschaftler.
- 37 politische Berater mit 39 DLC-Grundvarianten und acht kostenpflichtigen
  Fähigkeitsaufwertungen. Sämtliche numerischen Werte einschließlich Nachteile
  sind mit den lokalen deutschen Vorlagen verglichen. Fiktive Namen.
- Zusätzlich **Florian Klaus** als politischer Wirtschaftsberater mit eigenem
  Nutzerporträt: je +20 % Zivil- und Militärfabrikbau, +15 % Fabrikleistung und
  +10 Prozentpunkte Stabilität während der Anstellung für 150 politische Macht.
- **Ein Volk unter dem Schützenhut** als permanenter Startgeist mit
  +20 Prozentpunkten rekrutierbarer Bevölkerung. Freiwilligenarmee damit vor
  weiteren Faktoren bei 21,5 %; normale Mobilisierung und Nichtkern-Abzüge gelten.
- Kostenlose Entscheidung zur deutschen Einigung: die deutschen Startgebiete
  von 1936 einschließlich Flüren müssen WFL gehören und vollständig kontrolliert
  werden. Sie erhalten WFL-Kerne; weitere gehaltene GER-Kerne sind optional.
  Danzig und weitere östliche Ansprüche werden gesichert. Der
  +20-Prozentpunkte-Geist wird nur bei Erfolg entfernt.
- **Kevin von Beverungen I.** als neutraler Startmachthaber Polens mit
  Nutzerporträt, +5 % politischem Machtgewinn und +5 Prozentpunkten Stabilität.
  Eine eigene Startaktion erhält die originale polnische Länderhistorie.
- Deutscher Militärstab als 36 eigenständige WFL-Berater mit 37 Rollen:
  sechs Heerchefs, drei Marinechefs, vier Luftwaffenchefs, 16 Oberkommandos und
  acht Theoretiker. Originalnamen, Basispreise und Fähigkeiten; vorhandene
  Nutzerfotos und WFL-Rekrutierung. Zwei auch für Deutschland nutzbare
  österreichische Profile sind eingeschlossen. [Details](MILITAERSTAB.md).
- 67 klassische Herstellerprofile, 29 MIOs und zwei Herstellerwissenschaftler,
  einschließlich Varianten und optionaler deutscher Vertragshersteller.
- Eigener Anführer-Trait für Jan: +15 % politischer Machtgewinn und +10 %
  Fabrikleistung, sobald er als Regierungschef regiert.
- **Lukas Höhne I.** als bereits 1936 rekrutierter Feldmarschall, Stufe 9 und
  alle vier Fähigkeiten auf 9. Sieben kompatible Vanilla-Eigenschaften und
  eigenes großes/kleines Porträt aus dem neu bereitgestellten Offiziersbild.
- **Ian Jannis Foerster, Nils Schapfeld I. und Lars Stüwe** als drei ab Start
  rekrutierte Generäle auf Stufe 8 mit starken spezialisierten Fähigkeiten.
  Die drei Uniformporträts sind den Namen nach ausdrücklicher Motivbestätigung
  zugeordnet; Einzelwerte und Quellen stehen in [GENERALE.md](GENERALE.md).
- **78 Fokusse**, **46 sichtbare nationale Geister**, **48 Events**, **38 Entscheidungen**
  und sechs Entscheidungskategorien, vollständig auf Deutsch und Englisch.
- **Stab des Grafen** mit fünf Kandidaten für drei besondere Sitze:
  Dante Grossy, Neal Foerster, Max Heinsch, Max Müller und Till Hoehne.
  Ernennung in 14 Tagen, danach 175 Tage Abklingzeit; drei persönliche Vorhaben
  pro Person laufen automatisch parallel zum nationalen Fokus. Jede Stufe
  ersetzt die bisherigen Amtsboni. Eigene transparente Abzeichen und ein
  960 × 590 Pixel großes Informationsfenster bei (3300,1000) zeigen den Rat.
  Die 20 verborgenen Rangideen sind in insgesamt **133 Ideendefinitionen**
  enthalten; diese Sonderrollen belegen keine normalen politischen Beraterplätze.
  Absetzung, Machtverlust und alte Nachbesetzungsdialoge werden bereinigt.
  [Ablauf, Werte und Abgrenzung zum deutschen Vorbild](BERATERSTAB.md).
- Gemeinsame Wirtschafts- und Militärzweige; gegenseitig ausgeschlossene
  politische Einstiege für Bürgerrepublik, Schützenkönigreich und Schützenverwaltung.
  Die Bürgerrepublik besitzt einen durchgehenden Verwaltungs- und Forschungspfad.
  Krönung und Schützenverwaltung besitzen eigene Folgefokusse mit Jan als Anführer.
- Schützenverwaltung mit Ansprüchen auf den verbleibenden Staat Rheinland 51 und auf
  Westfalen 57, dynamischen Kriegszielen, kostenpflichtiger Integration
  erworbener Gebiete und abschließender Proklamation einer Niederrheinunion.
- Friedliche Schützenkampagnen und Referenden für Rheinland 51 und Westfalen 57,
  nach „Schützen zu Soldaten“ für alle drei politischen Routen zugänglich.
- Nuklearforschung +300 %, vier Nuklearprojekte +400 %, Nuklearbau +300 %,
  Bombenproduktion +200 %, ein eigener Stufe-5-Forscher und fünf Durchbruchpunkte.
  Ein zusätzlicher Slot ergänzt den bestehenden Technikschul-Slot: regulär vier
  Forschungsplätze nach beiden Fokussen. Laboranlage mit geprüftem Standort.
- Flugzeugwunder: alle 20 Flugzeug-Basis-/Rollentypen kosten ein Drittel IC.
  Weitere Hersteller-/MIO-Rabatte addieren sich regulär.
- Vier kostenpflichtige, einmalige Anwerbefeste mit je +0,05 Nichtkern-Mannstärke;
  insgesamt +20 Prozentpunkte. Voraussetzung: Jan und ein Nichtkerngebiet.
- Berufskolleg Wesel mit dauerhaft +5 % Forschung und zwei Industrieforschungsboni
  von je +100 % zusätzlich zum bisherigen Forschungsplatz. Rheinhandel gewährt
  dauerhaft je +15 % Zivil- und Militärfabrikbau.
- Rheinblockade mit garantiertem Wirtschaftsgeist und Antwortereignissen von
  Deutschland/Niederlanden; Anglo Bier Diplomatie mit drei sichtbaren Events
  und dauerhaft +100 gegenseitiger Meinung sowie +50 Handelsmeinung.
- Dorfkeller Diplomatie nach erfolgreicher Zapfhahnkrise: in 35 Tagen direkter
  Beitritt zu den demokratischen, britisch geführten Alliierten mit anschließendem
  Dorfkeller-Vertrag als Erzählereignis. Unabhängigkeit, Bündnisfreiheit und kein
  Krieg gegen Mitglieder sind Voraussetzung; kein Zufallswurf oder Anfrageereignis.
  [Bedingungen und Ablauf](DORFKELLER_DIPLOMATIE.md).
- Alkoholfreies Bier verbieten: +10 % Organisationserholung der Armee. Flachglas
  liefert drei Militärfabriken; der Folgefokus führt automatisch Kriegswirtschaft
  ein und ersetzt keine bereits vorhandene totale Mobilmachung.
- Vier Römerwardt-Fokusse liefern zusammen 120 Luftwaffen-EP, sofort einen Flugplatz
  auf mindestens Stufe 5 und permanente Ausbildungs-, Unfall-, Reichweiten-
  und Missionseffizienzboni.
- Reichspfandministerium mit +15 % Ressourcen, -10 % Rohstoffmangelmalus und
  +5 % Fabrikleistung. Die Zapfhahnkrise bietet drei sichtbare Ereignisse mit
  unterschiedlichen Handels- oder Trinkduellgeschichten und einmaligen Boni.
  Ein versteckter Zeitgeber sichert ausbleibende Antworten ab.
  [Pfand und Zapfhahnkrise](PFAND_UND_ZAPFHAHN.md).
- Räumlich geordnete Fokuszweige; das kontinuierliche Fokusfeld liegt bei
  (0,1650) mit mindestens 300 Pixeln Abstand unter dem gesamten normalen Baum.
  Geometrie und ursprüngliche Fokusinhalte werden getrennt geprüft.
  [Layout und Vorschau](FOKUS_LAYOUT.md).
- Vier Iran-Fokusse à 35 Tage: Erbfolgekrise, Gesandtschaft, Hochzeit und
  Treuevertrag. Der letzte Abschluss setzt unmittelbar Al Höhne mit dem
  Zigarrenporträt als neutralen Herrscher ein und macht Iran zur WFL-Marionette.
  Annexion, fremde Oberherrschaft, Fraktionen und Krieg werden im Abschluss
  behandelt; kein Zufallswurf oder fremdes Veto. WFL muss unabhängig und nicht
  kapituliert sein. Der bestehende Flürener Feldmarschall bleibt verfügbar.
  [Geschichte und Randfälle](IRAN_ERBFOLGE.md).
- Vier neue Wahlereignisse und weitere Brauerei-, Vereins-, Forschungs-
  und politische Abschlussfokusse. Alle 78 Fokuspositionen sind verschieden.
- Der Alaska-Zweig einschließlich USA-Staatsbesuch, Schenkung, drei Folgefokussen
  und zugehörigen Ereignissen und Geistern wurde am 9. November entfernt.
- Explizite Charakterbeförderung bei Regierungswechseln, gegen fehlende
  Kontrolle/Bauplätze abgesicherte Fabrikbelohnungen, begrenzte einmalige
  Entscheidungen und ein befristeter Reparaturdienst mit Kosten und Abklingzeit.
- PowerShell-Installer mit automatischer Steam-Suche, frei wählbarem
  Mod-Stammordner, Sicherungen und Wiederherstellung.

## Karten- und Installationsgrenzen

Provinz 3512 ist eine aus lokalen Kartendaten begründete **regionale Annäherung**,
keine nachgewiesene genaue Stadt- oder Ortsteilgrenze. Die Vanilla-Karte nennt
die Provinz nicht ausdrücklich Wesel oder Flüren. Befunde und verbleibende
Darstellungsfragen sind in [KARTENPRUEFUNG.md](KARTENPRUEFUNG.md) dokumentiert.

Die Installation ist erforderlich: tools/install.ps1 erzeugt eine angepasste
map/buildings.txt aus der lokalen Originaldatei und dem Projekt-Kartenrezept.
Der Originalhash muss zum geprüften Rezept passen. Einfaches Kopieren des
Repositorys in den Mod-Ordner erzeugt diese notwendige Datei nicht.
Originalspieldaten werden ausschließlich gelesen; die abgeleitete vollständige
Vanilla-Datei gehört nicht ins Git-Repository. Ein Spielupdate kann die
hashgebundene Installation bis zur erneuten Prüfung unterbrechen.

Der Descriptor-Zielbereich 1.19.5.* ist keine Bestätigung einer vollständigen
Kompatibilitätsprüfung. Andere Mods, die dieselben Staaten oder Gebäudeplätze
ändern, benötigen eine gesonderte Verträglichkeitsprüfung.

## Expansion und Integration

Friedliche Kampagnen kosten pro Staat einmalig 75 PP und dauern 90 Tage.
Der anschließende Referendumsantrag kostet weitere 100 PP. Der tatsächliche
Besitzer entscheidet über die Zulassung; bei Zustimmung folgt 30 Tage später
eine getrennte Ja-/Nein-Abstimmung. Nur ein gültiges Ja-Ergebnis bei passenden
Eigentums-, Kontroll-, Unabhängigkeits- und Friedensbedingungen überträgt den
Staat und fügt den WFL-Kern hinzu. Nach Ablehnung oder Abbruch ist ein zweiter
und letzter Antrag für weitere 100 PP möglich; die Kampagne bleibt einmalig.
Nach Erfolg ist kein weiterer Antrag möglich. Bei normalen Beziehungen betragen
die KI-Grundchancen 25 % Zulassung und 60 % Ja, also 15 % Beitritt pro Versuch.
Kosten bleiben verbraucht. Getrennte 120-Tage-Ereignisse beenden ausbleibende
Antworten; alte Zeitgeber können die zweite Runde nicht abbrechen.

Die militärischen Gebietsfokusse prüfen Unabhängigkeit, Kapitulation, fremden
Besitz, Bündnisse, eigene Untertanen und bereits laufenden Krieg erneut beim
Abschluss. Ihr Ziel wird dann aus dem aktuellen Besitzer des jeweiligen Staates
ermittelt. Bei ungültiger gewordenen Bedingungen gibt es eine dokumentierte
Ersatzbelohnung von 50 politischer Macht; eigener Besitz überspringt den Fokus.

Ein Kriegsziel erklärt keinen Krieg und überträgt kein Gebiet. Die Integration
kostet einmalig 100 PP für Rheinland und 150 PP für Westfalen. Sie verlangt
tatsächlichen Besitz, vollständige Kontrolle und Frieden. Bereits vorhandene
eigene Kernstaaten werden nicht nochmals kostenpflichtig integriert. Der
Union-Abschluss erkennt auch auf anderem Weg erworbene eigene Kernstaaten an.

## Noch ausstehend

Am 8. November wurden eine neue WFL-Testpartie sowie die Länderauswahl erreicht.
Jans Porträt, Name, Partei Schützenwesen und die aufrechte Flagge waren sichtbar.
Die Engine meldete bei Kevin noch fehlende Charakterreferenzen; die neue
Korrektur sucht Laufzeitfiguren über ihren eindeutigen Trait statt über den
statischen Namenstoken. Diese Korrektur und Al Höhnes Einsetzung müssen noch
im Spiel geprüft werden. Der Nutzer hat das Spiel geschlossen und die spätere
Bildschirmsteuerung per Escape beendet.

Offen sind Darstellung der Foto-/Herrscherporträts, tatsächliche Berater- und
Herstelleranzeige mit/ohne DLC, MIO-Vererbung, Wissenschaftler, nukleare Projekte,
Flugzeugkosten und Festboni im laufenden Spiel. Versorgung, Regierungswege,
Speichern/Laden und ein Lauf bis 1937 sind ebenfalls abzunehmen.
Auch der historische deutsche KI-Pfad mit dem verbleibenden Staat 51 und den
im Briefing genannten DLCs muss tatsächlich im Spiel geprüft werden.

Der Fokusumfang beträgt nach Entfernung des Alaska-Zweigs und Ergänzung des Beraterstabs **78**.
Die Wirtschaftserweiterung, Bierdiplomatie, Römerwardt und die neuen Wahlereignisse
benötigen noch eine Engine-Abnahme. Auch Darstellung, Bedienung und Speichern/Laden
des neuen Beraterstabs sind noch in HoI4 zu prüfen. Die zuletzt beobachteten Parserfehler bei
DLC-Beraterinstanzen und eine MIO-Positionsüberschneidung wurden korrigiert.
Weitere Inhalte und
belastbare Balance folgen auf die Abnahme dieses Stands.
Die politischen Routen bleiben die bisherigen Arbeitsannahmen; das
[Quellenbriefing](HOI4_Wesel_Flueren_Codex_Briefing.md) ist unverändert erhalten.


Die Bataillonsversammlung tagt automatisch alle sechs Monatswechsel. Der
Vorstand im Entscheidungsfenster zeigt sechs Mitglieder mit gelieferten
Porträts, möglichen Boni, Zusagen und Streit. Die allgemeine Stimmung beginnt
bei 75/100; Einflussnahme und Streit senken sie. Unter 40/20 Punkten gelten
−5/−10 Prozentpunkte Stabilität. Drei wiederholbare Entscheidungen verbessern
die Stimmung. „Geschäftsordnung auf Bierdeckeln“ senkt Einflussverluste um
25 %, „Der Ältestenrat am Tresen“ erlaubt, für 50 PP alle 30 Tage genau ein
verärgertes Mitglied zu beruhigen (+10 Stimmung). Sechs Bonusprofile und zwei
befristete Streitprofile werden bei jeder Sitzung neu beschlossen. Details:
[Bataillonsversammlung](BATAILLONSVERSAMMLUNG.md).
