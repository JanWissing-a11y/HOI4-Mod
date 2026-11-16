# Kevin von Beverungen I. in Polen

Stand: 8. November 2026.

Polen erhält auf Nutzerwunsch **Kevin von Beverungen I.** als neutralen
Herrscher. Die Unterideologie ist `despotism`, innerhalb der bestehenden
Vanilla-Gruppe `neutrality`. Seine beiden moderaten Eigenschaften gewähren
**+5 % politischen Machtgewinn** und **+5 Prozentpunkte Stabilität**.

Die eigene Datei `common/on_actions/zz_WFL_poland.txt` verwendet den lokal
belegten globalen `on_startup`-Hook mit explizitem `POL`-Scope. Sie erstellt
den Herrscher mit `create_country_leader`. Danach sucht `every_character` im
polnischen Landesscope nach der eindeutigen Eigenschaft
`WFL_POL_pragmatischer_koenig`. Im gefundenen **Charakterscope** setzt
`set_portraits` beide Porträts und `promote_character = yes` befördert genau
diese Instanz; Polen erhält anschließend Neutralität ohne Wahlen.

Ein echter Spielstart mit 1.19.4.2 zeigte, dass der zuvor unrekrutierte
Namensschlüssel nicht als Charakter-ID für `set_portraits` oder
`promote_character` verwendbar war. Deshalb behandelt der Code Name und
Laufzeit-ID jetzt ausdrücklich getrennt. Die lokale Vanilla-Vorlage
`common/scripted_effects/DEN_scripted_effects.txt:4120` sucht ebenfalls mit
`every_character` nach einem eindeutigen Trait und befördert die gefundene
Instanz mit `promote_character = yes`. Die lokale Effektdokumentation erlaubt
`set_portraits` ohne Charakterparameter innerhalb dieses Scopes.
`recruit_character` darf dagegen nur in der Spielhistorie stehen und wird hier
nicht verwendet.
Ein Initialisierungsflag verhindert erneute Erstellung oder Rücksetzung
späterer Regierungswechsel, falls der Hook nochmals ausgeführt wird. Ein nicht
existierendes Polen wird übersprungen. Vanilla-Länderhistorie, Starttruppen,
Technologien, Gesetze und die anderen Länder werden nicht überschrieben.

Spätere polnische Fokus- und Ereigniswege können wie bisher die Regierung
wechseln. Eine vollständige Abnahme aller polnischen DLC-Routen steht aus;
insbesondere können historische Personenabfragen andere Voraussetzungen haben,
wenn der Startregierungschef ersetzt wurde. Es werden keine globalen
Ideologien oder Originalcharaktere verändert.

Das gelieferte `Polnischer König mit Zepter und Reichsapfel.png` hat
1122 × 1402 Pixel. Der geprüfte Ausschnitt `(300,0,550,740)` bewahrt Gesicht,
Krone und königlichen Ornat. Mit `tools/prepare_portrait.ps1` entstehen die
große DDS (156 × 210), kleine DDS (65 × 67) und PNG-Vorschau. Das Original
wird ausschließlich gelesen. `tools/data/kevin_portrait.json` hält die
Quelldaten fest. Die Spielgrafiken liegen unter `gfx/leaders/POL`.

Die normale Einrichtung erfolgt beim neuen Spielstart. Vorhandene Spielstände
werden durch Dateiinstallation allein nicht zuverlässig nachgerüstet.
Porträt und tatsächliche Herrscherauswahl sind noch in der Engine zu prüfen.
Die begrenzte Testfixture vergibt absichtlich eine undurchsichtige Laufzeit-ID,
die sich vom Namensschlüssel unterscheidet. Sie prüft dadurch die Trait-Auswahl
und Charakter-Scopes, ohne den widerlegten direkten Namenszugriff nachzubilden.
Diese Fixture ist keine Engine-Simulation und bestätigt die neue Variante
noch nicht im laufenden Spiel.
