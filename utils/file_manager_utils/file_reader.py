"""
Module for reading various data files.
"""
import json


class FileReader:
    """
    Class FileReader for reading various data files.
    """
    @staticmethod
    def get_data_from_json(path: str) -> dict:
        """
        get_data_from_json method get data from json file
        :param path: input file path
        :type path: String
        :return: data from json file as dict
        :rtype: dict
        """
        with open(path, encoding='utf-8') as data_file:
            data: dict = json.load(data_file)
            return data
