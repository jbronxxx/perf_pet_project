import sys
import requests
from requests import Response
from config_reader.config_reader import config_reader
from logger.logger import CustomLogger

log_file_path = config_reader.log_file_path("logs/unit_tests_logs/unit_tests.log")
logger = CustomLogger(log_file_path, module_name="test_app").logger
HOST = config_reader.host


def test_products_list(create_product: None):
    logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
    with requests.get(f"{HOST}/api/get_products_list") as response:
        logger.info(f"Assert that '{response.status_code}' equals 200")
        assert (
            response.status_code == 200
        ), f"Failed to get products list. Response status code: {response.status_code}, text: {response.text}"


def test_create_product(create_product: Response):
    logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
    response = create_product
    logger.info(f"Assert that '{response.status_code}' equals 200")
    assert response.status_code == 200


def test_create_product_invalid_data():
    logger.info(f"Test '{sys._getframe(0).f_code.co_name}' started")
    with requests.post(
        f"{HOST}/api/create_product", json={"name_invalid": 12, "price": 19.99}
    ) as response:
        logger.info(f"Assert that '{response.status_code}' equals 400")
        assert (
            response.status_code == 400
        ), f"Response status code was not 400. Response: {response.text}"
