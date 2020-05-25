import logging

from platformen import Scraper
from platformen.mijnbuurtje import MijnBuurtjeSource, MijnBuurtjeSourceConfig


class PuurPapendrecht(Scraper):
    def __init__(self):
        super().__init__("https://www.puurpapendrecht.nl", 'Puur Papendrecht', "mbpp")
        # form list enpoint
        cfg = MijnBuurtjeSourceConfig(
            "https://www.puurpapendrecht.nl",
            "https://puurpapendrecht.nl/elkaar-helpen?themes_puurpapendrecht_deed%5B%5D=837&format=fragment",
            "https://puurpapendrecht.nl/elkaar-helpen/",
            "Papendrecht")
        self.add_source(MijnBuurtjeSource(cfg))

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)