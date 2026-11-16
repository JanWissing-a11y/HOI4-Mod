# Lukas Höhne I.

Stand: 4. November 2026. Auf Nutzerwunsch besitzt Wesel-Flüren einen bereits
1936 verfügbaren Feldmarschall namens **Lukas Höhne I.**

| Fähigkeit | Startwert |
| --- | --- |
| Stufe | 9 |
| Angriff | 9 |
| Verteidigung | 9 |
| Planung | 9 |
| Logistik | 9 |

Er erhält sieben starke, miteinander verträgliche Vanilla-Eigenschaften:

- `brilliant_strategist`: Brillanter Stratege.
- `organizer`: Organisator, zugleich Voraussetzung für Logistik und Planung.
- `offensive_doctrine`: weniger Organisationsverlust bei Bewegung.
- `logistics_wizard`: geringerer Versorgungsverbrauch, zusätzliche Nachschubfähigkeit.
- `thorough_planner`: höherer maximaler Planungsbonus.
- `organisational_leader`: höhere Verstärkungsrate.
- `inspirational_leader`: bessere Organisationserholung.

Die lokalen Spieltabellen enthalten Stufe 9 und alle vier Fähigkeiten mit Wert 9
für Feldmarschälle. Die Werte und Eigenschaften sind absichtlich außergewöhnlich
stark. Es werden keine globalen Fähigkeiten oder Vanilla-Traits geändert.
Jans Regierung und sein eigenes Porträt bleiben erhalten.

Das bereitgestellte Offiziersbild wird unverändert im Inhalt übernommen,
zugeschnitten und in 156 × 210 bzw. 65 × 67 große BGRA-DDS umgewandelt. Die
große PNG-Vorschau liegt neben den DDS. Quelle: Nutzerbild im Desktop-Ordner
Hoi4mod, 1075 × 1463 Pixel. Großer Ausschnitt: x=225, y=20, Breite=720,
Höhe=969. Das Originalbild wird ausschließlich gelesen.

Reproduktion in PowerShell mit dem Originalpfad als `$portraitSource`:

~~~powershell
& .\tools\prepare_portrait.ps1 -Source $portraitSource `
  -Output .\gfx\leaders\WFL\Portrait_WFL_lukas_hoehne_i.dds `
  -SmallOutput .\gfx\leaders\WFL\Portrait_WFL_lukas_hoehne_i_small.dds `
  -Preview .\gfx\leaders\WFL\Portrait_WFL_lukas_hoehne_i.png `
  -Crop @(225,20,720,969) -ExpectedSize @(1075,1463)
~~~

Die internen IDs sind `WFL_lukas_hoehne_i` und
`GFX_portrait_WFL_lukas_hoehne_i` mit kleiner `_small`-Variante. Die Rekrutierung
steht in der Länderhistorie. Ein bereits laufender Spielstand übernimmt diese
Startrekrutierung nicht automatisch; für die reguläre Verfügbarkeit ein neues
Spiel beginnen. Eine Sicht- und Funktionsprüfung in der Engine steht noch aus.
