import textract
import os

from src import AgenticRAG
from const import ContextualRAGConfig

from llama_index.core import Document
from utils.logger import get_logger

logger = get_logger()

class AgentService:
    def __init__(
        self,
        database_instance,
        config,
    ):
        self.agentic = AgenticRAG(config)
        self.database_instance = database_instance    
        
    def get_agent(self, agent_id):
        return self.agentic.get_agent(agent_id)
    
    def chat(self, query: str):
        return self.agentic.chat(query)

    def add_document(
        self, 
        file_path: str, 
        doc_id: str,
        username: str,
        object_name: str,
        file_name: str,
        file_type: str,
        file_size: int,
        ):
        try:
            user = self.database_instance.read_by(
                table="users",
                column="username",
                value=username
            )
            if not user:
                logger.error(f"User not found: {username}")
                return False
            
            content = textract.process(file_path).decode("utf-8")
            
            chunks = self.agentic.rag.add_new_document(
                doc_id=doc_id,
                doc=Document(
                    text=content,
                    metadata={
                        "doc_id": doc_id,
                    },
                )
            )
            
            if len(chunks) > 0:
                res = self.database_instance.create(
                    "documents",
                    **{
                        "id": doc_id,
                        "user_id": user["id"],
                        "object_name": object_name,
                        "file_name": file_name,
                        "file_type": file_type,
                        "file_size": file_size,
                    }
                )

                if not res:
                    logger.error(f"Failed to insert document {doc_id}")
                    return False
                
                logger.info(f"Document processed: {doc_id}")
                for i, chunk in enumerate(chunks):
                    logger.info(f"Inserting chunk {chunk}")
                    res = self.database_instance.create(
                        "chunks",
                        **{
                            "id": chunk.doc_id,
                            "document_id": doc_id,
                            "vector_id": chunk.doc_id,
                            "chunk_index": i
                        }
                    )
                    if not res:
                        logger.error(f"Failed to insert chunk {chunk.doc_id} for document {doc_id}")
                return True
            else:
                logger.error(f"Document processing failed: {doc_id}")
                return False
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return False
        finally:
            os.remove(file_path)