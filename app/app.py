from flask import Flask, Response, jsonify, request
from psycopg2 import OperationalError

from constants import APP_LOGS_PATH
from db.db_products import DbProduct
from logger.logger import CustomLogger

log = CustomLogger(log_file_path=APP_LOGS_PATH, module_name="app").logger

log.info("Starting app")
app = Flask(__name__)
db_product = DbProduct()


@app.route("/api/create_product", methods=["POST"])
def create_product() -> tuple[Response, int] | Response:
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must be a valid JSON"}), 400

    try:
        name = data.get("name")
        price = data.get("price")

        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Field 'name' must be a non-empty string"}), 400

        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Field 'price' must be a positive number"}), 400

        returning_id = db_product.create_product(name, price)

        if returning_id is None:
            log.warning(f"Attempted to create a product with a duplicate name: {name}")
            return jsonify({"error": f"Product with the name '{name}' already exists"}), 409

    except OperationalError as e:
        log.warning(f"Database connection error: {e}")
        return jsonify({"error": "The database currently unavailable"}), 503

    except Exception as e:
        log.error(f"An unexpected error occurred while creating a product '{name}': {e}'")
        return jsonify({"error": "An internal server error occurred."}), 500

    log.info(f"Created product: id: {returning_id}, name: {name}, price: {price}")
    return jsonify({"id": returning_id, "name": name, "price": price})

# @app.route("/api/get_products_list", methods=["GET"])
# def get_product_list():
#     if not products:
#         log.error("Products list is empty")
#         return jsonify({"error": "Products list is empty."}), 422
#     else:
#         product_ids = sorted(list(products.keys()))
#         products_list = []
#         for id in product_ids:
#             if "name" not in products[id] or "price" not in products[id]:
#                 log.warning(f"Product {id} has incomplete data")
#                 continue
#
#             product_data = {
#                 "id": id,
#                 "name": products[id]["name"],
#                 "price": products[id]["price"],
#             }
#             products_list.append(product_data)
#         log.info(f"Return all products: {products_list}")
#         return jsonify(products_list)
#
#
# @app.route("/api/get_product/<product_id>", methods=["GET"])
# def get_product_by_id(product_id):
#     try:
#         product_id = int(product_id)
#
#         if (
#             product_id in products
#             and "name" in products[product_id]
#             and "price" in products[product_id]
#         ):
#             log.info(f"Return product {product_id}")
#             return jsonify(
#                 {
#                     "id": product_id,
#                     "name": products[product_id]["name"],
#                     "price": products[product_id]["price"],
#                 }
#             )
#         else:
#             log.warning(f"Product {product_id} not found")
#             return jsonify({"error": f"Product with ID '{product_id}' not found."}), 404
#
#     except ValueError:
#         log.error("Invalid product ID format. Expected integer.")
#         return jsonify({"error": "Invalid product ID format. Expected a number."}), 400
