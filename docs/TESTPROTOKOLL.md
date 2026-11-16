# Prüfprotokoll

Stand: 4. November 2026. Windows, PowerShell 5.1, Python 3.10.10.
Lokale Steam-Installation: HoI4 **1.19.4.1**, Build **26282552**.
Dies ist ein Entwicklungsprototyp; eine vollständige Spielabnahme fehlt.

## Automatische Prüfungen

- `python tools/validate_mod.py --game-root "SPIELPFAD"`: bestanden.
  44 Skript-/Interface-/Porträtpool-Dateien, ein Tag, 44 Charaktere, 48 eigene Traits,
  40 eigene Sprites, 36 nationale Geister und 67 klassische Herstellerprofile,
  52 Fokusse, 37 Events, vier Kategorien und 25 Entscheidungen.
  Eigene Referenzen, DE/EN-Texte, BOM, Fokusgraph, Startgebiet, OOB,
  Flaggen, Grafikpfade, Tag-Kollision und effektive Provinzpartition geprüft.
- `python -m unittest discover -s tests -q`: **154 Tests bestanden**, 60,488 Sekunden.
  Enthalten sind beschädigte Referenzen und Grafiken, unzulässige Startdaten,
  Installer-Wiederholung/Backup/Restore/Fremddateischutz, Pfade mit Umlauten,
  Paketstruktur, militärische Zielauflösung und Referendums-Schutzbedingungen.
  Zusätzlich vollständiger lokaler Berater-/Herstellerwertevergleich, DLC-Paare,
  Berateraufwertungen, Porträt- und Namenspools, Jans Startregierung, Nichtkernfeste,
  Atom-/Flugzeugboni und Alaska-Übergabe unter geänderten Bedingungen.
- `git diff --check`: bestanden.
- Eigene Flaggen: 15 unkomprimierte 32-Bit-TGA-Dateien in 82×52, 41×26 und 10×7.
  Das ursprüngliche 24-Bit-Format wurde nach einem Engine-Hinweis ersetzt.
- Herrscherporträt: deterministischer Ausschnitt aus dem Nutzerbild,
  156×210 Pixel, unkomprimiertes BGRA-DDS. PNG-Vorschau visuell geprüft.
  Das Nutzeroriginal wurde ausschließlich gelesen; es wurde nicht verändert.
- Jans großes DDS ist per Hash unverändert; kleine Variante ergänzt.
  18 weitere Fotoausschnitte einschließlich kleiner DDS und Kontaktübersicht
  visuell geprüft. WFL-Personenpools greifen ausschließlich auf eigene Sprites zu.
- MIO-Vererbung und alle neuen Modifier/Projekt-/Gebäude-IDs anhand der lokalen
  Vanilla-Skripte und enginegenerierten Dokumentation geprüft. Kein Laufzeitbeleg.

Die militärischen Verhaltenstests verwenden einen begrenzten lokalen
Scope-Interpreter. Die Referendumtests prüfen wichtige Bedingungen am
tatsächlichen Skriptbaum. Beide Verfahren ersetzen die Engine nicht.

## Installation und Originaldateien

Der vollständige neue Stand wurde am 4. November lokal installiert. Alle
150 direkt aus dem Projekt installierten Dateien wurden anschließend binär
mit der Quelle verglichen: keine Abweichung. Die zusätzliche Gebäudedatei
entsteht weiterhin aus dem Kartenrezept.

Sicherung der früheren Aktualisierung:
`.wesel_flueren-backups/20261104-012850-2e712d48` im lokalen HOI4-Modordner.

Der Launcher hatte die Kommentar-Markierung im bestehenden eigenen Descriptor
entfernt. Die erste Aktualisierung brach deshalb vor Änderungen ab. Der Installer
erkennt diese umformatierte Form jetzt anhand einer vollständig geprüften eigenen
Installation, des exakt passenden Zielpfads und der installierten Name-/Versionswerte.
Fremde Pfade, Namen, Versionen und replace_path bleiben gesperrt. Zwei neue Tests
prüfen diese Fälle einschließlich Wiederherstellung der Launcher-Form.
Die vier Fest-Abbrüche verwenden ausdrücklich NOT mit einem einzelnen AND-Block;
ein zusätzlicher Test sichert diese eindeutige Negation ab.

Isolierte Installationen sowie Installation und Aktualisierung im eigenen
HoI4-Modordner wurden ausgeführt. Der Installer legt Sicherungen an und erzeugt
die vollständige Gebäudedatei ausschließlich innerhalb der Mod-Installation.
Die Vanilla-Datei wurde nach der Installation erneut geprüft und blieb unverändert:

`map/buildings.txt` SHA-256:
`0e50dac6146589200105b212cc489c9e68457d0d1e2087bb5211146679374934`.

Ein Enginefehler zur leeren letzten Gebäudezeile wurde korrigiert: Die
abgeleitete Datei endet wie das lokale Original ohne abschließende Leerzeile.
Ein Regressionstest deckt Originaldateien mit und ohne letzten Zeilenumbruch ab.

## Tatsächliche Engine-Beobachtungen

Die folgenden Engine-Beobachtungen gehören zum früheren Grundaufbau, vor den
hier ergänzten Foto-, Berater-, Hersteller-, Atom-, Flugzeug- und USA-Inhalten.
Diese neuen Inhalte wurden noch nicht in einer laufenden Partie abgenommen.

Der erste direkte Start übernahm den angegebenen separaten Profilpfad nicht
und lud das zuvor aktive Benutzer-Playset einschließlich Road to 56. Diese
Testprozesse wurden beendet; deren Fehler sind kein Test dieser Mod.

Auf ausdrücklichen Nutzerwunsch wurde Road to 56 aus der aktiven Ladeliste
entfernt. Für die anschließenden Starts enthält `dlc_load.json` ausschließlich
`mod/wesel_flueren.mod`; die früheren Listen liegen als lokale Sicherungen
im ignorierten Projektordner `.local-test/`. Der Launcher-Playset-Datenbank
wurde kein neues Playset hinzugefügt. Beim späteren Launcherstart muss das
gewünschte Playset weiterhin ausdrücklich ausgewählt werden.

Mit ausschließlich Wesel-Flüren wurden tatsächlich erreicht:

- Hauptmenü unter 1.19.4.1 ohne Absturz.
- Eigenes 1936-Szenario mit zutreffendem englischen Fallback-Text.
- Länderauswahl mit Wesel-Flüren, eigener Flagge, Bürgerrat und Startinformationen.
- Erneuter Start nach Korrekturen an Charakteren, Flaggen und Gebäudedatei.
  Die zuvor beobachteten WFL-Meldungen wurden dabei nicht erneut gefunden.

Die Engine warnte zunächst vor `recruit_character` in Events. Deshalb werden
jetzt alle vier Figuren in der Länderhistorie rekrutiert. Die Historie setzt
den Bürgerrat und spätere Events die gewählte Führung ausdrücklich mit
`promote_character` ein.

Das aktuelle Log enthält weiterhin Meldungen zu anderen bzw. Vanilla-Pfaden,
unter anderem einem installierten, aber nicht aktivierten FPS-Map-Descriptor,
Fahrzeug-Entities, baltischen Spielregeln sowie irakischer/deutscher Historie.
Ein Vergleich mit einer vollständig unveränderten Vanilla-Sitzung wurde nicht
durchgeführt; diese Meldungen wurden nicht pauschal als harmlos eingestuft.

Die Computersteuerung wurde durch die physische Escape-Taste beendet.
Danach wurden keine weiteren Spieleingaben vorgenommen.

Beim erneuten Lesen am 4. November enthielt das vorhandene error.log (zuletzt
geschrieben 00:13:33) außerdem einen fehlgeschlagenen WFL-Charakternamen.
Ein eigener Namenspool für WFL und WFL_KINGDOM wurde ergänzt; fünf gezielte Tests
prüfen beide Geschlechter, Nachnamen, Rufnamen und fehlende globale Überschreibungen.
Ein neuer Engine-Lauf zum Nachweis, dass diese Meldung verschwunden ist, fehlt.
Zu diesem Lesezeitpunkt lief kein hoi4-Prozess. dlc_load.json nannte nur FPS Map
und War declared sound falling pipe, weder WFL noch Road to 56. Diese Einstellungen
wurden in diesem Schritt nicht geändert; im Launcher muss WFL aktiviert werden.

## Noch nicht im Spiel abgenommen

- Laufende WFL-Partie, tatsächliche Startdivisionen und Versorgung.
- Regierungswechsel auf allen drei Wegen, königliches Porträt und Traitwirkung.
- Fokusbelohnungen, PP-Abzug und Abklingzeiten der Entscheidungen.
- Fotoporträts, Berater und Weiterbildungen, Hersteller/MIOs mit DLC-Umschaltung.
- Neues Atomprogramm, Wissenschaftlerzuweisung, tatsächliche Flugzeug-IC und
  Nichtkern-Mannstärke nach den vier Festen.
- USA-Staatsbesuch einschließlich Geschenkübergabe und Abbruchpfaden.
- Referendum: Zustimmung, Ablehnung, Ja/Nein, Eigentümerwechsel und Teilbesetzung.
- Militärische Expansion, Integration und deutscher historischer Rheinland-Fokus.
- Speichern/Laden, Lauf bis 1937/1939 und vollständige DLC-Verträglichkeit.

Die frühere Cloud-Prüfung vom 3. November umfasste elf Tests und ein deutlich
kleineres Grundgerüst. Die obigen Ergebnisse beziehen sich auf die lokale
Weiterentwicklung und ersetzen diesen älteren Entwicklungsstand.

## Wirtschafts-, Luftfahrt- und Gemeinschaftsausbau am 4. November

Die Erweiterung enthält 23 zusätzliche Fokusse, fünf Gemeinschafts-Wahlereignisse,
sechs sichtbare Bierdiplomatie-Ereignisse und zwei unsichtbare Abrechnungen.
Der vollständige lokale Testlauf nach dem Ausbau bestand: **148 Tests in
44,787 Sekunden**. Das umfasst zusätzlich Fabrikbau unter wechselndem Besitz,
Teilkontrolle, Entmilitarisierung und Baugrenzen, Kriegswirtschaft ohne Rückstufung
totaler Mobilmachung, Wahlbelohnungen ohne Doppelauszahlung, diplomatische
Annahme/Ablehnung, Partnerverlust, späte Antworten und 30-Tage-Abrechnungen.

Der Validator mit lokaler Spielinstallation bestand ebenfalls: 42 Skriptdateien,
52 Fokusse, 37 Events und 103 Ideen (36 nationale Geister, 67 Hersteller).
Fokuskoordinaten und abwärts gerichtete Voraussetzungen, eigene Meinungsmodifier
sowie bedingte Ereignisbeschreibungen werden nun zusätzlich geprüft.
Die lokalen Vanilla-Modifier, Focus-Icons und der Flugplatz-Standort im
Gebäuderezept wurden geprüft. `git diff --check` bestand.

Das vorhandene error.log vom früheren Start um 01:42 Uhr meldete vier
`Unexpected token: instance`-Fehler bei zwei WFL-Beratern und eine überlappende
MIO-Position. Die Instanz-Metadaten wurden entsprechend den lokalen deutschen
Vorlagen in die einzelnen Instanzen verschoben; der WFL-MIO-Knoten ohne
Man the Guns liegt nun auf einer eigenen Position. 17 zugehörige Tests bestanden.
Details stehen in LAUFZEITKORREKTUREN.md.

Die zuletzt gelesene Ladeliste enthält ausschließlich mod/wesel_flueren.mod.
Road to 56 ist darin deaktiviert. Für diesen Entwicklungsschritt wurde keine
neue Partie gestartet. Alle neuen Boni, Ereignisse und Laufzeitkorrekturen
bedürfen weiterhin einer erneuten Engine-Abnahme.

Der abschließend geprüfte Stand wurde lokal installiert. Alle **143** direkt
aus dem Projekt übernommenen Dateien sind binär identisch; die generierte
Gebäudedatei umfasst 66.686 Zeilen. Der SHA-256 der Vanilla-Gebäudedatei blieb
unverändert. Sicherung dieser Aktualisierung:
`.wesel_flueren-backups/20261104-200810-0e51009f`.

## Flaggenausrichtung korrigiert

Nach dem Nutzerhinweis auf eine kopfstehende Flagge wurde der TGA-Export von
oberen auf unteren Ursprung geändert, einschließlich umgekehrter physischer
Zeilenreihenfolge. Alle 15 Texturen wurden neu exportiert. Ein Bytevergleich
belegt für die große Flagge dieselben Pixel in exakt umgekehrter Zeilenfolge.
Die Bildvorlage bleibt aufrecht und unverändert. Lokale Vanilla-Flaggen dienen
als Formatvergleich, nicht als Beleg einer erneuten Engine-Abnahme.

Fünf gezielte Flaggen-/Validatorprüfungen bestanden (4,964 Sekunden). Der
Validator mit lokalem Spielpfad bestand ebenfalls. Alle 15 installierten
Flaggen wurden binär mit den korrigierten Projektdateien verglichen. Sicherung:
`.wesel_flueren-backups/20261104-202510-f6a0869e`. Eine erneute Sichtprüfung
im Spiel steht aus; HoI4 muss die neuen Texturen beim Neustart laden.

## Feldmarschall Lukas Höhne I.

Das neue Offiziersgemälde wurde visuell geprüft und deterministisch zugeschnitten
(225,20,720,969 aus 1075×1463). Große PNG-Vorschau sowie große und kleine DDS
liegen im Projekt und wurden installiert. Jans Porträt ist binär identisch mit
der Sicherung vor dieser Aktualisierung. Ein Schreibfehler des dokumentierten
Hashwertes in GRAFIKEN.md wurde berichtigt. Lukas ist genau einmal in der
Länderhistorie rekrutiert, ausschließlich als Feldmarschall ohne Regierungsrolle.
Stufe und alle vier Fähigkeiten stehen auf 9. Die sieben Vanilla-Eigenschaften
haben keine gegenseitigen Ausschlüsse; die erforderliche Organisator-Eigenschaft
ist vorhanden. Die lokale Fähigkeitentabelle enthält sämtliche eingestellten
Werte für Feldmarschälle.

Vier gezielte Kommandeurprüfungen und der vollständige Lauf mit **154 Tests in
60,488 Sekunden** bestanden. Validator mit lokalem Spielpfad: 44 Charaktere,
40 Sprites und 44 Skriptdateien, keine Fehler. Alle 150 direkt übernommenen
Projektdateien wurden binär mit der Installation verglichen. Sicherung:
`.wesel_flueren-backups/20261104-223809-12a3d7e1`.

Eine neue Partie ist für die Rekrutierung über die Länderhistorie erforderlich.
Porträtanzeige und Feldmarschallwirkung wurden noch nicht in der Engine geprüft.

## Drei Generäle und vollständiger deutscher Militärstab

Die endgültige Porträtzuordnung wurde vom Nutzer anhand der Motive bestätigt:
Ian Jannis Foerster hat wuschelige Haare und Brille, Nils Schapfeld I. den
Schützenhut und Brille, Lars Stüwe kurze Haare ohne Brille. Alle drei großen
PNG-Vorschauen wurden visuell geprüft und pixelweise mit den jeweiligen
DDS verglichen. Die großen Porträts von Jan und Lukas haben weiterhin ihre
unveränderten SHA-256-Werte. Quellen und Zuschnitte stehen in GENERALE.md.
Die Generäle starten auf Stufe 8, die einzelnen Fähigkeiten liegen zwischen
7 und 9; passende Eltern-Traits und gültige Generalrollen wurden geprüft.

36 eigenständige WFL-Militärberater mit 37 Rollen übernehmen den deutschen
Katalog einschließlich zweier ausdrücklich auch für GER zugelassener
österreichischer Profile. Originalpreise, Ressorts, Trait-IDs und vollständige
verschachtelte Traitdefinitionen wurden mit den lokalen Spieldaten verglichen.
Die notwendigen Götterdämmerung-Bedingungen für Fritschs Heerchefrolle und
Beyers Oberkommandorolle bleiben erhalten. Ein unabhängiger zweiter Agent
prüfte die deutschen Rollen und länderneutrale Traitverwendung ebenfalls.
Details und Quellen stehen in MILITAERSTAB.md.

Neun gezielte Kommandeur-/Generaltests und sieben Militärstabtests bestanden.
Der abschließende vollständige Lauf bestand mit **166 Tests in 65,073 Sekunden**.
Ein vorheriger Lauf hatte beim Umbenennen eines isolierten Installations-
Testverzeichnisses einmalig „Zugriff verweigert“ gemeldet. Die gezielte
Wiederholung dieses Tests und der vollständige abschließende Lauf bestanden;
der Installer wurde dafür nicht verändert.

Validator mit lokalem Spielpfad: **83 Charaktere, 48 eigene Anführer-Traits,
46 Sprites und 46 Skriptdateien**, keine Fehler. `git diff --check` bestand.
Alle **163** direkt übernommenen Projektdateien sind binär identisch installiert.
Die abgeleitete Gebäudedatei umfasst weiterhin 66.686 Zeilen; die Originaldatei
des Spiels ist unverändert. Sicherung dieser Aktualisierung:
`.wesel_flueren-backups/20261104-232925-e85059c8`.

Die zuletzt geprüfte Ladeliste enthält ausschließlich `mod/wesel_flueren.mod`;
Road to 56 bleibt deaktiviert. Für diesen Schritt wurde keine neue Partie
gestartet. Die neuen Startcharaktere benötigen regulär eine neue Partie;
Anzeige und tatsächliche Fähigkeitenwirkung sind noch in der Engine abzunehmen.

## 5. November: Wirtschaft, Mobilisierung, Referenden, Könige und Fokuslayout

Florian Klaus ist als politischer Berater für 150 PP mit je +20 % Zivil- und
Militärfabrikbau, +15 % Fabrikleistung und +10 Prozentpunkten Stabilität angelegt
und in der WFL-Startgeschichte rekrutiert. Der neue Startgeist erhöht den
rekrutierbaren Bevölkerungsanteil um 30 Prozentpunkte. Eine kostenlose,
erneut prüfende Einigungsentscheidung kernt alle aktuell deutschen Kernstaaten
erst nach eigenem Besitz und vollständiger Kontrolle und entfernt dabei den
Mobilisierungsgeist. Polen erhält per eigener Startaktion den neutralen Kevin
von Beverungen I. mit moderaten Eigenschaften. Die zusätzlichen Porträtquellen
und großen PNG-Vorschauen von Florian, Kevin und Al Höhne wurden visuell geprüft.

Rheinland und Westfalen besitzen jeweils genau zwei Anträge mit getrennten
Ereignisflaggen und Zeitgebern; die Basisgewichte sind 25/75 für Zustimmung und
60/40 für das anschließende Referendum. Tests führen Erfolg, Ablehnung,
Besitzwechsel, ausbleibende Antworten und verspätete Optionen aus.

Reichspfandministerium und Zapfhahnkrise ergänzen Wirtschaft und britische
Bierdiplomatie. Vier weitere Fokusse und vier Ereignisse führen über die
iranische Erbfolgekrise zur Krönung Al Höhnes und unmittelbaren Marionettenbildung.
Die begrenzten AST-Tests erfassen bestehenden/annektierten Iran, fremden/eigenen
Oberherrn, Krieg, entfernte Kerne, Fraktionen, DLC an/aus und wiederholte Aufrufe.
Diese Simulation bestätigt die Skriptlogik, keine tatsächliche Engineausführung.

Der vollständige Baum enthält jetzt **58 Fokusse**. Ein Rohtext- und AST-Vergleich
bestätigt die ursprünglichen 52 Fokusinhalte bis auf Positionen; alle sechs neuen
Blöcke stimmen mit den Vorlagen überein. Die aktualisierte Übersicht wurde auch
von Root visuell geprüft. Das kontinuierliche Feld unten links liegt mit einem
konservativen Abstand von **302 Pixeln** unter sämtlichen normalen Knoten und
Verbindungen. Ein Test verlangt mindestens 300 Pixel Abstand.

Vollständiger Testlauf: **203 Tests in 68,893 Sekunden bestanden**.
Validator mit lokalem Spielpfad: **86 Charaktere, 52 eigene Anführer-Traits,
52 Sprites, 107 Ideen, 58 Fokusse, 51 Events, 5 Kategorien, 28 Entscheidungen
und 64 Skriptdateien**, keine Fehler. Die 107 eindeutigen Ideen enthalten
**40 nationale Geister** und 67 klassische Herstellerprofile. `git diff --check`
bestand; Git meldete lediglich die bestehende CRLF/LF-Normalisierung.

Der geprüfte Stand wurde installiert. Alle **202** direkt übernommenen
Projektdateien sind binär identisch mit der Installation; die zusätzlich
abgeleitete Gebäudedatei umfasst 66.686 Zeilen. Originalgebäude, Jans Porträt
und Lukas' Feldmarschallporträt behalten ihre vorher dokumentierten SHA-256-Werte.
Sicherung: `.wesel_flueren-backups/20261105-012913-8f4ac97f`.
Die Ladeliste enthält ausschließlich `mod/wesel_flueren.mod`; Road to 56 ist aus.

Die geplante Bildschirmprüfung konnte noch nicht beginnen: Beide verfügbaren
Computersteuerungszugänge scheiterten bereits beim Initialisieren mit
`failed to write kernel assets ... Pfad nicht finden (os error 3)`, auch nach
Kernel-Reset. Es wurden deshalb keine neuen Ingame-Darstellungen oder Wirkungen
als beobachtet bestätigt. Der Nutzer hat angeboten, HoI4 zu starten; aktuelle
Spielprotokolle können unabhängig von der Bildschirmsteuerung geprüft werden.

## 8. November: Kartenfarbe und sofortiger Römerwardt-Ausbau

Wesel-Flürens politische Kartenfarbe ist auf Schützengrün **#236B3B**
(RGB 35, 107, 59) geändert. „Den Römerwardt ausbauen“ setzt den Flugplatz in
Staat 1082 bei Fokusabschluss sofort auf Stufe 5. Ein vorhandener Flugplatz
ab Stufe 5 bleibt erhalten. Besitz, vollständige Kontrolle, fehlende
Kapitulation und ein nicht entmilitarisierter Standort werden beim Abschluss
erneut geprüft; bei ungültigem Standort bleiben 50 PP Ersatz und in jedem
Fall 10 Luftwaffen-EP. Deutsche und englische Beschreibungen sind angepasst.

48 gezielte Prüfungen für Luftfahrt, Fokuslayout und Validator bestanden in
46,603 Sekunden. Der begrenzte Luftfahrt-Test führt Ausgangsstufen 0, 1, 4,
5, 7 und 10 jeweils mit gültigem Standort sowie Besitzverlust, Kontrollverlust,
Teilbesetzung, Kapitulation und Entmilitarisierung aus. Ein zweiter Agent
prüfte Syntax und Stufenschutz anhand lokaler Vanilla-Beispiele unabhängig.
Die aktuelle Darstellung sowie Schäden und vorhandene Bauaufträge wurden
nicht in der Engine geprüft.

Der frühere Spieltest erreichte am 8. November eine neue WFL-Partie.
Jan, das Schützenwesen und die aufrechte Flagge waren sichtbar. In den Logs
verbleibende fehlende Charakterreferenzen bei Kevin führten zur Suche der
Laufzeitherrscher über eindeutige Eigenschaften statt statischer Namenstokens.
Für diese neue Korrektur und Al Höhnes Einsetzung steht die Engine-Abnahme aus.
Der Nutzer schloss das Spiel; die folgende Bildschirmsteuerung wurde von ihm
mit Escape beendet. In diesem Schritt wurde sie nicht erneut gestartet.

Der abschließende Gesamtlauf bestand mit **205 Tests in 82,392 Sekunden**.
Validator mit lokalem Spielpfad und `git diff --check` bestanden ebenfalls.
Der Stand ist lokal installiert; alle **202** direkt übernommenen Projektdateien
sind binär mit der Installation verglichen. Sicherung:
`.wesel_flueren-backups/20261108-235459-5f3a933b`.
Die Ladeliste enthält weiterhin ausschließlich `mod/wesel_flueren.mod`.

### Fallschirmjäger ab Spielbeginn

`paratroopers = 1` steht jetzt im undatierten `set_technology`-Block der
WFL-Länderhistorie. Die lokale Vanilla-Definition in `common/technologies/infantry.txt`
bestätigt, dass diese Technologie die Untereinheit `paratrooper` freischaltet.
Startwert, Eindeutigkeit des Eintrags, Projektvalidator mit Spielpfad und
`git diff --check` bestanden. Die Änderung gilt für neue Partien; vorhandene
Spielstände werden durch die Länderhistorie nicht nachgerüstet.
Lokal installiert mit Sicherung `.wesel_flueren-backups/20261108-235844-0aeda132`.

## 9. November: Dorfkeller Diplomatie und Beitritt zu den Alliierten

Ein 35-Tage-Fokus folgt auf die Zapfhahnkrise auf x=28, y=5. Sowohl deren
erfolgreicher Kühlhandels- als auch Trinkduellpfad qualifiziert sich. Flüren
muss unabhängig, nicht kapituliert und bündnislos sein; Großbritannien muss
die demokratischen Alliierten führen. Der gemeinsame Skripttrigger prüft
das echte Allies-Template und schließt Krieg mit jedem Mitglied aus.
Bei Abschluss erfolgt der Beitritt direkt, danach ein reines Dorfkeller-
Erzählereignis. Veränderte Voraussetzungen, bereits bestehende Mitgliedschaft
und wiederholte Effektaufrufe werden gesondert behandelt. Details und
Vanilla-Belege stehen in [DORFKELLER_DIPLOMATIE.md](DORFKELLER_DIPLOMATIE.md).

Ein unabhängiger Agent prüfte die Skriptsyntax und ergänzte sieben begrenzte
Verhaltenstests mit 14 verschiedenen nachträglich ungültigen Voraussetzungen,
beiden Erfolgspfaden, Konflikten mit Bündnismitgliedern, bestehenden Bündnissen,
fehlgeschlagenem Beitritt und Wiederholung. Die 19 gezielten Diplomatie-,
Zapfhahn- und Layouttests bestanden. Validator mit Spielpfad: 59 Fokusse,
52 Ereignisse und 66 Skriptdateien, keine Fehler. `git diff --check` bestand.
Die neu gerenderte Layoutübersicht wurde visuell geprüft; das kontinuierliche
Feld hat weiterhin 302 Pixel Abstand. Kein neuer Ingame-Lauf wurde durchgeführt.

Abschließender Gesamtlauf: **212 Tests in 78,777 Sekunden bestanden**.
Der erste Installationsversuch meldete beim Veröffentlichen des vorbereiteten
Ordners „Zugriff verweigert“; die automatische Wiederherstellung wurde geprüft.
Der zweite unveränderte Versuch gelang. Alle **206** direkten Projektdateien
stimmen binär mit der Installation überein. Sicherung des erfolgreichen Laufs:
`.wesel_flueren-backups/20261109-204825-da0f50ea`.
Die Ladeliste enthält weiterhin ausschließlich `mod/wesel_flueren.mod`.

## 9. November: Alaska-Zweig entfernt

Entfernt sind der USA-Staatsbesuch und seine drei Folgefokusse
„Thermoskannen für Alaska“, „Eine Bürgerhalle für Alaska“ und
„Werkstätten unter dem Polarlicht“. Auch die sechs USA-Besuchsereignisse,
das Alaska-Wahlereignis `wfl_community.3`, vier ausschließlich zugehörige
Geister und die deutschen/englischen Texte sind entfernt. Die übrigen
Community-Ereignisse behalten ihre IDs 1, 2, 4 und 5.

Ein Agent bereinigte ausschließlich die betroffenen Tests, ein zweiter die
aktuelle Dokumentation. Die 13 gezielten Forschungs-, Luftfahrt-, Community-
und Layouttests bestanden. Der Gesamtlauf bestand mit **207 Tests in
63,642 Sekunden**. Der Validator mit lokalem Spielpfad bestätigt 55 Fokusse,
45 Ereignisse, 103 Ideen und 65 Skriptdateien ohne Fehler; darunter sind
36 nationale Geister. `git diff --check` bestand ebenfalls.

Die neu gerenderte schematische PNG wurde visuell geprüft: Die rechte
Alaska-Spalte entfällt; der Bereich für kontinuierliche Fokusse bleibt
302 Pixel unter dem normalen Baum frei. Ein neuer Engine-Lauf wurde nicht
durchgeführt. Bereits in alten Spielständen erworbene Gebiete werden durch
diese Entfernung nicht automatisch zurückübertragen.

Lokal installiert mit Sicherung
`.wesel_flueren-backups/20261109-210605-20426771`.
Alle **205** direkt übernommenen Projektdateien wurden binär mit der
Installation verglichen. Auch dort fehlen die entfernte USA-Ereignisdatei
und sämtliche Alaska-Verweise in Skripten und Lokalisierungen. Aktiv ist
weiterhin ausschließlich `mod/wesel_flueren.mod`.

## 9. November: Schützenrat und vollständige Freistellung der fünf Abzeichen

Der Schützenrat ergänzt 21 Fokusse: eine Gründung, fünf Ernennungen und
je drei automatische Nebenfokusse. Drei besondere Sitze stehen fünf Kandidaten
offen. Ernennungen dauern 14 Tage, die folgende Sperre 175 Tage. Die Aufgaben
beginnen nach 75–120 Tagen Vorbereitung und dauern 140/140/280 Tage. Eine
tägliche Zustandssteuerung führt sie parallel zum normalen Fokus aus.
Absetzung entfernt nur Amtsboni und laufende Arbeit; erreichte Ränge und
fertige Nebenfokusse bleiben erhalten. Regierungsverlust bereinigt den Rat.

Ein unabhängiger Agent prüfte die tatsächlichen Skripte mit 15 Verhaltenstests.
Dabei wurde ein alter Austauschdialog nach Regierungswechsel und Jans Rückkehr
als Fehler gefunden und behoben: Er bleibt ungültig und gesperrt, bis sein
Dialog tatsächlich abgebrochen wird. Die 15 Tests bestanden nach der letzten
Initialisierungskorrektur nochmals in 1,208 Sekunden. Fünf zusätzliche
Mutationstests prüfen GUI-Syntax, Inlay-/Fenster-/Widgetbindung, dynamische
Texte und Sprites. Drei Layouttests prüfen die normalen Positionen und beide
eingebetteten Bereiche auf Überdeckung.

Alle fünf Abzeichen sind mit Imagegen außen freigestellt und als Original-
PNG mit Alpha im Projekt gespeichert. Namen und Motive sind entsprechend der
Nutzervorgabe zugeordnet. Die 102×90-Fokus- und 128×128-UI-DDS-Dateien erhalten
den Alphakanal; dessen Wertebereich wurde auf 0–255 geprüft. Eine Vorschau vor
Schachbrettmuster und die neu gerenderte Fokusübersicht wurden visuell geprüft.
Quellen, Dateinamen und vollständige Prompts stehen in
[BERATERSTAB_GRAFIKEN.md](BERATERSTAB_GRAFIKEN.md).

Die Kartenfarbe verwendet ausdrücklich RGB. Der Installer ergänzt grüne WFL-
und WFL_KINGDOM-Einträge in lokal abgeleiteten `colors.txt`/`cosmetic.txt` und
erhält die jeweiligen Vanilla-Register vollständig. Zwei neue Installerfälle
prüfen Erhalt, Grund-/Kosmetiktag, Wiederinstallation und ungültige Farbwerte.

Der Gesamtlauf bestand mit **230 Tests in 97,153 Sekunden**. Validator mit
Spielpfad: **76 Fokusse, 47 Ereignisse, 123 Ideen und 74 Skriptdateien**, ohne
Fehler. `git diff --check` bestand. Keine neue Engine-Abnahme durchgeführt;
das Spiel muss für die neuen Skripte und Farben vollständig neu gestartet werden.

Lokal installiert mit Sicherung
`.wesel_flueren-backups/20261109-224432-91e7557e`.
Alle **244** direkten Projektdateien stimmen binär mit der Installation überein.
Beide abgeleiteten Farbregister beginnen mit dem vollständigen jeweiligen
Vanilla-Inhalt. Weiterhin ist ausschließlich `mod/wesel_flueren.mod` aktiviert.

## 10. November: Zoomkorrektur und Gestaltung des Beraterfensters

Der Nutzer bestätigte die funktionierende Beratermechanik im Spiel. Seine
vier Screenshots zeigten einen Darstellungsfehler: Bei herausgezoomtem
Fokusbaum blieb überwiegend ein schwarzer Hintergrund sichtbar, beim
Hineinzoomen wurden die Inhalte schrittweise freigegeben. Die leeren Sitze
im letzten Bild waren laut Nutzer durch die Kapitulation erklärt.

Das Hauptfenster und alle acht Untercontainer verwenden nun ausdrücklich
`clipping = no`. Das lokale Vanilla-Vorbild
`interface/GER_inner_circle_scripted_gui.gui` verwendet diese Einstellung
für sein zoomendes Fokus-Inlay ebenfalls. Ein eigener gezeichneter Hintergrund
in Schützengrün mit goldenen Akzenten enthält die drei Sitz- und fünf
Kandidatenkarten; die acht separaten schwarzen Kartenhintergründe entfallen.
Fenstergröße, Positionen, Texte und Beratermechanik bleiben erhalten.
Die reproduzierbare Zeichnung liegt in `tools/render_staff_panel.ps1`.

Drei neue Regressionstests prüfen sämtliche Container auf abgeschaltetes
Clipping, prüfen die Elternflächen von Containern und Textfeldern und
führen gezielt fehlerhafte Clipping-/Überlaufvarianten ein. Die acht
Inlaytests bestanden in 2,135 Sekunden. Der Hauptagent meldete zusätzlich
26 erfolgreiche Inlay-, Layout- und Beraterverhaltenstests sowie einen
fehlerfreien Validatorlauf mit 75 Skriptdateien und 69 Sprites.

Diese statischen Prüfungen bilden den Zoomrenderer der Engine nicht nach.
Die Darstellung nach der Korrektur ist noch im Spiel zu prüfen; die
Nutzerbestätigung der Mechanik bezieht sich auf den vorherigen Stand.


Die Dorfkeller-Diplomatie wurde im selben Stand ueberarbeitet: Der fertige
Vorgaengerfokus genuegt ohne versteckte Erfolgsmarkierung des britischen
Ereignisses. Die britische Regierungsform und ein Wechsel an der Spitze der
Alliierten sperren den Fokus nicht mehr; der Beitritt erfolgt ueber die
aktuelle Buendnisfuehrung. Die notwendigen Unabhaengigkeits-, Kapitulations-
und Kriegspruefungen bleiben bestehen und werden einzeln angezeigt. Zehn
Mechaniktests sowie drei Layouttests bestanden. Ohne den Spielstand ist
nicht nachgewiesen, welche alte Zusatzbedingung den Nutzer konkret sperrte.

Das aktuelle Fehlerprotokoll vom 10. November meldete ausserdem
`Invalid effect 'include_invisible'` in zwei `every_character`-Bloecken
fuer Polen und Iran. Die ungueltige Option wurde entfernt; das tatsaechliche
Vanilla-Beispiel `DEN_install_a_plenipotentiary` bestaetigt die Syntax ohne
sie. Alle 14 zugehoerigen Tests bestanden. Ein erneuter Engine-Start zum
Nachweis eines bereinigten Fehlerprotokolls steht noch aus.

Abschliessender Gesamtlauf: **236 Tests in 86,494 Sekunden bestanden**.
Validator mit lokalem Spielpfad ohne Fehler (75 Skriptdateien, 69 Sprites).
Lokal installiert; Sicherung: `20261110-105530-e2ba27fc`.


## 10. November: Deutsche Einigung mit Grenzen von 1936

Die Entscheidung prueft jetzt eine feste Liste der 24 deutschen Startstaaten
von 1936 plus Fluerens Heimatstaat 1082 (abgetrennt von Moselland 51).
Spaetere deutsche Kerne oder Annexionen vergroessern die Voraussetzung nicht.
Alle 25 Startstaaten werden gekernt; gehaltene und voll kontrollierte weitere
GER-Kerne werden optional mitgekernt. Fremde GER-Kerne und die fuenf oestlichen
Ansprueche aus GER_reassert_eastern_claims werden beansprucht (Danzig85,
Memel188, Gdingen807, Posen86, Kattowitz762). Bestehende Ansprueche und fremdes
Eigentum bleiben erhalten. Die einmalige Entfernung des Mobilisierungsgeists
und die erneute Pruefung bei Ausfuehrung bleiben erhalten.

Elf Verhaltenstests fuer die tatsaechlichen Skripte bestanden. Validator mit
lokalem Spielpfad bestand (76 Skriptdateien). Keine neue Engine-Abnahme.

Abschluss: **57 relevante Tests in 63,440 Sekunden bestanden**. Lokal
installiert mit Sicherung `20261110-111309-d69e2b10`.


## 10. November: Halbjaehrliche Bataillonsversammlung und Vorstand

Sechs Vorstandsmitglieder mit den vom Nutzer zugeordneten Portraets erhalten
je eine Einflussentscheidung und einen moeglichen Beschluss. Die Versammlung
arbeitet mit einem persistenten Zaehler von sechs Monatswechseln, erstmals
Juli1936; es gibt keine mehrfach belohnenden Nachrichtenoptionen. Alle Bilder
wurden ausschliesslich proportional eingepasst/konvertiert; die Originale sind
im Projekt erhalten. Die gruen-goldene Kartenansicht wurde als Layoutvorschau
visuell geprueft. Das Saalbild bleibt vollstaendig im Nachrichtenformat397x153.

13 deterministische Verhaltenstests bestanden (0,321Sekunden): Kalender inkl.
Januar-Doppelzaehlung, bestehende Spielstaende, jede der fuenf moeglichen
Kollateral-Verstimmungen, Zusage/Verweigerung, Abstimmungen, alle drei
Streitausgaenge, Ruecksetzen/Ersetzen, Kapitulation und alle acht Bonusprofile.
Der Validator prueft nun auch Nachrichten-IDs und Entscheidungs-GUI-Bindungen.
Zwei Mutationstests pruefen fehlerhafte Verweise. Validator mit Spielpfad PASS:
76Fokusse,48Ereignisse,131Ideen,34Entscheidungen,6Kategorien,77Sprites,
88Skriptdateien. Eine Engine-Abnahme ist noch offen.

Gesamtlauf: **255 Tests in 130,601 Sekunden bestanden**. Die Nachrichtentexte
wurden anschliessend fuer das feste Vanilla-Textfeld gekuerzt; keine erneute
Engine-Darstellung behauptet.

Lokal installiert mit Sicherung `20261110-231548-de61f1cf`; alle 287
direkten Quelldateien stimmen binaer mit der Installation ueberein.

## 10. November: Vorstandsstimmung, zwei Fokusse und Startflugzeugtechnik

Die sechs Vorstandskarten zeigen die möglichen Boni unter dem Fachbereich.
Kartenhöhe 240, Fensterhöhe 620 Pixel; lokale Layoutvorschau geprüft.
Countdown, Stimmung und Status verwenden normale lokalisierte Textbindungen
der Entscheidungs-GUI. Die zuvor verwendeten Inlay-Textbindungen wurden hier
ersetzt; eine neue Sichtprüfung in der Engine steht noch aus.

Persistente Stimmung startet bei 75/100, auch bei Migration bestehender
Spielstände ohne Zurücksetzen des Sitzungskalenders. Einflussnahme kostet
12 Stimmung, Kollateralstreit zusätzlich 6, eigene Verärgerung zusätzlich 8.
Unter 40/20 Punkten gelten nicht stapelnde −5/−10 Prozentpunkte Stabilität.
Blockaden und Eklats verschärfen die Stimmung sofort und monatlich. Drei
wiederholbare Entscheidungen ermöglichen Erholung; Kapitulation pausiert
die Mechanik und entfernt ihre wirksamen Staatsmali.

„Geschäftsordnung auf Bierdeckeln“ und „Der Ältestenrat am Tresen“ ergänzen
eine Fokusreihe rechts außen, je 35 Tage. Die Geschäftsordnung reduziert
alle Einflussverluste exakt um 25 % (9/4,5/6); Beschluss- und Monatsverluste
bleiben bestehen. Der Ältestenrat beruhigt genau ein verärgertes Mitglied
für 50 PP, mit 30 Tagen Abklingzeit und +10 Stimmung. Porträtreihenfolge und
Zieltext stimmen überein; Zusagen und verbrauchte Versuche bleiben erhalten.

Starttechnologien wurden gegen die installierten Definitionen geprüft:
mit By Blood Alone kleines 1936-Flugzeugmodell, leichte MGs und passende
Motoren, sonst die entsprechenden Jagdflugzeugtechnologien. Gilt nur für
neue Partien; Fallschirmjäger- und Infanterietechnologien bleiben erhalten.

Gesamtlauf vor Ergänzung der zwei Fokusse: **268 Tests in 274,565 Sekunden
bestanden**. Nach den Fokusänderungen: **40 gezielte Tests in 1,234 Sekunden
bestanden**, darunter sieben neue Fokus-/Vermittlungstests, zehn Stimmungstests,
Sitzungskalender, Starttechnik und Layout. Validator mit Spielpfad PASS:
78 Fokusse, 48 Ereignisse, 133 Ideen, 38 Entscheidungen, sechs Kategorien,
77 Sprites und 93 Skriptdateien. `git diff --check` bestanden.
Die Layoutprüfung hält das kontinuierliche Fokusfeld weiterhin frei.

Lokal installiert mit Sicherung `20261110-234853-df08f0cc`.
Alle **296 direkten Quelldateien** stimmen binär mit der Installation überein;
Gebäude- und Farbtabellen werden weiterhin aus dem lokalen Spiel erzeugt.
Kein Spielstart und keine neue Engine-Abnahme für diesen Schritt behauptet.


## 12. November: Textzeile unter der Vorstandsstimmung

Der Nutzerscreenshot zeigt das typografische Minus U+2212 vor der Zahl
als Fragezeichen. Die Vorstands-UI verwendet jetzt in Deutsch und Englisch
ASCII-Minus, auch in den zugehörigen Hinweisen und Tooltips. Die Kurzzeile
nennt ausdrücklich den Stimmungsverlust; die dynamische Auswahl zwischen
12 und 9 nach der Bierdeckel-Geschäftsordnung bleibt erhalten.
UTF-8-BOM und Textbindung wurden geprüft. Keine Spielregeln verändert
und keine neue Engine-Sichtprüfung behauptet.

Der erste Validatorlauf erkannte das inzwischen installierte HoI4 1.19.5.0
gegen den alten Descriptor-Zielbereich 1.19.4.*. Zielbereich auf 1.19.5.*
aktualisiert; Validator mit lokalem Spielpfad danach bestanden. Die
hashgebundene Vanilla-Gebäudequelle stimmt weiterhin mit dem Rezept überein.
Lokal installiert mit Sicherung `20261112-170335-62965cff`; alle 296
direkten Quelldateien stimmen mit der Installation überein.


## 16. November: Rekrutierbare Bevölkerung reduziert

WFL_volk_unter_schuetzenhut gewährt jetzt 20 statt 30 Prozentpunkte
rekrutierbare Bevölkerung (conscription = 0.20). Mit Freiwilligenarmee
sind das 21,5 % vor weiteren Faktoren, bei 240.000 Kernbevölkerung
48.000 zusätzlich potenziell Einziehbare. DE/EN-Beschreibungen des
Geists und seiner Entfernung durch die deutsche Einigung sowie aktuelle
Dokumentation angepasst. 14 bestehende Mobilisierungs-/Einigungstests
bestanden in 0,274 Sekunden; Validator mit lokalem Spielpfad bestanden.
Reiner Subagent-Review fand keine weiteren aktiven 30-Pp.-Referenzen.
Lokal installiert mit Sicherung `20261116-172204-bb6dc168`; alle 296
direkten Quelldateien stimmen mit der Installation überein.
Keine neue Engine-Abnahme.
