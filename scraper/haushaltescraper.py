import pdfquery
from pdfquery.cache import FileCache
from lxml import etree
import csv
from multiprocessing import Pool
import math

# This script requires Python 3

# Loosely based on example code by reddit user insainodwayno
# https://www.reddit.com/r/Python/comments/4bnjha/scraping_pdf_files_with_python/d1bsieu/

def parsePdf(pages):
	filename = "HH_2018_Band_2.pdf"
	print("Loading PDF {}".format(filename))
	#pdf = pdfquery.PDFQuery(filename)
	pdf = pdfquery.PDFQuery(filename, parse_tree_cacher=FileCache("cache/"))
	pdf.load(pages)
	
	# Append and return "bland objects" because
	# 'TypeError("can't pickle lxml.etree._Element objects",)'
	parsed_data = []

	for page in pages:
		print('--- Page {} --- '.format(page), end='')
		try:
			# First extract:
			# - Check for correct table header
			# - Check for position of table by checking page numbers in the corners
			data = pdf.extract([
				('with_parent', 'LTPage[page_index="{}"]'.format(page)),
				('with_formatter', "text"),
				('teilergebnisplan','LTTextLineHorizontal:in_bbox("56.871, 495.858, 136.16, 507.711")'),
			])
			if data['teilergebnisplan'] is None or data['teilergebnisplan'].strip() != "Teilergebnisplan":
				print('Skipped: Expected string "Teilergebnis" not found')
				continue

			# Calculate bboxes from bbox from row label
			ord_ertr_label = pdf.pq('LTTextLineHorizontal:contains("= Ordentliche Erträge ")')
			ord_aufw_label = pdf.pq('LTTextLineHorizontal:contains("= Ordentliche Aufwendungen ")')
			ay0 = math.floor(float(ord_ertr_label.attr('y0')))
			ay1 = math.ceil(float(ord_ertr_label.attr('y1')))
			by0 = math.floor(float(ord_aufw_label.attr('y0')))
			by1 = math.ceil(float(ord_aufw_label.attr('y1')))
			selector_ord_ertraege_value = 'LTTextLineHorizontal:in_bbox("362, {}, 426, {}")'.format(ay0, ay1)
			selector_ord_aufwendungen_value = 'LTTextLineHorizontal:in_bbox("362, {}, 426, {}")'.format(by0, by1)

			# Second extract:
			# - Grab the data we want
			data = pdf.extract([
				('with_parent', 'LTPage[page_index="{}"]'.format(page)),
				('with_formatter', "text"),
				('produktgruppe_name', 'LTTextLineHorizontal:in_bbox("250, 538, 600, 551")'),
				('produktgruppe_identifier', 'LTTextLineHorizontal:in_bbox("372, 526.458, 470, 538.311")'),
				('ord_ertraege_value', selector_ord_ertraege_value),
				('ord_aufwendungen_value', selector_ord_aufwendungen_value)
			])

			if len(data['produktgruppe_identifier'].split(' ')[1]) < 4:
				print("Skipped: Product identifier too short")
				continue
				
			parsed_data.append({
				'produktgruppe_name': data['produktgruppe_name'],
				'produktgruppe_identifier': data['produktgruppe_identifier'],
				'ord_ertraege_value': data['ord_ertraege_value'],
				'ord_aufwendungen_value': data['ord_aufwendungen_value']
			})
			print("Added data")

		except:
			print('An Exception occured')
			pass
	return parsed_data

if __name__ == '__main__':
	with Pool(processes=3) as p:
		# HH_2018_Band_2 - 596 pages
		pool_results = p.map(parsePdf, [list(range(1,200)), list(range(200,400)), list(range(400,590))])
		with open('eggs.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',')
			spamwriter.writerow(['Code-1', 'Code-2', 'Bezeichnung', 'Richtung', 'Betrag'])
			for process_results in pool_results:
				for process_result in process_results:
					produktgruppe_ebene2 = process_result['produktgruppe_identifier'].split(" ")[1]
					produktgruppe_ebene1 = produktgruppe_ebene2[0:2]
					spamwriter.writerow([produktgruppe_ebene1, produktgruppe_ebene2, process_result['produktgruppe_name'], 'Einnamen', process_result['ord_ertraege_value']])
					spamwriter.writerow([produktgruppe_ebene1, produktgruppe_ebene2, process_result['produktgruppe_name'], 'Ausgaben', process_result['ord_aufwendungen_value']])
