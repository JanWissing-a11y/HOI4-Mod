# Deutschland unter dem Schützenhut vereinen

Stand: 10. November 2026. Die kostenlose Entscheidung benötigt jetzt
**Deutschlands Startterritorium vom 1. Januar 1936**, einschließlich des für
Flüren abgetrennten Teils von Moselland. Spätere deutsche Kerngebiete,
Annexionen und Ansprüche erweitern diese Voraussetzung nicht mehr.

Erforderliche Staaten aus den lokalen Vanilla-Historien und Mod-Overrides
(GER-Eigentum 1936 plus WFL-Heimatstaat):

`5, 42, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 763, 909, 978, 1082`

WFL muss alle 25 Staaten **besitzen und vollständig kontrollieren**. Bloße
Besetzung ohne Eigentum und Teilkontrolle genügen weiterhin nicht. GER muss
nicht mehr existieren. Krieg oder Untertanenstatus fügen keine Sperre hinzu.
Auswahl und Ausführung prüfen denselben Ländertrigger
`WFL_controls_germany_1936`.

Alle 25 Startstaaten erhalten WFL-Kerne, auch wenn GER dort inzwischen seine
Kerne verloren hat. Weitere aktuelle GER-Kerne werden ebenfalls gekernt,
wenn WFL sie besitzt und vollständig kontrolliert. Fremde zusätzliche
GER-Kernstaaten blockieren die Entscheidung nicht.

Auf fremde aktuelle GER-Kernstaaten werden WFL-Ansprüche gesetzt. Zusätzlich
werden die fünf östlichen Ansprüche des Vanilla-Fokus
`GER_reassert_eastern_claims` ausdrücklich übernommen, soweit diese Staaten
nicht bereits WFL gehören:

| Staat | ID |
| --- | --- |
| Danzig | 85 |
| Memel | 188 |
| Gdingen | 807 |
| Posen | 86 |
| Kattowitz | 762 |

Diese Gebiete müssen nicht vorher erobert werden. Danzig besitzt 1936 keinen
GER-Kern; eine dynamische GER-Kernprüfung allein würde seinen Anspruch nicht
sichern. Bestehende Ansprüche und fremde Kerne werden niemals entfernt.
Ansprüche allein verleihen keinen WFL-Kern und übertragen keine Staaten.
Nach Abschluss eroberte Außengebiete werden durch diese einmalige Entscheidung
nicht nachträglich automatisch gekernt.

Der Staatsgeist `WFL_volk_unter_schuetzenhut` mit **+20 Prozentpunkten
rekrutierbarer Bevölkerung** wird bei Erfolg entfernt. Andere Staatsgeister
bleiben erhalten. `WFL_deutschland_vereint_done` verhindert eine Wiederholung.
Schlägt die erneute Prüfung beim Ausführen fehl, bleiben Staatsgeist und
Entscheidung erhalten. Ein bereits fehlender Staatsgeist verhindert den
Abschluss nicht.

Die Entscheidung behält ihre ID und funktioniert in alten Spielständen,
solange sie dort noch nicht erfolgreich abgeschlossen wurde. Regionale
Integrationen und Referenden bleiben eigenständig.

Elf begrenzte Skripttests prüfen die tatsächlichen Trigger und Effekte mit
festem Startgebiet, fehlendem Besitz, Teilkontrolle, optionalen Auslandsgebieten,
zusätzlichen Kernen, Ansprüchen und einmaligem Abschluss. Sie ersetzen keine
Engine-Prüfung.


Seit dem 16. November 2026 setzt der erfolgreiche Abschluss zusätzlich
den Staatsnamen **Groß Flürener Reich**. Bereits vereinte Spielstände
erhalten den Namen beim Laden beziehungsweise spätestens am nächsten
Spieltag; Kerne und sonstige Belohnungen werden dabei nicht erneut vergeben.
Eine spätere Krönung erhält diesen Namen.
