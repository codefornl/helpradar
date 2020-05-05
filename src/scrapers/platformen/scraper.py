import sys

from models.database import Db
from models.initiatives import Platform, BatchImportState


class Scraper:
    """
    Concept for a base class that defines and deals basic setup of a scraper 
    """
    def __init__(self, platform_url: str, name: str, code: str):
        self.platform_url = platform_url
        self.name = name
        self.code = code
        self._db = Db()

    def scrape(self):
        print(f"starting {self.name} ({self.code}) scraper")

    def should_continue(self, count):
        if sys.gettrace() is not None:
            return count <= 5
        else:
            return True

    def load_platform(self):
        """ retrieve platform instance or create it """
        platform = self._db.session.query(Platform).filter(Platform.url.like('%'+self.platform_url+'%')).first()
        if platform is None:
            platform = Platform(name=self.name,
                                url=self.platform_url,
                                place='Nederland')
            self._db.session.add(platform)
            # we can also raise exception or create default instance.
            # raise Exception("No platform found")

        return platform


class ScraperConcept(Scraper):
    """This is conceptual code for discussion purposes to go in Scraper class"""
    def start_scrape(self):
        try:
            platform = self.load_platform()
            # start batch
            batch = ImportBatch.start_new(platform)
            self.db.session.add(batch)
            self.db.session.commit()
        except Exception as e:
            print("Error while scraping: " + e.args[0])
            # TODO: Log and raise wrapped exception

        try:
            # This is not perfect given the NL voor Elkaar also uses a configuration object
            # because actually runs two separate scraping sessions for supply and demand
            self.scrape_list(batch)
        except Exception as e:
            batch.state = BatchImportState.FAILED
            print("Error while scraping: " + e.args[0])
            # TODO: Should do logging here
        else:
            batch.state = BatchImportState.IMPORTED

        batch.stopped_at = datetime.datetime.now(datetime.timezone.utc)

        self.db.session.commit()

    def scrape_list(self, batch):
        """
        Scrapes all initiatives and adds them to the batch.
        """
        has_more = True
        initiatives = []
        while has_more:
            current_initiatives = self.get_items(batch)
            if not current_initiatives:
                has_more = False
                continue

            for initiative in current_initiatives:
                self.scrape_item(initiative)
                if initiative is not None:
                    batch.initiatives.append(initiative)


    def get_items(self, batch):
        """
        Do HTTP Request, handle errors and return skeleton Import.
        This needs to hold some state given it will be called multiple times
        Assuming for instance paging is used to retrieve a list of all items.
        This implies state needs to be reset for each batch or we hold te state on
        the Batch itself. I have no idea if we can dynamically add attributes
        that simply are used only for a specific scraper.
        """
        return #[InitiativeImport()]

    def scrape_item(self, batch, item):
        """
        Do HTTP Request, handle error and scrape detail information of initiative.
        POssible the scraping can be deferred to the TreeParser or any other class
        """
        return item