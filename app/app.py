import math

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
        log.error(f"An unexpected error occurred while creating a product: {e}'")
        return jsonify({"error": "An internal server error occurred."}), 500

    log.info(f"Created product: id: {returning_id}, name: {name}, price: {price}")
    return jsonify({"id": returning_id, "name": name, "price": price})


@app.route("/api/get_products", methods=["GET"])
def get_products() -> tuple[Response, int] | Response:
    try:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        if page <= 0 or limit <= 0:
            log.info("Page and limit must be positive integers")
            return jsonify({"error": "Page and limit must be positive integers"}), 400
    except (ValueError, TypeError):
        log.error("Invalid page or limit value")
        return jsonify({"error": "Invalid page or limit value"}), 400

    offset = (page - 1) * limit

    try:
        products = db_product.get_all_products(limit=limit, offset=offset)
        products_list = products.get("products", [])
        total_items = products.get("totalItems", 0)
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

        final_response = {
            "totalItems": total_items,
            "totalPages": total_pages,
            "currentPage": page,
            "limit": limit,
            "products": products_list,
        }

        log.info("Returning all products list")
        return jsonify(final_response)

    except OperationalError as e:
        log.warning(f"Database connection error: {e}")
        return jsonify({"error": "The database currently unavailable"}), 503

    except Exception as e:
        log.error(f"An unexpected error occurred while getting products list: {e}'")
        return jsonify({"error": "An internal server error occurred."}), 500


@app.route("/api/get_product/<product_id>", methods=["GET"])
def get_product_by_id(product_id) -> tuple[Response, int] | Response:
    try:
        expected_product_id = int(product_id)
    except ValueError:
        log.error(f"Invalid product ID format: {product_id}. Expected integer.")
        return jsonify({"error": "Invalid product ID format. Expected a number."}), 400

    try:
        product = db_product.get_product_by_id(expected_product_id)

        if not product:
            log.info(f"Product with id: {expected_product_id} not found")
            return jsonify({"error": f"Product with id: {expected_product_id} not found"}), 404

        log.info(f"Returning product with id: {expected_product_id}")
        return jsonify(product)

    except OperationalError as e:
        log.warning(f"Database connection error: {e}")
        return jsonify({"error": "The database currently unavailable"}), 503

    except Exception as e:
        log.error(f"An unexpected error occurred while getting product with id: {product_id}: {e}'")
        return jsonify({"error": "An internal server error occurred."}), 500
