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
        FileManager.files_exist(old_names_list)
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
        FileManager.files_exist(file_name_list)
        for file_name in file_name_list:
            os.remove(os.path.normpath(file_name))

    @staticmethod
    def files_exist(files_path_list: list[str]):
        """
        files_exist method checks that files by the given paths exist
        :param files_path_list: list of paths to the files
        :type files_path_list: list[str]
        :exception FileNotFoundError: if one of the files are not found
        """
        not_exist_list: list[str] = []
        for file_path in files_path_list:
            path = os.path.normpath(file_path)
            if not os.path.isfile(path):
                not_exist_list.append(path)
        if len(not_exist_list) > 0:
            Logger().get_logger()\
                .error(f"FileNotFoundError. The files numbered in the next list '{not_exist_list}' don't exist. ")
            raise FileNotFoundError

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
        FileManager.files_exist(old_files_list)
        dest_folder: str = os.path.normpath(dest_folder)
        if os.path.isdir(dest_folder):
            for src_path in old_files_list:
                file: str = os.path.basename(src_path)
                shutil.move(src_path, os.path.join(dest_folder, file))
        else:
            Logger().get_logger().error(f"Destination directory '{dest_folder}' doesn't exist")
            raise NotADirectoryError

    @staticmethod
    def create_folder(path_prefix: str, folder_name: str):
        """
        create_folder method creates new folder inside another folder
        :param path_prefix: main path where new folder will be created
        :type path_prefix: str
        :param folder_name: name of the new folder
        :type folder_name: str
        :return: Nothing
        """
        Logger().get_logger().info(f"Creating new folder'{folder_name} in main directory '{path_prefix}'")
        path_prefix: str = os.path.normpath(path_prefix)
        if os.path.isdir(path_prefix):
            os.makedirs(os.path.join(path_prefix, folder_name))
        else:
            Logger().get_logger().error(f"Main directory (path_prefix) '{path_prefix}' doesn't exist")
            raise NotADirectoryError
