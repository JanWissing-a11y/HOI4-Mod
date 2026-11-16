# Flüren – Die Macht am Niederrhein

Lokaler Entwicklungsprototyp für **Hearts of Iron IV**: Ein unabhängiges
Flüren erhält einen eigenen Staat, eine Startarmee, einen Fokusbaum und
das Schützenwesen unter Jan Graf von Insel I., eine demokratische Alternative
und eine königliche Verwaltungsroute.
Entwickelt wird unter Windows gegen die vorhandene Steam-Version **1.19.5.0**.
Statische Prüfungen ersetzen keine Abnahme im Spiel. Tatsächlich ausgeführte
Prüfungen stehen in [docs/TESTPROTOKOLL.md](docs/TESTPROTOKOLL.md).

Die vollständige Projektübergabe mit aktuellem Stand, Dateistruktur, Konventionen,
Fehlerhistorie und priorisierten Aufgaben steht in
[docs/UEBERGABE_AN_KI.md](docs/UEBERGABE_AN_KI.md).

Enthalten sind **78 Fokusse, 46 sichtbare nationale Geister, 48 Events und 38
Entscheidungen**, vollständig auf Deutsch und Englisch. Dazu kommen
drei Divisionsvorlagen, zwei Startdivisionen, eigene Flaggen und das vom Nutzer
bereitgestellte Herrscherporträt für **Jan Graf von Insel I.**
Sein eigener Anführer-Trait erhöht den politischen Machtgewinn um **15 %**
und die Fabrikleistung um **10 %**.
Feldmarschall **Lukas Höhne I.** steht mit dem neuen Nutzerporträt bereits 1936
zur Verfügung: Stufe 9, Angriff/Verteidigung/Planung/Logistik jeweils 9 und
sieben starke Eigenschaften. [Details zum Feldmarschall](docs/FELDMARSCHALL.md).
Die Generäle **Ian Jannis Foerster, Nils Schapfeld I. und Lars Stüwe** starten
auf Stufe 8 mit hohen, unterschiedlich gewichteten Fähigkeiten und den anhand
der Bildmotive bestätigten Nutzerporträts. [Werte und Zuordnung](docs/GENERALE.md).

Jan führt das Schützenwesen bereits zum Spielstart. 18 Fotoausschnitte ersetzen
die übrigen WFL-Personenporträts, einschließlich der Länderpools für erzeugte
Personen. Die Nationalflagge enthält das gelieferte Flürener Wappen.

Die neuen Fokusse bieten ein stark beschleunigtes Atomprogramm, ein Nuklearlabor,
einen weiteren Forschungsplatz und Flugzeuge für ein Drittel IC. Vier einmalige
Anwerbefeste erhöhen die Nichtkern-Mannstärke um zusammen 20 Prozentpunkte.
Der **Stab des Grafen** ergänzt fünf eigene Kandidaten für drei besondere Sitze:
Dante Grossy, Neal Foerster, Max Heinsch, Max Müller und Till Hoehne.
Nach ihrer Ernennung bearbeiten sie persönliche Fokusreihen automatisch
parallel zum nationalen Fokus und verbessern dabei ihre Amtsboni. Freigestellte
Porträtabzeichen und ein eigenes Informationsfenster zeigen den aktuellen Rat.
Die 20 verborgenen Rangideen erhöhen den Gesamtumfang auf **133 Ideendefinitionen**;
die normalen politischen Beraterplätze bleiben eigenständig.
[Beraterstab, Ablauf und Werte](docs/BERATERSTAB.md).
38 politische Berater mit 40 Grundvarianten, acht zusätzlichen Aufwertungen,
67 klassischen Herstellerprofilen und 29 MIOs übernehmen deutsche Fähigkeiten.
Der deutsche Militärstab ergänzt 36 eigenständige WFL-Berater mit 37 Rollen
für Heer, Marine, Luftwaffe, Oberkommando und Theorie, mit Originalfähigkeiten
und Preisen sowie den vorhandenen Nutzerfotos. Eingeschlossen sind die beiden
auch für Deutschland nutzbaren österreichischen Profile.
[Militärstab](docs/MILITAERSTAB.md).
Wirtschaftsberater **Florian Klaus** liefert je +20 % Zivil- und Militärfabrikbau,
+15 % Fabrikleistung und +10 Prozentpunkte Stabilität während seiner Anstellung.
Der Startgeist **Ein Volk unter dem Schützenhut** erhöht die rekrutierbare
Bevölkerung dauerhaft um 20 Prozentpunkte. [Details](docs/FLORIAN_UND_MOBILISIERUNG.md).
Nach Besitz und vollständiger Kontrolle der deutschen Startgebiete von 1936
vergibt eine kostenlose Entscheidung dort WFL-Kerne und entfernt diesen
Mobilisierungsgeist. Danzig und weitere östliche Ansprüche bleiben unabhängig
davon erhalten. [Deutsche Einigung](docs/DEUTSCHE_EINIGUNG.md).
Polen startet mit **Kevin von Beverungen I.** als neutralem Herrscher:
+5 % politischer Machtgewinn und +5 Prozentpunkte Stabilität.
[Polens Herrscher](docs/POLEN.md).
Rheinland und Westfalen erlauben je einen zweiten Referendumsantrag. Bei normalen
Beziehungen betragen die KI-Grundchancen 25 % für die Zulassung und 60 % für
das anschließende Ja. [Referenden und Chancen](docs/REFERENDEN.md).
Neu: stärkeres Berufskolleg, Rheinhandel mit je +15 % Fabrikbau, Rheinblockade,
Flachglasumbau mit drei Militärfabriken, automatische Kriegswirtschaft,
Bierdiplomatie mit Großbritannien und ein vierteiliger Römerwardt-Luftfahrtzweig.
Das Reichspfandministerium bringt dauerhaft +15 % Ressourcen, einen um 10 %
geringeren Rohstoffmangelmalus und +5 % Fabrikleistung. In der Zapfhahnkrise
führen Eiswürfelverträge oder ein königliches Trinkduell zu eigenen Boni.
[Pfand und Zapfhahnkrise](docs/PFAND_UND_ZAPFHAHN.md).
Die **Dorfkeller Diplomatie** führt nach dem abgeschlossenen Zapfhahnkrisen-Fokus
in 35 Tagen direkt zu den tatsächlichen Alliierten unter ihrer aktuellen Führung.
Großbritannien muss Mitglied sein; Demokratie und britische Bündnisführung sind
nicht erforderlich. Flüren muss unabhängig, nicht kapituliert, bündnislos und
mit allen Mitgliedern ohne Krieg sein.
[Dorfkeller-Vertrag](docs/DORFKELLER_DIPLOMATIE.md).
Vier Iran-Fokusse erzählen von Erbfolgechaos, Höhnes Gesandtschaft, Hochzeit
und Treuevertrag. Der Abschluss macht Iran garantiert zur Flürener Marionette
mit **Al Höhne** als neutralem Herrscher und dem gelieferten Zigarrenporträt;
auch ein zuvor annektierter Iran wird wiederhergestellt. WFL muss unabhängig
und nicht kapituliert sein. [Iran-Erbfolge](docs/IRAN_ERBFOLGE.md).
Vier Wahlereignisse und weitere Vereins- und Forschungsfokusse ergänzen
den Ausbau. Details: [Wirtschaft und Bierdiplomatie](docs/WIRTSCHAFT_UND_BIERDIPLOMATIE.md),
[Atomprogramm und Flugzeugbau](docs/FOKUS_ERWEITERUNG.md),
[Berater](docs/BERATER_QUELLEN.md), [Aufwertungen](docs/BERATER_AUFWERTUNG.md),
[Hersteller](docs/HERSTELLER.md), [Grafiken](docs/GRAFIKEN.md).
Die Zweige sind räumlich geordnet; das Feld für kontinuierliche Fokusse liegt
mit freiem Abstand unter dem normalen Baum. [Fokuslayout](docs/FOKUS_LAYOUT.md).

Der neue Staat **1082** besteht ausschließlich aus der vorhandenen Provinz
**3512**, die aus Vanilla-Staat 51 abgetrennt wird. Das ist eine regionale
Annäherung an Wesel/Flüren, keine genaue Darstellung heutiger Stadtgrenzen.
Die restlichen Provinzen von Staat 51 bleiben bei Deutschland.
Die Kartenbefunde stehen in [docs/KARTENPRUEFUNG.md](docs/KARTENPRUEFUNG.md).

## Installation unter Windows

Im Projektordner PowerShell öffnen und ausführen:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1
~~~

Der Installer sucht die Steam-Installation automatisch und verwendet den
HoI4-Mod-Ordner unter dem tatsächlichen Windows-Dokumentenverzeichnis. Falls
die Suche den Spielordner nicht findet, den Pfad ausdrücklich angeben:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1 -GameRoot "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
~~~

**Den Installer verwenden: Einfaches Kopieren des Repositorys genügt nicht.**
Er erzeugt die benötigte Mod-Datei map/buildings.txt aus den lokal vorhandenen
Originaldaten und dem Kartenrezept in tools/data/building_overrides.json.
Vorher prüft er den SHA-256 der Originaldatei. Bei abweichenden Spieldaten bricht
er vor einer Änderung der vorhandenen Mod-Installation ab. Ein Spielupdate kann
deshalb eine erneute Kartenprüfung und Anpassung des Rezepts erfordern.
Die abgeleitete vollständige Vanilla-Datei wird nicht im Git-Repository abgelegt.

Der Installer schreibt wesel_flueren/ und wesel_flueren.mod ausschließlich
in den gewählten Mod-Ordner. Originaldateien des Spiels bleiben unverändert.
Für die Installation sind PowerShell 5.1 oder neuer, aber weder Python noch
Administratorrechte erforderlich. Playsets werden nicht automatisch verändert.

Anschließend im Paradox Launcher die lokale Mod **Flüren – Die Macht am
Niederrhein** einem eigenen Playset hinzufügen und aktivieren. Für die erste
Prüfung andere Mods deaktivieren und ein neues Spiel mit dem eigenen
1936-Lesezeichen **„Die Macht am Niederrhein“** beginnen.

## Aktualisieren, wiederherstellen und entfernen

Nach Änderungen den Installer erneut ausführen. Eine vorhandene, eindeutig zu
diesem Projekt gehörende Installation wird unter .wesel_flueren-backups/ gesichert.
Den ausgegebenen Sicherungsnamen zur Wiederherstellung verwenden:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\install.ps1 -RestoreBackup "ANGEZEIGTER-SICHERUNGSNAME"
~~~

Mit -Destination "D:\HoI4-Mods" lässt sich ein anderer **Mod-Stammordner**
angeben; der Installer legt darin weiterhin wesel_flueren/ und wesel_flueren.mod
an. Bei einer Wiederherstellung denselben Stammordner angeben.
Zum Entfernen die Mod im Launcher deaktivieren und genau diese beiden erzeugten
Einträge im Installationsziel löschen. Sicherungen können separat aufbewahrt werden.

## Territoriale Entwicklung

Alle drei politischen Routen können nach „Schützen zu Soldaten“ friedliche
Schützenkampagnen in Rheinland 51 und Westfalen 57 beginnen. Pro Staat kostet
die einmalige Kampagne 75 PP und dauert 90 Tage. Danach kostet der Antrag auf
ein Referendum weitere 100 PP. Der aktuelle Besitzer muss zustimmen; erst
30 Tage später kann die getrennte Ja-/Nein-Abstimmung folgen. Nur ein gültiges
Ja-Ergebnis bei weiterhin passenden Besitz-, Kontroll- und Friedensbedingungen
überträgt den Staat und macht ihn zum Kerngebiet. Ablehnung garantiert keinen
späteren Erfolg; nach Ablehnung oder Abbruch steht genau ein zweiter Antrag
für weitere 100 PP zur Verfügung. Die eingesetzten Kosten bleiben verbraucht.

Der militärische Pfad der Schützenverwaltung erhebt Ansprüche auf den verbleibenden Staat
Rheinland (51) und auf Westfalen (57). Folgefokusse erzeugen Kriegsziele gegen
den jeweiligen aktuellen Besitzer. Krieg und erfolgreicher Gebietserwerb bleiben
erforderlich; die Fokusse übertragen kein Land. Nach tatsächlichem Besitz,
vollständiger Kontrolle und Frieden kosten die einmaligen Integrationsentscheidungen
100 beziehungsweise 150 politische Macht. Bereits vorhandene eigene Kernstaaten
verursachen keine zusätzlichen Integrationskosten.

## Entwicklung und Prüfung

Python 3.10 oder neuer wird nur für die Entwicklungsprüfungen benötigt:

~~~powershell
python tools\validate_mod.py --game-root "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
python -m unittest discover -s tests -v
git diff --check
~~~

Der Prüfer kontrolliert eigene Syntax, Referenzen, Fokusgraph, Startdaten,
Flaggen und deutsche/englische Texte. Mit --game-root prüft er zusätzlich
installierte Version, Tag-Kollisionen, die wirksame Provinzpartition und direkte
Grafikpfade. Die statische Scope-Simulation für den Expansionszweig prüft unter
anderem wechselnde Besitzer und Integrationssperren; sie ist keine Engine-Simulation.
Spielengine, KI, Versorgung und Langzeitbalance sind gesondert im Spiel zu prüfen.
Der konkrete Ablauf steht in [docs/LOKAL_WEITERARBEITEN.md](docs/LOKAL_WEITERARBEITEN.md).

Der Descriptor-Eintrag supported_version="1.19.5.*" bezeichnet den Zielbereich,
keine bestätigte Kompatibilität für sämtliche Versionen dieses Bereichs.
Nach Entfernung des Alaska-Zweigs und Ergänzung des Beraterstabs umfasst der Baum 78 Fokusse.
Weitere Inhalte und Balance folgen auf die Abnahme dieser Erweiterung im Spiel.
Aktueller Umfang und offene Punkte stehen in [docs/STATUS.md](docs/STATUS.md).


Die automatische **Bataillonsversammlung** mit sechs Vorstandsmitgliedern
steht im Entscheidungsfenster bereit. Alle sechs Monatswechsel gibt es
ein Nachrichtenfenster mit dem gelieferten Saalbild und neu ausgewürfelte
Staatsboni. Die Karten zeigen mögliche Boni und den Abstimmungsstatus.
Einflussnahme kann Zusagen sichern, senkt aber die allgemeine Stimmung.
Unter 40/20 Punkten gelten −5/−10 Prozentpunkte Stabilität; drei Entscheidungen
verbessern die Stimmung. „Geschäftsordnung auf Bierdeckeln“ reduziert
Einflussverluste um 25 %, „Der Ältestenrat am Tresen“ schaltet die persönliche
Versöhnung frei. [Regeln und Wahrscheinlichkeiten](docs/BATAILLONSVERSAMMLUNG.md).

Neue Partien beginnen außerdem mit leichtem Flugzeug und leichter
Flugzeugbewaffnung: mit By Blood Alone kleines Flugzeugmodell 1936,
leichte MGs und passende Motoren; ohne DLC die entsprechende Jagdflugzeugtechnik.


Der Staat heißt bis zur deutschen Einigung **Flüren**, danach
**Groß Flürener Reich**. Die gelieferte grün-schwarz-goldene
Glockenflagge gilt für alle politischen Varianten und beide kosmetischen
Namensstufen. [Namenswechsel und Flagge](docs/STAATSNAME_UND_FLAGGE.md).
