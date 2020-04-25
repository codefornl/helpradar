from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine



class Db:
    session = None

    def __init__(self):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        engine = create_engine('sqlite:///helpradar.db')
        #Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        