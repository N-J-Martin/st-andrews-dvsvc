from datetime import datetime
import psycopg2

from llm_setup import get_db_logger


LOGGER = get_db_logger()


def insert_charity(
    conn: psycopg2.extensions.connection,
    index: int,
    link: str,
    name: str,
    summary: str | None
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity (index, url, name, summary) values (%s, %s, %s, %s)",
            (
                index, 
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
    index: int,
    id: int,
    description: str | None):

    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service (index, service_id, description) values (%s, %s, %s)",
            (
                index,
                id, 
                description
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert service [index=%s, service=%i]", index, id, 
    )


def insert_charity_number(
    conn: psycopg2.extensions.connection,
    index: int,
    charity_num: str,
    government: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity_num (index, charity_number, government) values (%s, %s, %s)",
            (
                index,
                charity_num,
                government
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity_number [index=%s, number=%s]", index, charity_num,
    )



def insert_phone_num(
    conn: psycopg2.extensions.connection,
    index: int,
    service: int, 
    phone: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into phone_num (index, service_id, phone_number) values (%s, %s, %s)",
            (
                index,
                service,
                phone
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert phone number [index=%s, service=%i, number=%s]", index, service, phone,
    )


def insert_email(
    conn: psycopg2.extensions.connection,
    index: int,
    service: int, 
    email: str,
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into email (index, service_id, email) values (%s, %s, %s)",
            (
                index,
                service,
                email
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert email [index=%s, service=%i, email=%s]", index, service, email,
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
    index: int,
    service: int,
    loc: int
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into service_location (index, service_id,  id) values (%s, %s, %s)",
            (
                index,
                service,
                loc
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity-location [index=%s, service=%i id=%i]", index, service, loc,
    )