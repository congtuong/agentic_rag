import time
import threading
import json
import os

from typing import Dict, Any, List, Tuple, Union
from llama_index.vector_stores.milvus.utils import (
    ScalarMetadataFilters,
    ScalarMetadataFilter,
    FilterOperatorFunction,
)
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.memory import VectorMemory , ChatMemoryBuffer
from llama_index.core import (
    Settings, 
)
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.core import QueryBundle

# import NodeWithScore
from llama_index.core.schema import NodeWithScore

from llama_index.core.retrievers import (
    BaseRetriever,
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)

from .contextual_rag import ContextualRAG
from utils.logger import get_logger
from utils.json_extractor import extract_json

logger = get_logger()

class AgenticRAG:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        self.rag = ContextualRAG()
        Settings.llm = self.rag.llm
        Settings.embed_model = self.rag.embedder
        self.agents = {}
        self.agent_live_time = int(config.get("AGENT_LIVE_TIME", 60*60*24))
        self._load_tools()
        
    def _load_tools(
        self,
        conversation_id: str = "default",  
        document_ids: List[str] = None,
        history: List[ChatMessage] = None,
    ):
        try:
            tools = []
            
            # from llama_index.core.tools.tool_spec.load_and_search import LoadAndSearchToolSpec
            # from llama_index.tools.google import GoogleSearchToolSpec

            # google_spec = GoogleSearchToolSpec(
            #     key=self.config.get("GOOGLE_API_KEY"), 
            #     engine=self.config.get("GOOGLE_SEARCH_ENGINE_ID"),
            #     )

            # # Wrap the google search tool as it returns large payloads
            # google_tools = LoadAndSearchToolSpec.from_defaults(
            #     google_spec.to_tool_list()[0],
            # ).to_tool_list()
            
            
            # from llama_index.core.tools import QueryEngineTool, ToolMetadata

            def milvus_tools(input: str):
                response = self.rag.contextual_search(
                    query=input,
                    top_k=1,
                    document_ids=document_ids,
                )
                return response
            
            query_tools = FunctionTool.from_defaults(
                fn=milvus_tools,
            )
            
            tools.append(
                query_tools
            )
            # tools.extend(google_tools)

            logger.info(f"Init history: {history}")
            memory = ChatMemoryBuffer.from_defaults(
                chat_history=history,
                llm=self.rag.llm,
                )
            
            def add_2_numbers(a, b):
                return a + b
            
            def multiply(a: int, b: int) -> int:
                """Multiply two integers and returns the result integer"""
                return a * b

            
            # tools.extend([
            #     FunctionTool.from_defaults(
            #         fn=add_2_numbers,
            #     ),
            #     FunctionTool.from_defaults(
            #         fn=multiply,
            #     ),
            # ])
            
            logger.info(f"Agent tools: {tools}")
            
            agent = ReActAgent.from_tools(
                tools=tools,
                memory=memory,
                llm=self.rag.llm,
                context="""
                You are an AI assistant. You must always use the provided tools to answer any question or solve any task.
                Do not attempt to answer directly. If you cannot solve the task using the tools, respond with:
                "I cannot complete this task without tools."

                NOTE: The vector search tool should be used every time.
                """,
                verbose=True,
            )
            
            # agent = milvus_index.as_chat_engine(
            #     llm=self.rag.llm,
            #     memory=memory,
            #     verbose=True,
            #     chat_mode="react",
            # )
                            
            self.agents[conversation_id] = {
                "agent": agent,
                "updated_at": time.time(),
            }
            return True
        
        except Exception as e:
            logger.error(f"Error loading tools: {e}")
            return False
        finally:
            threading.Thread(target=self.delete_dead_agents).start()
    
    def delete_dead_agents(self):
        current_time = time.time()
        dead_agents = []
        for conversation_id, agent in self.agents.items():
            if current_time - agent["updated_at"] > self.agent_live_time:
                dead_agents.append(conversation_id)
                
        for conversation_id in dead_agents:
            del self.agents[conversation_id]
        
    def chat(
        self, 
        query: str, 
        conversation_id: str = "default",
        ):
        
        response = self.agents[conversation_id]["agent"].chat(query)
        logger.info(f"Agent history: {self.agents[conversation_id]['agent'].memory.to_dict()}")
        
        return response

        