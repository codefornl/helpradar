from unittest import TestCase, mock
from unittest.mock import MagicMock

import context
from models import Platform, ImportBatch
from platformen import Scraper


class TestScraperDb(TestCase):

    def setUp(self):
        self.scraper = Scraper("www.platform.url", "Test Platform", "tp")

        # don't know how to mock properly yet so mocking out db
        # operations using partial mock.
        self.scraper.get_platform = MagicMock(name="get_platform")
        self.db_platform = Platform()
        self.scraper.get_platform.return_value = self.db_platform

    def test_should_set_url(self):
        """Tests the loading of the platform information"""
        assert self.scraper.platform_url == "www.platform.url"

    def test_return_platform(self):
        actual = self.scraper.load_platform()
        assert actual == self.db_platform

    def test_should_start_batch_with_platform(self):
        self.scraper.scrape()
        started_batch = self.scraper.get_current_batch()
        assert started_batch is not None
        assert started_batch.platform == self.db_platform
        assert started_batch.state == "running"
