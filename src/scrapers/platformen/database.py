from sqlalchemy import Column, Integer, String, Text, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Initiative(Base):
    __tablename__ = 'initiatives'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    category = Column(String(250))
    group = Column(String(250))
    description = Column(Text)
    name = Column(String(250))
    source = Column(String(250))
    source_id = Column(String(250))
    frequency = Column(String(250))
    location = Column(String(250))
    latitude = Column(Float)
    longitude = Column(Float)
    osm_address = Column(Text)


class Db:
    session = None

    def __init__(self):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        engine = create_engine('sqlite:///helpradar.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
