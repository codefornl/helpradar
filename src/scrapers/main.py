import os
import sys
import logging

from platformen import NLvoorElkaar, WijAmsterdam, CoronaHelpersScraper\
    # HeldNodig, MensenDieWillenHelpen, \
    # Zorgheldenauto, PuurPapendrecht, NijmegenOost
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

#HeldNodig().scrape()
#MensenDieWillenHelpen().scrape()
#Zorgheldenauto().scrape()
#PuurPapendrecht().scrape()
#NijmegenOost().scrape()
scrapers = [NLvoorElkaar(), WijAmsterdam(), CoronaHelpersScraper()]

if sys.argv[1] == '--help':
    # print('Usage:')
    # print('[Code(s)] [options] in any order')
    # print('options:')
    # print('--limit=x    the amount of items a scraper scrapes')
    print('If no arguments given, runs all scrapers')
    print('Use one or more codes as arguments to specify the scrapers to run:')
    print('{: <16}{}'.format("Code", "Name"))
    print('{: <16}{}'.format("____", "____"))
    for scraper in scrapers:
        print('{: <16}{}'.format(scraper.code, scraper.name))
else:
    print(f'Running {len(sys.argv)} scrapers. Use /? to see all individual scrapers')
    for scraper in scrapers:
        # should be commandline option
        # scraper.limit = 5

        # preferably each scraper runs in it's own thread.
        if len(sys.argv) == 1:
            scraper.scrape()
        elif len(sys.argv) > 1 and scraper.code in sys.argv:
            scraper.scrape()

    # Try to create geolocation for items
    Geocoder().geocode()
