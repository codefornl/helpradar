from datetime import datetime
import json
import os
from collections import namedtuple

from dateutil import parser
import requests_mock

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from models import InitiativeGroup
from platformen.wijamsterdam import WijAmsterdamSource


class TestWijAmsterdamPlatformSource(TestCase):
    response: str

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        test_path = os.path.dirname(__file__)
        file_path = os.path.join(test_path, "wijams.json")
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
        assert len(self.actual_result) == 2

    def test_should_set_dates(self):
        for i, actual in enumerate(self.actual_result):
            # using dateutil and not datetime because: https://stackoverflow.com/a/3908349/167131
            assert isinstance(actual.created_at, datetime)
            expected = parser.parse(self.response_objects[i].createdAt)
            assert expected == actual.created_at

    def test_should_not_write_lat_lon_if_exist(self):
        assert None is self.actual_result[0].latitude
        assert None is self.actual_result[0].longitude

    def test_should_write_lat_lon_if_exist(self):
        expected = self.response_objects[1]
        assert expected.position.lat == self.actual_result[1].latitude
        assert expected.position.lng == self.actual_result[1].longitude

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

    def test_should_use_theme_as_category(self):
        for i, actual in enumerate(self.actual_result):
            assert self.response_objects[i].extraData.theme == actual.category

    def test_should_use_organiser(self):
        for i, actual in enumerate(self.actual_result):
            assert self.response_objects[i].extraData.isOrganiserName == actual.organiser

    def test_should_use_extra_fields_for_original_json(self):
        for i, actual in enumerate(self.actual_result):
            try:
                _ = json.loads(actual.extra_fields)
            except json.JSONDecodeError:
                assert False
