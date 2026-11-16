# Eigene Grafiken

Stand: 5. November 2026.

## Herrscher und Personen

Jans bereits gewähltes Gemälde bleibt unverändert als großes DDS-Porträt
(156 × 210) erhalten. Eine kleine Variante (65 × 67) stammt aus demselben
Bild. Der SHA-256 des großen Porträts ist weiterhin
`e37886ad6c40bd7f4dcdbb97cfab05095acd57dd85dcb72e8c464c9b0b0d65e4`.

18 ausgewählte Fotoausschnitte ersetzen die übrigen WFL-Personenporträts.
`tools/data/advisor_portraits.json` dokumentiert Quelldateinamen und
Ausschnittkoordinaten. `tools/prepare_advisor_portraits.ps1` erzeugt große
und kleine DDS sowie ausgeschnittene PNG-Quellen. Die Fotos werden nur
beschnitten und skaliert, Gesichter nicht synthetisch verändert oder identifiziert.
Die Namen der Berater und Wissenschaftler sind fiktiv.

Die eigenen Länderpools in `portraits/WFL_portraits.txt` gelten für WFL und
den kosmetischen Königreich-Tag. Erfasst sind Heer, Marine, Politik, Agenten,
Wissenschaftler und allgemeine Personen-Fallbacks. Historische Porträts anderer
Länder werden nicht ersetzt. Die Wirkung auf bereits gespeicherte, vom Spiel
erzeugte Charaktere ist nicht zugesichert; für die Abnahme ein neues Spiel starten.

Feldmarschall **Lukas Höhne I.** verwendet das neu gelieferte Offiziersgemälde
als eigenes großes und kleines DDS. Der geprüfte Ausschnitt bewahrt Gesicht,
Mütze und Uniform. Bildquelle, Ausschnitt und Reproduktion sind in
[FELDMARSCHALL.md](FELDMARSCHALL.md) dokumentiert. Jans DDS bleibt unverändert.

Die drei Generäle verwenden ebenfalls eigene große und kleine DDS aus den
gelieferten Uniformporträts. Die bestätigte Zuordnung lautet: Ian Jannis Foerster
mit wuscheligen Haaren und Brille, Nils Schapfeld I. mit Schützenhut und Brille,
Lars Stüwe mit kurzen Haaren ohne Brille. Die Vorschauen wurden visuell geprüft.
Quellen und Ausschnitte stehen in [GENERALE.md](GENERALE.md) und
`tools/data/commander_portraits.json`.

Florian Klaus verwendet das am 5. November gelieferte `image.png`: Brille,
Pfeife und Anzug. Große und kleine DDS sowie die geprüfte PNG-Vorschau
stammen aus demselben Ausschnitt. Quelle und Reproduktion sind in
`tools/data/florian_klaus_portrait.json` und
[FLORIAN_UND_MOBILISIERUNG.md](FLORIAN_UND_MOBILISIERUNG.md) dokumentiert.

Polens neutraler Herrscher Kevin von Beverungen I. erhält das bereitgestellte
Königsgemälde mit Krone als großes und kleines DDS. Die geprüfte Vorschau zeigt
Gesicht und Ornat; Quelle und Ausschnitt stehen in `tools/data/kevin_portrait.json`
und [POLEN.md](POLEN.md).

Al Höhne verwendet das Zigarrengemälde aus `Selbstbewusster Offizier mit Zigarre.png`
für seine iranische Herrscherrolle. Der Ausschnitt (280,0,600,808) aus 1122×1402
zeigt Gesicht, Zigarre und goldene Uniform. Die große PNG-Vorschau wurde visuell
geprüft; große und kleine DDS entstehen aus demselben Ausschnitt. Reproduktion:
`tools/data/al_hoehne_portrait.json`. Das bestehende Feldmarschallporträt von
Lukas Höhne I. bleibt erhalten.

## Nationalflagge

Die Landesfarbe auf der politischen Karte ist seit dem 8. November 2026
Schützengrün **#236B3B** (RGB 35, 107, 59), definiert in
`common/countries/Wesel-Flueren.txt`. Die Flaggenfarben bleiben davon unabhängig.

Die Flagge trägt das gelieferte Flürener Wappen auf Weiß mit roten Randstreifen
und schmalen goldenen Trennlinien. Sie ersetzt die Grundflagge und alle vier
Ideologievarianten, jeweils in 82 × 52, 41 × 26 und 10 × 7 Pixeln.

Erzeugung: integriertes ImageGen, Modus **Bearbeitung/Compositing** mit dem
gelieferten Wappen als Referenz. Finale Bildquelle: `gfx/flags/source/WFL_flag.png`.
Originalwappen: `gfx/flags/source/WFL_coat_of_arms.png`.
Technische Konvertierung: `python tools/generate_flags.py`; alle 15 Spieltexturen
sind unkomprimierte 32-Bit-TGA. Die DDS- und TGA-Dateien sind bereits im Paket;
zum Spielen ist keine erneute Bildgenerierung nötig.

Nach dem Hinweis auf eine kopfstehende Ingame-Flagge wurde die TGA-Zeilenrichtung
korrigiert: Alle 15 Texturen verwenden jetzt Ursprung unten links (Descriptor
0x08) und entsprechend von unten nach oben gespeicherte BGRA-Zeilen. Die lokale
Vanilla-Flagge verwendet ebenfalls einen Ursprung unten links. Die aufrechte
PNG-Bildvorlage bleibt unverändert. Der Validator prüft die Ausrichtung und
Vollständigkeit aller Ideologievarianten. Ein Neustart von HoI4 lädt die neuen
Texturen; eine erneute Sichtprüfung im Spiel steht noch aus.

Verwendeter Prompt:

Use case: compositing. Asset type: flat national flag texture for the Hearts of Iron IV nation Wesel-Flueren. Input image 1 is the exact coat of arms to retain: a black-outlined red shield, yellow rising sun with red/yellow rays, one blue wavy horizontal band, and a large yellow bell. Create one finished horizontal flag, width:height exactly 82:52, with the flag filling the entire rectangular canvas edge to edge. Design: a clean white central field, narrow bright-red horizontal stripes along the top and bottom edges (each about 8% of flag height), with a thin golden-yellow line separating each red stripe from the white field (each about 2% of flag height). Center the supplied coat of arms prominently in the white field, occupying approximately 76% of the full flag height. Preserve the supplied shield, its proportions, the bell, the ray pattern, the single blue wave, black outlines and colors faithfully; do not redesign or simplify the emblem, and remove any white rectangle surrounding it by merging that white into the white flag field. Crisp clean heraldic graphic suitable for tiny game UI sizes. No text, letters, numbers, crown, additional emblems, flagpole, waving fabric, folds, shadow, lighting, texture, frame, perspective, background scene, watermark or decorative flourishes. This must be the actual flat flag graphic, not a mockup.
