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
            "insert into charity (url, name, summary) values (%s, %s, %s)",
            (
                link,
                name, 
                summary
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity [url=%s, name=%s]", link, name, 
    )


def insert_service(conn: psycopg2.extensions.connection,
    link: str,
    id: int,
    description: str | None):

    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service (url, service_id, description) values (%s, %s, %s)",
            (
                link,
                id, 
                description
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert service [url=%s, service=%i]", link, id, 
    )


def insert_charity_number(
    conn: psycopg2.extensions.connection,
    link: str,
    charity_num: str,
    government: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity_num (url, charity_number, government) values (%s, %s, %s)",
            (
                link,
                charity_num,
                government
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity_number [url=%s, number=%s]", link, charity_num,
    )



def insert_phone_num(
    conn: psycopg2.extensions.connection,
    link: str,
    service: int, 
    phone: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into phone_num (url, service_id, phone_number) values (%s, %s, %s)",
            (
                link,
                service,
                phone
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert phone number [url=%s, service=%i, number=%s]", link, service, phone,
    )


def insert_email(
    conn: psycopg2.extensions.connection,
    link: str,
    service: int, 
    email: str,
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into email (url, service_id, email) values (%s, %s, %s)",
            (
                link,
                service,
                email
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert email [url=%s, service=%i, email=%s]", link, service, email,
    )


def insert_location(
    conn: psycopg2.extensions.connection,
    id: int,
    name: str,
    lat: str,
    long: str
):
    
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into location (id, name, latitude, longitude) values (%s, %s, %s, %s)",
            (
                id,
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
    id: int,
    name: str
):
    
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into location (id, name, latitude, longitude) values (%s, %s, NULL, NULL)",
            (
                id,
                name,     
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert location [name=%s]", name,
    )


def insert_service_location(
    conn: psycopg2.extensions.connection,
    link: str,
    service: int,
    loc: int
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service_location (url, service_id,  id) values (%s, %s, %s)",
            (
                link,
                service,
                loc
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity-location [url=%s, service=%i id=%i]", link, service, loc,
    )