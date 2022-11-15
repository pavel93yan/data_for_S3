"""
Module is required for managing waiter
"""
from boto3_type_annotations.s3 import Client
from botocore.exceptions import ClientError, ParamValidationError
from utils.config_manager import ConfigReader
from utils.logger_manager import Logger


class WaiterManager:
    """
    Class WaiterManager is required for managing waiters
    """
    @staticmethod
    def wait_for_object_exists_in_S3(s3_client: Client, bucket: str, object_name: str):
        Logger().get_logger().info(f"Waiting for object '{object_name}' to appear in bucket '{bucket}'")
        waiter_config: dict = ConfigReader.get_main_config()['WaiterConfig']
        try:
            s3_client.get_waiter('object_exists').wait(Bucket=bucket, Key=object_name, WaiterConfig=waiter_config)
        except ClientError as e:
            Logger().get_logger().error(f"ClientError happened while waiting for object to appear: '{e}'")
            raise ClientError
        except ParamValidationError as e:
            Logger().get_logger().error(f"The parameters that were provided are incorrect: '{e}'")
            raise ValueError
