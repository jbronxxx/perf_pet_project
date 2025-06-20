import constants
import psycopg2
from logger.logger import CustomLogger


log = CustomLogger(log_file_path=constants.DB_PROVIDER_LOGS_PATH, module_name="db_provider").logger

class DBProvider:
    def __init__(self):
        self.connection = None

    def connect(self) -> None:
        log.info("Connecting to the database")
        try:
            self.connection = psycopg2.connect(
                host=constants.DB_HOST,
                user=constants.DB_USER,
                password=constants.DB_PASSWORD,
                database=constants.DB_NAME,
                port=constants.DB_PORT,
            )
            log.info("Connected to the database successfully")
        except psycopg2.Error as e:
            log.error(f"Error connecting to the database: {e}")
            print(f"Couldn't connect to the database: {e}")

    def close(self) -> None:
        log.info("Closing the connection to database")
        if self.connection is not None:
            self.connection.close()

