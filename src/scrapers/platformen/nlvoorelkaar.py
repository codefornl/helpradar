import requests
import json

from bs4 import BeautifulSoup
from .database import Initiative, Db


class NLvoorElkaar:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://www.nlvoorelkaar.nl/hulpvragen/update/resultmarkers.json?categories[]=45'

    def scrape(self):
        db = Db()
        # Category 45 is the one for Corona
        page = requests.get(self.URL)
        result = page.json()
        parsed_markers = []
        for marker in result['markers']:
            if marker['id'] not in parsed_markers:
                parsed_markers.append(marker['id'])
                markerurl = 'https://www.nlvoorelkaar.nl/hulpvragen/%s' % marker['id']
                detail = requests.get(markerurl)
                soup = BeautifulSoup(detail.content, 'html.parser')
                table = soup.find("dl")
                records = table.findAll("dd")
                description = soup.find("p").text.strip(' \t\n\r')

                db.session.add(Initiative(category=records[1].text,
                                          description=description,
                                          group="demand",
                                          source=markerurl,
                                          source_id=marker['id'],
                                          frequency=records[2].text,
                                          location=records[0].text,
                                          )
                               )

        db.session.commit()
