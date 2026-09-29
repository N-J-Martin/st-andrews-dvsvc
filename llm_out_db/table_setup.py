import psycopg2
from llm_setup import get_db_logger, connect
CHARITY_NUM_LENGTH = 8
MAX_STR_LENGTH = 2048 
PHONE_LENGTH = 30

def create_charity_table( conn: psycopg2.extensions.connection):
    # url regex from https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS charity CASCADE;
        CREATE TABLE charity(
        charity_id SERIAL PRIMARY KEY,
        url VARCHAR({MAX_STR_LENGTH}),
        name VARCHAR ({MAX_STR_LENGTH}) NOT NULL,
        summary VARCHAR({MAX_STR_LENGTH}),
        CHECK ( url ~ '(https://www.|http://www.|https://|http://)?[a-zA-Z]{{2,}}(.[a-zA-Z]{{2,}})(.[a-zA-Z]{{2,}})?/[a-zA-Z0-9]{{2,}}|((https://www.|http://www.|https://|http://)?[a-zA-Z]{{2,}}(.[a-zA-Z]{{2,}})(.[a-zA-Z]{{2,}})?)|(https://www.|http://www.|https://|http://)?[a-zA-Z0-9]{{2,}}.[a-zA-Z0-9]{{2,}}.[a-zA-Z0-9]{{2,}}(.[a-zA-Z0-9]{{2,}})?')
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity' table")

def create_service_table(conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            DROP TABLE IF EXISTS service CASCADE;
            CREATE TABLE service(
                service_id SERIAL PRIMARY KEY,
                charity_id INT REFERENCES charity(charity_id) ON UPDATE CASCADE ON DELETE CASCADE,
                description VARCHAR({MAX_STR_LENGTH})
            );""")
        
        
        conn.commit()
    
    LOGGER.info("Attempted to create 'service' table")
        
def create_charity_num_table( conn: psycopg2.extensions.connection):
    # improve charity number regex - current 1-8 alphanumeric digits
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS charity_num CASCADE;
        CREATE TABLE charity_num(
        charity_num_id SERIAL PRIMARY KEY,
        charity_id INT REFERENCES charity(charity_id) ON UPDATE CASCADE ON DELETE CASCADE,
        charity_number VARCHAR({CHARITY_NUM_LENGTH}) NOT NULL,
        government varchar({MAX_STR_LENGTH}) NOT NULL,
        UNIQUE (charity_id, charity_number),
        UNIQUE (charity_id, government),
        CHECK (government = 'england_wales' OR government = 'scotland' OR government = 'northern_ireland'),
        CHECK (charity_number ~ '[a-zA-z0-9]{{1,{CHARITY_NUM_LENGTH}}}')
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'charity_num' table")

def create_phone_num_table( conn: psycopg2.extensions.connection):
    # using E164 phone number format as is international standard
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS phone_num CASCADE;
        CREATE TABLE phone_num(
         phone_id SERIAL PRIMARY KEY,
         service_id INT REFERENCES service(service_id) ON UPDATE CASCADE ON DELETE CASCADE,    
         phone_number VARCHAR({PHONE_LENGTH}),
         UNIQUE (service_id, phone_number),
         CHECK ( phone_number ~ '\+[0-9]{{0,15}}' )
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'phone_num' table")

def create_email_table( conn: psycopg2.extensions.connection):
    # email regex from https://www.geeksforgeeks.org/how-to-validate-email-address-using-regexp-in-javascript/
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS email CASCADE;
        CREATE TABLE email(
         email_id SERIAL PRIMARY KEY,
         service_id INT REFERENCES service(service_id) ON UPDATE CASCADE ON DELETE CASCADE,
         email VARCHAR({MAX_STR_LENGTH}),
         UNIQUE(service_id, email),
         CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$')
        );
        """)
        conn.commit()
    
    LOGGER.info("Attempted to create 'email' table")

def create_location_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS location CASCADE;
        CREATE TABLE location(
         location_id INT PRIMARY KEY,
         name VARCHAR({MAX_STR_LENGTH}),
         latitude VARCHAR({MAX_STR_LENGTH}),
         longitude VARCHAR({MAX_STR_LENGTH})
        );""")

        conn.commit()
    
    LOGGER.info("Attempted to create 'location' table")

def create_service_location_table( conn: psycopg2.extensions.connection):
    with conn.cursor() as cursor:
        cursor.execute(f"""
        DROP TABLE IF EXISTS service_location CASCADE;
        CREATE TABLE service_location(
          service_id INT REFERENCES service(service_id) ON UPDATE CASCADE ON DELETE CASCADE,
          location_id INT REFERENCES location(location_id) ON UPDATE CASCADE ON DELETE CASCADE,
          PRIMARY KEY(service_id, location_id)
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

