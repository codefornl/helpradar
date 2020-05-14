import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from models import Platform, InitiativeImport, BatchImportState, Db
from models.initiatives import InitiativeImportState
from platformen import Scraper
from platformen.scraper import ScrapeException


class TestDatabase(TestCase):
    def test_default_sqlite(self):
        test_db = Db()
        assert test_db.get_db_url().startswith("sqlite")

    def test_postgres_from_env(self):
        testie = {"DB_USER": "klaas", "DB_PASSWORD": "vaak", "DB_HOST": "thuis", "DB_NAME": "1"}
        with patch.dict(os.environ, testie):
            test_db = Db()
            assert test_db.get_db_url().startswith("postgres")


class TestScraper(TestCase):

    def setUp(self):
        self.pf_source_mock = MagicMock()
        self.scraper = Scraper("www.platform.url", "Test Platform", "tp", [self.pf_source_mock])

        # don't know how to mock properly yet so mocking out db
        # operations using partial mock.
        self.scraper.get_platform = MagicMock(name="get_platform")
        self.db_platform = Platform()
        self.scraper.get_platform.return_value = self.db_platform

        self.save_mock = MagicMock(name="save_batch")
        self.scraper.save_batch = self.save_mock

        self.logger_mock = Mock()
        get_logger_mock = Mock(return_value=self.logger_mock)
        self.scraper.get_logger = get_logger_mock

    def test_should_set_url(self):
        """Tests the loading of the platform information"""
        assert self.scraper.platform_url == "www.platform.url"

    def test_return_platform(self):
        actual = self.scraper.load_platform()
        assert actual == self.db_platform

    def test_should_start_batch_with_platform(self):
        self.pf_source_mock.initiatives = MagicMock(
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
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        self.pf_source_mock.complete.assert_called_once_with(first_import)

    def test_should_add_completed_initiative_to_batch(self):
        first_import = InitiativeImport()
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().initiatives[0] == first_import

    def test_should_flag_batch_imported_on_success(self):
        first_import = InitiativeImport()
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([first_import]))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().state == BatchImportState.IMPORTED

    def test_should_handle_scrape_exception(self):
        self.pf_source_mock.initiatives = \
            MagicMock(side_effect=ScrapeException("Failed loading the list"))

        self.scraper.scrape()

        assert self.scraper.get_current_batch().state == BatchImportState.FAILED

    def test_should_set_batch_stopped_time(self):
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([InitiativeImport()]))

        self.scraper.scrape()

        batch = self.scraper.get_current_batch()
        assert batch.started_at < batch.stopped_at

    def test_invalid_stop_throws_error(self):
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([InitiativeImport()]))
        self.scraper.scrape()

        batch = self.scraper.get_current_batch()
        with self.assertRaises(ValueError):
            batch.stop(BatchImportState.PROCESSED)

    def test_should_save_batch_on_completion(self):
        self.scraper.scrape()

        assert self.save_mock.call_count == 2

    # At the moment I don't understand why the assert fails.
    def test_should_log_start(self):
        self.scraper.scrape()

        self.logger_mock.info.assert_any_call("Starting Test Platform (tp) scraper")

    def test_should_log_listing_exception(self):
        self.pf_source_mock.initiatives = \
            MagicMock(side_effect=ScrapeException("Failed loading the list"))

        self.scraper.scrape()

        self.logger_mock.exception.assert_called_once_with("Error while reading list of initiatives")

    def test_should_have_set_scraped_at(self):
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([InitiativeImport(
            source_uri="test/123"
        )]))

        self.scraper.scrape()

        now = datetime.utcnow()
        actual = self.scraper.get_current_batch().initiatives[0].scraped_at
        # can't mock datetime.utcnow so this is my workaround.
        datediff = now - actual
        assert datediff.seconds < 1

    def test_should_set_platform_url_as_source(self):
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([InitiativeImport(
            source_uri="test/123"
        )]))

        self.scraper.scrape()

        actual = self.scraper.get_current_batch().initiatives[0]
        assert self.scraper.platform_url == actual.source

    def scrape_collection_exception(self):
        self.pf_source_mock.initiatives = MagicMock(return_value=iter([InitiativeImport(
            source_uri="test/123"
        )]))

        self.pf_source_mock.complete = Mock(side_effect=ScrapeException("Test"))

        self.scraper.scrape()

    def test_should_log_item_exception(self):
        self.scrape_collection_exception()
        self.logger_mock.exception.assert_called_once_with("Error while collecting initiative test/123")

    def test_collect_should_set_initiative_import_error(self):
        self.scrape_collection_exception()

        actual: InitiativeImport = self.scraper.get_current_batch().initiatives[0]
        assert InitiativeImportState.IMPORT_ERROR == actual.state
        assert actual.error_reason.endswith("ScrapeException: Test\n")

    def test_collect_should_always_add_initiative(self):
        self.scrape_collection_exception()

        try:
            _ = self.scraper.get_current_batch().initiatives[0]
            assert True
        except IndexError:
            assert False
