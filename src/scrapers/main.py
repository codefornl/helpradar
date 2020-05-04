import os
import sys
from tools import Geocoder
#from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, Zorgheldenauto, PuurPapendrecht, CoronaHelpers, NijmegenOost
from platformen import NLvoorElkaar, WijAmsterdam

# CoronaHelpers().scrape(); Niet bruikbaar. te sterk beveiligd om binnen legale kaders te scrapen.

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
# Geocoder().geocode()
