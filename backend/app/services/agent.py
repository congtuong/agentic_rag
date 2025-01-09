import textract
import os
import threading

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
                    },
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
                res = self.delete_document(doc_id)
                return False
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            res = self.delete_document(doc_id)
            return False
        finally:
            os.remove(file_path)

    def delete_document(self, doc_id: str):
        res = self.database_instance.delete_by(
            "documents",
            "id",
            doc_id
        )
        if not res:
            logger.error(f"Failed to delete document {doc_id}")
            return False
        res = self.database_instance.delete_by(
            "chunks",
            "document_id",
            doc_id
        )
        if not res:
            logger.error(f"Failed to delete chunks for document {doc_id}")
            return False
        return True
    
    def create_conversation(self, chatbot_id: str, conversation_id: str, username: str):
        user = self.database_instance.read_by(
            table="users",
            column="username",
            value=username
        )
        if not user:
            logger.error(f"User not found: {username}")
            return False
    
        sql_query = """
            select documents.id from chatbot_knowledges join knowledges 
            on chatbot_knowledges.knowledge_id = knowledges.id join documents
            join knowledge_documents on documents.id = knowledge_documents.document_id
            where chatbot_knowledges.chatbot_id = ?;
        """
        documents = self.database_instance.execute_query(
            sql_query,
            (chatbot_id,),
            fetch_all=True,
            fetch_one=False
        )
        if not documents:
            logger.error("Failed to get documents in chatbot")
            return None
        
        doc_ids = [doc["id"] for doc in documents] if len(documents) > 0 else None
        
        if not self.agentic._load_tools(
            conversation_id=conversation_id,
            document_ids=doc_ids
        ): 
            logger.error(f"Failed to load tools for bot {chatbot_id}")
            return False
        
        conversation = self.database_instance.create(
            "conversations",
            **{
                "id": conversation_id,
                "chatbot_id": chatbot_id,
                "user_id": user["id"],
            }
        )
        
        if not conversation:
            logger.error(f"Failed to create conversation {conversation_id}")
            return False
        
        return True
    
    def get_conversation(self, conversation_id: str):
        sql_query = """
            select messages.* from conversations join messages on
            conversations.id = messages.conversation_id where conversations.id = ?;
        """
        
        messages = self.database_instance.execute_query(
            sql_query,
            (conversation_id,),
            fetch_all=True,
            fetch_one=False
        )
        
        if not messages:
            logger.error(f"Failed to get messages for conversation {conversation_id}")
            return None
        
        logger.info(f"Get conversation {conversation_id} messages successfully")
        
        return messages
    
    
    def chat(self, query: str, conversation_id:str):

        response = self.agentic.chat(
            query=query,
            conversation_id=conversation_id
        )

        return response
    
    