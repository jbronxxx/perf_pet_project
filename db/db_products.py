import constants
from db.db_provider import DBProvider
from logger.logger import CustomLogger

log = CustomLogger(constants.DB_PRODUCTS_LOGS_PATH, module_name="db_products").logger


class DbProduct:
    def __init__(self):
        provider = DBProvider()
        provider.connect()
        self.connection = provider.connection

    def create_product(self, product_name: str, product_price: float):
        if self.connection is None:
            log.error("Connection to database not established")
            raise ConnectionError("Connection to database not established")

        sql = """
            INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                log.info(f"Creating product with name '{product_name}' and price {product_price}")
                cursor.execute(sql, (product_name, product_price))
                self.connection.commit()
                returning_id = cursor.fetchone()[0]

                log.info(f"Product created with id {returning_id}")
                return returning_id
        except Exception as e:
            self.connection.rollback()

            log.error(f"Error creating product: {e}")
            raise RuntimeError(f"Error creating product: {str(e)}")
