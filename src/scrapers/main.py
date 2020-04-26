import os
import sys
from tools import Geocoder
#from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, Zorgheldenauto, PuurPapendrecht, CoronaHelpers, NijmegenOost
from platformen import NLvoorElkaar

# CoronaHelpers().scrape(); Niet bruikbaar. te sterk beveiligd om binnen legale kaders te scrapen.

#HeldNodig().scrape()
NLvoorElkaar().scrape()
#WijAmsterdam().scrape()
#MensenDieWillenHelpen().scrape()
#Zorgheldenauto().scrape()
#PuurPapendrecht().scrape()
#NijmegenOost().scrape()

# Try to create geolocation for items
Geocoder().geocode()
