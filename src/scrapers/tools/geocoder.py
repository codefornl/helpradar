import logging
import re
import time

from geopy.geocoders import Nominatim
from sqlalchemy import func, ARRAY, Integer

from models.database import Db
from models.geocoder import FeatureType
from models.initiatives import InitiativeImport


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)


class Geocoder:

    def __init__(self):
        self.geo_locator = Nominatim(user_agent="code-for-nl-covid-19")

    def batch(self, feature_type=None):
        logger = get_logger()
        db = Db()
        # Default concat function to sqlite
        concat_func = func.group_concat(InitiativeImport.id.distinct()).label("id_array")

        if db.session.bind.driver != "pysqlite":
            # Assume postgres
            concat_func = func.array_agg(InitiativeImport.id, type_=ARRAY(Integer)).label("id_string")

        location_set = db.session.query(
            InitiativeImport.location,
            concat_func
        ) \
            .filter(InitiativeImport.location.isnot(None)) \
            .filter(InitiativeImport.longitude.isnot(None)) \
            .filter(InitiativeImport.latitude.isnot(None)) \
            .with_for_update().group_by(InitiativeImport.location).all()

        # What if location set is blank?
        if len(location_set) == 0:
            logger.warning("Ik wil geocoderen, maar er is geen data.")
            exit()

        for item in location_set:
            self.geocode(item, db, feature_type=feature_type)

    def geocode(self, item, db, feature_type=None):
        logger = get_logger()
        match_address = "Niet gevonden"

        # Regex for postal code written as `9999XX`
        pattern = r"\d{4}[A-Z]{2}"
        p = re.compile(pattern)

        if isinstance(item[1], list):
            id_array = item[1]
        else:
            id_array = item[1].split(",")

        geocode_term = item[0]
        # item.location prepareren voor stadsdelen
        geocode_term = geocode_term.replace("Amsterdam Algemeen", "Amsterdam")

        if geocode_term.startswith("Stadsdeel"):
            geocode_term = geocode_term + " Amsterdam"

        # is the item.location National?
        if geocode_term in ["Landelijk", "Heel Nederland"]:
            match_address = "Nederland"
            match_lat = None
            match_lon = None
            logger.warning(geocode_term + " defined as `National`, " + str(len(id_array)) +
                           " entries set to `" +
                           match_address + "`")
        else:
            # is the item.location Dutch postal code correct?
            zip_without_space = p.findall(item.location)

            if len(zip_without_space) > 0:

                for hit in zip_without_space:
                    geocode_term = geocode_term.replace(hit, hit[:4] + "" + hit[4:])

            if feature_type is FeatureType.ADDRESS:
                feature_type = None
            match = self.geo_locator.geocode(geocode_term, country_codes=["NL"],
                                             featuretype=feature_type,
                                             addressdetails=True)

            if match is None:
                match_lat = None
                match_lon = None
                logger.warning(geocode_term + " not found, " + str(len(id_array)) +
                               " entries set to `" +
                               match_address + "`")
            else:
                if "postcode" in match.raw["address"]:
                    match_address = match.raw["address"]["postcode"]
                if "town" in match.raw["address"]:
                    match_address = match.raw["address"]["town"]
                elif "city" in match.raw["address"]:
                    match_address = match.raw["address"]["city"]

                match_lat = match.latitude
                match_lon = match.longitude
                logger.info(str(len(id_array)) + " entries mapped to: `" + match_address + "`")

        db.session.query(InitiativeImport).filter(InitiativeImport.id.in_(id_array)).update({
            InitiativeImport.osm_address: match_address,
            InitiativeImport.latitude: match_lat,
            InitiativeImport.longitude: match_lon
        }, synchronize_session=False)

        db.session.commit()
        time.sleep(1)  # Sleep so we don"t overstretch the nominatim api
