import constants
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = constants.DB_NAME
DB_USER = constants.DB_USER
DB_PASSWORD = constants.DB_PASSWORD
DB_HOST = constants.DB_HOST
DB_PORT = constants.DB_PORT

# 1. Connect to postgres
conn = psycopg2.connect(
    dbname="postgres",
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# 2. Create DB if not exists
cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
exists = cursor.fetchone()
if not exists:
    cursor.execute(f'CREATE DATABASE {DB_NAME}')
    print(f"Database {DB_NAME} created")
else:
    print(f"Database {DB_NAME} already exists")

cursor.close()
conn.close()

# 3. Connect to the new DB and create a table
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);
""")

conn.commit()
cursor.close()
conn.close()
print("Table created successfully")
