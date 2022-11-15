"""
Module is required for writing data into files
"""
import json
from utils.logger_manager import Logger


class FileWriter:
    """
    FileWriter class is required for writing data into files
    """
    @staticmethod
    def create_json_ingest_metadata_file(metadata: dict, path: str):
        """
        create_json_ingest_metadata_file method creates file with metadata for Matillion based on provided dict of
        data by required path
        :param metadata: metadata for Matillion jobs
        :type metadata: dict
        :param path: path where file will be saved
        :return: Nothing
        """
        Logger().get_logger().info(f"Creating json metadata file with path '{path} and next metadata'")
        if len(metadata) == 0:
            raise ValueError

        with open(path, "w") as outfile:
            json.dump(metadata, outfile)
