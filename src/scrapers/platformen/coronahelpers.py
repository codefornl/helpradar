import json
import logging
import requests
from time import sleep

from models.database import Db
from models.initiatives import InitiativeImport
from .scraper import Scraper


class WebScraper(Scraper):
    """ General scraper class """

    def __init__(self, platform_url: str, name: str, code: str):
        super().__init__(platform_url, name, code)
        self.domain = platform_url

        self.HTTPRequestHeaders = {}
        self.HTTPGetParameters = {}

        self.databaseHandler = Db()

    def scrape(self):
        return "Not implemented"

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def get_base_url(self):
        return "https://%s" % self.domain

    def get_http_response(self, input_url):
        logging.debug("Retrieving URL: %s" % input_url)

        return requests.get(input_url, params=self.HTTPGetParameters, headers=self.HTTPRequestHeaders)

    def get_http_response_content(self, input_url):
        http_response = self.get_http_response(input_url)
        return http_response.content

    def get_http_response_json(self, input_url):
        http_content = self.get_http_response_content(input_url)
        return json.loads(http_content)

    @staticmethod
    def sleep_for_thottling():
        sleep(0.1)

    def add_initiative_to_database(self, initiative):
        self.databaseHandler.session.add(initiative)
        self.databaseHandler.session.commit()


class CoronaHelpersScraper(WebScraper):
    def __init__(self):
        super().__init__("www.coronahelpers.nl", "Corona Helpers", "cohe")

        self.APIDeedsEndpoint = 'api/deeds'
        self.HTTPRequestHeaders = {
            'x-requested-with': 'XMLHttpRequest',
        }
        self.maxPageSize = 50
        self.pageStartCount = 1

    def check_connection_to_server(self):
        logging.debug("Checking connection to server")

        http_content_json = self.query_deeds_page_from_api(current_page=1, page_size=1)
        query_status = self.get_status_from_json(http_content_json)

        return int(query_status) == 200

    def query_deeds_page_from_api(self, current_page, page_size=50):
        logging.debug("Requesting page %s with page size %s" % (current_page, page_size))

        if page_size > self.maxPageSize:
            page_size = self.maxPageSize

        self.HTTPParameters = self.get_http_parameters_for_page_query(current_page, page_size)

        api_deeds_url = self.get_api_deeds_url()
        http_content_json = self.get_http_response_json(api_deeds_url)

        return http_content_json

    def query_deed_details_from_api(self, deed_id):
        logging.debug("Retrieving details for deed ID %s" % deed_id)

        self.HTTPGetParameters = {}

        api_deed_details_url = self.get_api_deed_details_url(deed_id)
        http_content_json = self.get_http_response_json(api_deed_details_url)
        deed_details = self.get_deed_details_from_json(http_content_json)

        return deed_details

    def get_page_count_from_api(self):
        logging.debug("Retrieving page count")

        http_content_json = self.query_deeds_page_from_api(self.pageStartCount)
        page_count = self.get_page_count_from_page_json(http_content_json)

        return page_count

    def query_deeds_page_json_from_api(self, current_page, page_size=50):

        http_content_json = self.query_deeds_page_from_api(current_page, page_size)
        deeds_query_results = self.get_deeds_from_page_json(http_content_json)

        return deeds_query_results

    def get_api_deeds_url(self):
        return "%s/%s" % (self.get_base_url(), self.APIDeedsEndpoint)

    def get_api_deed_details_url(self, deed_id):
        return "%s/%s" % (self.get_api_deeds_url(), deed_id)

    @staticmethod
    def get_data_from_json(input_json):
        return input_json["data"]

    @staticmethod
    def get_status_from_json(input_json):
        return input_json["status"]

    def get_deed_details_from_json(self, input_json):
        data = self.get_data_from_json(input_json)
        return data["deed"]

    def get_deeds_from_page_json(self, input_json):
        data = self.get_data_from_json(input_json)
        return data["results"]

    @staticmethod
    def get_deed_id_from_json(input_json):
        return input_json["id"]

    def get_page_count_from_page_json(self, input_json):
        data = self.get_data_from_json(input_json)
        pagination = data["pagination"]

        return pagination["pageCount"]

    @staticmethod
    def get_coordinates_from_deed_details(deed_details):

        parsed_coordinates = {"lat": None, "lng": None}

        coordinates = deed_details["coordinates"]
        if coordinates is not None:
            parsed_coordinates["lat"] = coordinates["lat"]
            parsed_coordinates["lng"] = coordinates["lng"]

        return parsed_coordinates

    @staticmethod
    def get_http_parameters_for_page_query(current_page, page_size):

        http_parameters = {
            'query': '',
            'page': str(current_page),
            'causes': '',
            'activities': '',
            'date': '',
            'pageSize': str(page_size),
            'withOrganization': 'true'}

        return http_parameters

    def scrape(self):
        logging.info("Starting CoronaHelpersScraper scraping")

        if not self.check_connection_to_server():
            logging.error("Can't connect to CoronaHelpers server API")
            return

        number_of_pages = self.get_page_count_from_api()

        for currentPage in range(number_of_pages):
            deeds_json = self.query_deeds_page_json_from_api(currentPage)
            self.sleep_for_thottling()

            for deedJSON in deeds_json:
                self.process_deed(deedJSON)
                self.sleep_for_thottling()

    def process_deed(self, deed_json):
        logging.info("Processing deed")

        deed_id = self.get_deed_id_from_json(deed_json)
        deed_details = self.query_deed_details_from_api(deed_id)
        initiative = self.create_initiative_from_deed_details(deed_details)
        self.add_initiative_to_database(initiative)

    def create_initiative_from_deed_details(self, deed_details):
        logging.info("Creating initiative from deed details")

        deed_id = self.get_deed_id_from_json(deed_details)
        coordinates = self.get_coordinates_from_deed_details(deed_details)

        initiative = InitiativeImport(
            category=deed_details["fullType"],
            group="supply",
            description=deed_details["summary"],
            # name = deedDetails[""],
            source=self.get_api_deed_details_url(deed_id),
            # frequency = deedDetails["subtype"],
            location=deed_details["address"],
            latitude=coordinates["lat"],
            longitude=coordinates["lng"]
        )

        return initiative
