"""
@author: Ferry de Boer

Defines abstract base class scraper for handling database operations,
error handling and other control logic that should be separated from
the scraping itself.
"""

import logging
import sys
import traceback
from abc import ABC
from datetime import datetime
from typing import Generator, List

import requests
from requests import HTTPError

from models.database import Db
from models.initiatives import Platform, BatchImportState, ImportBatch, InitiativeImport, InitiativeImportState


class ScrapeException(Exception):
    """
    Wrapper exception to ease exception handling to single type.
    Should be used by implementers of these base classes to wrap
    other exception types.
    """
    pass


class PlatformSourceConfig(object):
    """
    Container to hold standard items usually required for a platform source
    to operate.
    """
    def __init__(self, platform_url, list_endpoint, details_endpoint):
        self.platform_url = platform_url
        self.list_endpoint = list_endpoint
        self.details_endpoint = details_endpoint

    def get_list_url(self):
        return '%s%s' % (self.platform_url, self.list_endpoint)

    def get_initiative_url(self, initiative_id):
        return '%s%s%s' % (self.platform_url, self.details_endpoint, initiative_id)


class PlatformSource(ABC):
    """
    Implementations should this class should are doing the real
    scraping of data. Offers basic functionality for http response
    / error handling.
    """
    
    def __init__(self, config: PlatformSourceConfig):
        self.config = config

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        """
        Implementations will differ.
        Lists bare initiatives from an Api or web page.
        """
        yield None

    def complete(self, initiative: InitiativeImport):
        """
        Completes the initiative provided by the iterator.
        This leaves error handling and completion strategy
        to the caller.
        """
        pass

    @staticmethod
    def get(uri):
        try:
            response = requests.get(uri)
            response.raise_for_status()
            return response
        except HTTPError as e:
            # is the the right way to wrap?
            raise ScrapeException(f"Error while requesting {uri}") from e


class ScraperExceptionRecoveryStrategy:
    _count = 0
    """
    counts the times should raise is called
    """

    def __init__(self, max_tries: int):
        self.max_tries: int = max_tries

    # noinspection PyUnusedLocal
    def should_raise(self, ex: Exception):
        self._count += 1
        return self._count == self.max_tries


class Scraper(ABC):
    """
    Concept for a base class that defines and deals basic setup of a scraper 
    """

    def __init__(self, platform_url: str, name: str, code: str, sources: List[PlatformSource] = []):
        # Leave out until full conversion of scrapers.
        # if len(sources) == 0:
        #    raise ValueError("Expecting at least one source!")
        self._group = None
        self.platform_url: str = platform_url
        self.name: str = name
        self.code: str = code
        self._sources = sources
        self._db = Db()
        self._collect_recovery = ScraperExceptionRecoveryStrategy(3)
        self.limit: int = 0
        """Limits the iteration if a debugger is attached"""
        self._batch: ImportBatch

    def scrape(self):
        """
        Starts the scraping of given platform.
        This is all synchronous. Although this does help not flooding
        a web server even faster is does make it all a lot slower.
        """
        logger = self.get_logger()
        logger.info(f"Starting {self.name} ({self.code}) scraper")
        self._start_batch()

        try:
            total = 0
            for source in self._sources:
                for count, initiative in enumerate(source.initiatives()):
                    if not self.should_continue(count):
                        break
                    self._collect_initiative(initiative, source)
                    total = count

        except ScrapeException:
            self.get_logger().exception("Error while reading list of initiatives")
            self._batch.stop(BatchImportState.FAILED)
        else:
            self._batch.stop(BatchImportState.IMPORTED)
        finally:
            self.get_logger().info(f"Saving {total} scraped initiatives from {self._batch.platform.name}")
            self.save_batch()

    def _collect_initiative(self, initiative: InitiativeImport, source):
        if initiative is None:
            raise ValueError("Expecting an initiative instance!")

        try:
            source.complete(initiative)
            initiative.scraped_at = datetime.utcnow()
            initiative.source = self.platform_url
            self.get_logger().debug(f"Scraped {initiative.source_uri}")
        except ScrapeException as e:
            self.get_logger()\
                .exception(f"Error while collecting initiative {initiative.source_uri}")
            # There's maybe no point in doing this unless it's saved or at least counted.
            # this is actually indicating error with down the line processing.
            initiative.state = InitiativeImportState.IMPORT_ERROR
            ex_info = sys.exc_info()
            initiative.error_reason = "".join(traceback.format_exception(*ex_info))
            # Should probably do this very neat with a context manager.
            if self._collect_recovery.should_raise(e):
                raise e
        finally:
            # Always store initiative for traceability.
            self.add_initiative(initiative)

        # Not handling db errors, that is allowed to break execution!

    def _start_batch(self):
        platform = self.load_platform()
        self._batch = ImportBatch.start_new(platform)
        self.save_batch()

    def should_continue(self, count):
        """
        Method primarily for debugging purposes only
        """
        if self.is_limited():
            return count < self.limit
        else:
            return True

    def is_limited(self):
        return self.limit > 0

    def load_platform(self):
        """ retrieve platform instance or create it """
        platform = self.get_platform()
        if platform is None:
            platform = Platform(name=self.name,
                                url=self.platform_url,
                                place='Nederland')
            self._db.session.add(platform)
            # we can also raise exception or create default instance.
            # raise Exception("No platform found")

        return platform

    def get_platform(self):
        return self._db.session.query(Platform).filter(Platform.url.like('%' + self.platform_url + '%')).first()

    def get_current_batch(self) -> ImportBatch:
        return self._batch

    def add_source(self, source: PlatformSource):
        if source is None:
            raise ValueError("source is None")
        self._sources.append(source)

    def remove_sources(self, source: PlatformSource):
        if source is None:
            raise ValueError("source is None")
        self._sources.remove(source)

    def sources(self) -> List[PlatformSource]:
        return self._sources

    def save_batch(self):
        if self._batch is None:
            return

        if self._batch.id is None:
            self._db.session.add(self._batch)

        self._db.session.commit()

    def add_initiative(self, initiative):
        self._batch.initiatives.append(initiative)

    def get_logger(self) -> logging.Logger:
        raise NotImplementedError("Should be implemented by derived scraper")

    def set_group(self, group):
        """
        Restricts the scraper to a certain group. If it's not supported it
        will only log an error message and be ignored this scraping will proceed!
        """
        supports_group = self.supports_group(group)
        if not supports_group:
            if supports_group is None:
                self.get_logger().error(f"{self.name} can't pre-filter on group!")
            else:
                self.get_logger().error(f"{self.name} does not support {group}!")
        else:
            self._group = group

    def supports_group(self, group):
        """
        Implement this to indicate the scraper has support to restrict the scraping
        to one group. Return none to indicate when it has the possibility to filter
        but still has to scrape all items.
        """
        return None

    def get_group(self):
        return self._group
