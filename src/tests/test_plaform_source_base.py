import pytest
import requests_mock

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from platformen.scraper import PlatformSourceConfig, PlatformSource, ScrapeException


class TestPlatformSource(TestCase):

    def test_do_request_should_handle_http_errors(self):
        with requests_mock.Mocker() as request_mock:
            # https://docs.pytest.org/en/latest/assert.html
            # I don't like the nested contexts.
            # not sure how to do that with a decorator though!
            with pytest.raises(ScrapeException) as exinfo:
                config = PlatformSourceConfig(
                    "https://www.testplatform.nl",
                    "/supply",
                    "/supply"
                )

                source = PlatformSource(config)

                url = "https://www.testplatform.nl/supply"
                # just use a error code that triggers raise_for_status
                request_mock.get(url, status_code=400)

                source.get(config.get_list_url())
                assert f"Error while requesting {url}" in str(exinfo.value)
