import os
from pathlib import PurePath

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


class Db:
    session = None

    def __init__(self):
        # Create an engine that stores data

        url = Db.get_db_url()
        engine = create_engine(url)
        #Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    @staticmethod
    def get_db_url():
        path = PurePath(os.path.dirname(__file__))
        db_path = path.joinpath(str(path.parent), 'helpradar.db')
        return f"sqlite:///{db_path}"
        # return "postgres://%s:%s@%s/%s" % (
        #     os.getenv("DB_USER", "dev"),
        #     os.getenv("DB_PASSWORD", "dev"),
        #     os.getenv("DB_HOST", "devdb"),
        #     os.getenv("DB_NAME", "helpradar"),
        # )