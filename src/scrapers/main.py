import logging

from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, \
    Zorgheldenauto, PuurPapendrecht, NijmegenOost, CoronaHelpersScraper
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

CoronaHelpersScraper().scrape()

HeldNodig().scrape()
NLvoorElkaar().scrape()
WijAmsterdam().scrape()
MensenDieWillenHelpen().scrape()
Zorgheldenauto().scrape()
PuurPapendrecht().scrape()
NijmegenOost().scrape()

# Try to create geolocation for items
Geocoder().geocode()
