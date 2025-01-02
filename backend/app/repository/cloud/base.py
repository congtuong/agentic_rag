from abc import ABC, abstractmethod
from typing import List, Optional, Union

from utils.logger import get_logger

logger = get_logger()

class BaseCloudRepository(ABC):
    def __init__(
        self,
        **kwargs,
    ):
        """
        Initialize the cloud repository.
        """
        ...
        
    @abstractmethod
    def _connect(self):
        """
        Connect to the cloud service.
        """
        ...
    
    @abstractmethod
    def check_health(self) -> bool:
        """
        Check the health of the cloud service.
        """
        ...
    
    @abstractmethod
    def get_client(self):
        """
        Get the cloud client.
        """
        ...
    
    @abstractmethod
    def upload(
        self,
        bucket_name: str,
        object_name: str,
        file_path: str,
    ) -> bool:
        
        """
        Upload a file to the cloud.
        """
        ...
        
    @abstractmethod
    def download(
        self,
        bucket_name: str,
        object_name: str,
        file_path: str,
    ) -> bool:
        """
        Download a file from the cloud.
        """
        ...
        
    @abstractmethod
    def list_files(
        self,
        bucket_name: str,
    ) -> List[dict]:
        """
        List files in a bucket.
        """
        ...
        
    @abstractmethod
    def delete(
        self,
        bucket_name: str,
        object_name: str,
    ) -> bool:
        """
        Delete a file from the cloud.
        """
        ...
        
    @abstractmethod
    def create_bucket(
        self,
        bucket_name: str,
    ) -> bool:
        """
        Create a bucket in the cloud.
        """
        ...
    