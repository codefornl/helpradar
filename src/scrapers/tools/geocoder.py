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


class Match:
    def __init__(self, address, lat, lon):
        self.address = address
        self.lat = lat
        self.lon = lon


class Geocoder:
    # Regex for postal code written as `9999XX`
    POSTCAL_CODE_REGEX = re.compile(r"\d{4}[A-Z]{2}")
    # Regex that strips municipality from location if whole location doesn't deliver result
    # like finding Oisterwijk in  "'t Westend / 't Seuverick (Oisterwijk)"
    NLVE_MUNICIPALITY_REGEX = re.compile(r"[\w '-/]+\((?P<muni>[\w ]+)?\)")


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
            .filter(InitiativeImport.osm_address.is_(None)) \
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

        if isinstance(item[1], list):
            id_array = item[1]
        else:
            id_array = item[1].split(",")

        geocode_term = item[0]

        # item.location prepareren voor stadsdelen
        geocode_term = geocode_term.replace("Amsterdam Algemeen", "Amsterdam")

        matchers = [self.match_nederland, self.match_stadsdeel, self.match_nominatim, self.match_nominatim_nlve_muni]
        match = None
        for matcher in matchers:
            match = matcher(item, geocode_term, feature_type, id_array)
            if match:
                break

        if not match:
            match = Match(geocode_term, None, None)
            logger.warning(geocode_term + " not found, " + str(len(id_array)) +
                                                   " entries set to original`" +
                                                   geocode_term + "`")

        self.bulk_update(match.address, match.lat, match.lon, id_array)

        time.sleep(1)  # Sleep so we don"t overstretch the nominatim api

    def match_nederland(self, item, geocode_term, feature_type, id_array):
        if geocode_term in ["Landelijk", "Heel Nederland"]:
            match_address = "Nederland"
            match_lat = None
            match_lon = None
            get_logger().warning(geocode_term + " defined as `National`, " + str(len(id_array)) +
                           " entries set to `" +
                           match_address + "`")
            return Match(match_address, match_lat, match_lon)
        return None

    def match_stadsdeel(self, item, geocode_term, feature_type, id_array):
        if geocode_term.startswith("Stadsdeel"):
            match_address = "Amsterdam " + geocode_term.replace("Stadsdeel ", "")
            match_lat = None
            match_lon = None
            get_logger().warning(f"Geocode term starts with as stadsdeel {geocode_term}, {len(id_array)} "
                           f"entries set to `{match_address}` as result")
            return Match(match_address, match_lat, match_lon)
        return None

    def match_nominatim(self, item, geocode_term, feature_type, id_array):
        # is the item.location Dutch postal code correct?
        zip_without_space = self.POSTCAL_CODE_REGEX.findall(item.location)

        if len(zip_without_space) > 0:

            for hit in zip_without_space:
                geocode_term = geocode_term.replace(hit, hit[:4] + "" + hit[4:])

        if feature_type is FeatureType.ADDRESS:
            feature_type = None

        match = self.geo_locator.geocode(geocode_term, country_codes=["NL"],
                                         featuretype=feature_type,
                                         addressdetails=True)

        if match is None:
            return None
        else:
            match_address = None
            if "postcode" in match.raw["address"]:
                match_address = match.raw["address"]["postcode"]
            if "village" in match.raw["address"]:
                match_address = match.raw["address"]["village"]
            if "town" in match.raw["address"]:
                match_address = match.raw["address"]["town"]
            elif "city" in match.raw["address"]:
                match_address = match.raw["address"]["city"]

            match_lat = match.latitude
            match_lon = match.longitude
            get_logger().info(f"{str(len(id_array))} entries mapped to: `" + match_address + "`")
            return Match(match_address, match_lat, match_lon)

    def match_nominatim_nlve_muni(self, item, geocode_term, feature_type, id_array):
        match = self.NLVE_MUNICIPALITY_REGEX.match(geocode_term)
        if match:
            municipality = match.group('muni')
            get_logger().info(f"Trying to map {municipality} from {geocode_term}")
            return self.match_nominatim(item, municipality, feature_type, id_array)

        return None

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

        # Id's that already have lat/lon should only have the address updated
        count_address_only = self.db.session.query(InitiativeImport) \
            .filter(InitiativeImport.id.in_(ids)) \
            .filter(InitiativeImport.latitude != None) \
            .update({InitiativeImport.osm_address: address}, synchronize_session=False)
        logger.info(f"Updated {count_address_only} initiatives with address only.")

        self.db.session.commit()
