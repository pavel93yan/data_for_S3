"""
Module of logger_util. Class Logger is represented in this module.
"""
import logging
from utils.singleton_util import Singleton
from utils.config_manager import ConfigReader
from typing import Optional


class Logger(metaclass=Singleton):
    """
    Class Logger contains method of getting logger.
    Logger is based on Singleton metaclass for keep the only instance of logger.
    Methods: logger. This method returns instance of logger.
    """
    __logger: Optional[logging.Logger] = None
    __config: dict = ConfigReader().get_logger_config()
    __log_flag: str = ConfigReader().get_main_config()['log_file']

    def get_logger(self) -> logging.Logger:
        """
        Method is for configuring and getting logger
        :return: Instance of logger.
        :rtype: logging.Logger
        """

        if self.__logger is None:
            self.__logger = logging.getLogger(Logger.__name__)
            self.__logger.setLevel(self.__config['level'])
            ch = logging.StreamHandler()
            formatter = logging.Formatter(self.__config['format'])
            ch.setFormatter(formatter)
            self.__logger.addHandler(ch)
            if self.__log_flag == "True":
                fh = logging.FileHandler(self.__config['path'], mode=self.__config['mode'])
                fh.setFormatter(formatter)
                self.__logger.addHandler(fh)
        return self.__logger
