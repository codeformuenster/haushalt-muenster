# Haushaltspläne als CSV-Dateien

In diesem Ordner befinden sich die mit dem scraper aufbearbeiteten Daten, die aus den PDFs extrahiert wurden (siehe auch [README](../scraper/README.md) im scraper Ordner).

Die Haushaltsdaten der Stadt Münster in PDF-Form sind aufgeteilt in Band 1 und 2. In seltenen Fällen enthält Band 2 alle Daten, meistens jedoch nur Produktkategorien 03 bis 17.

Dateien mit dem Wort `complete` im Namen wurden stichprobenartig auf Korrektheit geprüft, z.T. manuell vervollständig und enthalten alle Daten aus Band 1 und 2, sofern Daten in den original PDFs getrennt in Band 1 und 2 vorliegen.

## Workflow

* PDFs der Haushalte herunterladen (`Haushaltsplan <Jahr>, Band 1` und `Band 2`):
  * [Stadt Münster: Münsters Haushalt - Der Haushaltsplan](https://www.stadt-muenster.de/finanzen/muensters-haushalt/der-haushaltsplan.html)
  * [Stadt Münster: Münsters Haushalt - Archiv](https://www.stadt-muenster.de/finanzen/muensters-haushalt/archiv.html)
* [scraper](../scraper/README.md) einrichten und Teilergebnis-CSVs (Band 1 und 2) erzeugen
* Teilergebnis-CSVs kombinieren, Teilergebnisse überprüfen (0€-Ergebnisse, starke Steigerungen usw.) und ggf. vervollständigen (z.B. mit LibreOffice Calc oder einem Texteditor)
* Neue ergebnisse.csv erzeugen mit `combine_complete.py`
* Ergebnis bei OpenSpending einpflegen

## Dateien in diesem Ordner

### Haushaltsdaten

Ergebnisdaten für die Haushaltsjahre 2007 bis 2017: [ergebnisse.csv](ergebnisse.csv)

Das Format der CSV entspricht grob dem Beispieldatensatz von OffenerHaushalt ([CSV](https://rawgit.com/okfde/offenerhaushalt.de/gh-pages/_haushalte-data/standard-datensatz-ohh.csv)) und von Moers ([CSV](https://s3.amazonaws.com/datastore.openspending.org/a6a16b964a7e784f99adecc47f26318a/moers-all/all-moers.csv)).

Haushaltsdaten CSVs pro Jahr liegen im Ordner [partial-data/](partial-data/).

Hinweise zu fehlerhaften PDFs:

- Einige der originalen PDFs konnten SumatraPDF (PDF Viewer für Windows) und in der verwendeten pdfquery Library nicht gelesen werden, diese müssen zur Verarbeitung repariert werden (z.B. mit pdf2go).
- Die PDF für den Haushalt 2015 wurde nachbearbeitet, indem Seiten in die horizontale Lage rotiert wurden (z.B. mit pdftk).

### Produktcodes

Aus den PDFs 2018 Band 1 und Band 2 für das Ergebnisjahr 2016: Codes und Bezeichnungen für die Produktbereiche (Code-1) sowie Produktgruppen (Code-2, Untergruppen der Produktbereiche), ergänzt um die Codes `0112 Gebäudemanagement` (im Haushalt 2007-2009) und `0505 Lastenausgleich` (2007-2011).

* [codes-2016-produktbereiche.csv](codes-2016-produktbereiche.csv)
* [codes-2016-produktgruppen.csv](codes-2016-produktgruppen.csv)

### Helferscripte

Script zur Erzeugung der `ergebnisse.csv` aus den Einzeldaten, Kombination und Anreicherung der Daten mit Codes der Produktbereiche: [combine_complete.py](combine_complete.py)
