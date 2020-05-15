from unittest import TestCase

from tools import Geocoder


class TestGeocoder(TestCase):
    def setUp(self):
        self.geocoder = Geocoder()

    def test_user_agent_set(self):
        assert self.geocoder.geolocator.headers.get('User-Agent') is not None