import os
import sys
from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, \
    Zorgheldenauto, PuurPapendrecht, NijmegenOost, CoronaHelpersScraper
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

#CoronaHelpersScraper().scrape()
#HeldNodig().scrape()
#MensenDieWillenHelpen().scrape()
#Zorgheldenauto().scrape()
#PuurPapendrecht().scrape()
#NijmegenOost().scrape()
scrapers = [NLvoorElkaar(), WijAmsterdam()]

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
