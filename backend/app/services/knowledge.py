from typing import List
from utils.logger import get_logger

logger = get_logger()

class KnowledgeService:
    def __init__(
        self,
        database_instance,
    ):
        self.database_instance = database_instance
        
        
    def create_knowledge(
        self,
        name: str,
        documents: List[str],
        knowledge_id: str,
        username: str,
    ):
        user = self.database_instance.read_by(
            "users",
            "username",
            username
        )
        if not user:
            logger.error(f"User not found: {username}")
            return False
        
        res = self.database_instance.create(
            "knowledges",
            **{
                "id": knowledge_id,
                "name": name,
                "user_id": user["id"],
            }
        )
        
        if not res:
            logger.error(f"Failed to create knowledge: {res}")
            return False
        
        for doc in documents:
            # TODO:
            # check if document exists for sqlite3, dont know why sqlite3 not return violation error
            # comment out if we are using postgres
            # BEGIN
            document = self.database_instance.read(
                "documents",
                doc
            )
            if not document:
                logger.error(f"Document not found: {doc}")
                res = self.delete_knowledge(knowledge_id)
                if not res:
                    logger.error(f"Failed to delete knowledge")
                return False
            # END
            
            res = self.database_instance.create(
                "knowledge_documents",
                **{
                    "knowledge_id": knowledge_id,
                    "document_id": doc,
                },
            )
            logger.info(f"Created knowledge document res: {res}")
            if not res:
                logger.error(f"Failed to create knowledge document: {doc}")
                res = self.delete_knowledge(knowledge_id)
                if not res:
                    logger.error(f"Failed to delete knowledge")

                return False
                
        return True
    
    
    def delete_knowledge(
        self,
        knowledge_id: str,
    ):
        logger.info(f"Deleting knowledge: {knowledge_id}")
        res = self.database_instance.delete_by(
            "knowledge_documents",
            "knowledge_id",
            knowledge_id
        )
        if not res:
            logger.error(f"Failed to delete knowledge documents")
            return False
        res = self.database_instance.delete_by(
            "knowledges",
            "id",
            knowledge_id
        )
        if not res:
            logger.error(f"Failed to delete knowledge")
            return False
        return True
    
    
    def create_chatbot(
        self,
        name: str,
        knowledges: List[str],
        chatbot_id: str,
        username: str,
    ):
        user = self.database_instance.read_by(
            "users",
            "username",
            username
        )
        if not user:
            logger.error(f"User not found: {username}")
            return False
        
        res = self.database_instance.create(
            "chatbots",
            **{
                "id": chatbot_id,
                "name": name,
                "user_id": user['id'],
                "config": "{}",
                "status": "private",
            }
        )
        
        if not res:
            logger.error(f"Failed to create chatbot: {res}")
            return False
        
        for kl_id in knowledges:
            # TODO:
            # check if knowledge exists for sqlite3, dont know why sqlite3 not return violation error
            # comment out if we are using postgres
            # BEGIN
            knowledge = self.database_instance.read(
                "knowledges",
                kl_id
            )
            if not knowledge:
                logger.error(f"Knowledge not found: {kl_id}")
                res = self.delete_chatbot(chatbot_id)
                if not res:
                    logger.error(f"Failed to delete chatbot")
                return False
            # END
            
            
            res = self.database_instance.create(
                "chatbot_knowledges",
                **{
                    "chatbot_id": chatbot_id,
                    "knowledge_id": kl_id
                }
            )
            if not res:
                logger.error(f"Failed to create chatbot knowledge: {kl_id}")
                res = self.delete_chatbot(chatbot_id)
                if not res:
                    logger.error(f"Failed to delete chatbot")
                    return False
                
        return True
    
    
    def delete_chatbot(
        self,
        chatbot_id: str,
    ):
        res = self.database_instance.delete_by(
            "chatbot_knowledges",
            "chatbot_id",
            chatbot_id
        )
        if not res:
            logger.error(f"Failed to delete chatbot documents")
            return False
        res = self.database_instance.delete_by(
            "chatbots",
            "id",
            chatbot_id
        )
        if not res:
            logger.error(f"Failed to delete chatbot")
            return False
        return True
    
    
    def get_chatbot(
        self,
        chatbot_id: str,
    ):
        chatbot = self.database_instance.read(
            "chatbots",
            chatbot_id
        )
        if not chatbot:
            logger.error(f"Chatbot not found: {chatbot_id}")
            return None
        
        sql_query = f"""
            SELECT knowledges.* FROM chatbot_knowledges join knowledges on 
            chatbot_knowledges.knowledge_id = knowledges.id WHERE 
            chatbot_knowledges.chatbot_id = ?;
        """
        
        chatbot_knowledges = self.database_instance.execute_query(
            sql_query,
            (chatbot_id,),
            fetch_all=True
        )
        if not chatbot_knowledges:
            logger.error(f"Failed to get chatbot knowledges")
            return None
        
        chatbot["knowledges"] = chatbot_knowledges
        
        return chatbot
        
        
    def list_documents(
        self,
        username: str,
    ):
        user = self.database_instance.read_by(
            "users",
            "username",
            username
        )
        
        if not user:
            logger.error(f"User not found: {username}")
            return None
        
        documents = self.database_instance.read_by(
            "documents",
            "user_id",
            user["id"],
            fetch_one=False,
            fetch_all=True
        )
        
        if not documents:
            logger.error(f"Documents not found: {username}")
            return None
        
        return documents
    
    
    def list_knowledges(
        self,
        username: str,
    ):
        user = self.database_instance.read_by(
            "users",
            "username",
            username
        )
        
        if not user:
            logger.error(f"User not found: {username}")
            return None
        
        knowledges = self.database_instance.read_by(
            "knowledges",
            "user_id",
            user["id"],
            fetch_one=False,
            fetch_all=True
        )
        
        if not knowledges:
            logger.error(f"Knowledges not found: {username}")
            return None
        
        return knowledges
    
    
    def list_documents_in_knowledge(
        self,
        knowledge_id: str,
    ):
        sql_query = """
            SELECT documents.* FROM knowledge_documents join documents on 
            knowledge_documents.document_id = documents.id WHERE 
            knowledge_documents.knowledge_id = ?;
        """
        
        documents = self.database_instance.execute_query(
            sql_query,
            (knowledge_id,),
            fetch_all=True,
            fetch_one=False
        )
        if not documents:
            logger.error(f"Failed to get documents in knowledge")
            return None
        
        return documents
        

    def list_chatbot(
        self,
        username: str,
    ):
        user = self.database_instance.read_by(
            "users",
            "username",
            username
        )
        
        if not user:
            logger.error(f"User not found: {username}")
            return None
        
        chatbots = self.database_instance.read_by(
            "chatbots",
            "user_id",
            user["id"],
            fetch_one=False,
            fetch_all=True
        )
        
        if not chatbots:
            logger.error(f"Chatbots not found: {username}")
            return None
        
        return chatbots


    def list_knowledges_in_chatbot(
        self,
        chatbot_id: str,
    ):
        sql_query = """
            SELECT knowledges.* FROM chatbot_knowledges join knowledges on 
            chatbot_knowledges.knowledge_id = knowledges.id WHERE 
            chatbot_knowledges.chatbot_id = ?;
        """
        
        knowledges = self.database_instance.execute_query(
            sql_query,
            (chatbot_id,),
            fetch_all=True,
            fetch_one=False
        )
        if not knowledges:
            logger.error("Failed to get knowledges in chatbot")
            return None
        
        return knowledges