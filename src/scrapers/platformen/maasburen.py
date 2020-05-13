"""
Created on Thu May  7 21:09:55 2020

@author: J.S. Kroodsma
"""

import re
from .TreeParser import TreeParser  # class for scraping static website
from .helpers import format_group, format_organizer

# Step 1: 
url = 'https://maasburen.nl/elkaar-helpen?theme%5B%5D=836&format=fragment&page='

outputs = []
counter = 1
while counter < 100:
    url0 = url + str(counter)
    # schemas: defines fields to be scraped
    # schema: fieldname:{xpath,all,cast,transform}
    schemas = {'initiatives':
                   {'xpath': '//a[@href]',
                    'all': True,
                    'transform': lambda elements: [e.attrib['href'] for e in elements if len(re.findall('https://maasburen.nl/elkaar-helpen/\\d{4,5}', e.attrib['href'])) > 0]}}
    # initialize TreeParser using url and schemas, returns html tree
    TreeParser0 = TreeParser(url0, None, schemas)
    if TreeParser0.tree is None:
        break
    output = TreeParser0.apply_schemas()
    outputs.append(output)
    counter = counter + 1

# accumulate initiatives
initiative_urls = []
for o in outputs:
    initiative_urls = initiative_urls + o['initiatives']

# step 2
schemas = {'name': {'xpath': '//title'},
           'orig_group': {'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()'},
           'group': {'xpath': '//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()', 'transform': format_group},
           'description': {'xpath': '//*[@class="content-section"]/p', 'all': True, 'transform': lambda elements: '\n'.join([e.text for e in elements if e.text is not None])},
           'organizer': {'xpath': '//a[@class="entity" and contains(@href, "deelnemers")]/@href', 'transform': format_organizer},
           'theme': {'xpath': '//span[@class="meta-item-content" and contains(text(),"Thema:")]'},
           'village': {'xpath': '//span[@class="meta-item-content" and contains(text(),"Dorp: ")]/text()', 'transform': lambda element_text: re.sub('Dorp: ', '', element_text)}}
ppScraper = TreeParser(None, None, schemas)
records = []
for url in initiative_urls[:50]:
    session_metadata = ppScraper.get_session_metadata(url)
    output = ppScraper.apply_schemas(metadata=session_metadata, url=url)
    records.append(output)
