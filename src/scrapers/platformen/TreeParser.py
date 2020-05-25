"""
Created on Sun Apr 19 11:27:06 2020

@author: J.S. Kroodsma
"""
import datetime as dt  # core modules
import logging
import os
import re
import requests

from lxml import etree


class TreeParser:
    """
    #class variables: same for all instances of class 
    
    variable naming:
    html_element: a single HTMLELement instance or a list of HTMLElement instances 
    element_transform_function: python function that transforms html_element to python string, numeric or list value
    tree: root html element of the website
    schema: dictionary for extracting a field from tree
    schemas: a dictionary of schemas
    ky: a key in schemas
    
    constants:
    LOG_FILE_NAME
    LOG_FILE_PATH: environ variable LOG_FILE_PATH or current directory at initialization
    
    """
    LOG_FILE_NAME = 'log_tree_parser.log'

    """initialization"""

    def __init__(self, url=None, tree=None, schemas=None, raise_error=True):

        # placeholders
        self.html = None
        self.url = url
        self.tree = tree
        self.schemas = schemas
        self.RAISE_ERROR = raise_error  # throws exception if true, logs exception if false

        # initialize logger, write logs to datestamped LOG_FILE_NAME
        self.LOG_FILE_PATH = nvl(os.getenv('LOG_FILE_PATH'), os.getcwd())
        datestr = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d')
        log_file_name = datestr + '_' + self.LOG_FILE_NAME
        logging.basicConfig(filename=self.LOG_FILE_PATH + '/' + log_file_name, level=logging.DEBUG)

        # GET website html        
        if url is None and tree is None and schemas is None:
            raise ValueError('no url and tree set')
        elif url is not None and tree is None:
            self.tree = self.__get_html_tree__(url)

    """property setters"""

    """class functions"""

    def __get_html_tree__(self, url):
        # body
        tree = None
        res = requests.get(url)
        if res.status_code <= 299:  # error handling
            self.url = url
            self.html = res.text
            # parse html
            tree = etree.HTML(self.html)
        else:
            error_msg = 'GET on {0} gives status_code {1}'.format(url, res.status_code)
            if self.RAISE_ERROR:
                raise ValueError(error_msg)
            else:
                logging.error(error_msg)
        return tree

    @staticmethod
    def __serialize__(html_element):
        """ serialize element to value """
        # body
        if type(html_element) in [etree._ElementUnicodeResult]:
            v = str(html_element)
        elif hasattr(html_element, 'text'):
            v = html_element.text
        else:
            # v=str(x)
            v = html_element
        return v

    def __transform_html_element_to_value__(self, html_element, element_transform_function=None):
        """ transform html_element(s) to python data type """
        # transform element
        if element_transform_function is not None:
            error_msg = 'element_transform_function is not callable {0}'.format(element_transform_function)
            if not callable(element_transform_function):
                if self.RAISE_ERROR:
                    raise NotFunctionError(error_msg)
                else:
                    logging.error(error_msg)
                v = None
            else:
                v = element_transform_function(html_element)
        else:
            v = html_element
        return v

    def get_session_metadata(self, url=None):
        """ utility returing scraping session metadata """
        url = nvl(url, self.url)
        source_url = re.findall('https:\/\/([A-Z,a-z,0-9,\-\.]+)\/', str(url))
        source_url = source_url[0] if len(source_url) > 0 else None
        metadata = {'source': source_url,
                    'source_uri': url,
                    'scraped_at': str(dt.datetime.now())}
        return metadata

    def set_schema(self, schemas):
        self.schemas = schemas
        return self

    def apply(self, schema=None, ky=None, t=None):
        """ apply a single schema to the html tree. returns dictionary {value,elements,element} """
        try:
            # body
            # get the schema
            schema = self.schemas[ky] if ky is not None else schema
            # unpack variables from schema
            xpath, all_elements, cast, element_transform_function = from_kwargs(schema, 'xpath', 'all', 'cast', 'transform')
            transform = nvl(t, element_transform_function)
            # prep outputs
            elements = []
            outputs = {'value': None, 'elements': elements, 'element': None}
            # execute xpath 
            if len(xpath) > 0:
                try:
                    elements = self.tree.xpath(xpath)
                except Exception as e:
                    error_msg = "apply failed to parse field {0} using xpath {1}. error: {2}".format(ky, xpath, e)
                    if self.RAISE_ERROR:
                        raise HtmlParseError(error_msg)
                    else:
                        logging.error(error_msg)
                # get first element
                element = elements[0] if len(elements) > 0 else None
                # transform + serialize
                if all_elements == True:  # use the first result element
                    value_input = elements
                else:
                    value_input = element
                value = self.__serialize__(
                    self.__transform_html_element_to_value__(value_input, transform))  # use all elements
                # set as attributesL elements,element
                self.elements = elements
                self.element = element
                outputs = {'value': value, 'elements': elements, 'element': element}
            self.outputs = outputs
        except Exception as e:
            print('error in apply')
            raise e
        # return value
        return self.outputs

    def apply_schemas(self, metadata={}, url=None):
        """ apply all schemas to html tree and return map name:value """
        try:
            # body
            if url is not None:
                self.tree = self.__get_html_tree__(url)
            if metadata == {}:
                metadata = self.get_session_metadata(url=url)
            map0 = {k: self.apply(ky=k).get('value') for k in self.schemas}
            [map0.update({k: metadata[k]}) for k in metadata]
            logging.info('SUCCESS: retrieved {0} fields from {1}'.format(len(map0.keys()), self.url))
        except Exception as e:
            print('error in apply_schemas')
            raise e
        # return value
        return map0

    def scrape_page(self, url):
        # body
        return self.apply_schemas(url=url)


# helpers
def nvl(x, default=''):
    return default if x is None else x


def from_kwargs(kwargs, *args):
    """ unpack key-values from kwargs into args variables """
    try:
        # body
        kw = tuple([kwargs.get(arg) for arg in args])
    except Exception as e:
        print('error in from_kwargs')
        raise e
    # return value
    return kw


# custom error classes
class NotFunctionError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors


class HtmlParseError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
