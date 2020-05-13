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

    def getBaseURL(self):
        return "https://%s" % self.domain

    def getHTTPResponse(self, URL):
        logging.debug("Retrieving URL: %s" % URL)

        return requests.get(URL, params=self.HTTPGetParameters, headers=self.HTTPRequestHeaders)

    def getHTTPResponseContent(self, URL):
        HTTPResponse = self.getHTTPResponse(URL)
        return HTTPResponse.content

    def getHTTPResponseJSON(self, URL):
        HTTPContent = self.getHTTPResponseContent(URL)
        return json.loads(HTTPContent)

    @staticmethod
    def sleepForThottling():
        sleep(0.1)

    def addInitiativeToDatabase(self, initiative):
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

    def checkConnectionToServer(self):
        logging.debug("Checking connection to server")

        HTTPContentJSON = self.queryDeedsPageFromAPI(currentPage=1, pageSize=1)
        queryStatus = self.getStatusFromJSON(HTTPContentJSON)

        return int(queryStatus) == 200

    def queryDeedsPageFromAPI(self, currentPage, pageSize=50):
        logging.debug("Requesting page %s with page size %s" % (currentPage, pageSize))

        if pageSize > self.maxPageSize:
            pageSize = self.maxPageSize

        HTTPParameters = self.getHTTPParametersForPageQuery(currentPage, pageSize)
        self.HTTPParameters = HTTPParameters

        APIDeedsURL = self.getAPIDeedsURL()
        HTTPContentJSON = self.getHTTPResponseJSON(APIDeedsURL)

        return HTTPContentJSON

    def queryDeedDetailsFromAPI(self, deedID):
        logging.debug("Retrieving details for deed ID %s" % deedID)

        self.HTTPGetParameters = {}

        APIDeedDetailsURL = self.getAPIDeedDetailsURL(deedID)
        HTTPContentJSON = self.getHTTPResponseJSON(APIDeedDetailsURL)
        deedDetails = self.getDeedDetailsFromJSON(HTTPContentJSON)

        return deedDetails

    def getPageCountFromAPI(self):
        logging.debug("Retrieving page count")

        HTTPContentJSON = self.queryDeedsPageFromAPI(self.pageStartCount)
        pageCount = self.getPageCountFromPageJSON(HTTPContentJSON)

        return pageCount

    def queryDeedsPageJSONFromAPI(self, currentPage, pageSize=50):

        HTTPContentJSON = self.queryDeedsPageFromAPI(currentPage, pageSize)
        deedsQueryResults = self.getDeedsFromPageJSON(HTTPContentJSON)

        return deedsQueryResults

    def getAPIDeedsURL(self):
        return "%s/%s" % (self.getBaseURL(), self.APIDeedsEndpoint)

    def getAPIDeedDetailsURL(self, deedID):
        return "%s/%s" % (self.getAPIDeedsURL(), deedID)

    @staticmethod
    def getDataFromJSON(JSON):
        return JSON["data"]

    @staticmethod
    def getStatusFromJSON(JSON):
        return JSON["status"]

    def getDeedDetailsFromJSON(self, JSON):
        data = self.getDataFromJSON(JSON)
        return data["deed"]

    def getDeedsFromPageJSON(self, JSON):
        data = self.getDataFromJSON(JSON)
        return data["results"]

    @staticmethod
    def getDeedIDFromJSON(JSON):
        return JSON["id"]

    def getPageCountFromPageJSON(self, JSON):
        data = self.getDataFromJSON(JSON)
        pagination = data["pagination"]

        return pagination["pageCount"]

    @staticmethod
    def getCoordinatesFromDeedDetails(deedDetails):

        parsedCoordinates = {"lat": None, "lng": None}

        coordinates = deedDetails["coordinates"]
        if coordinates is not None:
            parsedCoordinates["lat"] = coordinates["lat"]
            parsedCoordinates["lng"] = coordinates["lng"]

        return parsedCoordinates

    @staticmethod
    def getHTTPParametersForPageQuery(currentPage, pageSize):

        HTTPParameters = {
            'query': '',
            'page': str(currentPage),
            'causes': '',
            'activities': '',
            'date': '',
            'pageSize': str(pageSize),
            'withOrganization': 'true'}

        return HTTPParameters

    def scrape(self):
        logging.info("Starting CoronaHelpersScraper scraping")

        if not self.checkConnectionToServer():
            logging.error("Can't connect to CoronaHelpers server API")
            return

        numberOfPages = self.getPageCountFromAPI()

        for currentPage in range(numberOfPages):
            deedsJSON = self.queryDeedsPageJSONFromAPI(currentPage)
            self.sleepForThottling()

            for deedJSON in deedsJSON:
                self.processDeed(deedJSON)
                self.sleepForThottling()

    def processDeed(self, deedJSON):
        logging.info("Processing deed")

        deedID = self.getDeedIDFromJSON(deedJSON)
        deedDetails = self.queryDeedDetailsFromAPI(deedID)
        initiative = self.createInitiativeFromDeedDetails(deedDetails)
        self.addInitiativeToDatabase(initiative)

    def createInitiativeFromDeedDetails(self, deedDetails):
        logging.info("Creating initiative from deed details")

        deedID = self.getDeedIDFromJSON(deedDetails)
        coordinates = self.getCoordinatesFromDeedDetails(deedDetails)

        initiative = InitiativeImport(
            category=deedDetails["fullType"],
            group="supply",
            description=deedDetails["summary"],
            # name = deedDetails[""],
            source=self.getAPIDeedDetailsURL(deedID),
            # frequency = deedDetails["subtype"],
            location=deedDetails["address"],
            latitude=coordinates["lat"],
            longitude=coordinates["lng"]
        )

        return initiative
