"""
This is main module of script. Main logic of script is placed here.
config_data/main_config.json contains 'delete_flag', if it's set to 'True' then raw files in 'raw_data_dir' directory
will be deleted without moving to 'dir_to_move' directory where raw files are moved by default.

It's allowed to set paths to files and directories for Windows OS with the forward slash ('/').
"""

from utils.config_manager import ConfigReader
from utils.file_manager_utils.file_manager import FileManager
from utils.file_manager_utils.file_writer import FileWriter
from utils.file_manager_utils.file_reader import FileReader
from utils.file_manager_utils.file_name_manager import FileNameManager
from utils.aws_utils.s3_uploader import S3Uploader
from utils.time_manager import TimeManager
from utils.logger_manager import Logger
from utils.dataset_reader import DatasetReader
from boto3_type_annotations.s3 import Client
import boto3
import os


class MainScript:
    """
    class that contains main script
    """
    @staticmethod
    def run_main_script():
        """
        main method which runs the whole script
        :return: Nothing
        """
        configs: dict = ConfigReader.get_main_config()
        timestamp_mark: str = TimeManager.get_current_datetime(configs["time_format"])
        Logger().get_logger().info(f"Starting process of ingesting data to S3 with timestamp '{timestamp_mark}'")

        # start of AWS session and S3 client setting process
        aws_access_key_id: str = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key: str = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region_name: str = os.environ.get('REGION_NAME')
        aws_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        s3_client: Client = aws_session.client("s3")
        # end of AWS session and S3 client setting process

        # start of naming management of raw data files
        file_type: str = configs["data_files_name_pattern"]["file_type"]
        raw_data_dir: str = configs["raw_data_dir"]
        raw_data_file_names_list_src: list[str] = FileManager.get_list_of_raw_data_files(raw_data_dir, file_type)
        raw_data_file_paths_list_src: list[str] = FileNameManager\
            .generate_path_to_files(raw_data_dir, raw_data_file_names_list_src)
        ingest_raw_data_file_names_list: list[str] = FileNameManager\
            .generate_data_file_names(len(raw_data_file_paths_list_src), timestamp_mark)
        ingest_raw_data_file_paths_list = FileNameManager\
            .generate_path_to_files(raw_data_dir, ingest_raw_data_file_names_list)
        FileManager.rename_multiple_files(raw_data_file_paths_list_src, ingest_raw_data_file_paths_list)
        # end of naming management of raw data files

        # start of counting row in raw datasets
        row_count_list: list[int] = []
        for file_path in ingest_raw_data_file_paths_list:
            row_count_list.append(len(DatasetReader.read_dataset_from_csv(file_path)))
        # end of counting row in raw datasets

        # start of naming management and creating of ingest metadata file
        json_ingest_metadata: dict = FileReader.get_data_from_json("config_data/JSON_ingest_metadata_template.json")
        json_ingest_metadata["row_count"]: int = row_count_list[0]
        json_ingest_metadata_file_name: str = FileNameManager.generate_json_metadata_file_name(timestamp_mark)
        json_ingest_metadata_file_path_src: str = FileNameManager\
            .generate_path_to_files(raw_data_dir, json_ingest_metadata_file_name)
        FileWriter.create_json_ingest_metadata_file(json_ingest_metadata, json_ingest_metadata_file_path_src)
        # end of naming management and creating of ingest metadata file

        # start of naming management of S3 objects
        configs["s3_raw_obj_prefix"] = os.path.join(configs["s3_raw_obj_prefix"], f"time={timestamp_mark}")
        s3_raw_data_object_names_list: list[str] = FileNameManager\
            .generate_path_to_files(configs["s3_raw_obj_prefix"], ingest_raw_data_file_names_list)
        s3_json_metadata_object_name: str = FileNameManager\
            .generate_path_to_files(configs["s3_metadata_obj_prefix"], json_ingest_metadata_file_name)
        # end of naming management of S3 objects

        # start of uploading files to AWS S3 buckets
        S3Uploader.sent_multiple_files_to_s3_bucket_and_wait_for_them_being_uploaded(
            s3_client,
            ingest_raw_data_file_paths_list,
            configs["s3_raw_bucket"],
            s3_raw_data_object_names_list
        )
        S3Uploader.sent_file_to_s3_bucket_and_wait_for_it_being_uploaded(
            s3_client,
            json_ingest_metadata_file_path_src,
            configs["s3_metadata_bucket"],
            s3_json_metadata_object_name
        )
        # end of uploading files to AWS S3 buckets

        # start of managing files data and metadata files on local machine
        data_files_list: list[str] = ingest_raw_data_file_paths_list.copy()
        data_files_list.append(json_ingest_metadata_file_path_src)
        if configs["delete_flag"] == "True":
            FileManager.remove_multiple_files(data_files_list)
        else:
            new_folder_to_move_files: str = FileManager.create_folder(configs["dir_to_move"], timestamp_mark)
            FileManager.move_files_to_folder(data_files_list, new_folder_to_move_files)
        # end of managing files data and metadata files on local machine
        Logger().get_logger().info(f"End of process of ingesting data to S3")


if __name__ == '__main__':
    MainScript.run_main_script()

