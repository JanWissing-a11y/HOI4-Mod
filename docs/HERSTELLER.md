# Deutsche Hersteller für Wesel-Flüren

Stand: 4. November 2026. Grundlage ist die lokal installierte Version **1.19.4.1**.
Die Änderungen schaffen eigenständige WFL-Niederlassungen; deutsche Originale,
Originalgrafiken und deren Verfügbarkeit bleiben unverändert.

## Enthaltene Profile

- **67 klassische Profile**: 62 deutsche Basis-/Ausbauvarianten und fünf optionale
  tschechische Vertragspartner, die auch Deutschland erhalten kann.
- **29 MIOs**: 25 deutsche Organisationen und vier solche Vertragsorganisationen.
- Zwei fiktive Herstellerwissenschaftler mit den ursprünglichen Traits und
  Landforschungs-Skill 3: Dr. Emil Auenfeld (Porsche) und Dr. Karl Rheinberg (Henschel).

Klassische Rüstungsdesigner erscheinen ohne **Arms Against Tyranny**. Mit diesem
DLC erscheinen ihre MIO-Alternativen. Industriekonzerne bleiben in beiden Fällen
im klassischen Industrieslot verfügbar. Zusätzliche ursprüngliche DLC-Bedingungen
für einzelne Firmen bleiben erhalten: insbesondere La Résistance, Götterdämmerung
und Peace For Our Time. Diese DLCs werden durch die Mod nicht vorausgesetzt;
nicht vorhandene optionale Angebote bleiben verborgen.

## Freischaltung und Fähigkeiten

Die Grundprofile sind verfügbar; die meisten verbesserten klassischen Profile
ersetzen ihre Grundvariante nach **Berufskolleg**. Philipp Holzmann und die
Reichswerke haben drei Stufen: Grundprofil, Ausbau nach **Rüstungswerkstatt**,
weiterer Ausbau nach Rüstungswerkstatt und Berufskolleg. Organisation Todt wird
mit **Gewerbehöfe** verfügbar und mit Berufskolleg verbessert. Die Reichswerke
benötigen zunächst **Werkbank am Niederrhein**. Optionale tschechische Verträge
benötigen Berufskolleg; deren Bank setzt zusätzlich Frieden mit Großbritannien voraus.
Die beiden Holzmann-Endvarianten sind passend zu Arms Against Tyranny getrennt.
Die Freischaltung tauscht bereits eingestellte klassische Firmen nicht automatisch
aus. Eine verbesserte Variante wird anschließend im Herstellerslot ausgewählt;
ihre Einstellungsgebühr bleibt wie im kopierten Profil definiert.

MIOs erben per lokal dokumentiertem `include` den vollständigen ursprünglichen
Baum, seine Ausrüstungskategorien und sämtliche numerischen Ausrüstungs-,
Produktions- und Organisationsboni. `override_trait` passt ausschließlich
Verfügbarkeit, KI-Gewichte, lokale Flags, Wissenschaftlerverweise und interne
MIO-Verträge an. Deutsche Fokusvoraussetzungen werden durch **Berufskolleg**
ersetzt. Originale Größenanforderungen, Elternknoten und wechselseitige
Ausschlüsse bleiben erhalten. Die Hoesch-, Hamburger-Flugzeugbau- und
Aerodynamik-Verträge bleiben je WFL-Land einmalig und beeinflussen Deutschlands
Flags nicht. Für das Langstreckenbomber-Lernprogramm wird in WFL ein Partner
beim ersten Abschluss des zugehörigen Knotens ausgewählt.

Porsche und Henschel behalten ihre Wissenschaftlerfreischaltung: ohne MIO durch
Einstellung eines der beiden passenden klassischen Profile, mit MIO durch den
ursprünglichen Spezialprojekt-Knoten im eigenen WFL-Baum. Die beiden Charaktere
müssen in WFLs Länderhistorie rekrutiert sein. Die Fotos sind eigene WFL-Porträts;
Herstellerlogos stammen weiterhin aus der vorhandenen Spielinstallation.

## Quellen und technische Grenzen

Quellen: `common/ideas/GER.txt`, `common/ideas/czechoslovakia.txt`,
`common/military_industrial_organization/organizations/GER_organization.txt`,
`CZE_organization.txt`, die dort eingebundenen Vorlagen sowie
`organizations/_documentation.md` und `common/characters/GER.txt`.
Das native Dokument bestätigt ausdrücklich Vererbung mit `include`,
feldweise Änderungen mit `override_trait` und unveränderte Bonusfelder bei
nicht überschriebenen Werten. Die Verweise benötigen die installierten
Vanilla-Definitionen dieser Version; es werden keine Logos kopiert oder ersetzt.

Die Mod vergibt weder kostenlose Fabriken noch Häfen, Produktionslinien oder
fremde Wissenschaftler. Eine Werftorganisation bleibt auch bei einem Binnenland
an tatsächlich erforschte Schiffe und vorhandene Werften gebunden. Statische
Prüfungen bestätigen keine korrekte Engine-Anzeige, MIO-Vererbung zur Laufzeit
oder DLC-Umschaltung im Spiel; dafür bleiben separate Ingame-Tests erforderlich.
Die gezielten Regressionstests prüfen das vollständige Inventar, wechselseitige
DLC-Modi, erreichbare und überlappungsfreie klassische Ausbaustufen, WFL-isolierte
Scopes sowie die Wissenschaftler-Verweise. Mit erreichbarer Spielinstallation
werden sämtliche 67 klassischen Bonus-/Trait-/Kostenprofile zusätzlich direkt
mit ihren Quellen verglichen und alle 40 benötigten Logos gegen die vorhandenen
Vanilla-Sprite-Definitionen geprüft.

## Vollständiges klassisches Inventar

| Kategorie | Quelle | WFL-ID | Stufe |
| --- | --- | --- | ---: |
| tank_manufacturer | `porsche` | `WFL_mfr_porsche` | 0 |
| tank_manufacturer | `GER_porsche_improved` | `WFL_mfr_porsche_improved` | 1 |
| tank_manufacturer | `henschel` | `WFL_mfr_henschel` | 0 |
| tank_manufacturer | `GER_henschel_improved` | `WFL_mfr_henschel_improved` | 1 |
| tank_manufacturer | `GER_MAN` | `WFL_mfr_man` | 0 |
| tank_manufacturer | `GER_MAN_improved` | `WFL_mfr_man_improved` | 1 |
| tank_manufacturer | `GER_alkett` | `WFL_mfr_alkett` | 0 |
| tank_manufacturer | `GER_alkett_improved` | `WFL_mfr_alkett_improved` | 1 |
| tank_manufacturer | `GER_daimler_benz` | `WFL_mfr_daimler_benz` | 0 |
| tank_manufacturer | `GER_daimler_benz_improved` | `WFL_mfr_daimler_benz_improved` | 1 |
| naval_manufacturer | `germaniawerft` | `WFL_mfr_germaniawerft` | 0 |
| naval_manufacturer | `GER_germaniawerft_improved` | `WFL_mfr_germaniawerft_improved` | 1 |
| naval_manufacturer | `blohm_und_voss` | `WFL_mfr_blohm_und_voss` | 0 |
| naval_manufacturer | `GER_blohm_und_voss_improved` | `WFL_mfr_blohm_und_voss_improved` | 1 |
| naval_manufacturer | `GER_hdw` | `WFL_mfr_hdw` | 0 |
| naval_manufacturer | `GER_hdw_improved` | `WFL_mfr_hdw_improved` | 1 |
| naval_manufacturer | `GER_deschimag` | `WFL_mfr_deschimag` | 0 |
| naval_manufacturer | `GER_deschimag_improved` | `WFL_mfr_deschimag_improved` | 1 |
| naval_manufacturer | `GER_deutsche_werke` | `WFL_mfr_deutsche_werke` | 0 |
| naval_manufacturer | `GER_deutsche_werke_improved` | `WFL_mfr_deutsche_werke_improved` | 1 |
| naval_manufacturer | `GER_kriegsmarinewerft_wilhelmshaven` | `WFL_mfr_kriegsmarinewerft_wilhelmshaven` | 0 |
| naval_manufacturer | `GER_kriegsmarinewerft_wilhelmshaven_improved` | `WFL_mfr_kriegsmarinewerft_wilhelmshaven_improved` | 1 |
| aircraft_manufacturer | `messerschmitt` | `WFL_mfr_messerschmitt` | 0 |
| aircraft_manufacturer | `GER_messerschmitt_improved` | `WFL_mfr_messerschmitt_improved` | 1 |
| aircraft_manufacturer | `junkers` | `WFL_mfr_junkers` | 0 |
| aircraft_manufacturer | `GER_junkers_improved` | `WFL_mfr_junkers_improved` | 1 |
| aircraft_manufacturer | `focke_wulf` | `WFL_mfr_focke_wulf` | 0 |
| aircraft_manufacturer | `GER_focke_wulf_improved` | `WFL_mfr_focke_wulf_improved` | 1 |
| aircraft_manufacturer | `heinkel` | `WFL_mfr_heinkel` | 0 |
| aircraft_manufacturer | `GER_heinkel_improved` | `WFL_mfr_heinkel_improved` | 1 |
| aircraft_manufacturer | `dornier` | `WFL_mfr_dornier` | 0 |
| aircraft_manufacturer | `GER_dornier_improved` | `WFL_mfr_dornier_improved` | 1 |
| aircraft_manufacturer | `GER_arado_flugzeugwerke` | `WFL_mfr_arado_flugzeugwerke` | 0 |
| aircraft_manufacturer | `GER_arado_flugzeugwerke_improved` | `WFL_mfr_arado_flugzeugwerke_improved` | 1 |
| aircraft_manufacturer | `GER_fieseler` | `WFL_mfr_fieseler` | 0 |
| aircraft_manufacturer | `GER_fieseler_improved` | `WFL_mfr_fieseler_improved` | 1 |
| materiel_manufacturer | `rheinmetall` | `WFL_mfr_rheinmetall` | 0 |
| materiel_manufacturer | `mauser` | `WFL_mfr_mauser` | 0 |
| materiel_manufacturer | `opel` | `WFL_mfr_opel` | 0 |
| materiel_manufacturer | `GER_opel_improved` | `WFL_mfr_opel_improved` | 1 |
| materiel_manufacturer | `GER_carl_walther` | `WFL_mfr_carl_walther` | 0 |
| materiel_manufacturer | `GER_auto_union` | `WFL_mfr_auto_union` | 0 |
| materiel_manufacturer | `GER_auto_union_improved` | `WFL_mfr_auto_union_improved` | 1 |
| materiel_manufacturer | `GER_henschel_kassel_manufacturer` | `WFL_mfr_henschel_kassel_manufacturer` | 0 |
| materiel_manufacturer | `GER_focke_achgelis` | `WFL_mfr_focke_achgelis` | 0 |
| industrial_concern | `ig_faben` | `WFL_mfr_ig_faben` | 0 |
| industrial_concern | `GER_ig_faben_improved` | `WFL_mfr_ig_faben_improved` | 1 |
| industrial_concern | `krupp` | `WFL_mfr_krupp` | 0 |
| industrial_concern | `siemens` | `WFL_mfr_siemens` | 0 |
| industrial_concern | `GER_vereinigte_stahlwerke` | `WFL_mfr_vereinigte_stahlwerke` | 0 |
| industrial_concern | `GER_deutsche_reichsbahn` | `WFL_mfr_deutsche_reichsbahn` | 0 |
| industrial_concern | `GER_deutsche_reichsbahn_improved` | `WFL_mfr_deutsche_reichsbahn_improved` | 1 |
| industrial_concern | `GER_philipp_holzmann` | `WFL_mfr_philipp_holzmann` | 0 |
| industrial_concern | `GER_philipp_holzmann_improved` | `WFL_mfr_philipp_holzmann_improved` | 1 |
| industrial_concern | `GER_philipp_holzmann_improved_2` | `WFL_mfr_philipp_holzmann_improved_2` | 2 |
| industrial_concern | `GER_philipp_holzmann_improved_2_no_aat` | `WFL_mfr_philipp_holzmann_improved_2_no_aat` | 2 |
| industrial_concern | `GER_organization_todt` | `WFL_mfr_organization_todt` | 0 |
| industrial_concern | `GER_organization_todt_improved` | `WFL_mfr_organization_todt_improved` | 1 |
| industrial_concern | `GER_rwe` | `WFL_mfr_rwe` | 0 |
| industrial_concern | `GER_reichswerke` | `WFL_mfr_reichswerke` | 0 |
| industrial_concern | `GER_reichswerke_improved` | `WFL_mfr_reichswerke_improved` | 1 |
| industrial_concern | `GER_reichswerke_improved_2` | `WFL_mfr_reichswerke_improved_2` | 2 |
| tank_manufacturer | `CZE_skoda_works_german_manufacturer` | `WFL_mfr_cze_skoda_works_german_manufacturer` | 0 |
| tank_manufacturer | `CZE_bohmische_mahrische_maschinenfabrik_ag_german_manufacturer` | `WFL_mfr_cze_bohmische_mahrische_maschinenfabrik_ag_german_manufacturer` | 0 |
| aircraft_manufacturer | `CZE_zlin_aircraft` | `WFL_mfr_cze_zlin_aircraft` | 0 |
| materiel_manufacturer | `CZE_ceska_zbrojovka_uhersky_brod` | `WFL_mfr_cze_ceska_zbrojovka_uhersky_brod` | 0 |
| industrial_concern | `CZE_anglo_czechoslovak_bank` | `WFL_mfr_cze_anglo_czechoslovak_bank` | 0 |

## Vollständiges MIO-Inventar

| Quelle | WFL-ID | Geerbte Vorlage | Effektive Traitknoten | Angepasste Knoten |
| --- | --- | --- | ---: | ---: |
| `GER_porsche_organization` | `WFL_mio_porsche` | `generic_heavy_tank_organization` | 18 | 5 |
| `GER_henschel_organization` | `WFL_mio_henschel` | `generic_infantry_tank_organization` | 20 | 3 |
| `GER_man_organization` | `WFL_mio_man` | `generic_medium_tank_organization` | 17 | 1 |
| `GER_alkett_organization` | `WFL_mio_alkett` | `generic_assault_guns_organization` | 17 | 4 |
| `GER_daimler_benz_organization` | `WFL_mio_daimler_benz` | `generic_tank_organization` | 17 | 1 |
| `GER_deschimag_organization` | `WFL_mio_deschimag` | `generic_escort_ship_organization` | 14 | 0 |
| `GER_germaniawerft_organization` | `WFL_mio_germaniawerft` | `generic_battle_line_ship_organization` | 17 | 3 |
| `GER_blohm_und_voss_organization` | `WFL_mio_blohm_und_voss` | `generic_raider_ship_organization` | 19 | 3 |
| `GER_hdw_organization` | `WFL_mio_hdw` | `generic_submarine_organization` | 23 | 3 |
| `GER_deutsche_werke_organization` | `WFL_mio_deutsche_werke` | `generic_task_force_ship_organization` | 17 | 0 |
| `GER_kriegsmarinewerft_wilhelmshaven_organization` | `WFL_mio_kriegsmarinewerft_wilhelmshaven` | `generic_refurbishment_repair_organization` | 17 | 1 |
| `GER_messerschmitt_organization` | `WFL_mio_messerschmitt` | `generic_light_aircraft_organization` | 22 | 3 |
| `GER_junkers_organization` | `WFL_mio_junkers` | `generic_cas_aircraft_organization` | 19 | 3 |
| `GER_focke_wulf_organization` | `WFL_mio_focke_wulf` | `generic_range_focused_aircraft_organization` | 22 | 3 |
| `GER_heinkel_organization` | `WFL_mio_heinkel` | `generic_heavy_aircraft_organization` | 20 | 3 |
| `GER_dornier_organization` | `WFL_mio_dornier` | `generic_medium_aircraft_organization` | 19 | 2 |
| `GER_arado_flugzeugwerke_organization` | `WFL_mio_arado_flugzeugwerke` | `generic_multi_role_aircraft_organization` | 20 | 2 |
| `GER_fieseler_organization` | `WFL_mio_fieseler` | `generic_naval_aircraft_organization` | 15 | 2 |
| `GER_focke_achgelis_organization` | `WFL_mio_focke_achgelis` | `generic_helicopter_organization` | 9 | 2 |
| `GER_rheinmetall_organization` | `WFL_mio_rheinmetall` | `generic_artillery_organization` | 17 | 0 |
| `GER_mauser_organization` | `WFL_mio_mauser` | `generic_infantry_equipment_organization` | 18 | 4 |
| `GER_opel_organization` | `WFL_mio_opel` | `generic_motorized_mechanized_organization` | 19 | 4 |
| `GER_carl_walther_organization` | `WFL_mio_carl_walther` | `generic_support_equipment_organization` | 15 | 0 |
| `GER_auto_union_organization` | `WFL_mio_auto_union` | `generic_armored_car_organization` | 15 | 1 |
| `GER_henschel_kassel_organization` | `WFL_mio_henschel_kassel` | `generic_train_organization` | 17 | 1 |
| `CZE_skoda_works_german_organization` | `WFL_mio_cze_skoda_works_german` | `generic_tank_refurbishment_plant_organization` | 14 | 1 |
| `CZE_bohmische_mahrische_maschinenfabrik_ag_german_organization` | `WFL_mio_cze_bohmische_mahrische_maschinenfabrik_ag_german` | `CZE_tank_destroyer_organization` | 15 | 2 |
| `CZE_avia_german_organization` | `WFL_mio_cze_avia_german` | `generic_high_agility_fighter_aircraft_organization` | 16 | 3 |
| `CZE_ceska_zbrojovka_uhersky_brod_organization` | `WFL_mio_cze_ceska_zbrojovka_uhersky_brod` | `CZE_automatic_weapons_equipment_organization` | 20 | 1 |
