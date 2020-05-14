from unittest import TestCase, main

from platformen import CoronaHelpersScraper


class TestCoronaHelpersScraper(TestCase):

    def setUp(self):
        self.scraper = CoronaHelpersScraper()

    def test_create_scraper_object(self):
        self.assertEqual(type(self.scraper), CoronaHelpersScraper)
        self.assertIsNotNone(self.scraper.domain)

    def test_get_base_url(self):
        url = self.scraper.get_base_url()
        self.assertEqual(url, "https://www.coronahelpers.nl")

    def test_check_connection_to_server(self):
        self.assertTrue(self.scraper.check_connection_to_server())

    def test_get_page_count_from_api(self):
        self.scraper = CoronaHelpersScraper()
        page_count = self.scraper.get_page_count_from_api()
        self.assertTrue(int(page_count) > 1)

    def test_query_deeds_page_json_from_api(self):
        self.scraper = CoronaHelpersScraper()
        deeds_query_results = self.scraper.query_deeds_page_json_from_api(1)
        self.assertTrue(len(deeds_query_results) > 1)

    def test_get_api_deeds_url(self):
        self.scraper = CoronaHelpersScraper()
        url = self.scraper.get_api_deeds_url()
        self.assertEqual(url, "https://www.coronahelpers.nl/api/deeds")

    def test_get_api_deed_details_url(self):
        self.scraper = CoronaHelpersScraper()
        url = self.scraper.get_api_deed_details_url(123)
        self.assertEqual(url, "https://www.coronahelpers.nl/api/deeds/123")

    def test_get_data_from_json(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"data": "foobar"}
        data = self.scraper.get_data_from_json(test_json)
        self.assertEqual(data, "foobar")

    def test_get_status_from_json(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"status": "foobar"}
        data = self.scraper.get_status_from_json(test_json)
        self.assertEqual(data, "foobar")

    def test_get_deed_details_from_json(self):
        json_test_data = {"status": 200, "error": None, "data": {"deed": {"title": "foobar"}}}
        self.scraper = CoronaHelpersScraper()
        deed_details = self.scraper.get_deed_details_from_json(json_test_data)
        self.assertEqual(deed_details["title"], "foobar")

    def test_get_deeds_from_page_json(self):
        json_test_data = {"status": 200, "error": None, "data": {"results": "foobar"}}
        self.scraper = CoronaHelpersScraper()
        deed_details = self.scraper.get_deeds_from_page_json(json_test_data)
        self.assertEqual(deed_details, "foobar")

    def test_get_deed_id_from_json(self):
        self.scraper = CoronaHelpersScraper()
        test_json = {"id": "foobar"}
        data = self.scraper.get_deed_id_from_json(test_json)
        self.assertEqual(data, "foobar")

    def test_get_page_count_from_page_json(self):
        json_test_data = {"status": 200, "error": None, "data": {"results": [{}], "pagination": {"page": 1, "pageSize": 2, "rowCount": 826, "pageCount": 413}}}
        self.scraper = CoronaHelpersScraper()
        page_count = self.scraper.get_page_count_from_page_json(json_test_data)
        self.assertEqual(page_count, 413)

    def test_get_coordinates_from_deed_details(self):
        self.scraper = CoronaHelpersScraper()
        json_test_data = {"coordinates": None}
        coordinates = self.scraper.get_coordinates_from_deed_details(json_test_data)
        self.assertEqual(coordinates["lat"], None)
        self.assertEqual(coordinates["lng"], None)

        json_test_data = {"coordinates": {"lat": 123, "lng": 321}}
        coordinates = self.scraper.get_coordinates_from_deed_details(json_test_data)
        self.assertEqual(coordinates["lat"], 123)
        self.assertEqual(coordinates["lng"], 321)

    def test_get_http_parameters_for_page_query(self):
        self.scraper = CoronaHelpersScraper()
        http_parameters_result = self.scraper.get_http_parameters_for_page_query(123, 321)
        http_parameters_should_be = {
            'query': '',
            'page': '123',
            'causes': '',
            'activities': '',
            'date': '',
            'pageSize': '321',
            'withOrganization': 'true'}
        self.assertEqual(http_parameters_result, http_parameters_should_be)

    def test_create_initiative_from_deed_details(self):
        self.scraper = CoronaHelpersScraper()
        test_feed_details = {
            "id": 1337,
            "fullType": "volunteering_long",
            "summary": "test",
            "address": "someplace",
            "coordinates": {"lat": 52.2, "lng": 6.2}
        }
        initiative = self.scraper.create_initiative_from_deed_details(test_feed_details)
        self.assertEqual(initiative.source, "https://www.coronahelpers.nl/api/deeds/1337")
        self.assertEqual(initiative.category, "volunteering_long")
        self.assertEqual(initiative.description, "test")
        self.assertEqual(initiative.location, "someplace")
        self.assertEqual(initiative.latitude, 52.2)
        self.assertEqual(initiative.longitude, 6.2)


if __name__ == '__main__':
    main(verbosity=2)
