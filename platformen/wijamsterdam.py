import requests
import json

from bs4 import BeautifulSoup
from .database import Initiative, Db


class WijAmsterdam:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://wijamsterdam.nl/initiatieven'

    def scrape(self):
        db = Db()
        page = requests.get(self.URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='ideas-list')

        questions = results.find_all(class_='idea-item')
        for card in questions:
            title = card.find('h3').text.strip(' \t\n\r')
            rawlocation = card.find(class_='gebied').text.strip(' \t\n\r')
            description = card.find(
                'p').text.strip(' \t\n\r')
            link = card.find('a')['href']
<<<<<<< HEAD
            db.session.add(Initiative(name=title,
=======
            db.session.add(Initiative(category=title,
>>>>>>> 7d80ae4... Now merging various sites into a sqlite db
                                      description=description,
                                      group="unknown",
                                      source='https://wijamsterdam.nl' + link,
                                      source_id=link.strip('/initiatief/'),
                                      location=rawlocation,
                                      )
                           )

        db.session.commit()
