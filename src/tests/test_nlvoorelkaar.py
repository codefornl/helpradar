import os
from unittest import TestCase

import pytest
import requests_mock
from bs4 import BeautifulSoup

from models import InitiativeImport, InitiativeGroup
from platformen.nlvoorelkaar import NLvoorElkaarSource, NLvoorElkaar


class TestNLvoorElkaarPlatformSource(TestCase):

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        # for a large part a cloen of Wij Amsterdam test
        test_path = os.path.dirname(__file__)
        file_path = os.path.join(test_path, "test_responses", "nlvoorelkaar_supply.html")
        with open(file_path, 'r') as data_file:
            self.response = data_file.read()

        scraper = NLvoorElkaar()
        self.source = scraper._sources[0]

        self.url = "https://www.nlvoorelkaar.nl/hulpaanbod/179582"
        request_mock.get(self.url, text=self.response, status_code=200)
        self.request_mock = request_mock

        self.actual = InitiativeImport(source_id=179582, source_uri=self.url)
        scraper._sources[0].complete(self.actual)

    def test_table_name(self):
        assert self.actual.name == "Aanbod van Joeri"

    def test_table_category(self):
        assert self.actual.category == "Coronahulp"

    def test_table_organisation_kind(self):
        assert self.actual.organisation_kind == "een vrijwilliger"

    def test_description(self):
        assert self.actual.description.startswith("Naast het schrijven van mijn scriptie zou ik graag mensen helpen")

    def test_alternative_place_regex(self):
        assert self.actual.location == "Amstelveen"

    @pytest.mark.skip(reason="Test methods for debugging specific items")
    def test_missing_plaats(self):
        scraper = NLvoorElkaar()
        item = scraper._sources[0].complete(InitiativeImport(
            source_id=179582,
            source_uri="https://www.nlvoorelkaar.nl/hulpaanbod/179582"
        ))


class TestNLvoorElkaarPlatform(TestCase):

    def setUp(self):
        self.scraper = NLvoorElkaar()

    def test_should_support_group_restricting(self):
        assert self.scraper.supports_group(InitiativeGroup.SUPPLY)
        assert self.scraper.supports_group(InitiativeGroup.DEMAND)

    def test_should_have_deleted_other_source(self):
        self.scraper.set_group(InitiativeGroup.DEMAND)
        assert 1 == len(self.scraper.sources())
        assert InitiativeGroup.DEMAND == self.scraper.sources()[0].config.group
