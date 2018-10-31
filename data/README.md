# Haushaltspläne als CSV-Dateien

In diesem Ordner befinden sich die mit dem scraper aufbearbeiteten Daten, die aus den PDFs extrahiert wurden (siehe auch [README](../scraper/README.md) im scraper Ordner).

Die Haushaltsdaten der Stadt Münster in PDF-Form sind aufgeteilt in Band 1 und 2. In seltenen Fällen enthält Band 2 alle Daten, meistens jedoch nur Produktkategorien 03 bis 17.

Dateien mit dem Wort `complete` im Namen wurden stichprobenartig auf Korrektheit geprüft, z.T. manuell vervollständig und enthalten alle Daten aus Band 1 und 2, sofern Daten in den original PDFs getrennt vorliegen.

## Dateien in diesem Ordner

### Haushaltsdaten

Ergebnisdaten für die Haushaltsjahre 2007 bis 2016: [ergebnisse_2007_2016.csv](ergebnisse_2007_2016.csv)

### Haushaltsdaten pro Jahr

Hinweise:

- Notiz "rep.": Die original PDF ist fehlerhaft und wurde mit pdf2go repariert, da sie in SumatraPDF und/oder der Python Library nicht geöffnet werden konnte.
- Notiz "nachb.": Die original PDF wurde nachbearbeitet, z.B. Seiten in die für den scraper korrekte horizontale Lage rotiert.

#### 2007

* [ergebnis-2007-complete.csv](ergebnis-2007-complete.csv): Ergebnis für das Jahr 2007 aus "Haushaltsplan 2009, Band 2" (rep.)

#### 2008

* [ergebnis-2008-band1.csv](ergebnis-2008-band1.csv): Ergebnis für das Jahr 2008 aus "Haushaltsplan 2010, Band 1" (rep.)
* [ergebnis-2008-band2.csv](ergebnis-2008-band2.csv): Ergebnis für das Jahr 2008 aus "Haushaltsplan 2010, Band 2"

#### 2009

* [ergebnis-2009-band1.csv](ergebnis-2009-band1.csv): Ergebnis für das Jahr 2009 aus "Haushaltsplan 2011, Band 1" (rep.)
* [ergebnis-2009-band2.csv](ergebnis-2009-band2.csv): Ergebnis für das Jahr 2009 aus "Haushaltsplan 2011, Band 2" (rep.)

#### 2010

* [ergebnis-2010-band1.csv](ergebnis-2010-band1.csv): Ergebnis für das Jahr 2010 aus "Haushaltsplan 2012, Band 1"
* [ergebnis-2010-band2.csv](ergebnis-2010-band2.csv): Ergebnis für das Jahr 2010 aus "Haushaltsplan 2012, Band 2"

#### 2011

* [ergebnis-2011-band1.csv](ergebnis-2011-band1.csv): Ergebnis für das Jahr 2011 aus "Haushaltsplan 2013, Band 1"
* [ergebnis-2011-band2.csv](ergebnis-2011-band2.csv): Ergebnis für das Jahr 2011 aus "Haushaltsplan 2013, Band 2" (rep.)

#### 2012

* [ergebnis-2012-complete.csv](ergebnis-2012-complete.csv): Ergebnis für das Jahr 2012 aus "Haushaltsplan 2014, Band 2"

#### 2013

* [ergebnis-2013-band1.csv](ergebnis-2013-band1.csv): Ergebnis für das Jahr 2013 aus "Haushaltsplan 2015, Band 1"
* [ergebnis-2013-band2.csv](ergebnis-2013-band2.csv): Ergebnis für das Jahr 2013 aus "Haushaltsplan 2015, Band 2"

#### 2014

* [ergebnis-2014-band1.csv](ergebnis-2014-band1.csv): Ergebnis für das Jahr 2014 aus "Haushaltsplan 2016, Band 1"
* [ergebnis-2014-band2.csv](ergebnis-2014-band2.csv): Ergebnis für das Jahr 2014 aus "Haushaltsplan 2016, Band 2"

#### 2015

* [ergebnis-2015-band1.csv](ergebnis-2015-band1.csv): Ergebnis für das Jahr 2015 aus "Haushaltsplan 2017, Band 1" (nachb.)
* [ergebnis-2015-band2.csv](ergebnis-2015-band2.csv): Ergebnis für das Jahr 2015 aus "Haushaltsplan 2017, Band 2"

#### 2016

* [ergebnis-2016-band1.csv](ergebnis-2016-band1.csv): Ergebnis für das Jahr 2016 aus "Haushaltsplan 2018, Band 1"
* [ergebnis-2016-band2.csv](ergebnis-2016-band2.csv): Ergebnis für das Jahr 2016 aus "Haushaltsplan 2018, Band 2"

### Weitere Dateien

Aus den PDFs 2018 Band 1 und Band 2 für das Jahr 2016: Codes und Bezeichnungen für die Produktbereiche (Code-1) sowie Produktgruppen (Code-2, Untergruppen der Produktbereiche), ergänzt um die Codes `0112 Gebäudemanagement` (im Haushalt 2007-2009) und `0505 Lastenausgleich` (2007-2011).

* [codes-2016-produktbereiche.csv](codes-2016-produktbereiche.csv)
* [codes-2016-produktgruppen.csv](codes-2016-produktgruppen.csv)

Script zum Kombinieren und anreichern der Daten mit Codes der Produktbereiche: [combine_complete.py](combine_complete.py)
