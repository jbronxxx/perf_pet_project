import sys
from typing import Any, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import constants
from config_reader.config_reader import config
from logger.logger import CustomLogger

logger = CustomLogger(
    log_file_path=constants.UNIT_TESTS_LOGS_PATH, module_name="unit_tests_conftest"
).logger
HOST = config.local_host


@pytest.fixture
def mock_create_product_success() -> Generator[MagicMock | AsyncMock, Any, None]:
    logger.info(f"Run '{sys._getframe(0).f_code.co_name}' fixture")
    with patch("app.app.app.test_client") as mock_test_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "mock_name", "price": 19.99}
        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        mock_test_client.return_value = mock_client
        yield mock_test_client
