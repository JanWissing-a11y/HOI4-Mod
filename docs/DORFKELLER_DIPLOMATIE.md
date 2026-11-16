# Dorfkeller Diplomatie

Stand: 10. November 2026, lokale Referenz HoI4 1.19.4.2.

Der 35-Tage-Fokus `WFL_dorfkeller_diplomatie` setzt die Zapfhahnkrise und damit
die Anglo-Bier-Diplomatie voraus. Er liegt auf x=28, y=5 direkt darunter.
Die abgeschlossene Zapfhahnkrise genügt als Voraussetzung, unabhängig vom
Ereignisausgang. Die unsichtbare Erfolgsflagge ist keine zusätzliche Sperre mehr.
Damit bleiben auch ältere Spielstände und ein Abschluss durch Zeitablauf spielbar.

## Voraussetzungen

- Wesel-Flüren ist unabhängig, nicht kapituliert und in keinem Bündnis.
- Großbritannien existiert und gehört den Alliierten an.
- Die aktuelle Führung der Alliierten existiert, ist unabhängig und nicht kapituliert.
  Ein Führungswechsel oder eine andere britische Ideologie blockiert den Fokus nicht.
- Wesel-Flüren führt mit keinem Mitglied dieses Bündnisses Krieg.

Der gemeinsame Trigger in `common/scripted_triggers/WFL_dorfkeller_triggers.txt`
prüft diese Bedingungen bei Auswahl und Abschluss. Der Allies-Nachweis erfolgt
über `has_faction_template = faction_template_allies`; eine umbenannte Fraktion
bleibt erkennbar, ein anderes britisches Bündnis qualifiziert sich nicht.
Die Voraussetzungen erscheinen einzeln im Fokus-Tooltip statt als ein einziger
zusammengefasster, schwer zu prüfender Text.
Ist Flüren bereits bei den Alliierten mit Großbritannien, wird der Fokus
übersprungen. Eigene oder fremde Bündnisse werden niemals automatisch aufgelöst.
Bei ungültig gewordenen Bedingungen wird der Fokus regulär abgebrochen.

## Abschluss und Geschichte

Bei gültigem Abschluss fügt `ENG = { faction_leader = { add_to_faction = ROOT } }`
Flüren direkt den Alliierten hinzu. Der Effekt verwendet ihre aktuelle Führung,
auch wenn Großbritannien die Bündnisführung bereits abgegeben hat. Es gibt keinen Zufallswurf und keine britische
Entscheidungsoption, die den Beitritt ablehnen oder verzögern kann.
Die normale Kriegsbeitrittsmechanik bleibt bestehen; der Fokus erklärt keinen Krieg.
Der Abschluss prüft die Bedingungen erneut und vergibt bei einem unmöglichen
Beitritt einmalig 50 PP. Eine Abschlussflagge verhindert doppelte Beitritte,
Ereignisse oder Ersatzbelohnungen bei wiederholtem Effektaufruf.

Nach tatsächlicher Bündnisaufnahme folgt das Ereignis **Der Dorfkeller-Vertrag**:
Die britische Delegation findet statt eines Konferenzsaals eine Kegelbahn.
Auf einem Bierdeckel werden gegenseitiger Beistand und der Gläserdienst
vereinbart. London bestätigt den Beitritt, der Wirt rahmt die Urkunde ein und
legt den Pfandbon ins Staatsarchiv. Das Ereignis erzählt die Geschichte;
seine Schaltfläche hat keine weiteren Spielwirkungen.

## Quellen und Prüfung

Lokale Vanilla-Belege:

- `history/countries/ENG - Britain.txt`: Großbritannien erzeugt die Alliierten
  mit `create_faction_from_template = faction_template_allies`.
- `documentation/triggers_documentation.md`: `has_faction_template`,
  `is_faction_leader`, `has_government`, `is_in_faction_with` und `any_country`.
- `events/AAT_Denmark.txt`, Zeile 7458: `faction_leader = { add_to_faction = ROOT }`.
- `documentation/triggers_documentation.md`: `has_faction_template` prüft die
  Zugehörigkeit des Landes zu einer Fraktion mit der angegebenen Vorlage.
- `interface/goals.gfx`: das verwendete Symbol `GFX_goal_generic_alliance`.

Ein unabhängiger Agent hat die Voraussetzungen gegen diese Quellen geprüft.
Zehn begrenzte Skripttests prüfen Beitritt, alte Spielstände ohne Erfolgsflagge,
wechselnde Bündnisführung, britische Regierungswechsel, veränderte Partner, Kriege,
vorhandene Bündnisse und wiederholte Aufrufe. Sie ersetzen keine Engine-Abnahme.
Die Layoutprüfungen sichern weiterhin mindestens 300 Pixel Abstand des
kontinuierlichen Fokusfelds sowie freie Positionen für sämtliche 78 Fokusse.
Die aktualisierte schematische PNG-Übersicht wurde visuell geprüft; der Abstand
bleibt bei 302 Pixeln. Der neue Fokus liegt unter der Zapfhahnkrise und neben
der Iran-Hochzeit, ohne deren Position zu verändern.
Der zusätzliche Beraterstab liegt weiter rechts auf den Spalten 34–42.
Sein 960 × 590 Pixel großes Inlay bei x=3300, y=1000 überdeckt weder diese
Diplomatiereihe noch die kontinuierlichen Fokusse unten links.

Die frühere Sperre durch die Erfolgsflagge und die britische Regierungs- bzw.
Führungsrolle ist im Skript nachgewiesen. Welche davon den konkreten Spielstand
blockiert hat, ist ohne dessen Daten nicht feststellbar. Eine Engine-Abnahme der
Korrektur steht noch aus.
