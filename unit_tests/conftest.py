import sys
import pytest
import requests

import constants
from config_reader.config_reader import config
from logger.logger import CustomLogger

logger = CustomLogger(
    log_file_path=constants.UNIT_TESTS_LOGS_PATH, module_name="unit_tests_conftest"
).logger
HOST = config.local_host


@pytest.fixture
def create_product():
    logger.info(f"Run '{sys._getframe(0).f_code.co_name}' fixture")
    with requests.post(
        f"{HOST}/api/create_product", json={"name": "Test Product", "price": 19.99}
    ) as response:
        return response
