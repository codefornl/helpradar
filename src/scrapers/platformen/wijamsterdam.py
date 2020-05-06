import requests
import json

from bs4 import BeautifulSoup
from models.initiatives import InitiativeImport
from .scraper import Scraper


class WijAmsterdam(Scraper):
    """A simple example class"""

    def __init__(self):
        super().__init__("www.wijamsterdam.nl", "Wij Amsterdam", "wijams")
        self.URL = 'https://wijamsterdam.nl/initiatieven'

    def scrape(self):
        super().scrape()
        page = requests.get(self.URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='ideas-list')

        questions = results.find_all(class_='idea-item')
        count = 0
        for card in questions:
            title = card.find('h3').text.strip(' \t\n\r')
            rawlocation = card.find(class_='gebied').text.strip(' \t\n\r')
            description = card.find(
                'p').text.strip(' \t\n\r')
            link = card.find('a')['href']
            self._db.session.add(InitiativeImport(name=title,
                                      description=description,
                                      group="unknown",
                                      source='https://wijamsterdam.nl' + link,
                                      source_id=link.strip('/initiatief/'),
                                      location=rawlocation,
                                      )
                           )
            count += 1
            if not self.should_continue(count):
                break

        self._db.session.commit()
