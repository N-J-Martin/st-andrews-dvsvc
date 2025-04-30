import psycopg2
from llm_setup import get_db_logger, connect


def create_charity_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS charity CASCADE;
        CREATE TABLE charity(
        url VARCHAR(2048) PRIMARY KEY,
        name VARCHAR (2048) NOT NULL,
        summary VARCHAR(2048)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity' table")


def create_charity_num_table( conn: psycopg2.extensions.connection):
    # make constraint that government either eng or sco ?
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS charity_num CASCADE;
        CREATE TABLE charity_num(
        url VARCHAR(2048) REFERENCES charity(url),
        charity_number VARCHAR(8),
        government varchar(2048) NOT NULL,
        PRIMARY KEY (url, charity_number)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity_num' table")

def create_phone_num_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS phone_num CASCADE;
        CREATE TABLE phone_num(
         url VARCHAR(2048) REFERENCES charity(url),
         phone_number VARCHAR(30),
         PRIMARY KEY(url, phone_number)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'phone_num' table")

def create_email_table( conn: psycopg2.extensions.connection):
    # add email constraints
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS email CASCADE;
        CREATE TABLE email(
         url VARCHAR(2048) REFERENCES charity(url),
         email VARCHAR(2048),
         PRIMARY KEY(url, email)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'email' table")

def create_location_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS location CASCADE;
        CREATE TABLE location(
         id INT PRIMARY KEY ,
         name VARCHAR(2048)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'location' table")

def create_charity_location_table( conn: psycopg2.extensions.connection):
    # add phone number constraints
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS charity_location CASCADE;
        CREATE TABLE charity_location(
          url VARCHAR(2048) REFERENCES charity(url),
          id INT REFERENCES location(id),
          PRIMARY KEY(url, id)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity_location' table")

if __name__ == "__main__":
    LOGGER = get_db_logger()
    conn = connect.connect()
    create_charity_table(conn)
    create_charity_num_table(conn)
    create_phone_num_table(conn)
    create_email_table(conn)
    create_location_table(conn)
    create_charity_location_table(conn)
    conn.close()

