from flask import Flask, jsonify, request
from config_reader import config_reader
from logger import CustomLogger

log_file_path = config_reader.log_file_path(path="logs/app.log")
logger = CustomLogger(log_file_path).logger
app = Flask(__name__)
products = {}


@app.route("/api/create_product", methods=["POST"])
def create_product():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        logger.error("Invalid request format. Must include 'name' and 'price'")
        return (
            jsonify(
                {
                    "error": 'Invalid request format. Must include "name" and "price" fields.'
                }
            ),
            400,
        )
    product_id = len(products) + 1
    products[product_id] = data
    logger.info(
        f"Created product: id: {product_id}, name: {data['name']}, price: {data['price']}"
    )
    return jsonify({"id": product_id, "name": data["name"], "price": data["price"]})


@app.route("/api/get_products_list", methods=["GET"])
def get_product_list():
    if not products:
        logger.error("Products list is empty")
        return jsonify({"error": "Products list is empty."}), 422
    else:
        product_ids = sorted(list(products.keys()))
        products_list = []
        for id in product_ids:
            if "name" not in products[id] or "price" not in products[id]:
                logger.warning(f"Product {id} has incomplete data")
                continue

            product_data = {
                "id": id,
                "name": products[id]["name"],
                "price": products[id]["price"],
            }
            products_list.append(product_data)
        logger.info(f"Return all products: {products_list}")
        return jsonify(products_list)


@app.route("/api/get_product/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product_id = int(product_id)

        if (
            product_id in products
            and "name" in products[product_id]
            and "price" in products[product_id]
        ):
            return jsonify(
                {
                    "id": product_id,
                    "name": products[product_id]["name"],
                    "price": products[product_id]["price"],
                }
            )
        else:
            logger.warning(f"Product {product_id} not found")
            return jsonify({"error": f"Product with ID '{product_id}' not found."}), 404

    except ValueError:
        logger.error("Invalid product ID format. Expected integer.")
        return jsonify({"error": "Invalid product ID format. Expected a number."}), 400


if __name__ == "__main__":
    app.run(debug=config_reader.logging_level)
