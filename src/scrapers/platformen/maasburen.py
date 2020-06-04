import logging

from . import Scraper
from .mijnbuurtje import MijnBuurtjeSource, MijnBuurtjeSourceConfig


class Maasburen(Scraper):
    def __init__(self):
        super().__init__("https://maasburen.nl", "Maasburen", "mbmb")
        cfg = MijnBuurtjeSourceConfig(
            "https://maasburen.nl",
            "https://maasburen.nl/elkaar-helpen?theme%5B%5D=836&format=fragment",
            "https://maasburen.nl/elkaar-helpen/",
            "Gemeente Maasburen")
        self.add_source(MijnBuurtjeSource(cfg))

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)