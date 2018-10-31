import csv
import re

product_codes1 = dict()
product_codes2 = dict()

with open('codes-2016-produktbereiche.csv', newline='', encoding='UTF-8') as csvfile:
	codereader = csv.reader(csvfile, delimiter=',', quotechar='"')
	# https://stackoverflow.com/questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
	next(codereader, None) # skip the headers
	for row in codereader:
		product_codes1[row[0]] = row[1]

with open('codes-2016-produktgruppen.csv', newline='', encoding='UTF-8') as csvfile:
	codereader = csv.reader(csvfile, delimiter=',', quotechar='"')
	next(codereader, None)
	for row in codereader:
		product_codes2[row[0]] = row[1]

with open("ergebnisse_2007_2016.csv", 'w', newline='', encoding='utf-8') as results_csvfile:
	results_writer = csv.writer(results_csvfile, delimiter=',')
	results_writer.writerow(['Produktbereich', 'Produktgruppe', 'Produktbereichsname', 'Produktgruppenbezeichnung', 'Jahr', 'Richtung', 'Betrag', 'Betrag-Typ'])
	
	source_files = [
		'ergebnis-2007-complete.csv',
		'ergebnis-2008-complete.csv',
		'ergebnis-2009-complete.csv',
		'ergebnis-2010-complete.csv',
		'ergebnis-2011-complete.csv',
		'ergebnis-2012-complete.csv',
		'ergebnis-2013-complete.csv',
		'ergebnis-2014-complete.csv',
		'ergebnis-2015-complete.csv',
		'ergebnis-2016-complete.csv'
	]

	for source_file in source_files:
		print(source_file)
		with open(source_file, newline='', encoding='utf-8') as source_csvfile:
			source_reader = csv.DictReader(source_csvfile)
			next(source_reader, None)
			for source_row in source_reader:
				# Code-1,Code-2,Bezeichnung,Richtung,Betrag
				values = [
					source_row['Code-1'],
					source_row['Code-2'],
					product_codes1[source_row['Code-1']],
					source_row['Bezeichnung'],
					re.search("-([0-9]{4})-", source_file).group(1),
					source_row['Richtung'],
					source_row['Betrag'].replace(".","").replace(",","."), # to international number format 
					"Ergebnis"
				]
				results_writer.writerow(values)