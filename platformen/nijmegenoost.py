import requests
import json

from bs4 import BeautifulSoup
from .database import Initiative, Db


class NijmegenOost:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://nijmegen-oost.nl/elkaar-helpen?type%5B%5D=OFFERED&page='

    def scrape(self):
        db = Db()
        counter = 1
        while counter > 0:
            # print(self.URL + str(counter))
            page = requests.get(self.URL + str(counter))
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all(class_='postpreview')

            if len(results) > 0:
                counter += 1
                for card in results:
                    try:
                        title = card.find(
                            class_='heading3 heading3--semibold').text.strip(' \t\n\r')
                        name = card.find(
                            class_='entity-content-title').text
                        description = card.find(
                            class_='paragraph').text.strip(' \t\n\r')
                        rawtheme = card.find(
                            class_='postpreview-subtitle').text
                        final_link = None
                        source_id = None
                        link = card.find(class_='postpreview-content')
                        final_link = link['href']
                        source_id = final_link.split('/')[-2]

                        db.session.add(Initiative(name=name + " - " + title,
                                                  description=description,
                                                  group=rawtheme,
                                                  source=final_link,
                                                  source_id=source_id,
                                                  )
                                       )
                    except:
                        print(card)
                        pass
            else:
                counter = -1

        db.session.commit()
