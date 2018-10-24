# Haushalt Münster

## How to scrape data

### Requirements

Basics:

- A working Python 3 installation
- [pdfquery package](https://github.com/jcushman/pdfquery) for Python
- 4 GB of RAM or more and a multicore CPU (a 600 page document requires about 2.5GB in total during runtime, if processing is split into 3 processes via `multiprocessing`)

### Configure yourself an environment with Python and virtualenv

Run these commands in the cloned Git directory:

```
virtualenv venv
pip install pdfquery
```

#### Patch pdfquery or wait a while

pdfquery unfortunately has a [bug](https://github.com/jcushman/pdfquery/issues/67) that limits caching with a page `range()` (exact details to be determined). You can remove caching from the script (multiple runs on the same PDF will be slow), cut down your PDFs to just tables, or apply [this patch](pdfquery.patch) (for pdfquery 0.4.3 from pip) which changes the naming of cache files.

### Run the script

Download data from Stadt Münster website: [stadt-muenster.de - Münsters Haushalt](https://www.stadt-muenster.de/finanzen/muensters-haushalt/der-haushaltsplan.html)

Insert the PDF filename into haushaltescraper.py:

```
filename = "HH_2018_Band_2.pdf"
```

Run the script:

```
python haushaltescraper.py
```

The output will be written to a CSV file called `eggs.csv`.

