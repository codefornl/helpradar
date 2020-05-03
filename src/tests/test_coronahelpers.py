from unittest import TestCase, main

from platformen import CoronaHelpersScraper


class TestCoronaHelpersScraper(TestCase):

    def setUp(self):
        self.scraper = CoronaHelpersScraper()

    def test_createScraperObject(self):
        self.assertEqual(type(self.scraper), CoronaHelpersScraper)
        self.assertIsNotNone(self.scraper.domain)

    def test_getBaseURL(self):
        url = self.scraper.getBaseURL()
        self.assertEqual(url, "https://www.coronahelpers.nl")

    def test_checkConnectionToServer(self):
        self.assertTrue(self.scraper.checkConnectionToServer())

    def test_getPageCountFromAPI(self):
        self.scraper = CoronaHelpersScraper()
        page_count = self.scraper.getPageCountFromAPI()
        self.assertTrue(int(page_count) > 1)

    def test_queryDeedsPageJSONFromAPI(self):
        self.scraper = CoronaHelpersScraper()
        deeds_query_results = self.scraper.queryDeedsPageJSONFromAPI(1)
        self.assertTrue(len(deeds_query_results) > 1)

    def test_getAPIDeedsURL(self):
        self.scraper = CoronaHelpersScraper()
        url = self.scraper.getAPIDeedsURL()
        self.assertEqual(url, "https://www.coronahelpers.nl/api/deeds")

    def test_getAPIDeedDetailsURL(self):
        self.scraper = CoronaHelpersScraper()
        url = self.scraper.getAPIDeedDetailsURL(123)
        self.assertEqual(url, "https://www.coronahelpers.nl/api/deeds/123")

    def test_getDataFromJSON(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"data": "foobar"}
        data = self.scraper.getDataFromJSON(test_json)
        self.assertEqual(data, "foobar")

    def test_getStatusFromJSON(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"status": "foobar"}
        data = self.scraper.getStatusFromJSON(test_json)
        self.assertEqual(data, "foobar")

    def test_getDeedDetailsFromJSON(self):
        json_test_data = {"status": 200, "error": None, "data": {"deed": {"title": "foobar"}}}
        self.scraper = CoronaHelpersScraper()
        deed_details = self.scraper.getDeedDetailsFromJSON(json_test_data)
        self.assertEqual(deed_details["title"], "foobar")

    def test_getDeedsFromPageJSON(self):
        json_test_data = {"status": 200, "error": None, "data": {"results": "foobar"}}
        self.scraper = CoronaHelpersScraper()
        deed_details = self.scraper.getDeedsFromPageJSON(json_test_data)
        self.assertEqual(deed_details, "foobar")

    def test_getDeedIDFromJSON(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"id": "foobar"}
        data = self.scraper.getDeedIDFromJSON(test_json)
        self.assertEqual(data, "foobar")

    def test_getPageCountFromPageJSON(self):
        json_test_data = {"status": 200, "error": None, "data": {"results": [{}], "pagination": {"page": 1, "pageSize": 2, "rowCount": 826, "pageCount": 413}}}
        self.scraper = CoronaHelpersScraper()
        page_count = self.scraper.getPageCountFromPageJSON(json_test_data)
        self.assertEqual(page_count, 413)

    def test_getCoordinatesFromDeedDetails(self):
        self.scraper = CoronaHelpersScraper()
        json_test_data = {"coordinates": None}
        coordinates = self.scraper.getCoordinatesFromDeedDetails(json_test_data)
        self.assertEqual(coordinates["lat"], None)
        self.assertEqual(coordinates["lng"], None)

        json_test_data = {"coordinates": {"lat": 123, "lng": 321}}
        coordinates = self.scraper.getCoordinatesFromDeedDetails(json_test_data)
        self.assertEqual(coordinates["lat"], 123)
        self.assertEqual(coordinates["lng"], 321)

    def test_getHTTPParametersForPageQuery(self):
        self.scraper = CoronaHelpersScraper()
        http_parameters_result = self.scraper.getHTTPParametersForPageQuery(123, 321)
        http_parameters_should_be = {
            'query': '',
            'page': '123',
            'causes': '',
            'activities': '',
            'date': '',
            'pageSize': '321',
            'withOrganization': 'true'}
        self.assertEqual(http_parameters_result, http_parameters_should_be)

    def test_createInitiativeFromDeedDetails(self):
        self.scraper = CoronaHelpersScraper()
        test_feed_details = {
            "id": 1337,
            "fullType": "volunteering_long",
            "summary": "test",
            "address": "someplace",
            "coordinates": {"lat": 52.2, "lng": 6.2}
        }
        initiative = self.scraper.createInitiativeFromDeedDetails(test_feed_details)
        self.assertEqual(initiative.source, "https://www.coronahelpers.nl/api/deeds/1337")
        self.assertEqual(initiative.category, "volunteering_long")
        self.assertEqual(initiative.description, "test")
        self.assertEqual(initiative.location, "someplace")
        self.assertEqual(initiative.latitude, 52.2)
        self.assertEqual(initiative.longitude, 6.2)


if __name__ == '__main__':
    main(verbosity=2)
