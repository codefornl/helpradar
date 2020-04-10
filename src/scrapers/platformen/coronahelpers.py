# coding=utf8
import requests
import json
from .database import Initiative, Db

class CoronaHelpers:
    """A simple example class"""

    def __init__(self):
        self.URL = 'https://www.coronahelpers.nl/o/Corona-Helden/activiteiten/'

    def scrape(self):
        db = Db()

        # read data
        counter = 1
        while counter > 0:
            grab_url='https://www.coronahelpers.nl/api/deeds?query=&page=' + str(counter) + 'causes=&activities=&date=&pageSize=18&withOrganization=true'
            s = requests.session()
            response = s.get(grab_url,
            headers={
                'x-requested-with': 'XMLHttpRequest',
                'Accept':'application/json, text/plain, */*',
                'Accept-Language':'nl',
                'DNT':'1',
                'Pragma':'no-cache',
                'TE':'Trailers',
                'Host':'www.coronahelpers.nl',
                'Referer':'https://www.coronahelpers.nl/vrijwilligerswerk/activiteiten?page='+str(counter),
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
            result = json.loads(response.content)
            questions = result['data']['results']
            if counter < 46:
                print(counter)
                print(len(questions))
                counter += 1
                for card in questions:
                    if card['postcode'] is not None and card['city'] is not None:
                        location=card['postcode'] + ' ' + card['city']
                    elif card['postcode'] is not None:
                        location=card['postcode']
                    elif card['city'] is not None:
                        location=card['city']
                    else:
                        location=None
                    db.session.add(Initiative(name=card['organization']['name'],
                                            category=card['type'],
                                            description=card['summary'],
                                            group="demand",
                                            source=self.URL + str(card['id']),
                                            source_id=str(card['id']),
                                            location=location,
                                            frequency=card['subtype'],
                                            )
                                )
            else:
                counter = -1

        db.session.commit()
