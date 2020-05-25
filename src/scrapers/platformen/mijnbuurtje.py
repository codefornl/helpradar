import re
from datetime import date
from typing import Generator

from models import InitiativeImport
from platformen import Scraper
from platformen.TreeParser import TreeParser
from platformen.scraper import PlatformSource, PlatformSourceConfig, ScrapeException


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
    ITEM_SCHEMA = {'name': {'xpath': '//title'},
                   # 'orig_group': {
                   #     'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()'},
                   'group': {
                       'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()',
                       'transform': lambda text: MijnBuurtjeSource.format_group(text)},
                   'description': {'xpath': '//*[@class="content-section"]/p', 'all': True,
                                   'transform': lambda elements: '\n'.join(
                                       [e.text for e in elements if e.text is not None])},
                   'organiser': {'xpath': '//a[@class="entity" and contains(@href, "deelnemers")]/@href',
                                 'transform': lambda text: MijnBuurtjeSource.format_organizer(text)},
                   # 'organiser_kind': {'xpath': '//span[@class="meta-item-content" and contains(text(),"Vraag vanuit:")]',
                   #               'transform': lambda text: text.replace("Vraag vanuit: ", "")},
                   'category': {'xpath': '//span[@class="meta-item-content" and contains(text(),"Thema:")]'},
                   'created_at': {'xpath': '//div[@class="heading3 heading3--semibold"]/text()',
                                  'transform': lambda text: MijnBuurtjeSource.format_date(text)}}

    def __init__(self, config: MijnBuurtjeSourceConfig):
        super().__init__(config)
        self.item_parser = TreeParser(None, None, self.ITEM_SCHEMA)

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        page_counter = 1
        try:
            while page_counter < 100:
                list_page_url = self.config.list_endpoint + f"&page={page_counter}"
                # schemas: defines fields to be scraped
                # schema: fieldname:{xpath,all,cast,transform}
                schemas = {'initiatives':
                               {'xpath': '//a[@href and @class="postpreview-content"]',
                                'all': True,
                                'transform': lambda elements: [e.attrib['href'] for e in elements if len(
                                    re.findall(self.config.details_endpoint + "\\d{4,5}", e.attrib['href'])) > 0]}}

                # initialize TreeParser using url and schemas, returns html tree
                initiative_parser = TreeParser(list_page_url, None, schemas)
                if initiative_parser.tree is None:
                    break

                output = initiative_parser.apply_schemas()
                for o in output['initiatives']:
                    yield InitiativeImport(source_uri=o)

                page_counter = page_counter + 1
        except Exception as ex:
            raise ScrapeException("Error loading list of initiatives") from ex

    def complete(self, initiative: InitiativeImport):
        session_metadata = self.item_parser.get_session_metadata(initiative.source_uri)
        full_initiative = self.item_parser.apply_schemas(metadata=session_metadata,
                                                         url=initiative.source_uri)
        for key, value in full_initiative.items():
            setattr(initiative, key, value)
        initiative.location = self.config.location

    @staticmethod
    def format_group(original_group: str):
        if len(re.findall("Hulpvraag.*?", original_group)) > 0:
            return 'demand'
        else:
            return 'supply'

    @staticmethod
    def format_organizer(organizer: str):
        if organizer is not None:
            list0 = organizer.split('/')
            organizer_name = None if len(list0) == 0 else list0[len(list0) - 1]
            # get the first name of the organizer:
            if organizer_name is not None:
                organizer_name = re.sub('-', ' ', organizer_name)
                organizer_name = organizer_name.split(' ')[0]
            else:
                organizer_name = None
            return organizer_name

    # I assume there's a better way using locales
    MONTHS = ["januari", "februari", "maart", "april", "mei", "juni", "juli",
              "augustus", "september", "oktober", "november", "december"]

    @staticmethod
    def format_date(date_str: str):
        # TODO: This is an important field. Should break here!
        if not date_str:
            return None

        segments = date_str.split()
        if len(segments) != 3:
            msg = f"Expecting a 3 segment date, got {date_str}"
            raise ValueError(msg)

        month = MijnBuurtjeSource.MONTHS.index(segments[1].lower()) + 1
        d = date(int(segments[2]), month, int(segments[0]))
        return d


class MijnBuurtje(Scraper):
    pass


class MijnBuurtjes(Scraper):
    pass
    """
    Scraped alle bekende instanties van mijn buurtje
    """
