from constants import DB_LOGS_PATH
from db.db_provider import DBProvider
from logger.logger import CustomLogger

log = CustomLogger(DB_LOGS_PATH, module_name="db_products").logger


class DbProduct:
    def __init__(self):
        provider = DBProvider()
        provider.connect()
        self.connection = provider.connection

    def create_product(self, product_name: str, product_price: float) -> int | None:
        if self.connection is None:
            log.error("Connection to database not established")
            raise ConnectionError("Connection to database not established")

        sql = """
            INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                if not self.get_product_by_name(product_name):
                    log.info(
                        f"Creating product with name '{product_name}' and price {product_price}"
                    )
                    cursor.execute(sql, (product_name, product_price))
                    self.connection.commit()
                    returning_id = cursor.fetchone()[0]

                    log.info(f"Product created with id {returning_id}")
                    return returning_id
                else:
                    log.warning(f"Product with name '{product_name}' already exists")
                    return None
        except Exception as e:
            self.connection.rollback()

            log.error(f"Error creating product: {e}")
            raise RuntimeError(f"Error creating product: {str(e)}")

    def get_product_by_name(self, product_name: str) -> dict | None:
        if self.connection is None:
            log.error("Connection to database not established")
            raise ConnectionError("Connection to database not established")

        sql = """
            SELECT id, name, price FROM products WHERE name = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                log.info(f"Searching product with name: '{product_name}'")
                cursor.execute(sql, (product_name,))
                product = cursor.fetchone()

                if product:
                    log.info(f"Found product with name: '{product_name}'")
                    return {"id": product[0], "name": product[1], "price": product[2]}
                else:
                    log.info(f"Product with name '{product_name}' not found")
                    return None
        except Exception as e:
            log.error(f"Error getting product: {e}")
            raise RuntimeError(f"Error getting product: {str(e)}")
