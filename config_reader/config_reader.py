from typing import Any

import yaml

from constants import CONFIG_PATH


class ConfigReader:
    def __init__(self):
        self._read_config_file()

    def _read_config_file(self) -> None:
        """Read the config file and store it in a dictionary."""
        try:
            with open(CONFIG_PATH, "r") as stream:
                self._config = yaml.safe_load(stream)
        except FileNotFoundError:
            raise ValueError(f"Config file not found at: {CONFIG_PATH}")
        except PermissionError:
            raise ValueError("Not enough permissions to read config file")

    @property
    def config_file(self) -> dict[str, Any]:
        return self._config

    @property
    def local_host(self) -> str:
        """Get the local_host value from the config file."""
        host_value = self.config_file.get("local_host")
        if not isinstance(host_value, str):
            raise TypeError(
                f"Incorrect type for 'local_host': {type(host_value).__name__}"
            )
        return host_value

    @property
    def log_config(self) -> dict | None:
        """Get the logging section from the config file."""
        return self.config_file.get("logging")

    @property
    def log_level(self) -> str:
        """Get the logging level value from the config file."""
        if self.log_config is None:
            raise ValueError("'logging' section not found in config file")
        level_value = self.log_config.get("level")
        if not isinstance(level_value, str):
            raise TypeError(
                f"Incorrect type for 'log_level': {type(level_value).__name__}"
            )
        return level_value

    @property
    def log_format(self) -> str:
        """Get the logging format from the config file."""
        if self.log_config is None:
            raise ValueError("'logging' section not found in config file")
        formatter_value = self.log_config.get("formatter")
        if not isinstance(formatter_value, str):
            raise TypeError(
                f"Incorrect type for 'formatter': {type(formatter_value).__name__}"
            )
        return formatter_value


config = ConfigReader()
