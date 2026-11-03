# Mit Codex auf dem Windows-PC weiterarbeiten

Die Cloud-Sitzung hat keinen Zugriff auf den privaten PC. Dafür eine lokale
Codex-Sitzung verwenden, beispielsweise die offizielle Codex-Erweiterung für
Visual Studio Code. Eine Erlaubnis im Cloud-Chat stellt keine Verbindung zum PC her.

1. Git für Windows von https://git-scm.com/downloads/win installieren.
2. Visual Studio Code von https://code.visualstudio.com installieren.
3. In VS Code unter Erweiterungen nach Codex suchen. Die offizielle Erweiterung
   von OpenAI installieren und mit dem ChatGPT-Konto anmelden.
4. Mit Strg+Umschalt+P die Befehlspalette öffnen, „Git: Clone“ wählen und
   `https://github.com/JanWissing-a11y/HOI4-Mod.git` eingeben. Einen lokalen
   Speicherort wählen und danach den geklonten Projektordner in VS Code öffnen.
5. In Steam: Bibliothek → Hearts of Iron IV → Zahnrad → Verwalten → Lokale Dateien
   durchsuchen. Den vollständigen Pfad aus der Explorer-Adresszeile kopieren.
6. Im geöffneten Projekt eine lokale Codex-Aufgabe starten. Den Spielpfad nennen
   und Zugriffe auf diesen konkreten Ordner gegebenenfalls freigeben. Falls die
   Oberfläche zwischen lokal und Cloud unterscheidet, lokal wählen.
7. Das gewählte Herrscherbild als Originaldatei auf dem PC speichern und der
   lokalen Sitzung seinen Pfad nennen. Es ist im Repository noch nicht verfügbar.

## Übergabeauftrag

> Arbeite an der Mod Wesel/Flüren weiter. Lies README.md, docs/STATUS.md und das
> Projektbriefing in docs/. Mein HOI4-Steam-Ordner ist: HIER DEN SPIELPFAD EINFÜGEN.
> Prüfe die tatsächlich installierte Version und die Originaldateien ausschließlich
> lesend. Verifiziere WFL auf Tag-Kollisionen, das Startgebiet von Wesel/Flüren,
> Hauptstadt und Provinzen; übernimm keine ungeprüften Kandidaten aus dem Briefing.
> Ergänze zuerst ein 1936 auswählbares Land mit Hauptstadt, Technologien, Gesetzen,
> Flaggen und passender Startarmee. Baue anschließend die begonnenen Inhalte aus.
> Verwende die im Briefing genannten DLCs. Mein Herrscherbild ist für den Anführer
> des Schützenkönigreichs bestimmt; seinen Dateipfad teile ich dir mit. Verändere
> keine Originaldateien des Spiels. Schreibe die Mod ins Repository und installiere
> sie in einem eigenen Mod-Ordner. Prüfe statisch und soweit möglich im Spiel;
> dokumentiere tatsächlich ausgeführte Tests und verbleibende Einschränkungen.

Der vorläufige Herrschername ist „Schützenkönig von Flüren“. Niemand wurde anhand
des Fotos identifiziert. Bildformat und Porträtgröße gegen die Spielversion prüfen.

## Prüfwerkzeuge

Python 3.10 oder neuer wird für die Werkzeuge benötigt; das Spiel selbst braucht
Python nicht. In der Cloud ist Python 3.12 vorhanden. Unter Windows bei Bedarf
Python separat installieren. Im Projektordner ausführen:

```sh
python tools/validate_mod.py
python -m unittest discover -s tests -v
git diff --check
```

Für die Abnahme HOI4 über den Launcher mit der Mod starten. Die statischen
Prüfungen ersetzen keine Spielengine. Der aktuelle Stand ist nicht spielbar.
