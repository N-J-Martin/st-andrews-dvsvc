from datetime import datetime
import psycopg2

from llm_setup import get_db_logger


LOGGER = get_db_logger()


def insert_charity(
    conn: psycopg2.extensions.connection,
    link: str,
    name: str,
    summary: str | None
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity (url, name, summary) values (%s, %s, %s) returning charity_id",
            (
                link,
                name, 
                summary
            ),
        )
        charity_id = cursor.fetchone()[0]
        conn.commit()

    LOGGER.info(
        "Attempted to insert charity [url=%s, name=%s]", link, name, 
    )

    return charity_id


def insert_service(conn: psycopg2.extensions.connection,
    charity_id: int,
    description: str | None):

    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service (charity_id, description) values (%s, %s) returning service_id",
            (
                charity_id, 
                description
            ),
        )
        service_id = cursor.fetchone()[0]
        conn.commit()

    LOGGER.info(
        "Attempted to insert service [charity=%s, service=%i]", charity_id, id, 
    )

    return service_id


def insert_charity_number(
    conn: psycopg2.extensions.connection,
    charity_id: int,
    charity_num: str,
    government: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity_num (charity_id, charity_number, government) values (%s, %s, %s)",
            (
                charity_id,
                charity_num,
                government
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity_number [charity_id=%s, number=%s]", charity_id, charity_num,
    )



def insert_phone_num(
    conn: psycopg2.extensions.connection,
    service: int, 
    phone: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into phone_num (service_id, phone_number) values (%s, %s)",
            (
                service,
                phone
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert phone number [service=%i, number=%s]", service, phone,
    )


def insert_email(
    conn: psycopg2.extensions.connection,
    service: int, 
    email: str,
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into email (service_id, email) values (%s, %s)",
            (
                service,
                email
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert email [service=%i, email=%s]", service, email,
    )


def insert_location(
    conn: psycopg2.extensions.connection,
    location_id: int,
    name: str,
    lat: str,
    long: str
):
    
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into location (location_id, name, latitude, longitude) values (%s, %s, %s, %s)",
            (
                location_id,
                name,
                lat,
                long
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert location [name=%s]", name,
    )

def insert_location_no_coords(
    conn: psycopg2.extensions.connection,
    location_id: int,
    name: str
):
    
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into location (location_id, name, latitude, longitude) values (%s, %s, NULL, NULL)",
            (
                location_id,
                name,     
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert location [name=%s]", name,
    )


def insert_service_location(
    conn: psycopg2.extensions.connection,
    service: int,
    loc: int
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service_location ( service_id,  location_id) values (%s, %s)",
            (
                service,
                loc
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity-location [service=%i id=%i]", service, loc,
    )