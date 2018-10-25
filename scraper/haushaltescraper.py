import csv
import math
import pdfquery
import re
from lxml import etree
from multiprocessing import Pool
from pdfquery.cache import FileCache

# This script requires Python 3

# Loosely based on example code by reddit user insainodwayno
# https://www.reddit.com/r/Python/comments/4bnjha/scraping_pdf_files_with_python/d1bsieu/

def parsePdf(config):
	pages = config['pages']
	filename = config['filename']
	verbose = config['verbose']

	print("Loading PDF {}".format(filename))
	#pdf = pdfquery.PDFQuery(filename)
	pdf = pdfquery.PDFQuery(filename, parse_tree_cacher=FileCache("cache/"))
	pdf.load(pages)
	
	# Append and return "bland objects" because
	# 'TypeError("can't pickle lxml.etree._Element objects",)'
	parsed_data = []

	for page in pages:
		if verbose:
			print('--- Page {} --- '.format(page), end='')
		try:
			# First extract:
			# - Check for correct table header
			data = pdf.extract([
				('with_parent', 'LTPage[page_index="{}"]'.format(page)),
				('with_formatter', "text"),
				('teilergebnisplan','LTTextLineHorizontal:in_bbox("56, 495, 137, 508")')
			])
			if data['teilergebnisplan'] is None or data['teilergebnisplan'].strip() != "Teilergebnisplan":
				if verbose:
					print('Skipped: Expected string "Teilergebnisplan" not found')
				continue

			data = pdf.extract([
				('with_parent', 'LTPage[page_index="{}"]'.format(page)),
				('with_formatter', "text"),
				('produktgruppe','LTTextLineHorizontal:contains("Produktgruppe ")')
			])
			prod_gruppe_re = re.search(r"Produktgruppe ([0-9]{4})", data['produktgruppe'])
			produktgruppe_identifier = None
			if data['produktgruppe'] is None or prod_gruppe_re is None:
				if verbose:
					print('Skipped: Expected string "Produktgruppe" not found or id too short')
				continue
			else:
				produktgruppe_identifier = prod_gruppe_re.group(1)

			# Calculate value bboxes from known text
			ord_ertr_label = pdf.pq('LTTextLineHorizontal:contains("= Ordentliche Erträge ")')
			ord_ertr_y0 = math.floor(float(ord_ertr_label.attr('y0')))
			ord_ertr_y1 = math.ceil(float(ord_ertr_label.attr('y1')))
			selector_ord_ertraege_value = 'LTTextLineHorizontal:in_bbox("362, {}, 426, {}")'.format(ord_ertr_y0, ord_ertr_y1)

			ord_aufw_label = pdf.pq('LTTextLineHorizontal:contains("= Ordentliche Aufwendungen ")')
			ord_aufw_y0 = math.floor(float(ord_aufw_label.attr('y0')))
			ord_aufw_y1 = math.ceil(float(ord_aufw_label.attr('y1')))
			selector_ord_aufwendungen_value = 'LTTextLineHorizontal:in_bbox("362, {}, 426, {}")'.format(ord_aufw_y0, ord_aufw_y1)
			
			produktgruppe_id_ltt = pdf.pq('LTTextLineHorizontal:contains("Produktgruppe ")')
			produktgruppe_id_y0 = math.floor(float(produktgruppe_id_ltt.attr('y0')))
			produktgruppe_id_y1 = math.ceil(float(produktgruppe_id_ltt.attr('y1')))
			selector_produktgruppe_id = 'LTTextLineHorizontal:in_bbox("372, {}, 470, {}")'.format(produktgruppe_id_y0, produktgruppe_id_y1)

			# Second extract:
			# - Grab the data we want
			data = pdf.extract([
				('with_parent', 'LTPage[page_index="{}"]'.format(page)),
				('with_formatter', "text"),
				('produktgruppe_name', 'LTTextLineHorizontal:in_bbox("250, 535, 600, 555")'),
				('ord_ertraege_value', selector_ord_ertraege_value),
				('ord_aufwendungen_value', selector_ord_aufwendungen_value)
			])

			parsed_data.append({
				'produktgruppe_name': data['produktgruppe_name'],
				'produktgruppe_identifier': produktgruppe_identifier,
				'ord_ertraege_value': data['ord_ertraege_value'],
				'ord_aufwendungen_value': data['ord_aufwendungen_value']
			})
			if verbose:
				print("Added data")
			else:
				print("Added data from page {}, prod.id {}".format(page, produktgruppe_identifier))

		except Exception as e:
			print('An Exception occured: {}'.format(e))
			raise(e)
			pass
	return parsed_data

if __name__ == '__main__':
	## Config start - change these values
	processes = 3
	#pdf_filename = "input/HH_2017_Band_2_m_Lesez.pdf"                 # 586 pages
	#pdf_filename = "input/HH_2018_Band_2.pdf"                         # 596 pages
	#pdf_filename = "input/HH_2016_Band_2_Druckexemplar_mit_Lesez.pdf" # 586 pages
	#pdf_filename = "input/HPL_2015_Band_2_mit_Seitenz_m_Lesez.pdf"    # 584 pages
	#pdf_filename = "input/Band_2_HPL_2014.pdf"                        # 796 pages
	#pdf_filename = "input/HH_2013_Band_2-fixed.pdf"                   # 588 pages
	#pdf_filename = "input/Haushaltsplan_2012_Band_2.pdf"              # 590 pages
	#pdf_filename = "input/HPL_2011_Band_2-fixed.pdf"                  # 572 pages
	#pdf_filename = "input/HPL_2010_Band_2.pdf"                        # 588 pages
	pdf_filename = "input/Haushaltsplan_2009_Band_2-fixed.pdf"         # 796 pages
	out_filename = "output/ergebnis-2007-band2.csv"
	# pagelist is 0-indexed
	pagelist = [list(range(0,200)), list(range(200,400)), list(range(400,795))]
	# more detailed logging
	verbose = False
	## Config end

	# Generate a configuration dict for every process
	config = [{'filename': pdf_filename, 'pages': p, 'verbose': verbose} for p in pagelist]
	with Pool(processes=processes) as p:
		pool_results = p.map(parsePdf, config)
		with open(out_filename, 'w', newline='', encoding='utf-8') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',')
			spamwriter.writerow(['Code-1', 'Code-2', 'Bezeichnung', 'Richtung', 'Betrag'])
			for process_results in pool_results:
				for process_result in process_results:
					produktgruppe_ebene2 = process_result['produktgruppe_identifier']
					produktgruppe_ebene1 = produktgruppe_ebene2[0:2]
					spamwriter.writerow([produktgruppe_ebene1, produktgruppe_ebene2, process_result['produktgruppe_name'], 'Einnamen', process_result['ord_ertraege_value']])
					spamwriter.writerow([produktgruppe_ebene1, produktgruppe_ebene2, process_result['produktgruppe_name'], 'Ausgaben', process_result['ord_aufwendungen_value']])
