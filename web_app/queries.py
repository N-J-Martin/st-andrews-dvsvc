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
        out = []
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
                out =  cursor.fetchall()
                conn.commit()

            conn.close()
            return out
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

""" Gets all service ids under a charity"""
def get_services_by_charity_id(id: int):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT service_id, description
                FROM service
                WHERE index = %s

            """,
            (id,)
        )

        out = cursor.fetchall()
        conn.commit()
    conn.close()
    return out

""" Gets all emails for a service"""
def get_emails_by_service(charity_id: int, service_id:int):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT email
                FROM email
                WHERE index = %s and service_id = %s

            """,
            (charity_id, service_id)
        )

        out = cursor.fetchall()
        conn.commit()
    conn.close()
    return out

""" Gets all phone nums for a service"""
def get_phone_num_by_service(charity_id: int, service_id:int):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT phone_number
                FROM phone_num
                WHERE index = %s and service_id = %s

            """,
            (charity_id, service_id)
        )

        out = cursor.fetchall()
        conn.commit()
    conn.close()
    return out

""" Gets all locations for a service"""
def get_location_by_service(charity_id: int, service_id:int):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT name
                FROM service 
                INNER JOIN service_location USING (index, service_id)
                INNER JOIN location USING (id)
                where index = %s and service_id = %s

            """,
            (charity_id, service_id)
        )

        out = cursor.fetchall()
        conn.commit()
    conn.close()
    return out

""" Collates all service info required for a charity"""
def get_all_service_info_by_charity_id(id: int):
    service_list = get_services_by_charity_id(id)
    out = []
    for s in service_list:
        phone = get_phone_num_by_service(id, s[0])
        email = get_emails_by_service(id, s[0])
        locs = get_location_by_service(id, s[0])
        full = list(s)
        phone = [p[0] for p in phone]
        email = [e[0] for e in email]
        locs = [l[0] for l in locs]
        full.append(phone)
        full.append(email)
        full.append(locs)
        out.append(full)
    return out

""" Gets info just about charity"""
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

        out = cursor.fetchall()
        conn.commit()
    conn.close()
    return out
    
if __name__ == "__main__":
    print(get_all_service_info_by_charity_id(17))
    #print(get_charity_info_by_id(0))
    #print("dist")
    #print(get_locations("London", 1000))
