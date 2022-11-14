"""
Module for managing time data
"""
from datetime import datetime


class TimeManager:
    """
    Class TimeManager for managing time data
    """
    @staticmethod
    def get_current_datetime(datetime_format: str) -> str:
        """
        Method get_current_datetime for getting current datetime and return it in required format
        :param datetime_format: pattern used for datetime result
        :type datetime_format: str
        :return: current datetime as string
        """
        return datetime.today().strftime(datetime_format)
