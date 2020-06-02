import re
import time

from geopy.geocoders import Nominatim
from sqlalchemy import func, ARRAY, Integer

from models.database import Db
from models.geocoder import FeatureType
from models.initiatives import InitiativeImport


class Geocoder:

    def __init__(self):
        self.geo_locator = Nominatim(user_agent="codefornl-covid19")

    def batch(self, featuretype=None):
        db = Db()
        # Default concat function to sqlite
        concat_func = func.group_concat(InitiativeImport.id.distinct()).label('id_array')

        if db.session.bind.driver != 'pysqlite':
            # Assume postgres
            concat_func = func.array_agg(InitiativeImport.id, type_=ARRAY(Integer)).label('id_string')

        location_set = db.session.query(
            InitiativeImport.location,
            concat_func
        ) \
            .filter(InitiativeImport.location.isnot(None)) \
            .with_for_update().group_by(InitiativeImport.location).all()

        # What if location set is blank?
        if len(location_set) == 0:
            print("Ik wil geocoderen, maar er is geen data.")
            exit()

        for item in location_set:
            if featuretype is FeatureType.ADDRESS:
                # Use None
                self.geocode(item, db)
            else:
                self.geocode(item, db, featuretype=featuretype)

    def geocode(self, item, db, featuretype=None):
        id_array = []
        match_address = "Niet gevonden"

        # Regex for postal code written as `9999XX`
        pattern = r'\d{4}[A-Z]{2}'
        p = re.compile(pattern)

        if isinstance(item[1], list):
            id_array = item[1]
        else:
            id_array = item[1].split(',')

        geocodeterm = item[0]
        # item.location prepareren voor stadsdelen
        geocodeterm = geocodeterm.replace('Amsterdam Algemeen', 'Amsterdam')

        if geocodeterm.startswith('Stadsdeel'):
            geocodeterm = geocodeterm + ' Amsterdam'

        # is the item.location National?
        if geocodeterm in ['Landelijk', 'Heel Nederland']:
            match_address = 'Nederland'
            match_lat = None
            match_lon = None
            msg = "WARNING: " + geocodeterm + " defined as `National`, " + str(len(id_array)) + \
                  " entries set to `" + \
                  match_address + "`"
        else:
            # is the item.location Dutch postal code correct?
            zipwithoutspace = p.findall(item.location)

            if len(zipwithoutspace) > 0:

                for hit in zipwithoutspace:
                    geocodeterm = geocodeterm.replace(hit, hit[:4] + '' + hit[4:])

            match = self.geo_locator.geocode(geocodeterm, country_codes=['NL'],
                                             featuretype=featuretype,
                                             addressdetails=True)

            if match is None:
                match_lat = None
                match_lon = None
                msg = "WARNING: " + geocodeterm + " not found, " + str(len(id_array)) + \
                      " entries set to `" + \
                      match_address + "`"
            else:
                if 'postcode' in match.raw["address"]:
                    match_address = match.raw["address"]["postcode"]
                if 'town' in match.raw["address"]:
                    match_address = match.raw["address"]["town"]
                elif 'city' in match.raw["address"]:
                    match_address = match.raw["address"]["city"]

                match_lat = match.latitude
                match_lon = match.longitude
                msg = "SUCCESS: " + str(len(id_array)) + " entries mapped to: `" + match_address + "`"

        db.session.query(InitiativeImport).filter(InitiativeImport.id.in_(id_array)).update({
            InitiativeImport.osm_address: match_address,
            InitiativeImport.latitude: match_lat,
            InitiativeImport.longitude: match_lon
        }, synchronize_session=False)

        db.session.commit()
        print(msg)
        time.sleep(1)  # Sleep so we don't overstretch the nominatim api
