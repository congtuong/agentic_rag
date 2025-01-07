from elasticsearch import Elasticsearch
from unidecode import unidecode
from utils.logger import get_logger

# cfg = get_config()
logger = get_logger()

# TODO:
# Update ES class if needed
class ES:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 9200,
    ):
        if host is not None:
            self.es = Elasticsearch(f"http://{host}:{port}")
            logger.info(f"ES info: {self.es.info()}")
            logger.info(f"ES client connected to {host}:{port}")
            
        else:
            logger.error("ES client not connected")
            self.es = None
            
    def insert_chunk(
        self,
        index: str,
        text: str,
        chunk_uuid: str,
    ):
        """
        Insert a chunk of data into the index
        """
        logger.info(f"Inserting chunk into {index}")
        self.es.index(
            index=index,
            id=chunk_uuid,
            document={
                "text": text,
            },
        )
        logger.info(f"Chunk inserted into {index}")
        return True
        
    def insert_doc(
        self,
        index: str,
        text: str,
        doc_uuid: str,
    ):
        """
        Insert a document into the index
        """
        logger.info(f"Inserting document into {index}")
        self.es.index(
            index=index,
            id=doc_uuid,
            document={
                "text": text,
            },
        )
        logger.info(f"Document inserted into {index}")
        return True
        
    def get_doc(
        self,
        index: str,
        id: str,
    ):
        """
        Get a document from the index
        """
        logger.info(f"Getting document from {index}")
        doc = self.es.get(
            index=index,
            id=doc_uuid,
        )
        logger.info(f"Document retrieved from {index}")
        return doc
        
        