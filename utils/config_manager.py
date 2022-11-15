"""
Module for providing configs to application
"""
from utils.file_manager_utils.file_reader import FileReader


class ConfigReader(FileReader):
    """
    ConfigManager class for getting configs for different applications modules
    """
    __main_config_path: str = "config_data/main_config.json"
    __logger_config_path: str = "config_data/logger_config.json"

    @staticmethod
    def get_main_config() -> dict:
        """
        get_main_config - method for getting main configs
        :return: main configs as dict
        """
        return ConfigReader.get_data_from_json(ConfigReader.__main_config_path)

    @staticmethod
    def get_logger_config() -> dict:
        """
        get_logger_config - method for getting logger configs
        :return: logger configs as dict
        """
        return ConfigReader.get_data_from_json(ConfigReader.__logger_config_path)
