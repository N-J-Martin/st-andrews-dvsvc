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
        "Attempted to insert charity [url=%s, name=%s]", url, name, 
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
    phone: str
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into phone_num (url, phone_number) values (%s, %s)",
            (
                link,
                phone
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert phone number [url=%s, number=%s]", link, phone
    )


def insert_email(
    conn: psycopg2.extensions.connection,
    link: str,
    email: str,
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity (url, email) values (%s, %s)",
            (
                link,
                email
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert email [url=%s, email=%s]", link, email
    )


def insert_location(
    conn: psycopg2.extensions.connection,
    name: str,
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity (name) values (%s)",
            (
                name
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert location [name=%s]", name
    )


def insert_charity(
    conn: psycopg2.extensions.connection,
    link: str,
    loc: int
):
    with conn.cursor() as cursor:
        cursor.execute(
            "insert into charity (url, id) values (%s, %s)",
            (
                link,
                loc
            ),
        )

        conn.commit()

    LOGGER.info(
        "Attempted to insert charity-location [url=%s, id=%i]", link, loc
    )