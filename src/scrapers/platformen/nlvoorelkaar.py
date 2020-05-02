import requests
import json
import datetime

from bs4 import BeautifulSoup
from models.database import Db
from models.initiatives import InitiativeBase, Platform, ImportBatch, InitiativeImport, BatchImportState, InitiativeGroup


class InitiativeGroupConfig(object):

    def __init__(self, group, url, fieldmap):
        self.group = group
        self.url = url
        self.fieldmap = fieldmap

    def get_marker_url(self, id):
        markerurlsegment = 'hulpaanbod' if self.group == InitiativeGroup.SUPPLY else 'hulpvragen'
        return 'https://www.nlvoorelkaar.nl/%s/%s' % (markerurlsegment, id)

class NLvoorElkaar:
    """NL Voor Elkaar scraper die zowel vraag als aanbod ophaalt"""

    def __init__(self):
        # Category 45 is the one for Corona
        self.configs = {
            InitiativeGroup.SUPPLY: InitiativeGroupConfig(
                InitiativeGroup.SUPPLY,
                'https://www.nlvoorelkaar.nl/hulpaanbod/update/resultmarkers.json?page=&sectors[]=2&categories[]=45',
                {
                    "titel": "name",
                    "plaats": "location",
                    "categorie": "category",
                    "aangeboden door": "organisation_kind",
                })
            ,
            InitiativeGroup.DEMAND: InitiativeGroupConfig(
                InitiativeGroup.DEMAND,
                'https://www.nlvoorelkaar.nl/hulpvragen/update/resultmarkers.json?categories[]=45',
                {
                    "plaats": "location",
                    "categorie": "category",
                    "beschikbaarheid": "frequency",
                })
            }

    def scrape(self):
        self.db = Db()
        platform = self.load_platform()
        # create batch
        batch = ImportBatch.start_new(platform)
        self.db.session.add(batch)
        self.db.session.commit()

        try:
            # run supply scraper
            self.scrapegroup(self.configs[InitiativeGroup.SUPPLY], batch)
            # run demand scraper
            self.scrapegroup(self.configs[InitiativeGroup.DEMAND], batch)
        except Exception as e:
            batch.state = BatchImportState.FAILED
            print("Error while scraping: " + e.args[0])
            # TODO: Should do logging here
        else:
            batch.state = BatchImportState.IMPORTED


        batch.stopped_at = datetime.datetime.now(datetime.timezone.utc)

        self.db.session.commit()


    def scrapegroup(self, config: InitiativeGroupConfig, batch: ImportBatch):
        print('scraping ' + config.group)
        page = requests.get(config.url)
        # TODO: Handle http error codes
        result = page.json()
        parsed_markers = []

        for marker in result['markers']:
            if marker['id'] not in parsed_markers:
                # TODO: Error handling and possibly a retry
                parsed_markers.append(marker['id'])
                markerurl = config.get_marker_url(marker['id'])
                print('scraping ' + markerurl)
                try:
                    detail = requests.get(markerurl)
                    # TODO: Handle http error codes
                    soup = BeautifulSoup(detail.content, 'html.parser')

                    table = soup.find("dl")
                    records = table.findAll(["dd", "dt"])
                    description = soup.find("p").text.strip('\t\n\r')

                    initiative = InitiativeImport(description=description,
                                                group=config.group,
                                                source=markerurl,
                                                source_id=marker['id'])

                    setcount = 0
                    for i in range(0, len(records), 2):
                        #TODO: Error prevention
                        label = records[i].contents[1].strip("\":").lower()
                        if label in config.fieldmap:
                            setattr(initiative, config.fieldmap[label], records[i+1].contents[0])
                            setcount += 1

                    if(config.group == InitiativeGroup.DEMAND):
                        title = soup.find("h2", "result__title");
                        name = title.contents[0]

                    # TODO: Logging is no values are assigned
                except Exception as e:
                    print('error scraping ' + markerurl + ':' + e.args[0])
                    if initiative != None:
                        initiative.state = "processing_error"
                
                if initiative != None:
                    batch.initiatives.append(initiative)

                # debugging
                #if len(parsed_markers) >= 10:
                #    break

        self.db.session.commit()

    def load_platform(self):
        """ retrieve platform instance or create it """
        platform = self.db.session.query(Platform).filter(Platform.url.like('%www.nlvoorelkaar.nl%')).first()
        
        if(platform == None):
            platform = Platform(name='NL Voor Elkaar',
                description='In moeilijke tijden is het belangrijk om elkaar kracht te geven. Om te laten zien dat we samen, zelfs als we afstand moeten houden, sterker zijn dan welke crisis ook.',
                url='https://www.nlvoorelkaar.nl',
                place='Nederland')
            self.db.session.add(platform)

        return platform

