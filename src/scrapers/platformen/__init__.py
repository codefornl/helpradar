from .scraper import Scraper

from .coronahelpers import CoronaHelpersScraper
# from .heldnodig import HeldNodig
# from .mensendiewillenhelpen import MensenDieWillenHelpen
from .maasburen import Maasburen
from .nijmegenoost import NijmegenOost
from .nlvoorelkaar import NLvoorElkaar
# from .zorgheldenauto import Zorgheldenauto
from .puurpapendrecht import PuurPapendrecht
from .wijamsterdam import WijAmsterdam

__all__ = [
    'CoronaHelpersScraper',
    'Maasburen',
    'NijmegenOost',
    'NLvoorElkaar',
    'PuurPapendrecht',
    'Scraper',
    'WijAmsterdam',
]