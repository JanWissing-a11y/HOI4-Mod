# Entwicklungsstand

Stand: 3. November 2026.

Implementiert sind die vorläufige WFL-Länderdefinition und Länderhistorie, vier
fiktive Führungen, elf Fokusse, vier nationale Geister, zwei politische Events,
zwei einmalige Entscheidungen mit Kosten sowie deutsche und englische Texte.
Die politischen Wege Bürgerrepublik, Schützenkönigreich und Direktorium sind
gegenseitig ausgeschlossen. Ihre vollständigen Inhalte sind weiterhin Ausbauziele.

Der Python-Prüfer kontrolliert die im Projekt verwendete Skriptstruktur, eigene
Referenzen, Fokuszyklen, symmetrische Ausschlüsse und Textabdeckung. Er ist kein
vollständiger HOI4-Schema- oder Scope-Prüfer. Die automatisierten Negativtests
prüfen, dass typische Struktur- und Referenzfehler tatsächlich erkannt werden.

## Noch nicht spielbar

Es fehlen verifiziertes Startgebiet, Hauptstadt, Kerne, konkrete Technologien,
Gesetze, Startaufstellung, Flaggen und die finale Porträteinbindung. WFL besitzt
keinen Staat und ist nicht bei der Länderauswahl vorhanden. Es gibt keine Änderung
der Vanilla-Staatsdateien und keinen flächigen replace_path-Eintrag.

WFL ist noch auf Tag-Kollisionen zu prüfen. Vanilla-Icons, Kulturen, Ideologien
und Modifier müssen mit der tatsächlichen Spielversion abgeglichen werden.
Die unbestätigten IDs 51, 57, 529 und 3512 aus dem Briefing wurden nicht als
verifizierte Kartenreferenzen verwendet. supported_version ist nicht gesetzt.

## Entscheidungen aus dieser Sitzung

- Die Entwicklung der Wesel/Flüren-Mod soll beginnen.
- Das bereitgestellte Herrscherbild ist für den Anführer des Schützenkönigreichs
  bestimmt. Das Original liegt noch nicht als Bilddatei im Repository vor;
  deshalb gibt es noch keine aktive Porträtreferenz. Der Name ist vorläufig.
- HOI4 ist auf dem PC des Nutzers über Steam installiert. Aus der Cloud besteht
  kein Zugriff auf dessen lokale Dateien. Gewünscht ist die lokale Weiterarbeit.

Das unveränderte Briefing trennt frühere Anforderungen und Konzeptvorschläge.
Die politischen Wege sind reversible Arbeitsannahmen. Für den nächsten Schritt
siehe [LOKAL_WEITERARBEITEN.md](LOKAL_WEITERARBEITEN.md).

## Ausstehende Abnahme

Nach Kartenprüfung und Herstellung des auswählbaren Landes: Spielstart und neue
error.log-Meldungen prüfen; Wirtschafts- und Militärfokus abschließen; jede Route
separat wählen; Entscheidungen, Speichern und Laden prüfen; einen Lauf bis 1937
mit den im Briefing genannten DLCs und ohne andere Mods durchführen. Datum,
Spielversion, Methode und Ergebnisse im Prüfprotokoll dokumentieren.
