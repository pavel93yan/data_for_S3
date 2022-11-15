"""
Module for file managing
"""
import os
import shutil
from utils.logger_manager import Logger


class FileManager:
    """
    class FileManager is required for file managing
    """

    @staticmethod
    def rename_multiple_files(old_names_list: list[str], new_names_list: list[str]):
        """
        rename_multiple_files method renames names of the containing in one list to the names
        that the other list contains
        :param old_names_list: list with old file names (paths)
        :type old_names_list: list[str]
        :param new_names_list:  list with new file names (paths)
        :type new_names_list: list[str
        :return: Nothing
        """
        Logger().get_logger().info(f"Renaming the following list of the files '{old_names_list}'"
                                   f" to new names that are given in the next list '{new_names_list}'")
        if not FileManager.all_files_exist(old_names_list):
            raise FileNotFoundError
        for old_name, new_name in zip(old_names_list, new_names_list):
            os.rename(
                os.path.normpath(old_name),
                os.path.normpath(new_name)
            )

    @staticmethod
    def remove_multiple_files(file_name_list: list[str]):
        """
        remove_multiple_files method removes files that are contained in the list
        :param file_name_list:  list with file names (paths)
        :type file_name_list: list[str]
        :return: Nothing
        """
        Logger().get_logger().info(f"Removing the following list of the files '{file_name_list}'")
        if not FileManager.all_files_exist(file_name_list):
            raise FileNotFoundError
        for file_name in file_name_list:
            os.remove(os.path.normpath(file_name))

    @staticmethod
    def all_files_exist(files_path_list: list[str]) -> bool:
        """
        all_files_exist method checks that files by the given paths exist
        :param files_path_list: list of paths to the files
        :type files_path_list: list[str]
        :return: False if any of the files is not found. If all files exist = returns True
        :rtype: bool
        """
        not_exist_list: list[str] = []
        for file_path in files_path_list:
            path = os.path.normpath(file_path)
            if not os.path.isfile(path):
                not_exist_list.append(path)
        if len(not_exist_list) == 0:
            return True
        else:
            Logger().get_logger()\
                .error(f"FileNotFoundError. The files numbered in the next list '{not_exist_list}' don't exist. ")
            return False

    @staticmethod
    def move_files_to_folder(old_files_list: list[str], dest_folder: str):
        """
        move_files_to_folder method moves files from the list to new_folder
        :param old_files_list: list with paths to files
        :type old_files_list: list[str]
        :param dest_folder: folder where files wil be moved to
        :type dest_folder: str
        :return: Nothing
        """
        Logger().get_logger().info(f"Moving files from list '{old_files_list} to destination folder '{dest_folder}'")
        if not FileManager.all_files_exist(old_files_list):
            raise FileNotFoundError
        dest_folder: str = os.path.normpath(dest_folder)
        if os.path.isdir(dest_folder):
            for src_path in old_files_list:
                file: str = os.path.basename(src_path)
                shutil.move(src_path, os.path.join(dest_folder, file))
        else:
            Logger().get_logger().error(f"Destination directory '{dest_folder}' doesn't exist")
            raise NotADirectoryError

    @staticmethod
    def create_folder(path_prefix: str, folder_name: str) -> str:
        """
        create_folder method creates new folder inside another folder
        :param path_prefix: main path where new folder will be created
        :type path_prefix: str
        :param folder_name: name of the new folder
        :type folder_name: str
        :return: new folder path
        :rtype: str
        """
        Logger().get_logger().info(f"Creating new folder'{folder_name} in main directory '{path_prefix}'")
        path_prefix: str = os.path.normpath(path_prefix)
        if os.path.isdir(path_prefix):
            new_folder_path: str = os.path.join(path_prefix, folder_name)
            os.makedirs(new_folder_path)
            return new_folder_path
        else:
            Logger().get_logger().error(f"Main directory (path_prefix) '{path_prefix}' doesn't exist")
            raise NotADirectoryError

    @staticmethod
    def get_list_of_raw_data_files(directory: str, file_type: str) -> list[str]:
        """
        get_list_of_raw_data_files method helps to get list of files with required extension in required directory
        :param directory: path to directory form which raw file names will be obtained
        :type directory: str
        :param file_type: extension of required files. Provided for purposes of avoiding of reading non-required files
        :type file_type: str
        :return:  list of files with file_type extension
        :rtype: list[str]
        """
        directory: str = os.path.normpath(directory)
        if os.path.isdir(directory):
            content_list: list[str] = os.listdir(directory)
        else:
            Logger().get_logger().error(f"Directory (path_prefix) '{directory}' doesn't exist")
            raise NotADirectoryError
        files_list: list[str] = []
        for item in content_list:
            if item.endswith("." + file_type):
                files_list.append(item)
        if len(files_list) > 0:
            return files_list
        else:
            Logger().get_logger().error(f"There are no files with extensiom '.{file_type}' in folder '{directory}'")
            raise ValueError
