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
    def logging_config(self):
        return self.config_file.get("logging")

    @property
    def host(self) -> str:
        """Get the host value from the config file."""
        host_value = constants.HOST
        if not isinstance(host_value, str):
            raise TypeError(
                f"Incorrect type for type for 'host': {type(host_value).__name__}"
            )
        return host_value

    @property
    def logging_level(self) -> str:
        """Get the logging level value from the config file."""
        level_value = self.logging_config.get("level")
        if not isinstance(level_value, str):
            raise TypeError(
                f"Incorrect type for type for 'logging.level': {type(level_value).__name__}"
            )
        return level_value

    @property
    def log_file_paths(
        self,
    ) -> list[str]:
        """Get the log file paths from the config file."""
        paths = self.config_file.get("log_file_paths")
        if not isinstance(paths, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'log_file_file': {type(paths).__name__}"
            )
        return [str(path) for path in paths]

    def log_file_path(self, path: str) -> str:
        """Get the log file path from the config file."""
        paths = self.log_file_paths
        if not isinstance(paths, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'log_file_paths': {type(paths).__name__}"
            )

        result = [result_path for result_path in paths if result_path == path]
        return result[0]

    @property
    def logging_format(self) -> str:
        """Get the logging format from the config file."""
        formatter_value = self.logging_config.get("formatter")
        if not isinstance(formatter_value, str):
            raise TypeError(
                f"Incorrect type for type for 'logging.formatter': {type(formatter_value).__name__}"
            )
        return formatter_value

    @property
    def loggers_list(self) -> list[str]:
        """Get the loggers list from the config file."""
        loggers = self.logging_config.get("loggers")
        if not isinstance(loggers, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'logging.loggers': {type(loggers).__name__}"
            )
        return [str(logger) for logger in loggers]

    @property
    def database_config(self) -> dict:
        """Get the database configuration from the config file."""
        return {
            "db_type": constants.DB_TYPE,
            "db_host": self.host,
            "user": constants.DB_USER,
            "password": constants.DB_PASSWORD,
            "port": int(constants.DB_PORT),
            "name": constants.DB_NAME,
        }


config_reader = ConfigReader()
