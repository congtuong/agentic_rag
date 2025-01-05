from abc import ABC, abstractmethod

from utils.logger import get_logger

logger = get_logger()

class BaseDatabaseRepository(ABC):
    def __init__(
        self,
        **kwargs,
    ):
        """
        Initialize the database repository.
        """
        ...
        
    @abstractmethod
    def _connect(self):
        """
        Connect to the database.
        """
        ...
    
    @abstractmethod
    def check_health(self) -> bool:
        """
        Check the health of the database.
        """
        ...
    
    @abstractmethod
    def get_client(self):
        """
        Get the database client.
        """
        ...

    @abstractmethod
    def create(self, table: str, **kwargs):
        """
        Create a record in the database.
        """
        ...

    @abstractmethod
    def read(self, table: str, record_id: str):
        """
        Read a record from the database.
        """
        ...
        
    @abstractmethod
    def update(self, table: str, record_id: str, **kwargs):
        """
        Update a record in the database.
        """
        ...
        
    @abstractmethod
    def delete(self, table: str, record_id: str):
        """
        Delete a record from the database.
        """
        ...
        
        
    