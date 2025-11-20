from typing import Any

from psycopg2.extras import DictCursor

from constants import DB_LOGS_PATH
from db.db_provider import DBProvider
from logger.logger import CustomLogger

log = CustomLogger(DB_LOGS_PATH, module_name="db_products").logger


class DbProduct:
    def __init__(self):
        self.provider = DBProvider()
        self.provider.connect()
        self.connection = self.provider.connection

    def create_product(self, name: str, price: float) -> int | None:
        self.provider.check_connection()

        sql = """
            INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                if not self.get_product_by_name(name):
                    log.info(f"Creating product with name '{name}' and price {price}")
                    cursor.execute(sql, (name, price))
                    self.connection.commit()
                    returning_id = cursor.fetchone()[0]

                    log.info(f"Product created with id {returning_id}")
                    return returning_id
                else:
                    log.warning(f"Product with name '{name}' already exists")
                    return None
        except Exception as e:
            self.connection.rollback()

            log.error(f"Failed creating product: {e}")
            raise RuntimeError(f"Failed creating product: {str(e)}")

    def get_product_by_name(self, product_name: str) -> dict | None:
        self.provider.check_connection()

        sql = """
            SELECT id, name, price FROM products WHERE name = %s;
        """

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                log.info(f"Searching product with name: '{product_name}'")
                cursor.execute(sql, (product_name,))
                product = cursor.fetchone()

                if product:
                    log.info(f"Found product with name: '{product_name}'")
                    return dict(product)
                else:
                    log.info(f"Product with name '{product_name}' not found")
                    return None
        except Exception as e:
            log.error(f"Failed getting product: {e}")
            raise RuntimeError(f"Failed getting product: {str(e)}")

    def get_product_by_id(self, product_id: int) -> dict | None:
        self.provider.check_connection()

        sql = """SELECT id, name, price FROM products WHERE id = %s;"""

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                log.info(f"Searching product with id: '{product_id}'")
                cursor.execute(sql, (product_id,))
                product = cursor.fetchone()

                if product:
                    log.info(f"Product with id: {product_id} is found")
                    return dict(product)
                else:
                    log.info(f"Product with id: {product_id} not found")
                    return None
        except Exception as e:
            log.error(f"Failed getting product with id: {e}")
            raise RuntimeError(f"Failed getting product: {str(e)}")

    def get_all_products(self, limit: int, offset: int) -> dict[str, list[dict[str, Any]]]:
        self.provider.check_connection()

        sql = """SELECT id, name, price FROM products ORDER BY id LIMIT %s OFFSET %s;"""
        count_sql = """SELECT COUNT(*) FROM products"""

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                log.info("Getting all products")
                cursor.execute(
                    sql,
                    (
                        limit,
                        offset,
                    ),
                )
                products = cursor.fetchall()

                cursor.execute(count_sql)
                total_items = cursor.fetchone()[0]

                log.info("Returning products list")
                result_products = [dict(product) for product in products]

                return {"products": result_products, "totalItems": total_items}

        except Exception as e:
            log.error(f"Failed getting products list: {e}")
            raise RuntimeError(f"Failed getting products list: {str(e)}")
