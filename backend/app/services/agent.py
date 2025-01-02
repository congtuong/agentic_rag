from src import ContextualRAG
from const import ContextualRAGConfig
class AgentService:
    def __init__(self):
        self.contextual_rag = ContextualRAG(ContextualRAGConfig())
            

    def get_agent(self, agent_id):
        return self.contextual_rag.get_agent(agent_id)
    
    def chat(self, agent_id, query):
        return self.contextual_rag.chat(agent_id, query)