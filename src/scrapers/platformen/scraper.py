from models.database import Db

class Scraper(Object):
    """
    Base class that defines and deals basic setup of a scraper 
    """
    def __init__(platform_url):
        self.platform_url = platform_url
        self.db = Db()

    def load_platform():
        return None