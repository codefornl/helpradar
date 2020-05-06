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

if sys.argv[1] == '/?':
    print('If not argument given, runs all scrapers')
    print('Use one or more codes as arguments to specify the scrapers to run:')
    print('{: <16}{}'.format("Code", "Name"))
    print('{: <16}{}'.format("____", "____"))
    for scraper in scrapers:
        print('{: <16}{}'.format(scraper.code, scraper.name))
else:
    print(f'Running {len(sys.argv)} scrapers. Use /? to see all individual scrapers')
    for scraper in scrapers:
        test = scraper.code in sys.argv
        if len(sys.argv) == 1:
            scraper.scrape()
        elif len(sys.argv) > 1 and scraper.code in sys.argv:
            scraper.scrape()

    # Try to create geolocation for items
    Geocoder().geocode()
