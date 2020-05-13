"""
Created on Mon May  4 16:28:05 2020

@author: jskro
"""
from .TreeParser import TreeParser # class for scraping static website
from .helpers import format_group, format_organizer

# Step 1: 
url='https://nijmegen-oost.nl/elkaar-helpen?type%5B%5D=OFFERED&page='

outputs=[]
counter=1
while counter<100:
    url0='https://nijmegen-oost.nl/elkaar-helpen?theme%5B%5D=836&type%5B%5D=REQUESTED&type%5B%5D=OFFERED&page='+str(counter)
    # schemas: defines fields to be scraped
    # schema: fieldname:{xpath,all,cast,transform}
    schemas={'initiatives':
            {'xpath':'//a[@href and @class="postpreview-content"]',
             'all':True,
             'transform':lambda elements: [e.attrib['href'] for e in elements  ]}}
    # initialize TreeParser using url and schemas, returns html tree
    TreeParser0=TreeParser(url0,None,schemas)  
    if TreeParser0.tree==None:
        break
    output=TreeParser0.apply_schemas()
    outputs.append(output)
    counter=counter+1

#accumulate initiatives
initiative_urls=[]
for o in outputs:
    initiative_urls=initiative_urls+o['initiatives']
    
# step 2: scrape initiative page 
schemas={'name':{'xpath':'//title'},
         'orig_group':{'xpath':'//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()'},
         'group':{'xpath':'//span[@class="mb-help-request meta-item-icon"]/following-sibling::span[1]/text()','transform':format_group},
         'description':{'xpath':'//*[@class="content-section"]/p','all':True,'transform': lambda elements: '\n'.join([e.text for e in elements if e.text != None])},
         'organizer':{'xpath':'//a[@class="entity" and contains(@href, "deelnemers")]/@href','transform':format_organizer},
         'theme':{'xpath':'//span[@class="meta-item-content" and contains(text(),"Thema:")]'}}
ppScraper=TreeParser(None,None,schemas)
records=[]
for url in initiative_urls[:50]:
    session_metadata=ppScraper.get_session_metadata(url)
    output=ppScraper.apply_schemas(metadata=session_metadata,url=url)
    records.append(output)   
