import os
from unittest import TestCase

import pytest
import requests_mock
from bs4 import BeautifulSoup

from models import InitiativeImport
from platformen.nlvoorelkaar import NLvoorElkaarSource, NLvoorElkaar


class TestNLvoorElkaarPlatformSourceDemandOrg(TestCase):

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        # for a large part a cloen of Wij Amsterdam test
        test_path = os.path.dirname(__file__)
        file_path = os.path.join(test_path, "test_responses", "nlvoorelkaar_demand_org.html")
        with open(file_path, 'r') as data_file:
            self.response = data_file.read()

        scraper = NLvoorElkaar()
        self.source = scraper._sources[1]

        self.url = "https://www.nlvoorelkaar.nl/hulpvragen/183242"
        request_mock.get(self.url, text=self.response, status_code=200)
        self.request_mock = request_mock

        self.actual = InitiativeImport(source_id=183242, source_uri=self.url)
        scraper._sources[1].complete(self.actual)

    def test_table_name(self):
        assert self.actual.name == "Huishoudelijke ondersteuning en boodschappen"

    def test_table_category(self):
        assert self.actual.category == "Boodschappen, Huishoudelijk, Coronahulp"

    def test_helpdemand_organiser(self):
        assert(self.actual.organiser == "Gemeente Roosendaal")

    def test_description(self):
        assert self.actual.description.startswith("Mevrouw heeft haar arm gebroken en is opzoek naar iemand die haar kan ondersteunen")

    def test_alternative_place_regex(self):
        assert self.actual.location == "West (Roosendaal)"

    @pytest.mark.skip(reason="Test methods for debugging specific items")
    def test_missing_plaats(self):
        scraper = NLvoorElkaar()
        item = scraper._sources[0].complete(InitiativeImport(
            source_id=179582,
            source_uri="https://www.nlvoorelkaar.nl/hulpvragen/183242"
        ))
