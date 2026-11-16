# Abzeichen des Schützenrats

Stand: 9. November 2026. Alle fünf vom Nutzer benannten Originaldateien wurden
im Downloadordner gefunden. Die Originaldateien bleiben unverändert.
Die Freistellung erfolgte mit dem eingebauten **Imagegen**-Werkzeug. Transparent
ist nur die äußere dunkle Fläche einschließlich der Lücken am Lorbeerkranz;
die grün-weiße Fahne innerhalb der Medaillons gehört weiterhin zum Motiv.

| Name | Gelieferte Datei | Freigestelltes PNG im Projekt |
| --- | --- | --- |
| Dante Grossy | Militärmedaillon mit goldener Ehrenlaurbe.png | `gfx/interface/beraterstab/source/dante_grossy.png` |
| Neal Foerster | Goldenes Koch-Abzeichen mit Wasserglas.png | `gfx/interface/beraterstab/source/neal_foerster.png` |
| Max Heinsch | Bronzenes Medaillon mit grünem Uniformporträt.png | `gfx/interface/beraterstab/source/max_heinsch.png` |
| Max Müller | Militärisches Porträt mit Lorbeerwappen.png | `gfx/interface/beraterstab/source/max_mueller.png` |
| Till Hoehne | Militärisches Porträt mit Lorbeeremblem.png | `gfx/interface/beraterstab/source/till_hoehne.png` |

Alle fünf PNGs sind 1254 × 1254 Pixel groß und besitzen einen Alphakanal.
`tools/prepare_staff_icons.ps1` konvertiert die vorhandenen freigestellten
Dateien in 102 × 90 Pixel große Fokusgrafiken und 128 × 128 Pixel große
Fenstergrafiken. Seitenverhältnis und Alpha bleiben erhalten; das Werkzeug
führt keine weitere Freistellung durch. Die DDS-Dateien enthalten sowohl
vollständig transparente als auch vollständig deckende Pixel. Die fünf
kleinen Abzeichen wurden vor einem Schachbrettmuster visuell geprüft.
Die Fokusgrafiken besitzen zusätzlich die übliche Glanzanimation.

## Verwendete Bearbeitungsanweisungen

Für Dante Grossy wurde genau diese Anweisung mit seiner Originaldatei und
`transparent_background = true` verwendet:

```text
Edit target: the supplied square portrait medallion 'Militärmedaillon mit goldener Ehrenlaurbe.png'. Background removal only for a Hearts of Iron IV focus-tree icon. Preserve the complete existing medallion, its face identity and expression, clothing, objects, metal rim, gold/bronze laurel leaves, lower shield, lighting, textures and all green-white flag fabric INSIDE the medallion exactly as provided. Do not redesign, repaint, beautify or replace any person or object. Remove only the black/dark exterior backdrop OUTSIDE the complete medallion silhouette, including exterior negative gaps between laurel leaves. Those exterior pixels must be genuinely transparent alpha, with clean antialiased edges, no black fringe or rectangular shadow. Preserve protruding hair/chef hat and every laurel tip. Same centered composition and aspect ratio; entire badge remains uncropped. No new text or symbols. Return one transparent PNG.
```

Für die anderen vier Originaldateien wurde je eine eigene Bearbeitung mit
derselben folgenden Vorlage ausgeführt. `[DATEINAME]` wurde durch den jeweiligen
gelieferten Dateinamen aus der Tabelle ersetzt; auch hier war
`transparent_background = true` gesetzt:

```text
Background removal only. Edit the supplied portrait medallion '[DATEINAME]' for a Hearts of Iron IV focus icon. Preserve the entire original medallion and all its details: exactly the same person's facial identity/expression, clothes, held objects, gold or bronze laurel, metal rim, lower coat of arms, and green-white flag fabric INSIDE the rim. Remove ONLY the dark exterior background OUTSIDE the medallion silhouette and external gaps around laurel leaves; make it genuine transparent alpha. Keep the interior flag background. No redraw, new portrait, new objects, new text, or redesign. Keep protruding hair/chef hat and every leaf tip uncropped. Clean antialiased outline with no black halo. One square transparent PNG.
```

Die generative Freistellung kann trotz der Erhaltungsanweisung kleine
Detailabweichungen erzeugen. Die Motiv- und Namenszuordnung wurde anhand der
Originale überprüft. Eine Darstellung in der HoI4-Engine steht noch aus.
