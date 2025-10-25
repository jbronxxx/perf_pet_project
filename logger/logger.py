import logging
import sys
import os
from config_reader.config_reader import config


class CustomLogger:
    def __init__(self, log_file_path: str = None, module_name: str = None) -> None:
        self._logger = logging.getLogger(module_name)
        self._logger.setLevel(config.log_level)

        formatter = logging.Formatter(config.log_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            file_handler = logging.FileHandler(log_file_path, encoding="utf8", mode="a")
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger
