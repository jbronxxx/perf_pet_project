import logging
import sys
from config_reader import config_reader


log_level = config_reader.logging_level
log_format = config_reader.logging_format


class CustomLogger:
    def __init__(self, log_file_path: str):
        self.logger = logging.getLogger(f"{__name__}")
        self.logger.setLevel(log_level)

        formatter = logging.Formatter(log_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file_path, encoding="utf8", mode="a")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
