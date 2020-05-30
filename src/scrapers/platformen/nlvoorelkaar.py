import logging
import re
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

        try:
            result = page.json()
            for marker in result['markers']:
                initiative = InitiativeImport(
                    source_id=marker['id'],
                    source_uri=self.config.get_marker_url(marker['id']),
                    latitude=marker['lat'],
                    longitude=marker['lon'],
                )
                yield initiative
        except Exception as ex:
            msg = f"Error reading contents from {url}"
            raise ScrapeException(msg) from ex

    def complete(self, initiative: InitiativeImport):
        initiative_url = self.config.get_initiative_url(initiative.source_id)
        # This already raises ScrapeExceptions
        detail = PlatformSource.get(initiative_url)

        try:
            soup = BeautifulSoup(detail.content, 'html.parser')

            table = soup.find("dl")
            records = table.findAll(["dd", "dt"])
            initiative.description = soup.find("p").text.strip('\t\n\r ')
            initiative.group = self.config.group
            initiative.source = initiative_url

            set_count = self.extract_details_table(initiative, records)

            if self.config.group == InitiativeGroup.DEMAND:
                title = soup.find("h2", "result__title")
                initiative.name = title.contents[0]

            h5nodeAboveOrganiser = soup.find("h5", text="Aangesloten bij:")
            if h5nodeAboveOrganiser:
                initiative.organiser = h5nodeAboveOrganiser.next_sibling.next_sibling.get_text(strip=True)

            if not initiative.location:
                self.try_alternative_place(soup, initiative)
        except Exception as ex:
            msg = f"Error reading contents from {initiative_url}"
            raise ScrapeException(msg) from ex

        if set_count == 0:
            raise ScrapeException("Failed to load field map details table")

    def extract_details_table(self, initiative, records):
        set_count = 0
        for i in range(0, len(records), 2):
            label = records[i].contents[1].strip("\":").lower()
            if label in self.config.field_map:
                has_value = len(records[i + 1].contents) > 0
                if has_value:
                    value = records[i + 1].contents[0]
                    setattr(initiative, self.config.field_map[label], value)
                    set_count += 1
        return set_count

    @staticmethod
    def try_alternative_place(soup, initiative):
        """
        Looks to see if it can strip the place name from [placename]voorelkaar
        <li> Deze persoon staat ingeschreven op Amstelveenvoorelkaar</li>
        """
        checks = soup.find("li", text=re.compile("voorelkaar$"))
        if checks is not None:
            match = re.search("([a-zA-Z0-9]+)voorelkaar$", checks.text)
            if match:
                initiative.location = match.group(1)


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
