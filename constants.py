import os
import sys
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

# local_host from .env
LOCAL_HOST = os.getenv("LOCAL_HOST")

# DataBase settings from .env
DB_TYPE = os.getenv("DB_TYPE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")

# logs paths
LOGS_PATH = os.path.join(ROOT_PATH, "logs")
APP_LOGS_PATH = f"{LOGS_PATH}/app_logs/app.log"
UNIT_TESTS_LOGS_PATH = f"{LOGS_PATH}/unit_tests_logs/unit_tests.log"
DB_PROVIDER_LOGS_PATH = f"{LOGS_PATH}/db_logs/db_provider.log"
DB_PRODUCTS_LOGS_PATH = f"{LOGS_PATH}/db_logs/products_db.log"
