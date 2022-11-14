"""
Module for managing file names purposes
"""
from typing import Union
from utils.config_manager import ConfigManager
import os


class FileNameManager:
    """
    Class for managing file names purposes
    """
    @staticmethod
    def __generate_basic_file_name(file_type: str, datetime: str, order_num: str = "") -> str:
        """
        Private method for generating basic file name pattern
        :param file_type: file extension
        :type file_type: str
        :param datetime: datetime of files ingestion to S3
        :param order_num: 3 digits iterate number with '_' prefix if needed (e.g. _001)
        :return: file name
        :rtype: str
        """
        naming_pattern: dict = ConfigManager.get_main_config()['data_files_name_pattern']
        return f"{naming_pattern['source_name']}_{naming_pattern['table_name']}{order_num}_{datetime}.{file_type}"

    @staticmethod
    def generate_data_file_names(file_num: int, datetime: str) -> list[str]:
        """
        Module generate_data_file_names required to generate names of data files
        :param file_num: number of required file names
        :type file_num: int
        :param datetime: datetime of files ingestion to S3
        :type datetime: str
        :return: list of names of csv files
        :rtype: list[str]
        """
        file_type: str = ConfigManager.get_main_config()['data_files_name_pattern']['file_type']
        name_list: list = []
        for i in range(file_num):
            order_num: str = "_" + str(i + 1).zfill(3)
            name_list.append(FileNameManager.__generate_basic_file_name(file_type, datetime, order_num))
        return name_list

    @staticmethod
    def generate_json_metadata_file(datetime: str) -> str:
        """
        Method generate_json_metadata_file generates json metadata file name
        :param datetime: datetime of files ingestion to S3
        :type datetime: str
        :return: name of the metadata file
        :rtype: str
        """
        return FileNameManager.__generate_basic_file_name("json", datetime)

    @staticmethod
    def generate_path_to_file(prefix: str, names: Union[list[str], str], s3: bool = False) -> Union[list[str], str]:
        """
         Method generate_path_to_file can generate different paths to file. It combines given prefix with file or files
        name. Add prefix only ended with '/'.
        :param prefix: path to file directory
        :type prefix: str
        :param names: name or names of files to which it's needed to generate the path
        :param s3: flag to start generating of s3 object name. By default, is set to False.
        :type s3: bool
        :return: path or paths to files
        :rtype: list[str] or str
        """
        if type(names) == str and s3:
            path: str = prefix + names
            if s3:
                return path
            else:
                return os.path.normpath(path)

        if type(names) == list:
            for i in range(len(names)):
                if s3:
                    names[i]: str = prefix + names[i]
                else:
                    names[i]: str = os.path.normpath(os.path.join(prefix, names[i]))
        names.sort()
        return names
