"""
Module for reading datasets
"""
from utils.logger_manager import Logger
import pandas as pd
from typing import Optional


class DatasetReader:
    """
    Class DatasetReader is required to read datasets
    """

    @staticmethod
    def read_dataset_from_csv(path: str, chunksize: Optional[int] = None) -> pd.DataFrame:
        """
        Method reads datset from csv with required chunk size
        :param path: path where csv file is stored
        :type path: str
        :param chunksize: size of chunks of file while reading
        :type chunksize: Optional[int]
        :return:
        """
        Logger().get_logger().info(f"Reading dataset from csv file '{path}'")
        df_chunk: Optional[pd.TextFileReader, pd.DataFrame] = pd.read_csv(path, chunksize=chunksize)
        if chunksize is None:
            return df_chunk
        else:
            df_list: list = []
            for chunk in df_chunk:
                df_list.append(chunk)
            return pd.concat(df_list)
