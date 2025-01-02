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

from src.rag import ContextualRAG
from utils.logger import get_logger
from utils.json_extractor import extract_json

logger = get_logger()

class AgenticRAG:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        self.rag = ContextualRAG()
        Settings.llm = self.rag.llm
        Settings.embed_model = self.rag.embedder
        self._load_tools()
        
    def _load_tools(self):
        tools = []
        
        from llama_index.core.tools.tool_spec.load_and_search import LoadAndSearchToolSpec
        from llama_index.tools.google import GoogleSearchToolSpec

        # google_spec = GoogleSearchToolSpec(
        #     key=self.config.get("GOOGLE_API_KEY"), 
        #     engine=self.config.get("GOOGLE_SEARCH_ENGINE_ID"),
        #     )

        # # Wrap the google search tool as it returns large payloads
        # google_tools = LoadAndSearchToolSpec.from_defaults(
        #     google_spec.to_tool_list()[0],
        # ).to_tool_list()
        
        # tools.extend(google_tools)
        
        from llama_index.core.tools import QueryEngineTool, ToolMetadata

        def milvus_tools(input: str):
            response = self.rag.contextual_search(
                query=input,
                top_k=5,
            )
            return response
        
        query_tools = FunctionTool.from_defaults(
            fn=milvus_tools,
            # metadata=ToolMetadata(
            #     name="milvus_tools",
            #     description="Searches the milvus database for the given input.",
            # ),
        )
        
        tools.append(
            query_tools
        )
     
        memory = ChatMemoryBuffer.from_defaults(chat_history=[], llm=self.rag.llm)
        
        # agent = ReActAgent(
        #     tools=tools,
        #     memory=memory,
        #     context="""
        #     You are an AI assistant. You must always use the provided tools to answer any question or solve any task. 
        #     Do not attempt to answer directly. If you cannot solve the task using the tools, respond with:
        #     "I cannot complete this task without tools."
        #     """,
        #     llm=self.rag.llm,
        #     verbose=True,
        # )
        
        def add_2_numbers(a, b):
            return a + b
        
        def multiply(a: int, b: int) -> int:
            """Multiply two integers and returns the result integer"""
            return a * b

        
        tools.extend([
            FunctionTool.from_defaults(
                fn=add_2_numbers,
            ),
            FunctionTool.from_defaults(
                fn=multiply,
            ),
        ])
        
        logger.info(f"Agent tools: {tools}")
        
        agent = ReActAgent.from_tools(
            tools=tools,
            memory=memory,
            llm=self.rag.llm,
            context="""
            You are an AI assistant. You must always use the provided tools to answer any question or solve any task.
            Do not attempt to answer directly. If you cannot solve the task using the tools, respond with:
            "I cannot complete this task without tools."
            """,
            verbose=True,
        )
        
        # agent = milvus_index.as_chat_engine(
        #     llm=self.rag.llm,
        #     memory=memory,
        #     verbose=True,
        #     chat_mode="react",
        # )
        
        self.agent = agent
        
    def chat(self, query: str):
        return self.agent.chat(query)
        