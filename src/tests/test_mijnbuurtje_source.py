import re
from datetime import datetime, date
from unittest import TestCase

import requests_mock
from coverage.annotate import os

from platformen.mijnbuurtje import MijnBuurtjeSource, MijnBuurtjeSourceConfig


class TestMijnBuurtjePlatformSource(TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        test_path = os.path.dirname(__file__)
        list_file_path = os.path.join(test_path, "test_responses", "mijnbuurtje_list.html")
        with open(list_file_path, 'r', encoding='utf8') as data_file:
            self.list_response = data_file.read()

        item_file_path = os.path.join(test_path, "test_responses", "mijnbuurtje_item.html")
        with open(item_file_path, 'r', encoding='utf8') as data_file:
            self.item_response = data_file.read()

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        self.config = MijnBuurtjeSourceConfig("testbuurtje.nl",
                                         "https://testbuurtje.nl/elkaar-helpen?theme%5B%5D=836&format=fragment",
                                         "https://testbuurtje.nl/elkaar-helpen/",
                                         "Test Town")
        self.test_source = MijnBuurtjeSource(self.config)

        request_mock.get(self.config.list_endpoint + "&page=1", text=self.list_response, status_code=200)
        request_mock.get(self.config.list_endpoint + "&page=2", text=None, status_code=200)
        item_url_matcher = re.compile("/elkaar-helpen/[0-9]+")
        request_mock.get(item_url_matcher, text=self.item_response, status_code=200)
        self.request_mock = request_mock
        self.actual_result = [item for item in self.test_source.initiatives()]
        self.test_source.complete(self.actual_result[0])
        self.actual_item = self.actual_result[0]

    def test_should_list_two_items(self):
        assert 2 == len(self.actual_result)

    def test_should_scrape_name(self):
        assert "Hulp bij Maasburen.nl" == self.actual_item.name

    def test_should_scrape_description(self):
        assert "Hallo buurt- en dorpsgenoten!" in self.actual_item.description
        assert "en we nemen contact met je op." in self.actual_item.description

    def test_should_scrape_group(self):
        assert "supply" == self.actual_item.group

    def test_should_scrape_organiser_start(self):
        assert "Buurtverbinders" == self.actual_item.organiser

    def test_should_scrape_category(self):
        assert self.actual_item.category.startswith("#CoronaHulp, Bewonersinitiatieven")

    def test_should_scrape_created_at(self):
        assert date(2020, 4, 18) == self.actual_item.created_at

    def test_should_scrape_location(self):
        assert self.actual_item.location.startswith("Middelaar, Molenhoek, Mook, Plasmolen")