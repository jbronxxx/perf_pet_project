import sys
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

import constants
from config_reader.config_reader import config
from logger.logger import CustomLogger

logger = CustomLogger(
    log_file_path=constants.UNIT_TESTS_LOGS_PATH, module_name="unit_tests_conftest"
).logger
HOST = config.local_host


@pytest.fixture
def mock_db_create_product() -> Generator[MagicMock, Any, None]:
    logger.info(f"Run '{sys._getframe(0).f_code.co_name}' fixture")
    with patch("app.app.db_product.create_product") as mock_db:
        yield mock_db


# @pytest.fixture
# def mock_get_all_products_from_db() -> Generator[MagicMock, Any, None]:
#     logger.info(f"Run '{sys._getframe(0).f_code.co_name}' fixture")
#     with patch("app.app.db_product.get_all_products") as mock_db:
#         yield mock_db
