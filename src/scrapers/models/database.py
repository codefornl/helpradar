import os
from pathlib import PurePath

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

class Db:
    session = None

    def __init__(self):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        
        path = PurePath(os.path.dirname(__file__))
        print(path.parent)
        engine = create_engine('sqlite:///' + str(path.parent) + '\\helpradar.db')
        #Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        