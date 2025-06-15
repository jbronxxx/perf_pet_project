import sys
import pytest
import requests

from config_reader import config_reader
from logger import CustomLogger


log_file_path = config_reader.log_file_path(path="logs/unit_tests.log")
logger = CustomLogger(log_file_path).logger
HOST = config_reader.host


@pytest.fixture
def create_product():
    logger.info(f"Run '{sys._getframe(0).f_code.co_name}' fixture")
    with requests.post(
        f"{HOST}/api/create_product", json={"name": "Test Product", "price": 19.99}
    ) as response:
        return response
