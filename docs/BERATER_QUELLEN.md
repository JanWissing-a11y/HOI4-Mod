# Quellenprüfung der politischen Berater

Stand: 4. November 2026. Unabhängige, ausschließlich lesende Prüfung der lokalen
Steam-Installation von HOI4 **1.19.4.1**. Dies ist eine Daten- und Scopeprüfung,
kein Beleg für die tatsächliche Anzeige oder Anwendung im Spiel.

## Umfang und Kosten

`common/characters/GER.txt` enthält **37 Charakter-IDs mit 39 politischen
Beraterrollen**. Die beiden zusätzlichen Rollen sind alternative DLC-Instanzen
von Reinhard Heydrich und Ernst Thälmann. Eine Suche in den übrigen lokalen
Charakterdateien fand keine weiteren politischen Rollen unter `GER_`-Charakter-IDs.
`common/ideas/GER.txt` enthält keine separate `political_advisor`-Sektion und
keine zusätzlichen alten Ideen unter den einschlägigen Berater-Tokens.

Standardkosten sind **150 politische Macht**, belegt durch
`common/defines/00_defines.lua`, `DEFAULT_PP_COST_FOR_POLITICAL_ADVISOR = 150`.
Nur die drei unten ausgewiesenen Rollen überschreiben diesen Standard mit 50/75.
Die Tabelle nennt Basiswerte; Kostenmodifikatoren können den Preis im Spiel ändern.

| Quell-Charakter-ID | Basis-PP | Eigenschaft(en), alternative Instanzen mit / getrennt |
| --- | ---: | --- |
| `GER_otto_strasser` | 150 (Standard) | `GER_revolutionary_nationalist_advisor` |
| `GER_hermann_goring` | 150 (Standard) | `GER_overseer_four_year_plan` |
| `GER_joachim_von_ribbentrop` | 50 | `GER_reich_minister_foreign_affairs_ribbentrop` |
| `GER_konstantin_von_neurath` | 50 | `GER_reich_minister_foreign_affairs_neurath` |
| `GER_fritz_todt` | 150 (Standard) | `GER_reich_engineer` |
| `GER_albert_speer` | 150 (Standard) | `GER_reich_architect` |
| `GER_hjalmar_schacht` | 75 | `GER_mefo_bills_architect` |
| `GER_walther_funk` | 150 (Standard) | `GER_reich_minister_of_economy` |
| `GER_joseph_goebbels` | 150 (Standard) | `GER_reich_minister_of_propaganda` |
| `GER_rudolf_hess` | 150 (Standard) | `GER_first_among_equals` |
| `GER_heinrich_himmler` | 150 (Standard) | `prince_of_terror` |
| `GER_martin_bormann` | 150 (Standard) | `GER_secretary_to_the_fuhrer` |
| `GER_leni_riefenstahl` | 150 (Standard) | `GER_film_director` |
| `GER_franz_seldte` | 150 (Standard) | `GER_reich_minister_for_labor` |
| `GER_hanns_kerrl` | 150 (Standard) | `GER_reich_minister_of_church_affairs` |
| `GER_reinhard_heydrich` | 150 (Standard) | `GER_reich_security_main_office_director_lar` / `GER_reich_security_main_office_director_no_lar` |
| `GER_wilhelm_canaris` | 150 (Standard) | `head_of_the_abwehr` |
| `GER_hans_oster` | 150 (Standard) | `anti_fascist_agent` |
| `GER_alfred_hugenberg` | 150 (Standard) | `monarchist_media_mogul` |
| `GER_carl_friedrich_goerdeler` | 150 (Standard) | `GER_price_commissioner` |
| `GER_julius_leber` | 150 (Standard) | `connected_citizen` |
| `GER_kurt_schumacher` | 150 (Standard) | `democratic_reformer` |
| `GER_theodor_heuss` | 150 (Standard) | `liberal_journalist` |
| `GER_hans_luther` | 150 (Standard) | `GER_former_reichsbank_president` |
| `GER_ludwig_erhard` | 150 (Standard) | `economic_reformer` |
| `GER_hermann_erhardt` | 150 (Standard) | `GER_freikorps_commander` |
| `GER_adolf_friedrich_von_mecklenburg` | 150 (Standard) | `GER_minister_of_the_colonies` |
| `GER_wilhelm_von_gayl` | 150 (Standard) | `GER_monarchist_jurist` |
| `GER_andreas_hermes` | 150 (Standard) | `GER_minister_of_agriculture` |
| `GER_dietrich_bonhoeffer` | 150 (Standard) | `GER_influential_pastor` |
| `GER_ernst_thalmann` | 150 (Standard) | `communist_revolutionary` / `GER_proletarian_leader` |
| `GER_walter_ulbricht` | 150 (Standard) | `GER_inflexible_communist_organizer` |
| `GER_wilhelm_zaisser` | 150 (Standard) | `GER_intelligence_coordinator` |
| `GER_otto_ruhle` | 150 (Standard) | `marxist_philosopher` |
| `GER_hermann_duncker` | 150 (Standard) | `GER_workers_educator` |
| `GER_august_thalheimer` | 150 (Standard) | `GER_stakhonovite_collectivist1` |
| `GER_bernhard_bastlein` | 150 (Standard) | `GER_seasoned_socialist_resistance_fighter` |

## DLC-Instanzen und Verfügbarkeit

- Heydrich: mit La Résistance `GER_reich_security_main_office_director_lar`,
  ohne La Résistance `GER_reich_security_main_office_director_no_lar`.
- Thälmann: ohne Götterdämmerung `communist_revolutionary`, mit Götterdämmerung
  `GER_proletarian_leader`.
- Insbesondere Canaris und Zaisser verwenden Spionagefähigkeiten; deren
  La-Résistance-Bedingungen und gegebenenfalls eine vorhandene Geheimdienstbehörde
  sind auch bei WFL sinnvoll. Nicht installierte DLCs dürfen nicht vorausgesetzt werden.
- Die originalen Einstellungsbedingungen enthalten deutsche Fokus-IDs,
  `original_tag = GER`, deutsche Charakterabfragen, politische Flags und teilweise
  `always = no`. Eine Kopie dieser Bedingungen würde viele WFL-Profile verbergen
  oder dauerhaft sperren. Eine WFL-Adaption muss diese Rekrutierungssperren von
  den eigentlichen Fähigkeiten trennen.

## Eigentliche Fähigkeiten und zusätzliche Rollenfelder

Alle **39 referenzierten Eigenschaften** sind in
`common/country_leader/00_traits.txt` definiert. Ihre eigentlichen numerischen
Modifier sind länderneutral; trotz mancher `GER_`-Namen enthalten diese
Modifierblöcke keinen harten Deutschland-Länderscope. Die global vorhandenen
Trait-IDs können deshalb auch einem eigenständigen WFL-Charakter zugewiesen werden.

Zu berücksichtigen sind zusätzliche Felder außerhalb der Traits:

- Goebbels hat `do_effect = { NOT = { has_government = fascism } }`.
- Schumacher hat `do_effect = { NOT = { has_government = democratic } }`.
- Die ältere Thälmann-Instanz hat
  `do_effect = { NOT = { has_government = communism } }`.
- `communist_revolutionary.ai_will_do` enthält eine Prüfung auf den amerikanischen
  Fokus `USA_suspend_the_presecution`. Das betrifft die KI-Auswahl, nicht die
  kommunistische tägliche Unterstützung. Ein eigenes neutrales WFL-KI-Gewicht
  vermeidet diese sachfremde Abhängigkeit.

Himmlers ursprüngliche Rolle enthält ein `on_add` mit ausschließlich
`custom_effect_tooltip = GER_SS_himmler_recruit`. Dieser Tooltip verspricht
SS-Rekrutierung und ist **keine eigenständige Implementierung dieser Fähigkeit**.
Die zugehörige Kategorie in
`common/decisions/categories/SS_decision_categories.txt` verlangt
`original_tag = GER` und den Fokus `GER_expand_ss_recruitment`; weitere
Entscheidungen in `common/decisions/SS.txt` verwenden feste Deutschland- und
Deutschland-Untertanen-Scopes. Unverändert kopiert wäre dieser Zusatz bei WFL
irreführend. Die eigentlichen `prince_of_terror`-Modifier funktionieren unabhängig
von diesem deutschen Entscheidungssystem.

Eine vollständige Kopie deutscher Fokus-, Event- oder SS-Systeme ist mit der
Übernahme der Beraterprofile nicht automatisch umgesetzt. Der folgende Abgleich
bezieht sich auf die Basisprofile und ihre unmittelbaren Fähigkeiten.

## Abgleich der implementierten WFL-Basisprofile

Am 4. November 2026 wurden `common/characters/WFL_advisors.txt`,
`common/country_leader/WFL_advisor_traits.txt` und das Quellenmanifest
`tools/data/WFL_advisors.json` unabhängig mit den obigen Dateien verglichen.
Die Umsetzung deckt alle 37 Quellcharaktere mit 39 Basisrollen ab; Basispreise
und numerische Effekte einschließlich negativer Werte stimmen überein.
Die beiden komplementären DLC-Instanzpaare und alle drei `do_effect`-Bedingungen
sind erhalten. Canaris' WFL-Profil benötigt weiterhin einen Geheimdienst.

WFL verwendet eigene Charakter- und Trait-IDs. Deutsche Fokus-/Flag-Sperren,
der sachfremde USA-KI-Hook und der irreführende SS-Rekrutierungs-Tooltip sind
nicht in die Basisprofile übernommen. Die zusätzliche deutsche SS-Rekrutierung
gehört damit ausdrücklich nicht zu deren Fähigkeiten. Dieser Abgleich bestätigt
die Datenübernahme, nicht die tatsächliche Einstellbarkeit oder Wirkung in der Engine.

## Spätere aktive Trait-Aufwertungen

Die 39 Anfangsrollen sind nicht die gesamte Menge erreichbarer Beraterfähigkeiten.
`common/national_focus/germany.txt` ersetzt bei acht Profilen den politischen
Trait durch eine verbesserte Variante. Diese acht zusätzlichen Traits sind ebenfalls
in `common/country_leader/00_traits.txt` definiert und besitzen länderneutrale
Modifier. Wer sämtliche Fähigkeitsvarianten übernehmen möchte, muss sie zusätzlich
zu den Anfangsrollen berücksichtigen; deutsche Fokus-IDs allein schalten bei WFL
keine solche Aufwertung frei.

| Quellprofil | Verbesserter Trait | Deutscher Auslöser-Fokus |
| --- | --- | --- |
| `GER_wilhelm_zaisser` | `GER_secretary_of_state_security` | `GER_form_the_stasi` |
| `GER_ernst_thalmann` | `GER_militant_communist` | `GER_ressurect_the_red_front_fighters_league` |
| `GER_august_thalheimer` | `GER_stakhonovite_collectivist2` | `GER_nationalize_industries` |
| `GER_walter_ulbricht` | `GER_staunch_stalinist` | `GER_proletarian_dictatorship` |
| `GER_kurt_schumacher` | `GER_staunch_socialist` | `GER_embrace_liberal_leanings` |
| `GER_wilhelm_canaris` | `head_of_the_abwehr_improved` | `GER_realpolitik` |
| `GER_hans_oster` | `intelligence_service_deputy` | `GER_realpolitik` |
| `GER_adolf_friedrich_von_mecklenburg` | `GER_minister_of_the_colonies_2` | `GER_weltpolitik` |

Die im deutschen Fokusbaum ebenfalls sichtbare Ersetzung von Himmlers Trait
durch `GER_reichsfuhrer_ss` ist auskommentiert. Sie ist keine aktive zusätzliche
Beraterrolle dieser Version.
