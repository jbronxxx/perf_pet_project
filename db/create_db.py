import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from constants import DB_HOST, DB_LOGS_PATH, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from logger.logger import CustomLogger

log = CustomLogger(DB_LOGS_PATH, module_name="db_products").logger


def create_db_if_not_exist() -> None:
    try:
        with psycopg2.connect(
            dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        ) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as curs:
                curs.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
                exists = curs.fetchone()

                if not exists:
                    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
                    curs.execute(create_db_query)
                    log.info(f"Database {DB_NAME} created")
                else:
                    log.info(f"Database {DB_NAME} already exists")
    except psycopg2.Error as e:
        log.error(f"An error occurred while creating the database: {e}")
        exit(1)


def create_products_table() -> None:
    try:
        with psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
                """
                )
            log.info("Table created successfully")
    except psycopg2.Error as e:
        log.error(f"An error occurred while creating the table: {e}")
        exit(1)


if __name__ == "__main__":
    create_db_if_not_exist()
    create_products_table()
