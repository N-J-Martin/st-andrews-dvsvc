import psycopg2
from llm_setup import get_db_logger, connect


def create_charity_table( conn: psycopg2.extensions.connection):
    # url regex from https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS charity CASCADE;
        CREATE TABLE charity(
        url VARCHAR(2048) PRIMARY KEY,
        name VARCHAR (2048) NOT NULL,
        summary VARCHAR(2048),
        CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?')
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity' table")

def create_service_table(conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS service CASCADE;
            CREATE TABLE service(
                url VARCHAR(2048) REFERENCES charity(url),
                service_id INT,
                description VARCHAR(2048),
                PRIMARY KEY (url, service_id)
            );
                       """)
        
        
        conn.commit()
    
    LOGGER.info("Attempted to create 'service' table")
        
def create_charity_num_table( conn: psycopg2.extensions.connection):
    # improve charity number regex - current 1-8 alphanumeric digits
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS charity_num CASCADE;
        CREATE TABLE charity_num(
        url VARCHAR(2048) REFERENCES charity(url),
        charity_number VARCHAR(8) NOT NULL,
        government varchar(2048) NOT NULL,
        PRIMARY KEY (url, charity_number),
        CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?'),
        CHECK (government = 'england_wales' OR government = 'scotland' OR government = 'northern_ireland'),
        CHECK (charity_number ~ '[a-zA-z0-9]{1,8}')
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity_num' table")

def create_phone_num_table( conn: psycopg2.extensions.connection):
    # using E164 phone number format as is international standard
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS phone_num CASCADE;
        CREATE TABLE phone_num(
         url VARCHAR(2048),
         service_id INT,    
         phone_number VARCHAR(30),
         FOREIGN KEY (url, service_id) REFERENCES service(url, service_id),
         PRIMARY KEY(url, service_id, phone_number),
         CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?'),
         CHECK ( phone_number ~ '\+[0-9]{0,15}' )
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'phone_num' table")

def create_email_table( conn: psycopg2.extensions.connection):
    # email regex from https://www.geeksforgeeks.org/how-to-validate-email-address-using-regexp-in-javascript/
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS email CASCADE;
        CREATE TABLE email(
         url VARCHAR(2048),
         service_id INT,
         email VARCHAR(2048),
         FOREIGN KEY (url, service_id) REFERENCES service(url, service_id),
         PRIMARY KEY(url, service_id, email),
         CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?'),
         CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
        );
        """)
        conn.commit()
    
    LOGGER.info("Attempted to create 'email' table")

def create_location_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS location CASCADE;
        CREATE TABLE location(
         id INT PRIMARY KEY ,
         name VARCHAR(2048)
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'location' table")

def create_service_location_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS service_location CASCADE;
        CREATE TABLE service_location(
          url VARCHAR(2048),
          service_id INT,
          id INT REFERENCES location(id),
          FOREIGN KEY (url, service_id) REFERENCES service(url, service_id),
          PRIMARY KEY(url, service_id, id),
          CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?')

        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'service_location' table")

if __name__ == "__main__":
    LOGGER = get_db_logger()
    conn = connect.connect()
    create_charity_table(conn)
    create_service_table(conn)
    create_charity_num_table(conn)
    create_phone_num_table(conn)
    create_email_table(conn)
    create_location_table(conn)
    create_service_location_table(conn)
    conn.close()

