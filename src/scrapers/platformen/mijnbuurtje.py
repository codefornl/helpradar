import json
import locale
import logging
import re
import time
from datetime import date
from typing import Generator
from calendar import month_name

from lxml import etree

from models import InitiativeImport
from platformen.TreeParser import TreeParser
from platformen.scraper import PlatformSource, PlatformSourceConfig, ScrapeException, Scraper


class MijnBuurtjeSourceConfig(PlatformSourceConfig):
    def __init__(self, platform_url, list_endpoint, details_endpoint, location: str = None):
        """
         Parameters
        ----------
        location : str
            The name of the main region this mijn buurtje instance is about.
        """

        super().__init__(platform_url, list_endpoint, details_endpoint)
        self.location = location


class MijnBuurtjeSource(PlatformSource):
    ITEM_SCHEMA = {'name': {"xpath": "//div/h1[1]/text()"},
                   # 'orig_group': {
                   #     'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()'},
                   'group': {
                       'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()',
                       'transform': lambda text: MijnBuurtjeSource.format_group(text)},
                   'description': {
                       "xpath": "//div[contains(@class, 'content-section')][3]/*/node()",
                       'all': True,
                       'transform': lambda elements: MijnBuurtjeSource.recursive_text(elements)},
                   'organiser': {'xpath': "//a[@class='entity']/div[contains(@class, 'entity-content')]/div[contains("
                                          "@class, 'entity-content-title')]/text()",
                                 'transform': lambda text: MijnBuurtjeSource.format_organizer(text)},
                   # 'organiser_kind': {'xpath': '//span[@class="meta-item-content" and contains(text(),"Vraag vanuit:")]',
                   #               'transform': lambda text: text.replace("Vraag vanuit: ", "")},
                   'category': {
                       'xpath': '//span[@class="meta-item-content" and contains(text(),"Thema:")]',
                       'transform': lambda elem: MijnBuurtjeSource.strip_text(elem, "Thema: ")},
                   'frequency': {
                       "xpath": "//span[@class='mb-calendar meta-item-icon']/following-sibling::span[1]/text()",
                       "transform": lambda elem: MijnBuurtjeSource.json_frequency(elem)},
                   'created_at': {
                       'xpath': '//div[@class="heading3 heading3--semibold"]/text()',
                       'transform': lambda text: MijnBuurtjeSource.format_date(text)},
                   'location': {
                       'xpath': '//span[@class="meta-item-content" and contains(text(),"Dorp:")]',
                       'transform': lambda elem: MijnBuurtjeSource.strip_text(elem, "Dorp: ")},
                   }
    MONTHS = None
    if not MONTHS:
        try:
            locale.setlocale(locale.LC_ALL, 'nl_NL.utf-8')
            MONTHS = list(month_name)
        except locale.Error:
            MONTHS = ["", "januari", "februari", "maart", "april", "mei", "juni",
                      "juli", "augustus", "september", "oktober", "november", "december"]

    delay = 10

    def __init__(self, config: MijnBuurtjeSourceConfig, delay: int = 10):
        super().__init__(config)
        self.delay = delay
        self.item_parser = TreeParser(None, None, self.ITEM_SCHEMA)
        self.initiative_links_re = re.compile(self.config.details_endpoint + "\\d{4,5}/[a-zA-Z0-9-]+")

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        page_counter = 1
        try:
            while page_counter < 100:
                list_page_url = self.config.list_endpoint + f"&page={page_counter}"

                # schemas: defines fields to be scraped
                # schema: fieldname:{xpath,all,cast,transform}
                schemas = {'initiatives':
                               {'xpath': '//a[@href and contains(@class, "postpreview-content")]',
                                'all': True,
                                'transform': lambda elements: self.find_initiative_links(elements)}}

                # initialize TreeParser using url and schemas, returns html tree
                initiative_parser = TreeParser(list_page_url, None, schemas)
                if initiative_parser.tree is None:
                    break

                output = initiative_parser.apply_schemas()
                for uri in output['initiatives']:
                    yield InitiativeImport(source_uri=uri[0])

                page_counter = page_counter + 1
        except Exception as ex:
            raise ScrapeException("Error loading list of initiatives") from ex

    def complete(self, initiative: InitiativeImport):
        try:
            # Robots.txt mentions 10 secs crawl delay.
            time.sleep(self.delay)

            session_metadata = self.item_parser.get_session_metadata(initiative.source_uri)
            full_initiative = self.item_parser.apply_schemas(metadata=session_metadata,
                                                             url=initiative.source_uri)
            for key, value in full_initiative.items():
                setattr(initiative, key, value)

            if not initiative.location:
                initiative.location = self.config.location

        except Exception as ex:
            raise ScrapeException(f"Error scraping {initiative.source_uri}") from ex

    def find_initiative_links(self, elements):
        """
        filters links. Input seems to be 1 on 1 now. Extracted to method for easier debugging.
        """
        initiatives = []
        for e in elements:
            links = re.findall(self.initiative_links_re, e.attrib['href'])
            if len(links) > 0:
                initiatives.append(links)

        return initiatives

    @staticmethod
    def strip_text(element, strip: str):
        if element is None:
            return None
        if not element.text:
            return None

        stripped = element.text.replace(strip, "")
        return stripped

    @staticmethod
    def recursive_text(elements):
        texts = []
        for e in elements:
            if type(e) in [etree._ElementUnicodeResult]:
                texts.append(f"{e.strip()}")
            else:
                if e.tag == "p" or e.tag == "span" or e.tag == "div":
                    texts.append(f"{e.text.strip()}")
        return ' '.join(texts)

    @staticmethod
    def format_group(original_group: str):
        if len(re.findall("Hulpvraag.*?", original_group)) > 0:
            return 'demand'
        else:
            return 'supply'

    @staticmethod
    def format_organizer(organizer):
        if organizer is not None:
            organizer = re.sub('-', ' ', organizer)
            name_segments = organizer.split()
            organizer_name = None if len(name_segments) == 0 else name_segments[0]

            return organizer_name

    @staticmethod
    def format_date(date_str: str):
        # TODO: This is an important field. Should break here!
        if not date_str:
            raise ValueError("Always expecting a date string for conversion!")

        try:
            day, mon_name, year = date_str.split()
            month = MijnBuurtjeSource.MONTHS.index(mon_name.lower())
            d = date(int(year), month, int(day))
            return d
        except ValueError as e:
            msg = f"Expecting a three segment date, got {date_str}."
            raise ValueError(msg) from e

    @staticmethod
    def json_frequency(elem: str):
        frequency = {"on": elem}
        return json.dumps(frequency)


class MijnBuurtje(Scraper):
    """
    Scrapes all known mijn buurtje instances.
    """
    def __init__(self):
        super().__init__("https://mijnbuurtje.nl", "Mijn Buurtje", "mibu")
        self._add_instance("https://nijmegen-oost.nl", "Nijmegen")
        self._add_instance("https://puurpapendrecht.nl", "Papendrecht", {"themes_puurpapendrecht_deed%5B%5D": 837})
        self._add_instance("https://maasburen.nl", "Maasburen")
        self._add_instance("https://onsoverbetuwe.nl", "Overbetuwe")
        self._add_instance("https://buurtkanaal.nl", "Brummen")
        self._add_instance("https://onzewippolder.nl", "Delft")
        self._add_instance("https://kijkopdevoordijk.nl", "Delft")
        self._add_instance("https://buitenhofbruist.nl", "Delft")
        self._add_instance("https://onstanthof.nl", "Delft")
        self._add_instance("https://kenhem.com", "Ede")
        self._add_instance("https://lindenholtleeft.nl", "Nijmegen")
        self._add_instance("https://wijwijchen.nl", "Wijchen")
        self._add_instance("https://mienthuus.de", "Kranenburg")
        self._add_instance("https://buurtkiep.nl", "Den Bosch")
        self._add_instance("https://stinskracht.nl", "Zwolle")
        self._add_instance("https://entrede.nl", "Ede")
        self._add_instance("https://centrede.nl", "Ede")
        self._add_instance("https://haareneen.nl", "Haaren")
        self._add_instance("https://utdorp.nl", "Venlo")
        self._add_instance("https://mooimergelland.nl", "Eijsden-Margraten")
        self._add_instance("https://onsalphenchaam.nl", "Alphen-Chaam")
        self._add_instance("https://westersite.nl", "Amsterdam West")
        self._add_instance("https://onsoosterhuizen.nl", "Apeldoorn")
        self._add_instance("https://mijnbrakkenstein.nl", "Nijmegen")
        self._add_instance("https://mijnspijkerkwartier.nl", "Arnhem")
        self._add_instance("https://lentselucht.nl", "Nijmegen")
        self._add_instance("https://onsthuus.nl", "Boxtel")
        self._add_instance("https://nieuw-dijk.nl", "Nieuw-Dijk")

    def _add_instance(self, url, location, query_params = None):
        if not query_params:
            query_params = {"theme%5B%5D": 836}

        qparams = "&".join([f"{k}={v}" for (k, v) in query_params.items()])
        cfg = MijnBuurtjeSourceConfig(
            url,
            f"{url}/elkaar-helpen?{qparams}&format=fragment",
            f"{url}/elkaar-helpen/",
            location)
        self.add_source(MijnBuurtjeSource(cfg))

    def get_logger(self) -> logging.Logger:
        return logging.getLogger("platformen.mijnbuurtje")

    def supports_group(self, group):
        return True
