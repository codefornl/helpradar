import logging
from typing import Generator

from bs4 import BeautifulSoup

from models.initiatives import InitiativeImport, InitiativeGroup
from .scraper import Scraper, PlatformSource, PlatformSourceConfig, ScrapeException


class NLvoorElkaarSourceConfig(PlatformSourceConfig):
    # Category 45 is the one for Corona
    _LIST_ENDPOINT = "/update/resultmarkers.json?categories[]=45"

    def __init__(self, group, url, field_map):
        super().__init__(
            url,
            '/hulpaanbod' + self._LIST_ENDPOINT if group == InitiativeGroup.SUPPLY else "/hulpvragen" + self._LIST_ENDPOINT,
            '/hulpaanbod/' if group == InitiativeGroup.SUPPLY else "/hulpvragen/"
        )
        self.group = group
        self.url = url
        self.field_map = field_map

    def get_marker_url(self, url_id):
        markerurl_segment = 'hulpaanbod' if self.group == InitiativeGroup.SUPPLY else 'hulpvragen'
        return f"https://www.nlvoorelkaar.nl/{markerurl_segment}/{url_id}"


class NLvoorElkaarSource(PlatformSource):

    def __init__(self, config: NLvoorElkaarSourceConfig):
        super().__init__(config)

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        url = self.config.get_list_url()
        page = PlatformSource.get(url)
        result = page.json()

        for marker in result['markers']:
            initiative = InitiativeImport(
                source_id=marker['id'],
                source_uri=self.config.get_marker_url(marker['id']),
                latitude=marker['lat'],
                longitude=marker['lon'],
            )
            yield initiative

    def complete(self, initiative: InitiativeImport):
        initiative_url = self.config.get_initiative_url(initiative.source_id)

        try:
            detail = PlatformSource.get(initiative_url)

            soup = BeautifulSoup(detail.content, 'html.parser')

            table = soup.find("dl")
            records = table.findAll(["dd", "dt"])
            initiative.description = soup.find("p").text.strip('\t\n\r')
            initiative.group = self.config.group
            initiative.source = initiative_url

            setcount = 0
            for i in range(0, len(records), 2):
                # TODO: Error prevention
                label = records[i].contents[1].strip("\":").lower()
                if label in self.config.field_map:
                    setattr(initiative, self.config.field_map[label], records[i + 1].contents[0])
                    setcount += 1

            if self.config.group == InitiativeGroup.DEMAND:
                title = soup.find("h2", "result__title")
                initiative.organiser = title.contents[0]

            # TODO: Logging is no values are assigned
        except ScrapeException as e:
            # should not catch
            # ('error scraping ' + initiative_url + ':' + e.args[0])
            if initiative is not None:
                initiative.state = "processing_error"


class NLvoorElkaar(Scraper):
    """NL Voor Elkaar scraper die zowel vraag als aanbod ophaalt"""

    def __init__(self):
        super().__init__("https://www.nlvoorelkaar.nl", 'NL Voor Elkaar', "nlve")
        self.add_source(NLvoorElkaarSource(
            NLvoorElkaarSourceConfig(
                InitiativeGroup.SUPPLY,
                self.platform_url,
                {
                    "titel": "name",
                    "plaats": "location",
                    "categorie": "category",
                    "aangeboden door": "organisation_kind",
                })))
        self.add_source(NLvoorElkaarSource(
            NLvoorElkaarSourceConfig(
                InitiativeGroup.DEMAND,
                self.platform_url,
                {
                    "plaats": "location",
                    "categorie": "category",
                    "beschikbaarheid": "frequency",
                })))

    def scrape(self):
        # Could better use template method on base class instead of require super call
        super().scrape()

    def get_logger(self) -> logging.Logger:
        return logging.getLogger("platformen.nlvoorelkaar")
