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
    else:
        northLat = geopy.distance.distance(distance).destination((lat, long), bearing=0).latitude
        southLat = geopy.distance.distance(distance).destination((lat, long), bearing=180).latitude
        eastLong = geopy.distance.distance(distance).destination((lat, long), bearing=90).longitude
        westLong = geopy.distance.distance(distance).destination((lat, long), bearing=0).longitude

        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * from location
                            WHERE ((cast (latitude as double precision)) between %s and %s) and ( (cast(longitude as double precision)) between %s and %s);
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
    getLocations("London", 10)
