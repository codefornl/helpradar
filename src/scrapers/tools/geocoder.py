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
        self.db = Db()

    def batch(self, feature_type=None):
        logger = get_logger()
        # Default concat function to sqlite
        concat_func = func.group_concat(InitiativeImport.id.distinct()).label("id_array")

        if self.db.session.bind.driver != "pysqlite":
            # Assume postgres
            concat_func = func.array_agg(InitiativeImport.id, type_=ARRAY(Integer)).label("id_string")

        location_set = self.db.session.query(
            InitiativeImport.location,
            concat_func
        ) \
            .filter(InitiativeImport.location.isnot(None)) \
            .with_for_update().group_by(InitiativeImport.location).all()

        # What if location set is blank?
        if len(location_set) == 0:
            logger.warning("Ik wil geocoderen, maar er is geen data.")
            exit()

        for item in location_set:
            self.geocode(item, feature_type)

    def geocode(self, item, feature_type=None):
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

        # is the item.location National?
        if geocode_term in ["Landelijk", "Heel Nederland"]:
            match_address = "Nederland"
            match_lat = None
            match_lon = None
            logger.warning(geocode_term + " defined as `National`, " + str(len(id_array)) +
                           " entries set to `" +
                           match_address + "`")
        elif geocode_term.startswith("Stadsdeel"):
            match_address = "Amsterdam " + geocode_term.replace("Stadsdeel ", "")
            match_lat = None
            match_lon = None
            logger.warning(f"Geocode term starts with as stadsdeel {geocode_term}, {len(id_array)} "
                           f"entries set to `{match_address}` as result")
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
                match_address = geocode_term
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

        self.bulk_update(match_address, match_lat, match_lon, id_array)

        time.sleep(1)  # Sleep so we don"t overstretch the nominatim api

    def bulk_update(self, address, lat, lng, ids):
        logger = get_logger()
        # Updates address and lat/lng for Initiatives that don't have lat/lng from platform.
        count_nolocation = self.db.session.query(InitiativeImport) \
            .filter(InitiativeImport.id.in_(ids)) \
            .filter(InitiativeImport.latitude == None) \
            .update({
            InitiativeImport.osm_address: address,
            InitiativeImport.latitude: lat,
            InitiativeImport.longitude: lng}, synchronize_session=False)
        logger.info(f"Updated {count_nolocation} initiatives with address and geo coordinates.")

        # Id's that already have lat/lng should only have the address updated
        count_address_only = self.db.session.query(InitiativeImport) \
            .filter(InitiativeImport.id.in_(ids)) \
            .filter(InitiativeImport.latitude != None) \
            .update({InitiativeImport.osm_address: address}, synchronize_session=False)
        logger.info(f"Updated {count_address_only} initiatives with address only.")

        self.db.session.commit()
