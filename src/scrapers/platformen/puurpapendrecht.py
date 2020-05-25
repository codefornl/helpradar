import logging

from platformen import Scraper
from platformen.mijnbuurtje import MijnBuurtjeSource
from platformen.scraper import PlatformSourceConfig


class PuurPapendrecht(Scraper):
    def __init__(self):
        super().__init__("https://www.puurpapendrecht.nl", 'Puur Papendrecht', "pp")
        # form list enpoint themes_puurpapendrecht_deed%5B%5D=837&
        cfg = PlatformSourceConfig(
            "https://www.puurpapendrecht.nl",
            "https://puurpapendrecht.nl/elkaar-helpen?format=fragment",
            "https://puurpapendrecht.nl/elkaar-helpen/")
        self.add_source(MijnBuurtjeSource(cfg))

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)