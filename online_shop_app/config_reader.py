import yaml


class ConfigReader:
    def __init__(self):
        self._read_config_file()

    def _read_config_file(self):
        """
        Read the config file and store it in a dictionary.
        """
        try:
            with open("app_config.yaml", "r") as stream:
                self.__config = yaml.safe_load(stream)
        except FileNotFoundError:
            raise ValueError("Config file not found")
        except PermissionError:
            raise ValueError("Not enough permissions to read config file")

    @property
    def config_file(self):
        return self.__config

    @property
    def logging_config(self):
        return self.config_file.get("logging")

    @property
    def host(self) -> str:
        host_value = self.config_file.get("host")
        if not isinstance(host_value, str):
            raise TypeError(
                f"Incorrect type for type for 'host': {type(host_value).__name__}"
            )
        return host_value

    @property
    def logging_level(self) -> str:
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
        paths = self.config_file.get("log_file_paths")
        if not isinstance(paths, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'log_file_file': {type(paths).__name__}"
            )
        return [str(path) for path in paths]

    def log_file_path(self, path: str) -> str:
        paths = self.log_file_paths
        if not isinstance(paths, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'log_file_paths': {type(paths).__name__}"
            )

        result = [result_path for result_path in paths if result_path == path]
        return result[0]

    @property
    def logging_format(self) -> str:
        formatter_value = self.logging_config.get("formatter")
        if not isinstance(formatter_value, str):
            raise TypeError(
                f"Incorrect type for type for 'logging.formatter': {type(formatter_value).__name__}"
            )
        return formatter_value

    @property
    def loggers_list(self) -> list[str]:
        loggers = self.logging_config.get("loggers")
        if not isinstance(loggers, (list, tuple)):
            raise TypeError(
                f"Incorrect type for type for 'logging.loggers': {type(loggers).__name__}"
            )
        return [str(logger) for logger in loggers]

    @property
    def database_config(self):
        database = self.config_file.get("database")
        if not isinstance(database, dict):
            raise TypeError(
                f"Incorrect type for type for 'database': {type(database).__name__}"
            )
        return {
            "db_type": str(database.get("type")),
            "user": str(database.get("user")),
            "password": database.get("password"),
            "port": int(database.get("port")),
            "name": str(database.get("name")),
        }


config_reader = ConfigReader()
