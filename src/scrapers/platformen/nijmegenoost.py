import logging

from platformen import Scraper
from platformen.mijnbuurtje import MijnBuurtjeSource, MijnBuurtjeSourceConfig


class NijmegenOost(Scraper):
    def __init__(self):
        super().__init__("https://nijmegen-oost.nl", "Nijmegen Oost", "mbno")
        cfg = MijnBuurtjeSourceConfig(
            "https://nijmegen-oost.nl",
            "https://nijmegen-oost.nl/elkaar-helpen?theme%5B%5D=836&format=fragment",
            "https://nijmegen-oost.nl/elkaar-helpen/",
            "Nijmegen")
        self.add_source(MijnBuurtjeSource(cfg))

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)