import os
import sys
from tools import Geocoder
from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, Zorgheldenauto, PuurPapendrecht, NijmegenOost
from platformen import CoronaHelpersScraper

import logging
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
