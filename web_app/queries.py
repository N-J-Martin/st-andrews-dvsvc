import os
from dotenv import load_dotenv
import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geopy.distance
load_dotenv()
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
PORT = os.environ["DB_PORT"]
USER_AGENT = "DASAD/0.1"
DELAY = 1
geolocator = Nominatim(user_agent=USER_AGENT)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=DELAY)

def connect() -> psycopg2.extensions.connection:

    print("Connecting to PostgreSQL database with: %s".format(locals()))
    try:
        with psycopg2.connect(
            host=DB_HOST,
            port=PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        ) as conn:
            print("Connected to PostgreSQL database")
            return conn
    except psycopg2.DatabaseError as error:
        print("Failed to connect to PostgreSQL database: %s".format(error))

""" Calulates a square(ish) of given distance from given location.
    Points at North, South, East, West calculated by geodesic distance.
    Use these coordinates to filter locations to within this square
"""
def getLocations(location: str, distance: int):
    lat, long = getCoordinates(location)
    if lat is None and long is None:
        print(f"Error: No coordinates for location: {location}")
        return []
    else:
        northLat = geopy.distance.distance(distance).destination((lat, long), bearing=0).latitude
        southLat = geopy.distance.distance(distance).destination((lat, long), bearing=180).latitude
        eastLong = geopy.distance.distance(distance).destination((lat, long), bearing=90).longitude
        westLong = geopy.distance.distance(distance).destination((lat, long), bearing=0).longitude

        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT charity.name, charity.url, service.description, location.name, phone_num.phone_number, email.email 
                            From charity
                            INNER JOIN service 
                            ON charity.url = service.url
                            INNER JOIN phone_num 
                            ON service.url = phone_num.url and service.service_id = phone_num.service_id
                            INNER JOIN email
                            ON  service.url = email.url and service.service_id = email.service_id
                            INNER JOIN service_location 
                            ON  service.url = service_location.url and service.service_id = service_location.service_id
                            INNER JOIN location
                            ON service_location.id = location.id
                            WHERE ((cast (location.latitude as double precision)) between %s and %s) and ( (cast(location.longitude as double precision)) between %s and %s);
                            """, (southLat, northLat, westLong, eastLong))
            return cursor.fetchall()
            conn.commit()

        conn.close()

def getCoordinates(location: str):
    try:
      conv = geocode(location, exactly_one=True)
      if conv is not None:
         return conv.latitude, conv.longitude
      return None, None
    except Exception as e:
      print(f"Error: {e}")
      return None, None

if __name__ == "__main__":
    print(getLocations("London", 10))
