from enum import Enum
from utils.config import get_config

config = get_config()

PROMPT_DOC = """<document>
{WHOLE_DOCUMENT}
</document>
"""

PROMPT_CHUNK = """Here is the chunk we want to situate within the whole document

{CHUNK_CONTENT}

Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else."""

ASSISTANT_SYSTEM_PROMPT = """
You are an advanced AI agent designed to assist users by searching through a diverse knowledge base
of files and providing relevant information.

Here are something you should pay attention to:
{INSTRUCTIONS}

If there are any product's link, please provide the link in the response.

Please answer in markdown format.
"""

QA_PROMPT = """We have provided context information below.
---------------------
{CONTEXT}"
---------------------
Given this information, please answer the question: {QUERY}

Please ONLY return in json format like this:
{{
    "result": ### Your answer here, MUST BE IN MARKDOWN FORMAT
    "is_chat_false": ### You must decide if the answer is true with the context and question provided
}}
"""


SUPPORTED_FILE_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
]

class LLMService(Enum):
    """
    Enum for the different services that the LLM can provide.
    """
    
    def __str__(self):
        return self.value
    
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    HUGGINFACEHUB = "huggingface_hub"

class EmbedderService(Enum):
    """
    Enum for the different services that the Embedder can provide.
    """
    
    def __str__(self):
        return self.value
    
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    HUGGINFACEHUB = "huggingface_hub"
    
class VectorDBService(Enum):
    """
    Enum for the different services that the VectorDB can provide.
    """
    
    def __str__(self):
        return self.value
    
    MILVUS = "milvus"

class RerankerService(Enum):
    """
    Enum for the different services that the Reranker can provide.
    """
    
    def __str__(self):
        return self.value
    
    FLAGEMBEDDING = "flag_embedding"

class ContextualRAGConfig:
    """
    Class to hold configuration values.
    """
    
    def __init__(self):
        self.llm_service = LLMService.OPENAI
        self.embedder_service = EmbedderService.HUGGINGFACE
        self.vectordb_service = VectorDBService.MILVUS
        self.reranker_service = RerankerService.FLAGEMBEDDING
        self.buffer_size = 1
        self.breakpoint_percentile_threshold = 90
        self.embedder_model = "BAAI/bge-small-en-v1.5"
        self.reranker_model = "BAAI/bge-reranker-large"
        self.reranker_top_n = 5
        self.llm_model = "gpt-4o-mini"
        
        self.key = config.get("OPEN_AI_API_KEY")
        self.vectordb_uri = config.get("MILVUS_URI")
        self.vectordb_collection = config.get("MILVUS_COLLECTION")
        self.vectordb_reinit = True if config.get("MILVUS_REINIT_COLLECTION") == "true" else False
        self.es_host = config.get("ELASTICSEARCH_HOST")
        self.es_port = config.get("ELASTICSEARCH_PORT")
        self.es_chunk_index = config.get("ELASTICSEARCH_CHUNK_INDEX")
        