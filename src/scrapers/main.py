import getopt
import os
import sys
import logging
from optparse import OptionParser

from platformen import NLvoorElkaar, WijAmsterdam, CoronaHelpersScraper\
    # HeldNodig, MensenDieWillenHelpen, \
    # Zorgheldenauto, PuurPapendrecht, NijmegenOost
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

parser = OptionParser(add_help_option=False)
parser.add_option("-h", "--help", help="show this help message and exit", action="store_true")
parser.add_option("-l", "--limit", help="LIM is the amount of items each scraper scrapes.", type="int", metavar="LIM")
parser.add_option("-g", "--nogeo", help="Disables the geocoder", action="store_true", dest="nogeo")

#HeldNodig().scrape()
#MensenDieWillenHelpen().scrape()
#Zorgheldenauto().scrape()
#PuurPapendrecht().scrape()
#NijmegenOost().scrape()
scrapers = [NLvoorElkaar(), WijAmsterdam(), CoronaHelpersScraper()]


def docs():
    parser.print_help()
    print('')
    print('If no arguments given, runs all scrapers')
    print('Use one or more codes as arguments to specify the scrapers to run:')
    print('{: <16}{}'.format("Code", "Name"))
    print('{: <16}{}'.format("____", "____"))
    for s in scrapers:
        print('{: <16}{}'.format(s.code, s.name))


(opts, args) = parser.parse_args()

if opts.help:
    docs()
else:
    print(f'Running {len(args)} scrapers. Use --help to see all individual scrapers')
    for scraper in scrapers:
        if opts.limit:
            scraper.limit = opts.limit

        # preferably each scraper runs in it's own thread.
        if not args:
            scraper.scrape()
        elif args and scraper.code in args:
            scraper.scrape()

    # Try to create geo location for items
    if not opts.nogeo:
        Geocoder().geocode()