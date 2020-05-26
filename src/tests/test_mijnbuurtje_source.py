import re
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

        page_ = self.config.list_endpoint + "&page=1"
        request_mock.get(page_, text=self.list_response, status_code=200)
        request_mock.get(self.config.list_endpoint + "&page=2", text=None, status_code=200)
        item_url_matcher = re.compile("/elkaar-helpen/[0-9]+")
        request_mock.get(item_url_matcher, text=self.item_response, status_code=200)
        self.request_mock = request_mock
        self.actual_result = [item for item in self.test_source.initiatives()]

    def test_should_list_two_items(self):
        assert 2 == len(self.actual_result)
