"""
Module for providing configs to application
"""
from utils.file_manager import FileManager


class ConfigManager(FileManager):
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
        return ConfigManager.get_data_from_json(ConfigManager.__main_config_path)

    @staticmethod
    def get_logger_config() -> dict:
        """
        get_logger_config - method for getting logger configs
        :return: logger configs as dict
        """
        return ConfigManager.get_data_from_json(ConfigManager.__logger_config_path)
