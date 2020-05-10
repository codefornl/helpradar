import json
import os
from collections import namedtuple

import requests_mock

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from models import InitiativeGroup
from platformen.wijamsterdam import WijAmsterdamSource


class TestWijAmsterdamPlatformSource(TestCase):
    response: str

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        file_path = os.path.join(os.getcwd(), "wijams.json")
        with open(file_path, 'r') as data_file:
            self.response = data_file.read()
            self.response_objects = \
                json.loads(
                    self.response,
                    object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        self.url = "https://api2.openstad.amsterdam/api/site/197/idea"
        self.source = WijAmsterdamSource()

        request_mock.get(self.url, text=self.response, status_code=200)
        self.request_mock = request_mock
        self.actual_result = [item for item in self.source.initiatives()]

    def test_should_return_initiatives(self):
        with requests_mock.Mocker() as request_mock:
            request_mock.get(self.url, text=self.response, status_code=200)

            assert len([i for i in self.source.initiatives()]) == 2

    def test_should_set_dates(self):
        with requests_mock.Mocker() as request_mock:
            request_mock.get(self.url, text=self.response, status_code=200)

            gen =  self.source.initiatives()
            init = next(gen)
            assert init.created_at == self.response_objects[0].createdAt

    def test_should_not_write_lat_lon_if_exist(self):
        with requests_mock.Mocker() as request_mock:
            request_mock.get(self.url, text=self.response, status_code=200)

            gen = self.source.initiatives()
            actual = next(gen)
            assert None is actual.latitude
            assert None is actual.longitude

    def test_should_write_lat_lon_if_exist(self):
        with requests_mock.Mocker() as request_mock:
            request_mock.get(self.url, text=self.response, status_code=200)

            result = [i for i in self.source.initiatives()]
            expected = self.response_objects[1]
            assert result[1].latitude == expected.position.lat
            assert result[1].longitude == expected.position.lng

    def test_should_set_title(self):
        assert self.response_objects[0].title == self.actual_result[0].name

    def test_should_merge_summary_and_description(self):
        description = f"{self.response_objects[0].summary}\n--------\n{self.response_objects[0].description}"
        assert description == self.actual_result[0].description

    def test_should_set_group_supply(self):
        assert InitiativeGroup.SUPPLY == self.actual_result[0].group
        assert InitiativeGroup.SUPPLY == self.actual_result[1].group

    def test_should_set_url(self):
        for i, actual in enumerate(self.actual_result):
            assert self.response_objects[i].extraData.isOrganiserWebsite == actual.url

