# Korrekturen aus dem Spielprotokoll

Stand: 4. November 2026, lokale HoI4-Version 1.19.4.1.
Grundlage ist das vorhandene `logs/error.log` vom Spielstart um 01:42 Uhr.
Die folgenden Änderungen wurden statisch geprüft. Ein erneuter Engine-Start
zum Nachweis, dass die Meldungen verschwunden sind, steht noch aus.

## Politische Berater mit DLC-Varianten

Die Engine meldete viermal `Unexpected token: instance` in
`common/characters/WFL_advisors.txt`. Betroffen waren die beiden Varianten von
`WFL_advisor_16` und `WFL_advisor_31`.

Der Importer hatte Name und Porträts direkt in den Charakterkörper geschrieben
und anschließend zwei `instance`-Blöcke ergänzt. Die lokalen deutschen Vorlagen
`GER_reinhard_heydrich` und `GER_ernst_thalmann` bestehen dagegen ausschließlich
aus Instanzblöcken; Name, Porträts und Beraterrolle stehen jeweils innerhalb
derselben Instanz. Der Importer verwendet jetzt diese Struktur und wurde zum
Erzeugen der korrigierten Charakterdatei verwendet.

Die 37 Charakter-IDs, 39 Rollen, Preise, numerischen Traits und komplementären
DLC-Bedingungen bleiben erhalten. Die Landesgeschichte und Originalspieldateien
wurden bei dieser Korrektur nicht geändert.

Die Beraterprüfung kontrolliert nun zusätzlich die Instanzstruktur und einen
erneuten Import gegen die lokale Vanilla-Installation. Sieben Beraterprüfungen
bestanden in 0,709 Sekunden.

## Blohm-und-Voss-Talentbaum

Das Protokoll meldete für `WFL_mio_blohm_und_voss` die doppelte Position `[8,1]`.
Ursache sind zwei aus der generischen Vanilla-Vorlage geerbte Talente:
`generic_mio_trait_high_speed_operation_stores` und dessen Alternative
`generic_mio_trait_high_speed_operation_stores_no_mtg`. Ihre Sichtbarkeit ist
nach Man the Guns getrennt; ihre Position ist trotzdem identisch.

Nur in der WFL-Niederlassung erhält die Alternative ohne Man the Guns einen
zusätzlichen horizontalen Versatz und liegt damit auf `[9,1]`. Die ursprünglichen
Boni, DLC-Bedingungen, Elternknoten und relativen Bezugsknoten bleiben gleich.
Deutschlands Organisation wird nicht verändert.

Die Herstellerprüfung löst die Vererbung aus generischer, deutscher und eigener
Definition auf. Sie prüft eindeutige effektive Koordinaten sowie unveränderte
Bonusfelder und Elternbeziehungen. Zehn Herstellerprüfungen bestanden in
0,278 Sekunden.
