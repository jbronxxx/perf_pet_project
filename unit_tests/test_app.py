import sys
from unittest.mock import MagicMock, patch

import constants
from app.app import app
from config_reader.config_reader import config
from logger.logger import CustomLogger

logger = CustomLogger(log_file_path=constants.UNIT_TESTS_LOGS_PATH, module_name="test_app").logger
HOST = config.local_host


class TestApp:
    @patch("app.app.db_product.get_all_products")
    def test_products(self, mock_get_all_products_from_db: MagicMock):
        logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
        mock_bd_products = {
            "products": [
                {"id": 1, "name": "Test_product_1", "price": 19.99},
                {"id": 2, "name": "Test_product_2", "price": 29.99},
            ],
            "totalItems": 2,
        }

        mock_get_all_products_from_db.return_value = mock_bd_products

        client = app.test_client()
        response = client.get("/api/products?page=1&limit=2")

        logger.info("Assert response.status_code is '200'")
        assert response.status_code == 200

        expected_response_json = {
            "metaInformation": {
                "currentPage": 1,
                "limit": 2,
                "totalItems": 2,
                "totalPages": 1,
            },
            "products": mock_bd_products["products"],
        }
        logger.info("Assert response.json is expected")
        assert response.json == expected_response_json
        mock_get_all_products_from_db.assert_called_once_with(limit=2, offset=0)

    @patch("app.app.db_product.create_product")
    def test_add_product(self, mock_create_db_product: MagicMock):
        logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
        mock_create_db_product.return_value = 1
        json = {"name": "Test Product", "price": 19.99}
        expected_json = {"id": 1, "name": "Test Product", "price": 19.99}
        client = app.test_client()

        response = client.post("/api/add-product", json=json)

        logger.info(f"Assert that '{response.status_code}' equals 200")
        assert response.status_code == 200

        logger.info(f"Assert response.json is '{expected_json}'")
        assert response.json == expected_json
        mock_create_db_product.assert_called_once_with(name="Test Product", price=19.99)

    # TODO: Update test
    @patch("app.app.db_product.create_product")
    def test_add_product_invalid_data(self):
        expected_error_text = {
            "error": 'Invalid request format. Must include "name" and "price" fields.'
        }

        logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
        client = app.test_client()

        response = client.post("/api/create_product", json={"name_invalid": 12, "price": 19.99})

        logger.info(f"Assert that '{response.status_code}' equals 400")
        assert (
            response.status_code == 400
        ), f"Response status code was not 400. Response: {response.text}"
        assert response.json == expected_error_text
