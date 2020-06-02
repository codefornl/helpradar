from sqlalchemy import Enum


class FeatureType(Enum):
    COUNTRY = "country"
    STATE = "state"
    CITY = "city"
    SETTLEMENT = 'settlement'
    ADDRESS = 'address'
