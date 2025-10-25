import sys

import pytest

import constants
from app.app import app
from config_reader.config_reader import config
from logger.logger import CustomLogger

logger = CustomLogger(log_file_path=constants.UNIT_TESTS_LOGS_PATH, module_name="test_app").logger
HOST = config.local_host


class TestApp:
    @pytest.mark.skip("'/api/get_products_list' route is not implemented yet")
    def test_products_list(self, mock_create_product_success):
        logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
        client = app.test_client()

        response = client.get("/api/get_products_list")

        assert response.status_code == 200, (
            f"Failed to get products list."
            f" Response status code: {response.status_code}, text: {response.text}"
        )

    def test_create_product(self, mock_create_product_success):
        logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
        client = app.test_client()

        response = client.post("/api/create_product", json={"name": "Test Product", "price": 19.99})

        logger.info(f"Assert that '{response.status_code}' equals 200")
        assert response.status_code == 200

    def test_create_product_invalid_data(self):
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
