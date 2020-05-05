from unittest import TestCase
from unittest.mock import MagicMock

import context
from platformen import Scraper


class TestScraperDb(TestCase):

    def setUp(self):
        self.scraper = Scraper("www.platform.url", "Test Platform", "tp")

    #@mock.patch('models.database.Db')
    def test_should_set_url(self):
        """Tests the loading of the platform information"""
        assert self.scraper.platform_url == "www.platform.url"

    # def test_return_new_platform_if_none(self):
    #     with mock.patch('scrapers.models.Db') as db_mock:
    #         scraper = Scraper("www.platform.url")
    #
    #         session_mock = MagicMock()
    #         session_mock.query = MagicMock(return_value=None)
    #         db_mock.session.return_value = session_mock
    #         scraper.load_plaform()
