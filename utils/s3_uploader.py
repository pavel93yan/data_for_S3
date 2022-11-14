"""
Module for needs of file uploading to S3
"""
from boto3_type_annotations.s3 import Client
from botocore.exceptions import ClientError, ParamValidationError
from utils.aws_waiter_manager import WaiterManager
from utils.logger_manager import Logger


class S3Uploader:
    """
    Class S3Uploader for needs of file uploading to S3
    """
    @staticmethod
    def put_file_to_s3_bucket(s3_client: Client,  file_name: str, bucket: str, object_name: str):
        """
        Method put_file_to_s3_bucket is required to start uploading file to s3 bucket
        :param s3_client: S3 client
        :type s3_client: Client
        :param file_name: path to file that is required to be uploaded
        :type file_name: str
        :param bucket: bucket where file is required to be uploaded to
        :type bucket: str
        :param object_name: key / object name / path inside the bucket where file is required to be uploaded to
        :type object_name: str
        :return: doesn't return anything
        """
        Logger().get_logger().info(f"Uploading file '{file_name}' to '{bucket}' as '{object_name}'")
        try:
            s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            Logger().get_logger().error(f"ClientError happened while uploading file: '{e}'")
            raise ClientError
        except ParamValidationError as e:
            Logger().get_logger().error(f"The parameters that were provided are incorrect: '{e}'")
            raise ValueError

    @staticmethod
    def put_file_to_s3_bucket_and_wait_for_it_being_uploaded(s3_client: Client,  file_name: str,
                                                             bucket: str, object_name: str):
        """
        Method ut_file_to_s3_bucket_and_wait_for_it_being_uploaded is required to start uploading file to s3 bucket
        and then wait until this upload will be ended
        :param s3_client: S3 client
        :type s3_client: Client
        :param file_name: path to file that is required to be uploaded
        :type file_name: str
        :param bucket: bucket where file is required to be uploaded to
        :type bucket: str
        :param object_name: key / object name / path inside the bucket where file is required to be uploaded to
        :type object_name: str
        :return: doesn't return anything
        """
        S3Uploader.put_file_to_s3_bucket(s3_client,  file_name, bucket, object_name)
        WaiterManager.wait_for_object_exists_in_S3(s3_client, bucket, file_name)
