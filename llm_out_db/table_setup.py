import psycopg2
from llm_setup import get_db_logger, connect


def create_charity_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE charity(
        url VARCHAR(2048) PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        summary VARCHAR(2048)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity' table")


def create_charityNum_table( conn: psycopg2.extensions.connection):
    # make constraint that government either eng or sco ?
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE charityNum(
        url VARCHAR(2048) FOREIGN KEY REFERENCES charity(url),
        charity_number VARCHAR(8),
        government varchar(3) NOT NULL
        PRIMARY KEY (url, charity_number)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charityNum' table")

def create_phoneNum_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE phoneNum(
         url VARCHAR(2048) FOREIGN KEY REFERENCES charity(url),
         phone_number VARCHAR(15)
         PRIMARY KEY(url, phone_number)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'phoneNum' table")

def create_email_table( conn: psycopg2.extensions.connection):
    # add email constraints
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE email(
         url VARCHAR(2048) FOREIGN KEY REFERENCES charity(url),
         email VARCHAR(30)
         PRIMARY KEY(url, email)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'email' table")

def create_location_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE location(
         id INT PRIMARY KEY AUTOINCREMENT,
         name VARCHAR(30)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'location' table")

def create_charityLocation_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE charityLocation(
          url VARCHAR(2048) FOREIGN KEY REFERENCES charity(url),
          id INT FOREIGN KEY REFERENCES location(id),
          PRIMARY KEY (url, int)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charityLocation' table")

if __name__ == "__main__":
    LOGGER = get_db_logger()
    conn = connect.connect()
    create_charity_table(conn)
    create_charityNum_table(conn)
    create_phoneNum_table(conn)
    create_email_table(conn)
    create_location_table(conn)
    create_charityLocation_table(conn)

