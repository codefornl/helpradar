from unittest import TestCase

import context
from platformen import CoronaHelpersScraper

class TestCoronaHelpersScraper(TestCase):
    def test_createScraperObject(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        self.assertEqual(type(coronaHelpersScraper), CoronaHelpersScraper)
        self.assertIsNotNone(coronaHelpersScraper.domain)

    def test_getBaseURL(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        URL = coronaHelpersScraper.getBaseURL()
        self.assertEqual(URL, "https://www.coronahelpers.nl")

    def test_checkConnectionToServer(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        hasConnectionToServer = coronaHelpersScraper.checkConnectionToServer()
        self.assertTrue(hasConnectionToServer)

    def test_getPageCountFromAPI(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        pageCount = coronaHelpersScraper.getPageCountFromAPI()
        self.assertTrue(int(pageCount) > 1)

    def test_queryDeedsPageJSONFromAPI(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        deedsQueryResults = coronaHelpersScraper.queryDeedsPageJSONFromAPI(1)
        self.assertTrue(len(deedsQueryResults) > 1)

    def test_getAPIDeedsURL(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        URL = coronaHelpersScraper.getAPIDeedsURL()
        self.assertEqual(URL, "https://www.coronahelpers.nl/api/deeds")

    def test_getAPIDeedDetailsURL(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        URL = coronaHelpersScraper.getAPIDeedDetailsURL(123)
        self.assertEqual(URL, "https://www.coronahelpers.nl/api/deeds/123")

    def test_getDataFromJSON(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        testJSON = {"data": "foobar"}
        data = coronaHelpersScraper.getDataFromJSON(testJSON)
        self.assertEqual(data, "foobar")

    def test_getStatusFromJSON(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        testJSON = {"status": "foobar"}
        data = coronaHelpersScraper.getStatusFromJSON(testJSON)
        self.assertEqual(data, "foobar")

    def test_getDeedDetailsFromJSON(self):
        jsonTestData = {"status": 200, "error": None, "data": {"deed": {"title": "foobar"}}}
        coronaHelpersScraper = CoronaHelpersScraper()
        deedDetails = coronaHelpersScraper.getDeedDetailsFromJSON(jsonTestData)
        self.assertEqual(deedDetails["title"], "foobar")

    def test_getDeedsFromPageJSON(self):
        jsonTestData = {"status": 200, "error": None, "data": {"results": "foobar"}}
        coronaHelpersScraper = CoronaHelpersScraper()
        deedDetails = coronaHelpersScraper.getDeedsFromPageJSON(jsonTestData)
        self.assertEqual(deedDetails, "foobar")

    def test_getDeedIDFromJSON(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        testJSON = {"id": "foobar"}
        data = coronaHelpersScraper.getDeedIDFromJSON(testJSON)
        self.assertEqual(data, "foobar")

    def test_getPageCountFromPageJSON(self):
        jsonTestData = {"status": 200, "error": None, "data": {"results": [{}], "pagination": {"page": 1, "pageSize": 2, "rowCount": 826, "pageCount": 413}}}
        coronaHelpersScraper = CoronaHelpersScraper()
        pageCount = coronaHelpersScraper.getPageCountFromPageJSON(jsonTestData)
        self.assertEqual(pageCount, 413)

    def test_getCoordinatesFromDeedDetails(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        jsonTestData = {"coordinates": None}
        coordinates = coronaHelpersScraper.getCoordinatesFromDeedDetails(jsonTestData)
        self.assertEqual(coordinates["lat"], None)
        self.assertEqual(coordinates["lng"], None)

        jsonTestData = {"coordinates": {"lat": 123, "lng": 321}}
        coordinates = coronaHelpersScraper.getCoordinatesFromDeedDetails(jsonTestData)
        self.assertEqual(coordinates["lat"], 123)
        self.assertEqual(coordinates["lng"], 321)

    def test_getHTTPParametersForPageQuery(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        HTTPParametersResult = coronaHelpersScraper.getHTTPParametersForPageQuery(123, 321)
        HTTPParametersShouldBe = {
            'query': '',
            'page': '123',
            'causes': '',
            'activities': '',
            'date': '',
            'pageSize': '321',
            'withOrganization': 'true'}
        self.assertEqual(HTTPParametersResult, HTTPParametersShouldBe)

    def test_createInitiativeFromDeedDetails(self):
        coronaHelpersScraper = CoronaHelpersScraper()
        testFeedDetails = {
            "id": 1337,
            "fullType": "volunteering_long",
            "summary": "test",
            "address": "someplace",
            "coordinates": {"lat": 52.2, "lng": 6.2}
        }
        initiative = coronaHelpersScraper.createInitiativeFromDeedDetails(testFeedDetails)
        self.assertEqual(initiative.source, "https://www.coronahelpers.nl/api/deeds/1337")
        self.assertEqual(initiative.category, "volunteering_long")
        self.assertEqual(initiative.description, "test")
        self.assertEqual(initiative.location, "someplace")
        self.assertEqual(initiative.latitude, 52.2)
        self.assertEqual(initiative.longitude, 6.2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
