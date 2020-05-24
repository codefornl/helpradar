from typing import Generator

from models import InitiativeImport
from platformen import Scraper
from platformen.scraper import PlatformSource, PlatformSourceConfig



class MijnBuurtjeSource(PlatformSource):
    def __init__(self, config: PlatformSourceConfig):
        super().__init__(config)
        self.config = config

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        yield None

    def complete(self, initiative: InitiativeImport):

class MijnBuurtje(Scraper):


class MijnBuurtjes(Scraper):
    """
    Scraped alle bekende instanties van mijn buurtje
    """