import os
from unittest import TestCase, skip
from dateutil import parser

import pytest
import requests_mock

from data import responses
from models import InitiativeImport, InitiativeGroup
from platformen.coronapioniers import CoronaPioniers


class TestCoronaPioniersSupplyPlatformSource(TestCase):

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        self.response_list = responses.read("coronapioniers_api_list.json")
        self.response_item = responses.read("coronapioniers_api_item.json") #response for id 343
        self.response_tags = responses.read("coronapioniers_api_tags.json") #response for all tags
        self.response_media = responses.read("coronapioniers_api_media.json") #response for id 272

        scraper = CoronaPioniers()
        self.source = scraper._sources[0]

        self.item_url = "https://coronapioniers.vpro.nl/api/v3/posts/343"
        self.list_url = "https://coronapioniers.vpro.nl/api/v3/posts/geojson?has_location=mapped&limit=200&offset=0&order=desc&order_unlocked_on_top=true&orderby=created&source%5B%5D=sms&source%5B%5D=twitter&source%5B%5D=web&source%5B%5D=email&status%5B%5D=published&status%5B%5D=draft"
        self.tags_url = "https://coronapioniers.vpro.nl/api/v3/tags"
        self.media_url = "https://coronapioniers.vpro.nl/api/v3/media/272"

        request_mock.get(self.item_url, text=self.response_item, status_code=200)
        request_mock.get(self.list_url, text=self.response_list, status_code=200)
        request_mock.get(self.tags_url, text=self.response_tags, status_code=200)
        request_mock.get(self.media_url, text=self.response_media, status_code=200)
        self.request_mock = request_mock

        self.actual_result_list = [item for item in self.source.initiatives()]

        self.actual = next((x for x in self.actual_result_list if x.source_id == 343), None)
        self.source.complete(self.actual)

    def test_table_name(self):
        assert self.actual.name == "Kaartjes Kunst 10 kaartjes 10 kunstenaars"

    def test_table_category(self):
        assert self.actual.category == "Gezelschap, Kunst, Cultuur, Overig, Zorg, Mentale steun, Lokale ondernemers"

    def test_adres(self):
        assert self.actual.osm_address is None

    def test_latitude(self):
        assert self.actual.latitude == 52.476487
    
    def test_longitude(self):
        assert self.actual.longitude == 4.658048

    def test_organiser(self):
        assert self.actual.organiser is None

    def test_url(self):
        assert self.actual.url == "https://kaartjeskunst.nl/"

    def test_phone(self):
        assert self.actual.phone is None

    def test_group(self):
        assert self.actual.group == InitiativeGroup.SUPPLY

    def test_extra_fields(self):
        assert self.actual.extra_fields == "{'image': 'https://coronapioniers.vpro.nl/storage/5/e/5e9dbea86f8e1-93451054_153152782848670_6039521182504117936_n1.jpg'}"

    def test_created_at(self):
        assert self.actual.created_at == parser.parse("2020-04-20 15:24:24+00:00")

    def test_source(self):
        assert self.actual.source == "https://coronapioniers.vpro.nl"

    def test_source_uri(self):
        #in the item json the url value is "https://coronapioniers.vpro.nl/api/v3/posts/343"
        assert self.actual.source_uri == "https://coronapioniers.vpro.nl/posts/343"
    
    def test_source_id(self):
        assert self.actual.source_id == 343

    def test_scraped_at(self):
        assert self.actual.scraped_at is not None

    def test_description(self):
        assert self.actual.description.startswith("Meer dan ooit, stromen kaartjes naar jarigen, vrienden en ouderen. Broedplaats")

    def test_alternative_place_regex(self):
        assert self.actual.location is None

class TestCoronaPioniersPlatform(TestCase):
    def setUp(self):
        self.scraper = CoronaPioniers()

    def test_should_support_group_restricting(self):
        assert self.scraper.supports_group(InitiativeGroup.SUPPLY)
