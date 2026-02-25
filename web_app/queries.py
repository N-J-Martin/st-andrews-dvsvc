import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
PORT = os.environ["DB_PORT"]

def connect() -> psycopg2.extensions.connection:

    print("Connecting to PostgreSQL database with: %s", locals())
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
        print("Failed to connect to PostgreSQL database: %s", error)

def getLocations():
     conn = connect()
     with conn.cursor() as cursor:
        cursor.execute("SELECT * from location;")
        print(cursor.fetchall())
        conn.commit()

     conn.close()

if __name__ == "__main__":
    getLocations()
