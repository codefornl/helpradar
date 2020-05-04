"""
Created on Sat Apr 25 19:00:30 2020

@author: J.S. Kroodsma

defines scrapers for /hulpradar
usage: instantiate scraper, call .scrape_page(url) method

base class is TreeParser, scraper subclasses. schemas to use is defined in the class definition
# ppScraper: https://puurpapendrecht.nl
"""
from .TreeParser import TreeParser


class ppScraper(TreeParser):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""

    def __init__(self):
        """ fields to extract from https://puurpapendrecht.nl """
        schemas = {'description': {'xpath': '//*[@class="content-section"]/p', 'all': True,
                                   'transform': lambda elements: '\n'.join(
                                       [e.text for e in elements if e.text is not None])}
                   }
        super().__init__(schemas=schemas)
