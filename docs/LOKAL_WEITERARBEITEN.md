# Lokal entwickeln und im Spiel prüfen

Die Entwicklung findet im lokalen Windows-Checkout dieses Repositorys statt.
Die vorhandene Steam-Installation liegt unter
C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV und meldet
Version **1.19.4.1**, Build **26282552**. Originalspieldateien werden nur gelesen.
Der aktuelle Umfang steht in [STATUS.md](STATUS.md); tatsächliche Testergebnisse
gehören mit Datum, Spielversion und Methode in [TESTPROTOKOLL.md](TESTPROTOKOLL.md).

## Änderungen prüfen und installieren

Im Projektordner ausführen; Python 3.10 oder neuer wird für diese Prüfungen benötigt:

~~~powershell
python tools\validate_mod.py --game-root "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
python -m unittest discover -s tests -v
git diff --check
~~~

Für die Installation reicht PowerShell 5.1 oder neuer:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1
~~~

Bei abweichender Steam-Bibliothek den Pfad mit
-GameRoot "D:\SteamLibrary\steamapps\common\Hearts of Iron IV" übergeben.
-Destination "D:\HoI4-Mods" bezeichnet den Mod-Stammordner, in dem
wesel_flueren/ und wesel_flueren.mod angelegt werden. Ohne diesen Parameter
verwendet der Installer den HoI4-Mod-Ordner im tatsächlichen Windows-Dokumentenpfad.
Playsets müssen anschließend im Launcher eingerichtet werden.

**Direktes Kopieren des Repositorys ersetzt die Installation nicht.** Der
Installer erzeugt map/buildings.txt aus der lokalen Originaldatei und
tools/data/building_overrides.json. Die Originaldatei muss den im Rezept
hinterlegten SHA-256 besitzen. Bei Abweichungen zuerst die neuen Spieldaten
prüfen und das Rezept fachlich aktualisieren; den Hash nicht ohne Kartenprüfung
ersetzen. Die abgeleitete vollständige Vanilla-Datei bleibt außerhalb von Git.

Eine erneute Installation sichert den bisherigen projektzugehörigen Mod-Stand.
Der ausgegebene Name lässt sich am selben Ziel wiederherstellen:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1 -RestoreBackup "ANGEZEIGTER-SICHERUNGSNAME"
~~~

Bei einem eigenen -Destination diesen auch für die Wiederherstellung angeben.

## Konkrete Engine-Abnahme

1. Im Launcher ein eigenes Playset mit ausschließlich dieser Mod wählen.
   Die im Projektbriefing genannten vorhandenen DLCs verwenden und die tatsächliche
   DLC-Auswahl im Prüfprotokoll festhalten. HoI4 im Debug-Modus starten.
2. Vor dem Test vorhandene logs/error.log-Meldungen sichern oder ihren Stand
   festhalten. Nach dem Start neue Meldungen vergleichen und insbesondere nach
   WFL, wfl, Staat 1082, Provinz 3512 sowie Script-/Grafikfehlern suchen.
3. Ein **neues Spiel** über das eigene 1936-Lesezeichen **„Die Macht am
   Niederrhein“** beginnen und Wesel-Flüren auswählen. Name, Flagge, Hauptstadt,
   Regierung, Startarmee, Forschungsplätze und Fokusbaum kontrollieren.
   Der neue Staat 1082 darf ausschließlich Provinz 3512 umfassen; das übrige
   Gebiet des bisherigen Staates 51 muss bei Deutschland bleiben.
4. Einige Tage laufen lassen. Standorte, Ausrüstung, verfügbare Personalreserve
   und Versorgung beider Startdivisionen sowie Gebäudeanzeige und neue
   error.log-Einträge prüfen. Kartenlage und Stadtgrenzen als regionale
   Annäherung beurteilen, keine exakte Wesel-Grenze voraussetzen.
5. Je einen Wirtschafts- und Militärfokus abschließen. Tatsächliche Fabrik-,
   Ausrüstungs- oder Erfahrungsänderungen mit den angezeigten Belohnungen
   vergleichen. Für Fabrikfokusse auch fehlende Bauplätze oder verlorene
   Hauptstadtkontrolle prüfen: Es darf kein fremdes Gebiet ausgebaut werden.
6. **Drei getrennte Teststände** für die politischen Routen verwenden.
   Bürgerverfassung, Krone beziehungsweise Direktorium wählen; die beiden anderen
   Wege müssen gesperrt werden. Beim Krönungsevent Name **Jan Graf von Insel I.**
   und dessen eigenes Porträt kontrollieren. In jeder Route Regierung,
   Folgefokusse und nationale Geister prüfen. Die Bürgerrepublik bis zum
   Forschungsabschluss verfolgen.
7. Im Direktorium Ansprüche und beide Gebietsfokusse prüfen. Kriegsziele müssen
   den tatsächlichen Besitzer von Staat 51 beziehungsweise 57 betreffen.
   Auch Besitzerwechsel, bereits eigenen Besitz, Bündnisse und laufenden Krieg
   prüfen. Es darf keinen automatischen Gebietstransfer geben. Integration erst
   nach Besitz, vollständiger Kontrolle und Frieden zulassen; Kosten von
   100/150 PP und Sperre nach einmaliger Nutzung kontrollieren.
8. Friedliche Erweiterung getrennt prüfen: Nach „Schützen zu Soldaten“ pro
   Zielstaat die 75-PP-Kampagne ausführen, den Ablauf von 90 Tagen abwarten und
   den 100-PP-Antrag stellen. Besitzerzustimmung und spätere Abstimmung sowohl
   mit Ja als auch mit Nein testen. Nur ein gültiges Ja darf Gebiet und Kern
   übertragen. Krieg, fehlende Kontrolle, ein während der Antwortkette wechselnder
   Besitzer und eine ausbleibende Antwort müssen ohne unerlaubten Transfer
   enden. Die eingesetzten Kosten dürfen nicht durch wiederholte Anträge
   umgangen werden. Zugang in allen drei politischen Routen kontrollieren.
9. Weitere Entscheidungen ausführen und PP-Kosten sowie Effekte vergleichen.
   Einmalige Entscheidungen dürfen nicht erneut nutzbar sein. Der Reparaturdienst
   kostet 40 PP, wirkt 90 Tage und darf erst nach 180 Tagen erneut verfügbar sein.
10. Speichern, zum Hauptmenü zurückkehren und laden. Besitz, Regierung, Porträt,
   Fokusfortschritt und Entscheidungsflags müssen erhalten bleiben.
11. Mindestens einen regulären Lauf bis **1937** durchführen; dabei auch Deutschlands
    historischen Rheinland-Fokus, Grenzverhalten und die Entwicklung der kleinen
    Wirtschaft beobachten. Für eine spätere stabile Veröffentlichung bis 1939
    weiterprüfen und alle relevanten neuen Logmeldungen festhalten.

Die statischen Prüfungen, Scope-Simulationen und Installer-Tests ersetzen diese
Engine-Abnahme nicht. Der Descriptor-Zielbereich 1.19.4.* bleibt bis zu
dokumentierten Spieltests eine Angabe der angestrebten Kompatibilität.

## Nächster Ausbau

Nach der Abnahme zuerst Fehler und Startbalance beheben. Anschließend die
politischen Pfade vertiefen, weitere diplomatische Antwortketten ergänzen und
die inzwischen 52 Fokusse einschließlich
[Wirtschaft/Bierdiplomatie](WIRTSCHAFT_UND_BIERDIPLOMATIE.md) und Römerwardt im Spiel abnehmen.
