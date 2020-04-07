import time
from geopy.geocoders import Nominatim
from platformen import Initiative, Db

class Geocoder:

    def __init__(self):
        self.geolocator = Nominatim(user_agent="codefornl-covid19")

    def geocode(self):
        db = Db()
        locationset = db.session.query(Initiative).filter(Initiative.location.isnot(None)).with_for_update().all()
        for item in locationset:

            # item.location prepareren voor `landelijk`
            if item.location=='Landelijk':
                match = self.geolocator.geocode(item.location)
            else:
                match = self.geolocator.geocode('Nederland')

            # todo - item.location prepareren voor `postcode`

            match = self.geolocator.geocode(item.location)
            if match is None:
                print("ERROR  : " + item.location + " niet gevonden")
                item.osm_address = "Niet gevonden"
            else:
                item.osm_address = match.address
                item.latitude = match.latitude
                item.longitude = match.longitude
                db.session.add(item)
                db.session.commit()
                print("SUCCESS: " + match.address)
            db.session.add(item)
            db.session.commit()
            time.sleep(1) # Sleep so we don't overstretch the nominatim api



    