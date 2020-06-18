import re
from unittest import TestCase

from geopy import Point

from tools import Geocoder


class TestGeocoder(TestCase):
    def setUp(self):
        self.geocoder = Geocoder()

    def test_user_agent_set(self):
        assert self.geocoder.geo_locator.headers.get('User-Agent') is not None

