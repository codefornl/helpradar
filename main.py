import os
import sys
<<<<<<< HEAD
from tools import Geocoder
from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam, MensenDieWillenHelpen, Zorgheldenauto, PuurPapendrecht, CoronaHelpers, NijmegenOost

# CoronaHelpers().scrape(); Niet bruikbaar. te sterk beveiligd om binnen legale kaders te scrapen.
=======

from platformen import HeldNodig, NLvoorElkaar, WijAmsterdam

>>>>>>> 7d80ae4... Now merging various sites into a sqlite db

HeldNodig().scrape()
NLvoorElkaar().scrape()
WijAmsterdam().scrape()
<<<<<<< HEAD
MensenDieWillenHelpen().scrape()
Zorgheldenauto().scrape()
PuurPapendrecht().scrape()
NijmegenOost().scrape()

# Try to create geolocation for items
Geocoder().geocode()
=======

>>>>>>> 7d80ae4... Now merging various sites into a sqlite db
