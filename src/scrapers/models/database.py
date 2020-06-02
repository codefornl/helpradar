from os import environ, path
from pathlib import PurePath

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Db:
    session = None

    def __init__(self):
        # Create an engine that stores data

        url = Db.get_db_url()
        engine = create_engine(url)
        # Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    @staticmethod
    def get_db_url():
        if environ.get("DB_HOST"):
            return "postgres://%s:%s@%s/%s" % (
                environ["DB_USER"],
                environ["DB_PASSWORD"],
                environ["DB_HOST"],
                environ["DB_NAME"],
            )
        dir_path = PurePath(path.dirname(__file__))
        db_path = path.join(str(dir_path.parent), 'helpradar.db')
        return f"sqlite:///{db_path}"
