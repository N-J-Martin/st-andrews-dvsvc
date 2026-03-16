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

""" Selects charities with locations (appears multiple for multiple locations), 
that are within euclidean distance of given location and distance. 
    ordered by distance to location
"""
def get_locations(location: str, distance: int):
    lat, long = get_coordinates(location)
    if lat is None and long is None:
        print(f"Error: No coordinates for location: {location}")
        return []
    else:
        conn = connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""

                                SELECT * from (
                                    SELECT distinct charity.index, charity.name, location.name, charity.url, charity.summary, |/((((cast (location.latitude as double precision)) - %s)^2) + (((cast (location.longitude as double precision)) - %s)^2)) as distance
                                    FROM location
                                    NATURAL JOIN service_location
                                    NATURAL JOIN service
                                    INNER JOIN charity on charity.index = service.index
                                ) temp
                                WHERE distance < %s
                                ORDER BY distance
                                """, (lat, long, distance))
                return cursor.fetchall()
                conn.commit()

            conn.close()
        except Exception as e:
            print(f"Error: {e}")

def get_coordinates(location: str):
    try:
      conv = geocode(location, exactly_one=True)
      if conv is not None:
         return conv.latitude, conv.longitude
      return None, None
    except Exception as e:
      print(f"Error: {e}")
      return None, None


def get_services_by_charity_id(id: int):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT DISTINCT service.description, location.name, email.email, phone_num.phone_number
                FROM charity 
                INNER JOIN service 
                ON charity.index = service.index
                INNER JOIN service_location
                ON service.index = service_location.index and service.service_id = service_location.service_id
                INNER JOIN location
                on service_location.id = location.id
                INNER JOIN email
                on service.index = email.index and  service.service_id = email .service_id
                INNER JOIN phone_num
                on service.index = phone_num.index and service.service_id = phone_num.service_id
                WHERE charity.index = %s

            """,
            (id,)
        )

        return cursor.fetchall()
        conn.commit()
    conn.close()

def get_charity_info_by_id(index: str):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT charity.url, charity.summary, charity_num.charity_number, charity.name
                FROM charity 
                LEFT OUTER JOIN charity_num
                ON charity.index = charity_num.index
                WHERE charity.index = %s

            """,
            (index,)
        )

        return cursor.fetchall()
        conn.commit()
    conn.close()
    
if __name__ == "__main__":
    print(get_services_by_charity_id(0))
    print(get_charity_info_by_id(0))
    print("dist")
    print(get_locations("London", 1000))
