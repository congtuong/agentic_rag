import boto3

from typing import List

from .base import BaseCloudRepository
from utils.logger import get_logger

logger = get_logger()

class S3CloudRepository(BaseCloudRepository):
    def __init__(
        self,
        region_name: str,
        access_key: str,
        secret_key: str,
    ):
        """ 
        Initialize the S3 cloud repository.
        
        
        Args:
            region_name (str): The region name.
            access_key (str): The access key.
            secret_key (str): The secret key.
        """
        self.region_name = region_name
        self.access_key = access_key
        self.secret_key = secret_key
        
        self._connect()
        super().__init__()
        
    def _connect(self):
        """
        Connect to the S3 cloud service.
        """
        self.client = boto3.client(
            "s3",
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )
        
        if not self.check_health():
            raise Exception("Error connecting to S3")

        logger.info("Connected to S3")
        
    
    def check_health(self) -> bool:
        """
        Check the health of the S3 cloud service.
        """
        try:
            self.client.list_buckets()
            return True
        except Exception as e:
            logger.error(f"Error checking health of S3: {e}")
            return False
        
    def get_client(self):
        """
        Get the S3 cloud client.
        """
        return self.client
    
    def upload(
        self,
        object_name: str,
        bucket_name: str,
        file_path: str,
    ) -> bool:
        """
        Upload a file to the S3 cloud.
        
        Args:
            object_name (str): The object name.
            bucket_name (str): The bucket name.
            file_path (str): The file path.
        """
        try:
            self.client.upload_file(
                file_path,
                bucket_name,
                object_name,
            )
            logger.info(f"Uploaded file to S3: {object_name}")
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False
        
        return True
    
    def download(
        self,
        object_name: str,
        bucket_name: str,
        file_path: str,
    ) -> bool:
        """
        Download a file from the S3 cloud.
        
        Args:
            object_name (str): The object name.
            bucket_name (str): The bucket name.
            file_path (str): The file path.
        """
        try:
            self.client.download_file(
                bucket_name,
                object_name,
                file_path,
            )
            
        except Exception as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False
        
        return True

    def list_files(
        self,
        bucket_name: str,
    ) -> List[dict]:
        """
        List files in a bucket.
        
        Args:
            bucket_name (str): The bucket name.
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name,
            )
            
            return response.get("Contents", [])
        except Exception as e:
            logger.error(f"Error listing files in S3: {e}")
            return []
        
    def delete(
        self,
        object_name: str,
        bucket_name: str,
    ) -> bool:
        """
        Delete a file from the S3 cloud.
        
        Args:
            object_name (str): The object name.
            bucket_name (str): The bucket name.
        """
        try:
            self.client.delete_object(
                Bucket=bucket_name,
                Key=object_name,
            )
        except Exception as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
        
        return True
    
    def create_bucket(
        self,
        bucket_name: str,
    ) -> bool:
        """
        Create a bucket in the S3 cloud.
        
        Args:
            bucket_name (str): The bucket name.
        """
        try:
            self.client.create_bucket(
                Bucket=bucket_name,
            )
        except Exception as e:
            logger.error(f"Error creating bucket in S3: {e}")
            return False
        
        return True
    
    def upload_fileobj(
        self,
        file: any,
        bucket_name: str,
        object_name: str,
    ) -> bool:
        """
        Upload a file object to the S3 cloud.
        
        Args:
            object_name (str): The object name.
            file_path (str): The file path.
        """
        try:
            self.client.upload_fileobj(
                file,
                bucket_name,
                object_name,
            )
            logger.info(f"Uploaded file object to S3: {object_name}")
        except Exception as e:
            logger.error(f"Error uploading file object to S3: {e}")
            return False
        
        return True
        

