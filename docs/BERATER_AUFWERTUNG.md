# Weiterbildung der politischen Berater

Stand: 4. November 2026. Referenz ist die lokal installierte HoI4-Version
**1.19.4.1**. Diese Erweiterung ergänzt die 37 WFL-Beraterprofile um die acht
aktiven späteren Fähigkeitsvarianten der deutschen Vorlage.

Nach dem Fokus **„Die Berufskolleg Wesel“** erscheint die Entscheidungskategorie
**„Weiterbildung der politischen Berater“**. Jede Weiterbildung kostet einmalig
**100 politische Macht**. Der passende WFL-Charakter muss im Land vorhanden,
bereits eingestellt und tatsächlich in der Rolle political_advisor tätig sein.
Eine zusätzliche Länderflagge verhindert die wiederholte Nutzung.

## Zuordnung

| WFL-Profil | Alter WFL-Trait | Neue Eigenschaft | Verbesserte Vanilla-Vorlage |
| --- | --- | --- | --- |
| WFL_advisor_33 | WFL_advisor_skill_35 | WFL_advisor_upgrade_01 | GER_secretary_of_state_security |
| WFL_advisor_31 | WFL_advisor_skill_33 | WFL_advisor_upgrade_02 | GER_militant_communist |
| WFL_advisor_36 | WFL_advisor_skill_38 | WFL_advisor_upgrade_03 | GER_stakhonovite_collectivist2 |
| WFL_advisor_32 | WFL_advisor_skill_34 | WFL_advisor_upgrade_04 | GER_staunch_stalinist |
| WFL_advisor_22 | WFL_advisor_skill_23 | WFL_advisor_upgrade_05 | GER_staunch_socialist |
| WFL_advisor_17 | WFL_advisor_skill_18 | WFL_advisor_upgrade_06 | head_of_the_abwehr_improved |
| WFL_advisor_18 | WFL_advisor_skill_19 | WFL_advisor_upgrade_07 | intelligence_service_deputy |
| WFL_advisor_27 | WFL_advisor_skill_28 | WFL_advisor_upgrade_08 | GER_minister_of_the_colonies_2 |

Die Trait-Blöcke sind vollständig aus den acht aktiven Quellvarianten übernommen,
einschließlich aller numerischen Werte und Nachteile. Die alte Eigenschaft wird
entfernt, bevor die neue hinzugefügt wird. Alte und neue Boni werden deshalb
nicht absichtlich gestapelt. Auch der Verlust bisheriger Vorteile gehört zum
Quellabgleich: Die Geheimdienstaufwertung des Profils WFL_advisor_18 ersetzt
beispielsweise dessen bisherige Stabilitäts-/Ideologiewerte durch das neue
Spionageprofil. Der Nachteil von -5 Prozent Wachstum der Produktionseffizienz
in WFL_advisor_upgrade_04 bleibt ausdrücklich erhalten.

## DLCs und Rollenbedingungen

Alle acht aktiven Upgrade-Fokusse liegen im neuen deutschen Alternativzweig,
dessen Zugang über GER_oppose_hitler_ww Götterdämmerung voraussetzt. Daher
verlangen alle acht WFL-Weiterbildungen **Götterdämmerung**.

Zusätzlich benötigen die Spionageaufwertungen 01, 06 und 07 **La Résistance**
und eine vorhandene Geheimdienstbehörde. Profil 07 behält außerdem die bereits
für seine Grundrolle erforderliche Bedingung **Waking the Tiger**.
Bei Profil 02 wird ausschließlich die aktive Götterdämmerung-Grundvariante
WFL_advisor_skill_33 ersetzt. Die alternative ältere Rolle ohne dieses DLC
wird nicht mit dem falschen Trait verändert.

Die Grundrolle von WFL_advisor_22 hat wie ihre deutsche Vorlage die Bedingung
do_effect = NOT democratic. Die Weiterbildung lässt diese Rollenbedingung
unverändert und ist deshalb nur bei nicht demokratischer Regierung nutzbar.
So werden keine 100 PP für einen zu diesem Zeitpunkt gesperrten Effekt verlangt.
Ein späterer Regierungswechsel unterliegt weiterhin derselben ursprünglichen
Rollenbedingung. Die demokratischen/kommunistischen Unterstützungswerte und
diplomatischen Nachteile der Quellprofile werden nicht stillschweigend entfernt.

## Technische Umsetzung und Nachweise

Die Entscheidungen verwenden remove_trait und add_trait mit dem bestehenden
WFL-Charakter und slot = political_advisor. Dieses Verfahren ist in der lokalen
documentation/effects_documentation.md für Länder- und Charakterscope dokumentiert
und wird in common/national_focus/germany.txt genau für diese Upgrades verwendet.
Es wird keine Beraterrolle entfernt oder neu angelegt, kein Charakter neu
rekrutiert und kein zusätzlicher Beraterplatz belegt. Name, Porträt, Idee-Token,
Anstellung und bisherige Rollenbedingungen bleiben am bestehenden Charakter.

Quellen:

- common/country_leader/00_traits.txt: die acht vollständigen Upgrade-Traits.
- common/national_focus/germany.txt: aktive Ersetzungen und DLC-Zweigzugang.
- tools/data/WFL_advisors.json: bestehende WFL-Zuordnung und DLC-Grundrollen.
- [BERATER_QUELLEN.md](BERATER_QUELLEN.md): unabhängiger vollständiger Quellenbericht.

Die neuen Trait-Dateien enthalten keine deutschen Länder-, Fokus- oder
Charakterabhängigkeiten. Die Basisdateien der Berater, deren Importer und
die Länderhistorie werden durch diese Ergänzung nicht verändert.

## Prüfung und verbleibende Abnahme

tests/test_advisor_development.py prüft einmalige Zahlung, tatsächliche
Trait-Ersetzung, unveränderte Anzahl eingestellter Berater, Sperren bei fehlender
Rekrutierung/Anstellung/Rolle/Berufskolleg, jede erforderliche DLC-Bedingung,
Geheimdienstbehörde und die besondere Regierungsbedingung von Profil 05.
Mit erreichbarer lokaler Installation wird zusätzlich der komplette Inhalt aller
acht neuen Traits gegen die Originaldatei verglichen.

Diese Tests bilden nur den benötigten Skriptausschnitt ab. Eine Engine-Abnahme
der acht Upgrades, ihrer sofortigen Modifier-Neuberechnung, des Entlassens und
Wiedereinstellens sowie Speichern/Laden steht gesondert aus. Der Einsatz des
originalen Vanilla-Verfahrens ist ein technischer Nachweis für die gewählte
Umsetzung, kein Ersatz für diese Spieltests.
