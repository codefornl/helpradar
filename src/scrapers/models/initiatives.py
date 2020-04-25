from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

#from .database import Base

Base = declarative_base()

#class InitiativeBase(Base):
#    __tablename__ = 'initiatives'
#    id = Column(Integer, primary_key=True)
#    name = Column(String(200))
#    description = Column(Text)
#    url = Column(String(500))
#    latitude = Column(Float)
#    longitude = Column(Float)
#    discriminator = Column('type', String(50))
#    __mapper_args__ = {'polymorphic_on': discriminator}


#class Platform(InitiativeBase):
#    __tablename__ = 'platforminitiatives'
#    __mapper_args__ = {'polymorphic_identity': 'platform'}
#    id = Column(Integer, ForeignKey('initiatives.id'), primary_key=True)
#    place = Column(Text)


class Initiative(Base):
    __tablename__ = 'initiatives'
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