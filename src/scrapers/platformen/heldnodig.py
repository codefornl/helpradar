import requests
import json

from bs4 import BeautifulSoup
from .database import Initiative, Db


class HeldNodig:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://heldnodig.nl/'

    def scrape(self):
        db = Db()
        page = requests.get(self.URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='container')

        questions = results.find_all(class_='card')
        for card in questions:
            title = card.find('h5').text.strip(' \t\n\r')
            rawlocation = card.find('h6').text.strip(' \t\n\r')
            # remove (maps) from rawlocation, split on first space
            rawlocation = rawlocation.strip('(Maps)')

            description = card.find(
                'p', class_='card-text').text.strip(' \t\n\r')

            db.session.add(Initiative(category=title,
                                      description=description,
                                      group="demand",
                                      source=self.URL,
                                      location=rawlocation,
                                      )
                           )

        db.session.commit()
