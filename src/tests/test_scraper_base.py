import unittest
import mock
import platformen


from platformen import Scraper

class TestScraperDb(unittest.TestCase):

    @mock.patch('models.database.Db')
    def test_should_create_platform_if_none(self, mock_db):
        """Tests the loading of the platform information"""
        scraper = Scraper("www.platform.url")

        