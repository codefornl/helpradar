import logging
import sys
from collections import namedtuple
from typing import Generator

import requests
import json

from dateutil import parser

from models.initiatives import InitiativeImport, InitiativeGroup
from .scraper import Scraper, PlatformSource, PlatformSourceConfig, ScrapeException


class WijAmsterdamSource(PlatformSource):
    """
    Very trivial source. Reads all ideas from Wij Amsterdam open api
    and returns them immediately
    """

    def __init__(self):
        super().__init__(PlatformSourceConfig(
            "https://www.wijamsterdam.nl",
            "https://api2.openstad.amsterdam/api/site/197/idea",
            None
        ))

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        response = self.get(self.config.list_endpoint)

        try:
            data = json.loads(
                response.content,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

            for item in data:
                initiative = self.map_initiative(response, item)
                yield initiative
        except Exception as ex:
            msg = f"Error reading contents from {self.config.list_endpoint}"
            raise ScrapeException(msg) from ex

    @staticmethod
    def map_initiative(response, item):
        initiative = InitiativeImport(
            source_id=item.id,
            source_uri=f"https://wijamsterdam.nl/initiatief/{item.id}",
            # using dateutil and not datetime because: https://stackoverflow.com/a/3908349/167131
            created_at=parser.parse(item.createdAt),
            name=item.title,
            description=f"{item.summary}"
                        f"\n--------\n"
                        f"{item.description}",
            group=InitiativeGroup.SUPPLY,
            extra_fields=response.content.decode("utf-8")
            # Probably better to leave email / phone empty
            # name is already tricky maybe albeit open data.
        )

        if hasattr(item.extraData, "area"):
            initiative.location = item.extraData.area
        if hasattr(item.extraData, "isOrganiserName"):
            initiative.organiser = item.extraData.isOrganiserName
        if hasattr(item.extraData, "theme"):
            initiative.category = item.extraData.theme
        if hasattr(item.extraData, "isOrganiserWebsite"):
            initiative.url = item.extraData.isOrganiserWebsite
        if hasattr(item, "position"):
            initiative.latitude = item.position.lat
            initiative.longitude = item.position.lng

        return initiative

    def complete(self, initiative: InitiativeImport):
        pass


class WijAmsterdam(Scraper):

    def __init__(self):
        source = WijAmsterdamSource()
        super().__init__(
            source.config.platform_url,
            "Wij Amsterdam",
            "wams",
            [source])

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
