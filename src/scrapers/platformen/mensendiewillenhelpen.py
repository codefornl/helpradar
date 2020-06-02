import json

import requests

from models import InitiativeImport, Db


class MensenDieWillenHelpen:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://www.gewoonmensendiemensenwillenhelpen.nl/ik-wil-helpen'

    @staticmethod
    def scrape():
        db = Db()

        # read data
        response = requests.get(
            'https://api-server-271218.appspot.com/v1/tasks?zipcode=')
        result = json.loads(response.content)
        # print(result)

        questions = result['data']['tasks']
        for card in questions:
            db.session.add(
                InitiativeImport(
                    name=card['firstName'],
                    category=card['TaskType']['name'],
                    description=card['description'],
                    group="demand",
                    source='https://www.gewoonmensendiemensenwillenhelpen.nl/ik-wil-helpen',
                    source_id=card['id'],
                    location=card['zipcode'] + ' ' + card['city'],
                    frequency=card['when'],
                )
            )

        db.session.commit()
