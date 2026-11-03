# Prüfprotokoll

Stand: 3. November 2026. Umgebung: Linux-Cloud, Python 3.12.

Ausgeführt und erfolgreich:

- `python3 tools/validate_mod.py`: zehn Skriptdateien, ein Tag, vier Charaktere,
  vier Ideen, elf Fokusse, zwei Events, eine Kategorie und zwei Entscheidungen;
  eigene Referenzen, Fokusgraph und DE/EN-Lokalisierung geprüft.
- `python3 -m unittest discover -s tests -v`: elf Tests ausgeführt, elf bestanden.
  Darunter gezielt beschädigte Referenzen, zyklische Fokusvoraussetzungen,
  asymmetrische Ausschlüsse, doppelte Events und fehlerhafte Lokalisierung.
- `git diff --check`: keine Whitespace-Fehler.

Nicht ausgeführt: Spielstart, Länderauswahl, Kartenprüfung, Porträtanzeige,
DLC-Kompatibilität, Effekte und Regierungswechsel in der Engine, Entscheidungen
im Spiel, Speichern/Laden und Langzeitläufe. Eine erfolgreiche statische Prüfung
ist kein Nachweis der Spielbarkeit.
