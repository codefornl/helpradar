from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Base class for both platforms and helpinitiatives
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

# so far only a basic definition of platforms.
#class Platform(InitiativeBase):
#    __tablename__ = 'platforms'
#    __mapper_args__ = {'polymorphic_identity': 'platform'}
#    id = Column(Integer, ForeignKey('initiatives.id'), primary_key=True)
#    place = Column(Text)

# Group each import run in a batch for later importing.
#class ImportBatch(Base):
#    __tablename__ = 'importbatches'
#    id = Column(Integer, primary_key=True)
#    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
#    started_at = Column(DateTime, nullable=False)
#    stopped_at = Column(DateTime, nullable=False)
#    state = Column(Enum("running", "imported", "failed", "processed", "processing_error"), nullable=False)

class InitiativeImport(Base):
    __tablename__ = 'initiative_imports'
    id = Column(Integer, primary_key=True)
    #batch_id = Column(Integer, ForeignKey('importbatches.id'), nullable=False)
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
    phone = Column(String(30))
    organiser = Column(String(150))
    url = Column(String(500))
    extra_info = Column(Text)
    extra_fields = Column(Text)
    source_uri = Column(String(500), nullable=False, server_default='http://unknown.org')
    created_at = Column(DateTime)
    scraped_at = Column(DateTime)
    state = Column(Enum("imported", "processed", "processing_error"), nullable=False, server_default='imported')