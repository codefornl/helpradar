"""
Created on Mon Apr 20 14:11:31 2020

@author: jskro
"""
import datetime as dt
import re

from .TreeParser import TreeParser  # class for scraping static website
from models import InitiativeImport, Db

# initialize Db
db = Db()

"""
    steps
    1. get all initiativen from wijamsterdam.nl
    2. scrape each initiatief, collect in records
    3. insert records into db table 
"""
# Step 1
# get all "initiatieven" urls from wijamsterdam
# SCRAPER is defined by: url, schemas, metadata
url = 'https://wijamsterdam.nl/initiatieven'
# schemas: defines fields to be scraped
# schema: fieldname:{xpath,all,cast,transform}
schemas = {'initiatives':
               {'xpath': '//*[@class="tile-list ideas-list"]/div/a[@href]',
                'all': True,
                'transform': lambda elements: [e.attrib.values() for e in elements]}}
# metadata: 
metadata = {'source_url': re.findall('https:\/\/([A-Z,a-z,0-9,\.]+)\/', url)[0],
            'source_uri': url,
            'scraped_at': str(dt.datetime.now()),
            'created_at': dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d')}
# initialize TreeParser using url and schemas, returns html tree
TreeParser0 = TreeParser(url, None, schemas)
# Parse html tree, optionally add metadata dictionary
output = TreeParser0.apply_schemas(metadata)
initiatief_urls = ['https://wijamsterdam.nl' + i[0] for i in output['initiatives']]

# Step 2
# scrape initiatief-page
schemas = {'name': {'xpath': '//h1'},
           'description': {'xpath': '//div[@style]/div[string-length(text()) >= 0]/text()', 'all': True, 'transform': str},
           'categories': {'xpath': '//span[contains(text(),"Categorie:")]/../text()', 'cast': str},
           'organiser': {'xpath': '//p[@class="initiative-owner-details initiative-owner-name"]'},
           'adres': {'xpath': '//span[contains(text(),"Gebied:")]/../text()', 'cast': str},
           'url': {'xpath': '//p[@class="initiative-owner-details initiative-owner-website"]/a'},
           'phone': {'xpath': '//p[@class="initiative-owner-details initiative-owner-phone"]/a'},
           'group': {'xpath': ''},
           'notes': {'xpath': ''}
           }
# description (xpath) returns multiple elements, define clean_description and set in schemas.description.transform
clean_description = lambda x: ''.join([re.sub('\n|\n  |\n    |\s{2,}', '', e) for e in x])
schemas['description']['transform'] = clean_description

records = []  # store scraper output in records
c = 1
MAX_URLS = 10
for url in initiatief_urls:
    metadata = {'source_url': re.findall('https:\/\/([A-Z,a-z,0-9,\.]+)\/', url)[0],
                'source_uri': url,
                'scraped_at': str(dt.datetime.now()),
                'created_at': dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d')}
    TreeParser0 = TreeParser(url, None, schemas)
    output = TreeParser0.apply_schemas(metadata)
    records.append(output)
    if c > MAX_URLS:  # scraping all 300+ initiatives took a bit long
        break
    c = c + 1

# Step 3 insert into db
for r in records:
    # TODO: determine which fields are inserted into DB
    db.session.add(InitiativeImport())
