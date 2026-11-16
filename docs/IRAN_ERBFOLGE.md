# Iran: Al Höhnes Thronfolge

Vier Fokusse à 35 Tage folgen auf `WFL_vereinsdiplomatie`: **Teheraner Thronstolpern**, **Höhnes persische Mission**, **Liebe geht durch den Zapfhahn**, **Al Höhne und der Treuevertrag**. Die eigene Spalte nutzt x=30, y=3–6. Der Layoutprozess hält das kontinuierliche Fokusfeld unten links frei.

Die Geschichte ist eine erfundene Hofkomödie mit dubiosen Todesfällen, einer ausdrücklich erwachsenen Prinzessin Shirin, einer einvernehmlichen Romanze und Hochzeit. Die männliche Thronfolge ist eine erfundene Regel dieses Hofes. Lukas Höhne wird als **Al Höhne** neutraler iranischer Schah. Der bestehende Feldmarschall `WFL_lukas_hoehne_i` bleibt unverändert; eine eigene Charakterdefinition bildet ausschließlich die neue Herrscherrolle ab. Al Höhnes Eigenschaft gibt +5 % politische Macht und +5 Prozentpunkte Stabilität.

## Verbindlicher Abschluss

Alle Fokusse verlangen ein unabhängiges, nicht kapituliertes WFL. Ein Wechsel des iranischen Herrschers, ein Krieg, ein fremder Oberherr, ein bereits von WFL unterworfener Iran und ein vollständig annektierter Iran sperren den Pfad nicht. Der letzte Fokus ruft **sofort** `WFL_establish_iranian_puppet_effect` auf. Die vier Eventfenster erzählen die Geschichte, ihre Schaltflächen blockieren keine Wirkungen. Es gibt keine Zufallswürfe und keine ablehnbare Anfrage an die iranische KI.

Der Effekt:

1. Stellt einen nicht mehr existierenden Iran durch Übertragung seiner Kernstaaten an `PER` wieder her. Dadurch können bisherige Eigentümer iranische Kerngebiete verlieren; sie werden weder annektiert noch politisch umgestürzt. Falls andere Skripte sämtliche iranischen Kerne entfernt haben, wird der historisch bestätigte Hauptstadtstaat **266 (Teheran/Persien)** als einzelner Anker verwendet. Ein bereits existierender Iran behält seine bisherigen Grenzen; fremde Nicht-Iran-Gebiete werden nicht zusätzlich übertragen.
2. Löst ausschließlich PER von einem fremden Oberherrn. Führt PER selbst ein Bündnis mit WFL, übernimmt WFL dessen Führung. Ein fremdes iranisch geführtes Bündnis wird aufgelöst; sonst verlässt PER nur ein fremdes Bündnis. Andere Regierungen werden nicht geändert.
3. Setzt PER direkt per `puppet` unter WFL. `end_wars = yes` und `end_civil_wars = yes` beenden dessen bisherige Kriegsbeziehungen. Mit Together for Victory wird zusätzlich explizit `autonomy_puppet` mit Freiheitswert 0 gesetzt; ohne dieses DLC bleibt der Vanilla-Marionetteneffekt bestehen.
4. Gibt PER die tatsächliche Kontrolle seiner eigenen Staaten zurück. Wenn `any_character` noch keine Instanz mit dem eindeutigen Trait `WFL_PER_fluerentreuer_schah` findet, erstellt `create_country_leader` den Herrscher mit dem Namensschlüssel `WFL_PER_al_hoehne`. Anschließend wählt `every_character` diese Instanz anhand des Traits, setzt im Charakterscope beide Porträts und befördert sie mit `promote_character = yes`. Name und Laufzeit-ID werden nicht gleichgesetzt. Danach gilt `neutrality` ohne Wahlen. Eine bereits vorhandene Instanz mit diesem Trait wird wiederverwendet. Der history-exklusive Befehl `recruit_character` steht nicht im Laufzeiteffekt.
5. Setzt eine Abschlussflagge und zeigt die Krönung. Ein wiederholter Effektaufruf verändert weder einen späteren Herrscherwechsel noch die Karte erneut.

Die Marionettenbildung ist damit für den freigeschalteten Fokuspfad fest geskriptet. Die üblichen späteren Spielhandlungen können die Beziehung erneut verändern. Es wird keine dauerhafte Unterwerfung durch periodische Zwangseffekte behauptet.

## Quellen und Prüfung

Der tatsächliche Iran-TAG `PER`, der Hauptstadtstaat 266 und die Befehle wurden gegen die installierten Vanilla-Dateien **1.19.4.1** geprüft:

- `documentation/effects_documentation.md`: `transfer_state`, `end_puppet`, `puppet`, `set_autonomy`, `set_state_controller_to`, `create_country_leader`, `set_portraits`, `promote_character`, `set_politics`, `leave_faction`, `dismantle_faction`, `set_faction_leader`.
- Laufzeitkorrektur vom 8. November: Der echte Spielstart mit 1.19.4.2 widerlegte die Annahme, dass `create_country_leader` den Namen einer bisher unrekrutierten Definition als direkt ansprechbare Charakter-ID registriert. Der korrigierte Zugriff verwendet deshalb eine Trait-Suche. `common/scripted_effects/DEN_scripted_effects.txt:4120` zeigt genau dieses Vanilla-Muster: `every_character`, eindeutiges `has_trait` und `promote_character = yes`. Die Effektdokumentation erlaubt `set_portraits` im Charakterscope ohne erneuten ID-Parameter. Die tatsächliche Funktion der neuen Variante ist noch in der Engine zu prüfen; die frühere Schlussfolgerung aus der Dokumentation allein war nicht ausreichend.
- `common/scripted_effects/ETH_scripted_effects.txt`: Wiederherstellung eines nicht existierenden TAGs durch `transfer_state = PREV` in dessen Länderscope, danach `set_autonomy` mit DLC bzw. `puppet` ohne DLC.
- `common/scripted_effects/AST_scripted_effects.txt`: fremden Oberherrn über `overlord = { end_puppet = PREV }` lösen und anschließend neu unterwerfen.
- `history/countries/PER - Persia.txt`: Hauptstadt 266; `common/country_tags/00_countries.txt`: Iran/Persien = PER.

`tests/test_iran_succession.py` führt den tatsächlich geparsten Effekt gegen gezielte Weltzustände aus: bestehender Iran, fremde Marionette, eigene Marionette, Krieg, Annexion mit mehreren Eigentümern, eigene Besetzung, entfernter Kernbestand, DLC an/aus, Bündnisführung und wiederholter Aufruf. Erstellte Charaktere besitzen absichtlich undurchsichtige IDs statt ihrer Namensschlüssel. Auch bereits aus einem Spielstand geladene Instanzen werden anhand ihres Traits erkannt. Die Prüfung ist ein begrenzter AST-Interpreter und **kein Ersatz für einen Engine-Test**. Charaktername, Porträt-Sprites, DDS-Abmessungen, Fokusverkettung und deutsch/englische Lokalisierung werden zusätzlich geprüft.

Quellporträt: vom Nutzer bereitgestelltes `Selbstbewusster Offizier mit Zigarre.png`. Importmanifest: `tools/data/al_hoehne_portrait.json`.
