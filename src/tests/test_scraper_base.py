from unittest import TestCase, mock
from unittest.mock import MagicMock

import context
from models import Platform, ImportBatch, InitiativeImport, BatchImportState
from platformen import Scraper
from platformen.scraper import ScrapeException


class TestScraper(TestCase):

    def setUp(self):
        self.pf_source_mock = MagicMock()
        self.scraper = Scraper("www.platform.url", "Test Platform", "tp", [self.pf_source_mock])

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
        self.pf_source_mock.__iter__ = MagicMock(
            side_effect=self.assert_running_batch_on_iter)

        self.scraper.scrape()

    def assert_running_batch_on_iter(self):
        started_batch = self.scraper.get_current_batch()
        assert started_batch is not None
        assert started_batch.platform == self.db_platform
        assert started_batch.state == "running"

        return iter([InitiativeImport()])

    def test_should_iterate_platform_source(self):
        first_import = InitiativeImport()
        self.pf_source_mock.__iter__ = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        self.pf_source_mock.complete.assert_called_once_with(first_import)

    def test_should_add_completed_initiative_to_batch(self):
        first_import = InitiativeImport()
        self.pf_source_mock.__iter__ = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().initiatives[0] == first_import

    def test_should_flag_batch_imported_on_success(self):
        first_import = InitiativeImport()
        self.pf_source_mock.__iter__ = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().state == BatchImportState.IMPORTED

    def test_should_handle_scrape_exception(self):
        self.pf_source_mock.__iter__ = \
            MagicMock(side_effect=ScrapeException("Failed loading the list"))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().state == BatchImportState.FAILED

    def test_should_save_batch_on_completion(self):
        save_mock = MagicMock(name="save_batch")
        self.scraper.save_batch = save_mock

        self.scraper.scrape()

        assert save_mock.call_count == 2

