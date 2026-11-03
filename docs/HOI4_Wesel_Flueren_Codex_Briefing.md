# Projektübergabe: Hearts of Iron IV – Wesel/Flüren

Stand: 3. November 2026. Dieses Dokument ist die vollständige Aufgabenbeschreibung für eine neue Codex-Sitzung. Die Mod soll dort von Grund auf entwickelt werden.

## 1. Auftrag und verbindliche Vorgaben

Der Nutzer möchte eine Mod für **Hearts of Iron IV**, in der **Wesel/Flüren als eigener Staat** spielbar ist. Es handelt sich um Wesel am Niederrhein und den Ortsteil Flüren in Nordrhein-Westfalen.

Vom Nutzer ausdrücklich ausgewählte Inhalte:

- Eigener nationaler Fokusbaum.
- Neues Land beziehungsweise eigenes Szenario.
- Events und Entscheidungen.
- Änderungen an Einheiten und Spielwerten.

Der Nutzer möchte die eigentliche Entwicklung in Codex durchführen. Diese Datei dient als Übergabe; jetzt muss noch kein fertiges Mod-ZIP entstehen.

### Spiel und vorhandene DLCs

Der Nutzer nennt die **aktuelle Spielversion**, aber keine konkrete Versionsnummer. Folgende DLCs sind vorhanden:

| Nutzernennung | Offizieller Titel beziehungsweise Einordnung |
| --- | --- |
| Blood Alone | By Blood Alone |
| Götterdämmerung | Götterdämmerung |
| Man the Guns | Man the Guns |
| La Resistance | La Résistance |
| Together for Victory | Together for Victory |
| Waking the Tiger | Waking the Tiger |
| Death or Dishonor | Death or Dishonor |

Keine weiteren DLCs voraussetzen. Dass manche älteren Erweiterungen inzwischen zum Grundspiel gehören können, verändert diese Vorgabe nicht. Maßgeblich sind die tatsächlich installierte Spielversion und die dort verfügbaren Inhalte.

Deutsch ist die sinnvolle Standardsprache für Mod-Texte und Dokumentation. Ein englischer Fallback ist empfehlenswert. Windows ist die vorgesehene Standardplattform für eine einfache Installation; der tatsächliche Entwicklungsrechner ist noch nicht bekannt.

## 2. Was bisher tatsächlich existiert

**Es wurde noch keine funktionsfähige Mod implementiert.** Es gibt keinen getesteten Fokusbaum, keine fertige Länderdefinition, keine geprüfte Karte und keinen fertigen Installer. Bisher erfolgten Konzeptarbeit und Recherchen zur technischen Umsetzung. Leere Arbeitsordner oder heruntergeladene Referenzdateien sind kein Implementierungsfortschritt.

Es gab keinen Starttest in HoI4. Aussagen wie „spielbar“, „voll kompatibel“ oder „getestet“ dürfen erst nach entsprechender Prüfung verwendet werden.

Eine neue Codex-Sitzung benötigt keinen Zugriff auf den bisherigen Arbeitsordner, um anzufangen. Die unten genannten Onlinequellen und vor allem die lokale HoI4-Installation reichen als technische Grundlage aus.

## 3. Bisher vorgeschlagenes Konzept – noch keine Nutzervorgabe

Die folgenden Ideen wurden vom Assistenten vorgeschlagen. Der Nutzer hat sie bislang weder ausdrücklich bestätigt noch verworfen. Sie können als sinnvolle Arbeitsannahmen für die erste Version dienen, sind aber anpassbar.

### Szenario

- Arbeitstitel: **Freistaat Wesel-Flüren – Die Macht am Niederrhein**.
- Empfohlener Start: **1. Januar 1936**.
- Fiktive Ausgangslage: Eine international anerkannte Sonderregelung am Niederrhein hat einen unabhängigen Staat unter einem lokalen Bürgerrat entstehen lassen.
- Die übrige Welt bleibt möglichst nahe am regulären HoI4-Szenario.
- Ziel: Ein kleiner, überlebensfähiger Staat mit regionalem Charakter, wirtschaftlichem Aufbau, glaubwürdiger Verteidigung und optionaler Expansion.
- Das ist ausdrücklich alternative Geschichte. Heutige lokale Bezüge können als humorvolle Anspielungen verwendet werden; sie müssen nicht als historische Tatsachen von 1936 dargestellt werden.

### Drei mögliche politische Wege

| Route | Spielidee | Mögliche Inhalte |
| --- | --- | --- |
| Bürgerrepublik | Demokratischer Handels- und Verwaltungsstaat | Verfassung, kommunaler Aufbau, niederländische Beziehungen, Forschung und Kooperation |
| Schützenkönigreich | Fiktive lokale Monarchie | Krönung des Schützenkönigs, Hofrat, Traditionsverbände, Königsgarde und bewaffnete Neutralität |
| Niederrhein-Direktorium | Expansiver Regionalstaat | Mobilisierung, regionale Ansprüche, Ultimaten, mögliche Kriege und Integration eroberter Gebiete |

Die drei Routen sollten sich spielmechanisch unterscheiden und gegenseitig ausschließen. Expansion erfordert nicht automatisch eine faschistische Route. Die konkrete Ideologiezuordnung und Führungsfiguren sind noch frei.

### Lokale Motive

Gut geeignete Bezüge sind Bürgerhalle Flüren, Auesee, Berliner Tor, Kornmarkt, Rhein und Lippe, Rheinhandel, Jungschützen und Schützentradition. Beispiele für Fokus- oder Entscheidungstitel:

- „Der Rat der Bürgerhalle“
- „Werkbank am Niederrhein“
- „Die Bürgerhalle ausbauen“
- „Rheinhandel beleben“
- „Schützen zu Soldaten“
- „Übungsplatz am Auesee“
- „Das Berliner Tor sichern“
- „Die Krone von Flüren“
- „Niederrheinunion ausrufen“

Diese Namen sind Entwurfsvorschläge. Nicht ohne Auftrag reale Privatpersonen zu Politikern, Generälen oder Gegnern machen. Für die erste Version können fiktive Figuren und generische Spielporträts verwendet werden.

## 4. Empfohlener Umfang der ersten vollständigen Version

Die folgenden Zahlen sind Planungsziele und keine bereits zugesagten beziehungsweise fertigen Inhalte:

- Etwa **40–50 Fokusse** in einem zusammenhängenden Fokusbaum.
- Gemeinsame Wirtschafts- und Militärzweige sowie drei politische Routen.
- Etwa **10–15 Events**, einschließlich diplomatischer Antwortketten.
- Etwa **10–15 Entscheidungen**, mit Bedingungen, Kosten und sinnvollen Abklingzeiten.
- Mehrere nationale Geister, darunter Anfangsnachteile und spätere Verbesserungen.
- Eigene Flagge in allen benötigten Größen; bei Bedarf Varianten für politische Formen.
- Zwei bis drei regionale Divisionsvorlagen und eine kleine ausgerüstete Startarmee.
- Eigene Flaggen- und gegebenenfalls Fokusgrafiken. Vorhandene Spielgrafiken können für die erste funktionierende Version wiederverwendet werden.
- Deutsche Lokalisierung sämtlicher eigener sichtbarer Texte.
- Installation, Deinstallation, Versionsangaben, bekannte Einschränkungen und Prüfprotokoll.

Nicht gleich zu Beginn eine Total Conversion, neue Weltkarte oder vollständig neue Waffensysteme bauen. Erst einen vollständig spielbaren Ablauf herstellen, dann die Inhalte ausbauen.

## 5. Wichtigste technische Entscheidung: Startgebiet und Karte

**Noch nicht gelöst:** Welche genaue HoI4-Provinz Wesel beziehungsweise Flüren repräsentiert und welche aktuelle Staatsdatei betroffen ist.

In den Vorrecherchen tauchten Staat **51** als Rheinland und Staat **57** als Westfalen auf. Das sind ausschließlich Suchansätze. Dateinamen, Gebietsgrenzen und Zuordnungen müssen in der tatsächlich installierten Vanilla-Version überprüft werden. Besonders wichtig: Öffentlich verfügbare Kaiserreich-Dateien verändern die Karte und sind **keine Vanilla-Referenz**.

Auch Provinz-IDs **529** und **3512** wurden als mögliche Kandidaten im weiteren Gebiet untersucht. **Keine davon wurde als Wesel verifiziert. Nicht ungeprüft als Hauptstadt festlegen.**

### Vorgehen zur Verifizierung

1. Lokale Spielversion und Installationspfad bestimmen.
2. Staatsdefinitionen in `history/states/` und Provinzdefinitionen in `map/definition.csv` lesen.
3. Provinzposition anhand der tatsächlichen Karte prüfen; gegebenenfalls im Spiel mit Debug-Tooltips beziehungsweise Nudge arbeiten.
4. Hauptstadtprovinz, Hauptstadtstaat, bestehende Eigentümer, Siegpunkte und Gebäude dokumentieren.
5. Erst danach Besitz, Kerne, Startarmee und Fokusbelohnungen darauf aufbauen.

### Zwei mögliche Umsetzungen

| Variante | Vorteil | Zu beachten |
| --- | --- | --- |
| Einen bestehenden Großraum dem neuen Land zuweisen | Weniger Kartenarbeit; guter Start für eine erste Version | Das Gebiet ist deutlich größer als Wesel/Flüren. Das offen dokumentieren und Ressourcen, Industrie und Bevölkerung balancieren. |
| Einen eigenen kleinen Staat aus bestehenden Provinzen bilden | Genauere regionale Darstellung | Alle betroffenen Staatsdefinitionen, strategischen Regionen und gegebenenfalls Gebäude-, Flugplatz- und Versorgungspositionen auf Konsistenz prüfen. Keine Provinz darf doppelt zugewiesen sein oder fehlen. |

Die erste Variante wurde dem Nutzer als vorläufiger Ansatz genannt. Sie ist eine Arbeitsannahme, keine ausdrücklich genehmigte genaue Grenzziehung.

Bei Änderungen bestehender Staatsdateien den tatsächlichen relativen Dateipfad übernehmen. Nicht einfach eine zweite Datei mit derselben State-ID hinzufügen. Keine flächigen `replace_path`-Einträge für ganze Vanilla-Verzeichnisse verwenden, wenn einzelne gezielte Überschreibungen ausreichen.

### Optionaler versionsabhängiger Installer

Es wurde vorgeschlagen, die erforderliche Staatsdatei erst bei der Installation aus dem lokalen Spiel zu übernehmen und ausschließlich im Mod-Ordner anzupassen. Das könnte veraltete Kopien vermeiden. Ein solcher Installer existiert noch nicht und ist keine zwingende Anforderung.

Wenn dieser Weg gewählt wird:

- Originaldateien des Spiels nur lesen.
- Nur eindeutig zu dieser Mod gehörende Dateien schreiben oder ersetzen.
- Pfade mit Leerzeichen, Umlauten und gegebenenfalls OneDrive-Dokumenten unterstützen.
- Eigentümer, Kerne, demilitarisierte Zonen und spätere Datumsblöcke korrekt behandeln.
- Änderungen strukturiert parsen; globale Regex-Ersetzungen dürfen nicht versehentlich Kommentare, andere Blöcke oder Zitate verändern.
- Bei unbekannter Struktur mit verständlicher Meldung abbrechen.
- Vorhandene Installation sichern beziehungsweise einen Wiederherstellungsweg anbieten.
- Installation ohne Administratorrechte und ohne zusätzliche Downloads bevorzugen.
- Nicht stillschweigend Python auf dem Spielrechner voraussetzen. Ein einfaches Windows-Paket mit PowerShell ist eine Option, sofern es tatsächlich getestet wird.

## 6. Technische Leitplanken

### Land und Startzustand

- Vorgeschlagener interner Tag: `WFL`. Zuerst auf Kollisionen prüfen.
- Eigene Länderdefinition, Länderhistorie, Charaktere und Startaufstellung verwenden.
- Das Land muss bereits bei der Länderauswahl am vorgesehenen Startdatum existieren und auswählbar sein.
- Nicht ausschließlich auf einen `on_startup`-Besitzwechsel setzen, der erst nach der Länderauswahl stattfindet.
- Ein eigener Start-Lesezeichen-Eintrag ist optional, aber für die Auffindbarkeit hilfreich.
- Staatsunabhängigkeit, Hauptstadt, Kerne, Technologien, Gesetze, Forschung, Stabilität und Kriegsunterstützung explizit festlegen.
- Eine echte, passende OOB-Datei laden; Startdivisionen müssen auf kontrollierten, gültigen Provinzen stehen.
- Keine unrealistisch kostenlose Vollmobilisierung und keine unbeabsichtigt riesigen Ausrüstungsvorräte.

### Fokusbaum

- Baum eindeutig an `WFL` binden, damit er nicht anderen Ländern zugewiesen wird.
- IDs konsistent mit Präfix `WFL_` benennen.
- Voraussetzungen, gegenseitige Ausschlüsse und mögliche UND-/ODER-Verknüpfungen sorgfältig prüfen.
- Alle politisch vorgesehenen Endpunkte müssen erreichbar sein.
- Kein Fokus darf als Belohnung dauerhaft fremde oder inzwischen verlorene Gebiete ausbauen.
- Zustandsabhängige Belohnungen absichern; Tooltips müssen den tatsächlichen Effekten entsprechen.
- Bauplätze und bereits erreichte Gebäudegrenzen berücksichtigen.
- Diplomatische Ablehnungen dürfen keine unerreichbaren Pflichtfokusse hinterlassen.

### Charaktere und Politik

- Aktuelle Charakterdefinitionen und `recruit_character` verwenden, sofern die Spielversion das erwartet.
- Reihenfolge von Rekrutierung und Regierungssetzung beachten.
- Bei mehreren Figuren derselben Ideologie ausdrücklich sicherstellen, dass die richtige Person regiert.
- Porträtpfade in der installierten Version verifizieren. Keine geratenen Dateinamen als geprüft behandeln.

### Events und Entscheidungen

- Eindeutiger Event-Namespace, zum Beispiel `wfl`.
- Auslöser und Empfänger explizit setzen.
- Bei diplomatischen Ketten Länder- und Staatsscope sowie `ROOT`/`FROM` prüfen.
- Antworten auf abgelehnte Angebote, verschwundene Länder, geänderte Eigentümer und laufende Kriege vorsehen.
- Keine unbegrenzten kostenlosen Fabriken, Divisionen, Manpower oder Forschungsslots durch wiederholbare Entscheidungen.
- Einmalige Entscheidungen mit Flags absichern, wiederholbare mit Kosten und Abklingzeiten.
- Keine unnötigen täglich weltweit laufenden Skripte. Für seltene Ereignisse einmalige Auslöser, geeignete On-Actions oder terminierte Events bevorzugen.

### Einheiten und Spielwerte

- Regionale Boni möglichst über eigene nationale Geister und länderspezifische Effekte umsetzen.
- Änderungen sollen grundsätzlich nur das neue Land betreffen.
- Globale Vanilla-Einheiten oder Ausrüstung nur überschreiben, wenn das bewusst gewollt und begründet ist.
- Beispiel: schnellere Ausbildung regionaler Infanterie, leichte Verteidigungsboni, günstigere Standardausrüstung nach einem Rüstungsfokus.
- Aktuelle Modifier-Namen, Technologie-IDs und Ausrüstungs-Archetypen aus der lokalen Version übernehmen.

### DLC-Verträglichkeit

- Keine Inhalte aus nicht genannten Erweiterungen voraussetzen.
- Vorhandenes By Blood Alone bedeutet: Flugzeugvarianten und Luft-OOB müssen zum verwendeten Flugzeugdesigner passen, falls solche Inhalte eingebaut werden.
- Man the Guns bei eventuellen Marinevarianten beachten.
- Für La Résistance können Geheimdienstinhalte angeboten werden; sie sind für einen funktionierenden ersten Build nicht zwingend.
- Auch mit Götterdämmerung müssen alle konkreten deutschen Fokus- und Skriptbezüge geprüft werden. Nicht auf alte deutsche Fokus-IDs vertrauen.
- Ein deutschhistorischer KI-Pfad kann durch ein neues unabhängiges Gebiet beeinflusst werden. Dieses Zusammenspiel ausdrücklich testen.

### Dateien und Darstellung

- Spielskripte mit passender UTF-8-Kodierung; Lokalisierungsdateien nach den Anforderungen der installierten Version, üblicherweise UTF-8 mit BOM.
- Passende Lokalisierungsheader und Dateinamenssuffixe verwenden.
- TGA-Flaggen typischerweise in `82×52`, `41×26` und `10×7` Pixeln; tatsächliche Anforderungen prüfen.
- Grafikreferenzen und Sprite-Namen müssen auf existierende Dateien zeigen.
- Keine fremden Mod-Grafiken oder kompletten Mod-Dateien ungeprüft übernehmen.

## 7. Empfohlene Projektstruktur

Beispiel; tatsächliche Dateien können nach Bedarf ergänzt werden:

```text
projekt/
  README.md
  CHANGELOG.md
  docs/
    konzept.md
    technische_entscheidungen.md
    testprotokoll.md
  tools/
    validate_mod.py
    package_mod.py
    install.ps1                 # nur falls sinnvoll
  mod/
    wesel_flueren.mod
    wesel_flueren/
      descriptor.mod
      common/
        country_tags/
        countries/
        characters/
        national_focus/
        ideas/
        decisions/
          categories/
        on_actions/
        scripted_effects/
        opinion_modifiers/
        bookmarks/              # optional
      history/
        countries/
        states/
        units/
      events/
      localisation/
        german/
        english/                # optionaler Fallback
      gfx/
        flags/
          medium/
          small/
        interface/
      interface/
```

Descriptor-Dateien mit realer Zielversion und gültigem Installationspfad versehen. Ein `supported_version`-Eintrag ist keine Bestätigung, dass die Mod auf dieser Version getestet wurde.

## 8. Entwicklungsablauf in Codex

### Schritt 1 – Umgebung und Quellen prüfen

Vorhandenes Repository und dessen Anweisungen lesen. Dann Spielversion, Installationspfad, Dokumenten-/Mod-Ordner und verfügbare DLCs ermitteln. Wenn die Spielinstallation nicht erreichbar ist, den benötigten Pfad oder die gezielt erforderlichen Originaldateien beim Nutzer anfordern. Inzwischen unabhängig davon an Konzept und eigenen Inhalten arbeiten.

### Schritt 2 – Minimal spielbares Land

Zuerst Länder-Tag, Definition, Historie, Startgebiet, Hauptstadt, Flagge und einfache OOB umsetzen. Erstes Ziel: Neues Spiel starten, Wesel-Flüren auswählen und einige Tage ohne modbedingten Fehler laufen lassen.

### Schritt 3 – Ein vollständiger Spielpfad

Grundlegende Wirtschaft, Militär und eine politische Route mit echten Belohnungen, Events und Entscheidungen vollständig implementieren. Diesen Ablauf testen, bevor weitere Verzweigungen dazukommen.

### Schritt 4 – Restliche Inhalte und Balance

Weitere Routen ergänzen. Anfangsnachteile, Industrie, Manpower, Ausrüstung und diplomatische Chancen aufeinander abstimmen. Große Gebietstransfers müssen einen nachvollziehbaren Preis oder Widerstand haben.

### Schritt 5 – Auslieferung

Geprüftes ZIP mit einfacher Anleitung erstellen. Dem Nutzer mitteilen, was enthalten ist, welche HoI4-Version geprüft wurde und welche Einschränkungen verbleiben. Keine Veröffentlichung im Workshop ohne gesonderten Auftrag.

## 9. Prüfliste und Abnahmekriterien

### Automatisch prüfbar

- Klammern, Anführungszeichen und Skriptstruktur sind gültig.
- Keine doppelten eigenen Länder-, Fokus-, Event-, Entscheidungs- oder Charakter-IDs.
- Alle referenzierten eigenen IDs existieren.
- Alle eigenen sichtbaren Texte besitzen Lokalisierung.
- Fokusvoraussetzungen bilden keine Zyklen; gegenseitige Ausschlüsse sind konsistent.
- Keine unbeabsichtigte Überschreibung kompletter Vanilla-Verzeichnisse.
- Hauptstadt und Startdivisionen gehören zum vorgesehenen Startgebiet.
- Bei Kartenänderungen: eindeutige Provinzzuteilung und konsistente Verweise.
- Alle eigenen Grafikpfade existieren; Flaggenformate und Größen stimmen.
- ZIP-Struktur und Descriptor-Pfade entsprechen der Installationsanleitung.
- Falls ein Installer enthalten ist: mit repräsentativen Dateistrukturen, Leerzeichen, Umlauten, fehlenden Dateien und wiederholter Installation prüfen; Originalspiel bleibt unverändert.

### Im Spiel prüfen

- Sauberer Start ohne relevante neue Einträge im `error.log`.
- Land ist auswählbar und besitzt Flagge, Namen, Hauptstadt, Regierung, Fokusbaum und Armee.
- Ein Fokus aus Wirtschafts- und Militärzweig lässt sich abschließen; Effekte werden tatsächlich angewendet.
- Jede politische Route lässt sich in einem eigenen Testspiel auswählen; die anderen werden entsprechend gesperrt.
- Eventoptionen wirken auf den richtigen Empfänger.
- Diplomatische Zusage und Ablehnung funktionieren.
- Entscheidungen ziehen korrekte Kosten ab, halten Abklingzeiten ein und sind nicht unbegrenzt ausnutzbar.
- Mindestens ein längerer Lauf bis 1937; vor einer stabilen Veröffentlichung möglichst auch bis 1939.
- Speichern und Laden erhält Figuren, Besitz, Flags und Fortschritt.
- Spiel mit den genannten DLCs und ohne andere Mods prüfen.

Für jedes Prüfergebnis Datum, Spielversion und tatsächliche Methode festhalten. **Statische Validierung ersetzt keinen Starttest im Spiel.** Ist das Spiel in Codex nicht verfügbar, diese Einschränkung ausdrücklich dokumentieren und eine präzise manuelle Testanleitung liefern.

## 10. Technische Quellen und Recherchehinweise

Die lokale aktuelle Spielinstallation ist die wichtigste Referenz für IDs und Syntax. Nicht alle Wiki-Seiten waren während der Vorrecherche direkt lesbar. Suchergebnisse und Spiegelungen können veraltet sein.

### Offizielle Versionsinformationen

- Paradox-Ankündigungen auf Steam: https://store.steampowered.com/news/posts/?appids=394360&feed=steam_community_announcements
- Bei der Recherche am 3. November 2026 wurde dort **QoL Patch 1.19.4**, veröffentlicht am **27. Oktober 2026**, mit einem Hotfix-Hinweis vom **29. Oktober 2026** gefunden. Das ist der damalige Recherchestand, keine Feststellung über die tatsächlich beim Nutzer installierte Version. Vor Entwicklungsbeginn erneut abgleichen.

### Dokumentation

- Länder: https://hoi4.paradoxwikis.com/Country_creation
- Fokusbaum: https://hoi4.paradoxwikis.com/National_focus_modding
- Entscheidungen: https://hoi4.paradoxwikis.com/Decision_modding
- Charaktere: https://hoi4.paradoxwikis.com/Character_modding
- Staaten: https://hoi4.paradoxwikis.com/State_modding
- Karte: https://hoi4.paradoxwikis.com/Map_modding
- Effekte: https://hoi4.paradoxwikis.com/Effect
- Modifier: https://hoi4.paradoxwikis.com/Modifiers
- Nationale Geister: https://hoi4.paradoxwikis.com/Idea_modding
- On-Actions: https://hoi4.paradoxwikis.com/On_actions

### Ergänzende technische Hilfsmittel

- CWTools-HoI4-Konfiguration: https://github.com/cwtools/cwtools-hoi4-config
- Relevante Schema-Dateien liegen unter anderem in `Config/common/characters.cwt`, `ideas.cwt`, `national_focus.cwt`, `decisions.cwt`, `bookmarks.cwt` sowie `Config/effects.cwt`, `Config/modifiers.cwt` und `Config/history/country_history.cwt`.
- CWTools ist eine hilfreiche zusätzliche Prüfung, aber weder das Spiel selbst noch eine Garantie für vollständige Übereinstimmung mit jeder aktuellen Version.
- Kaiserreich-Code: https://github.com/Kaiserreich/Kaiserreich-HOI4 – allenfalls als Beispiel für eine andere Mod. Dessen Staatsgrenzen, IDs, Kategorien, Lokalisierungen und Skripte nicht als Vanilla-Vorgaben behandeln.

## 11. Noch offene Entscheidungen

Nur Punkte nachfragen, die nicht aus der erreichbaren Installation oder diesem Briefing ableitbar sind und die konkrete Umsetzung blockieren:

1. Tatsächliche Spielversion und Zugriff auf die HoI4-Installation.
2. Genaues Startgebiet beziehungsweise gewünschte geografische Genauigkeit, falls dies vor einer Kartenänderung entschieden werden muss.
3. Persönliche Namen, Porträts oder Vereinslogos nur dann, wenn der Nutzer sie ausdrücklich verwenden möchte und die Dateien bereitstellt.

Für andere reversible Details zunächst die oben genannten Arbeitsannahmen verwenden. Insbesondere sind kein weiteres allgemeines Brainstorming und keine erneute Abfrage des bereits festgelegten Landes oder DLC-Umfangs erforderlich.

## 12. Direkt nutzbarer Startauftrag für Codex

> Lies dieses Briefing vollständig und entwickle die darin beschriebene Hearts-of-Iron-IV-Mod für Wesel/Flüren von Grund auf. Beachte die Trennung zwischen bestätigten Nutzervorgaben und vorgeschlagenen Arbeitsannahmen. Prüfe zuerst das Repository, die tatsächliche Spielversion und verfügbare lokale Spieldateien. Verifiziere das Startgebiet und sämtliche Provinz-/Staat-IDs, statt die ungeprüften Kandidaten aus der Vorrecherche zu übernehmen. Erstelle zuerst ein minimal spielbares unabhängiges Land für 1936 und erweitere es dann um Fokusbaum, politische Routen, Events, Entscheidungen und länderspezifische Einheitenboni. Implementiere die Inhalte vollständig, lokalisiere sie auf Deutsch und liefere ein installierbares Paket mit Anleitung und ehrlichem Prüfprotokoll. Nutze die genannten DLCs als Kompatibilitätsrahmen. Arbeite selbstständig an den nicht blockierten Aufgaben weiter; frage nur nach konkret fehlenden Informationen. Originaldateien des Spiels dürfen nicht verändert werden. Behaupte keine Ingame-Tests, die du nicht durchgeführt hast.
