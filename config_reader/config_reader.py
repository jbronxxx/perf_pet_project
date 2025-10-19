import yaml
import constants


class ConfigReader:
    def __init__(self):
        self._read_config_file()

    def _read_config_file(self):
        """Read the config file and store it in a dictionary."""
        try:
            with open("app_config.yaml", "r") as stream:
                self._config = yaml.safe_load(stream)
        except FileNotFoundError:
            raise ValueError("Config file not found")
        except PermissionError:
            raise ValueError("Not enough permissions to read config file")

    @property
    def config_file(self):
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
    def log_config(self):
        return self.config_file.get("logging")

    @property
    def log_level(self) -> str:
        """Get the logging level value from the config file."""
        level_value = self.log_config.get("level")
        if not isinstance(level_value, str):
            raise TypeError(
                f"Incorrect type for 'log_level': {type(level_value).__name__}"
            )
        return level_value

    @property
    def root_log_file_path(
        self,
    ) -> str:
        """Get the logs files root path from the config file."""
        root_log_path = constants.LOGS_PATH
        if not isinstance(root_log_path, str):
            raise TypeError(
                f"Incorrect type for 'root_log_file_path': {type(root_log_path).__name__}"
            )
        return root_log_path

    @property
    def log_format(self) -> str:
        """Get the logging format from the config file."""
        formatter_value = self.log_config.get("formatter")
        if not isinstance(formatter_value, str):
            raise TypeError(
                f"Incorrect type for 'formatter': {type(formatter_value).__name__}"
            )
        return formatter_value


config = ConfigReader()
