import time
from geopy.geocoders import Nominatim
from platformen import Initiative, Db
import re

class Geocoder:

    def __init__(self):
        self.geolocator = Nominatim(user_agent="codefornl-covid19")

    def geocode(self):
        db = Db()
        locationset = db.session.query(Initiative).filter(Initiative.location.isnot(None)).with_for_update().all()

        # Regex voor postcode geschreven ls `9999XX`
        pattern = r'\d{4}[A-Z]{2}'
        p = re.compile(pattern)
        for item in locationset:
            geocodeterm = item.location
            # item.location prepareren voor stadsdelen
            geocodeterm = geocodeterm.replace('Amsterdam Algemeen', 'Amsterdam')

            if geocodeterm.startswith('Stadsdeel'):
                geocodeterm = geocodeterm + ' Amsterdam'
            
            # item.location prepareren voor `landelijk`
            if geocodeterm in ['Landelijk', 'Heel Nederland']:
                geocodeterm = 'Nederland'
            else:
                # item.location prepareren voor `postcode`
                zipwithoutspace = p.findall(item.location)

                if len(zipwithoutspace) > 0:

                    for hit in zipwithoutspace:
                        geocodeterm = geocodeterm.replace(hit, hit[:4] + '' + hit[4:])

            match = self.geolocator.geocode(geocodeterm)

            if match is None:
                print("ERROR  : " + geocodeterm + " niet gevonden")
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





    