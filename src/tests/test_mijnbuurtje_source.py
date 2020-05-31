import json
import re
from datetime import date
from unittest import TestCase
from unittest.mock import patch

import requests_mock

from data import responses
from models import InitiativeImport
from platformen.TreeParser import HtmlParseError, TreeParser
from platformen.mijnbuurtje import MijnBuurtjeSource, MijnBuurtjeSourceConfig
from platformen.scraper import ScrapeException


class TestMijnBuurtjePlatformSource(TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.list_response = responses.read("mijnbuurtje_list.html")
        self.item_response = responses.read("mijnbuurtje_item.html")
        self.item_nolocation_response = responses.read("mijnbuurtje_nolocation_item.html")

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        self.config = MijnBuurtjeSourceConfig("testbuurtje.nl",
                                         "https://testbuurtje.nl/elkaar-helpen?theme%5B%5D=836&format=fragment",
                                         "https://testbuurtje.nl/elkaar-helpen/",
                                         "Test Town")
        self.test_source = MijnBuurtjeSource(self.config)

        self.setup_list_requests(request_mock)
        self.setup_item_request(request_mock, self.item_response)
        self.request_mock = request_mock
        self.actual_result = [item for item in self.test_source.initiatives()]
        self.test_source.complete(self.actual_result[0])
        self.actual_item = self.actual_result[0]

    def setup_item_request(self, request_mock, response):
        item_url_matcher = re.compile("/elkaar-helpen/[0-9]+")
        request_mock.get(item_url_matcher, text=response, status_code=200)

    def setup_list_requests(self, request_mock):
        request_mock.get(self.config.list_endpoint + "&page=1", text=self.list_response, status_code=200)
        request_mock.get(self.config.list_endpoint + "&page=2", text=None, status_code=200)

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

    def test_should_scrape_frequency(self):
        frequency = json.loads(self.actual_item.frequency)
        assert frequency['on'] == "Maandag, Dinsdag, Woensdag, Donderdag, Vrijdag, Zaterdag, Zondag"

    @requests_mock.Mocker()
    def test_should_set_location(self, request_mock):
        self.setup_item_request(request_mock, self.item_nolocation_response)
        test_source = MijnBuurtjeSource(self.config)
        actual = InitiativeImport(source_uri=self.config.details_endpoint + "1234")
        test_source.complete(actual)

        assert actual.location == self.config.location

    @requests_mock.Mocker()
    def test_should_wrap_initiatives_exceptions(self, request_mock):
        test_source = MijnBuurtjeSource(self.config)
        self.setup_list_requests(request_mock)

        with patch.object(TreeParser, 'apply_schemas', side_effect=HtmlParseError()):
            with self.assertRaises(ScrapeException):
                _ = [item for item in test_source.initiatives()]

    @requests_mock.Mocker()
    def test_should_wrap_complete_exceptions(self, request_mock):
        test_source = MijnBuurtjeSource(self.config)
        self.setup_item_request(request_mock, self.item_response)

        with patch.object(TreeParser, 'apply_schemas', side_effect=HtmlParseError()):
            with self.assertRaises(ScrapeException):
                _ = test_source.complete(InitiativeImport(source_uri=self.config.details_endpoint + "1234"))

