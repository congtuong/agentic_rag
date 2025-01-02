import json
import torch
import textract

from typing import List, Dict, Any
from transformers import BitsAndBytesConfig
from pymilvus import MilvusClient, DataType
from tempfile import SpooledTemporaryFile
from tqdm import tqdm

from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.openai import OpenAI

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.vector_stores.milvus import MilvusVectorStore

from llama_index.core.node_parser import SemanticSplitterNodeParser

from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker

from llama_index.core.llms import ChatMessage
from llama_index.core.schema import Node, NodeWithScore, QueryBundle, TextNode
from llama_index.core import (
    VectorStoreIndex, 
    StorageContext,
    Document,
    Settings,
)
from const import (
    LLMService,
    EmbedderService,
    VectorDBService,
    RerankerService,
    ContextualRAGConfig,
    PROMPT_DOC,
    PROMPT_CHUNK,
    ASSISTANT_SYSTEM_PROMPT,
    QA_PROMPT,
    
)
from utils.logger import get_logger
from utils.json_extractor import extract_json

logger = get_logger()

class ContextualRAG:
    def __init__(self, config: ContextualRAGConfig = ContextualRAGConfig()):
        self.config = config
        logger.info("Loading LLM")
        self.llm = self._load_llm(config.llm_service, config.llm_model) 
        Settings.llm = self.llm
        logger.info("Loaded LLM!")

        logger.info("Loading Embedder")
        self.embedder = self._load_embedder(config.embedder_service, config.embedder_model)
        Settings.embed_model = self.embedder
        logger.info("Loaded Embedder!")

        logger.info("Loading VectorDB")
        self.vectordb = self._load_vectordb(config.vectordb_service)
        logger.info("Loaded VectorDB!")

        logger.info("Loading Splitter")
        self.splitter = self._load_splitter(config.buffer_size, config.breakpoint_percentile_threshold)
        logger.info("Loaded Splitter!")

        logger.info("Loading Reranker")
        self.reranker = self._load_reranker(config.reranker_service, config.reranker_model, config.reranker_top_n)
        logger.info("Loaded Reranker!")
        
    def _load_llm(
            self,
            llm_service: str,
            llm_model: str,
        ):
        """
        return LLM object
        """
        if llm_service == LLMService.OPENAI:
            return OpenAI(llm_model, api_key=self.config.key)
        elif llm_service == LLMService.HUGGINGFACE:
            return HuggingFaceLLM(
                model_name="Qwen/Qwen2.5-0.5B-Instruct",
                tokenizer_name="Qwen/Qwen2.5-0.5B-Instruct",
                # context_window=3900,
                # max_new_tokens=256,
                # model_kwargs={"quantization_config": BitsAndBytesConfig(
                #         load_in_4bit=True,
                #         bnb_4bit_compute_dtype=torch.float16,
                #         bnb_4bit_quant_type="nf4",
                #         bnb_4bit_use_double_quant=True,
                #     )},
                generate_kwargs={"temperature": 0.2, "top_k": 50, "top_p": 0.95},
                # device_map="auto",
            )
        else:
            raise ValueError(f"Invalid LLM service: {llm_service}")
        
    def _load_embedder(
            self,
            embedder_service: str,
            embedder_model: str,
        ):
        """
        return Embedder object
        """
        if embedder_service == EmbedderService.OPENAI:
            return OpenAIEmbedding(embedder_model)
        elif embedder_service == EmbedderService.HUGGINGFACE:
            return HuggingFaceEmbedding(embedder_model)
        else:
            raise ValueError(f"Invalid Embedder service: {embedder_service}")
        
    def _load_vectordb(
            self,
            vectordb_service: str,
        ):
        """
        return VectorDB object
        """
        if vectordb_service == VectorDBService.MILVUS:
            client = MilvusClient(self.config.vectordb_uri)
            schema = MilvusClient.create_schema(
                auto_id=False,
                enable_dynamic_field=True,
            )
            logger.info("Loading collection")
            
            # for dev purposes
            # drop if collection exists
            # if client.has_collection(collection_name="collection"):
            #     logger.info("Dropping collection")
            #     client.drop_collection(collection_name="collection")

            if not client.has_collection(collection_name="collection"):                
                shape_check = self.embedder.get_text_embedding("test")
                logger.info(f"Shape check: {len(shape_check)}")            
                schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=len(shape_check))
                schema.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=36)
                schema.add_field(field_name="id", datatype=DataType.INT64, auto_id=True, is_primary=True)
                schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=4096)
                
                client.create_collection(collection_name="collection", schema=schema)
                
                index_params = MilvusClient.prepare_index_params()

                # 4.2. Add an index on the vector field.
                index_params.add_index(
                    field_name="embedding",
                    metric_type="L2",
                    index_type="IVF_FLAT",
                    index_name="vector_index",
                    params={ "nlist": 128 }
                )

                # 4.3. Create an index file
                client.create_index(
                    collection_name="collection",
                    index_params=index_params,
                    sync=False # Whether to wait for index creation to complete before returning. Defaults to True.
                )
            
            logger.info(f"Collection stats: {client.get_collection_stats(collection_name='collection')}")

            client.load_collection(collection_name="collection")

            return client
        else:
            raise ValueError(f"Invalid VectorDB service: {vectordb_service}")
        
    
    def _load_splitter(
        self,
        buffer_size: int = 1,
        breakpoint_percentile_threshold: int = 95,
    ):
        """
        return NodeParser object
        """
             
        return SemanticSplitterNodeParser(
            embed_model=self.embedder,
            buffer_size=buffer_size,
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
        )
        
    
    def _load_reranker(
        self,
        reranker_service: str,
        reranker_model: str,
        top_n: int = 5,
    ):
        """
        return Reranker object
        """
        if reranker_service == RerankerService.FLAGEMBEDDING:
            return FlagEmbeddingReranker(
                model=reranker_model,
                top_n = top_n,
            )
        else:
            raise ValueError(f"Invalid Reranker service: {reranker_service}")

    def chunk_text(
        self,
        doc: Document,
        doc_id: str,
    ):
        """
        return list of chunks
        """
        
        nodes = self.splitter.get_nodes_from_documents([doc])
            
        return [
            Document(
                text=node.text,
                metadata={
                    "doc_id": doc_id,
                    "node_id": node.node_id,
                },
            ) for node in nodes
        ]
        
    def generate_contextual(
        self,
        chunk_text: str,
        doc: Document,
    ):
        """
        return contextual response
        """
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant.",
            ),
            ChatMessage(
                role="user",
                content=f"""
                {PROMPT_DOC.format(WHOLE_DOCUMENT=doc.text)}
                {PROMPT_CHUNK.format(CHUNK_CONTENT=chunk_text)}
                """
            ),
        ] 

        # logger.info(f"chunk_text: {chunk_text}")
        
         
        contextualized_content = self.llm.chat(
            messages=messages,
        ).message.content
        
        # logger.info(f"contextualized_content: {contextualized_content}")
        
        # return the prepended content
        return Document(
            text="\n\n".join([contextualized_content, chunk_text]),
            metadata=doc.metadata,
        )
    
    def add_new_document(
        self,
        doc_id: str,
        doc: Document,
    ) -> bool:
        """
        handle new document
        """
        
        chunks = self.chunk_text(doc, doc_id)

        chunks = tqdm(chunks, desc="Generating contextual responses")

        total_inserted = 0
        contextual_chunks = []
        for chunk in chunks:
            contextual_chunks.append(self.generate_contextual(chunk.text, doc))
        
        for contextual_chunk in contextual_chunks:
            embeddings = self.embedder.get_text_embedding(contextual_chunk.text)
            res = self.vectordb.insert(
                collection_name="collection",
                data = [
                    {
                        "doc_id": doc_id,
                        "embedding": embeddings,
                        "text": contextual_chunk.text,
                    }
                ]
            )
            
            total_inserted += res["insert_count"]
        
        logger.info(f"Collection updated with document: {doc_id}")
        logger.info(f"Total inserted: {total_inserted}")
        
        return True
        


    def sematic_search(
        self,
        query: str,
        top_k: int = 5,
        context: Dict[str, Any] = None,
        system_prompt: str = ASSISTANT_SYSTEM_PROMPT,
    ):
        """
        return list of top_k documents
        """
        
        embeddings = self.embedder.get_text_embedding(query)
        # logger.info(f"Embeddings: {embeddings}")
        
        # logger.info("Searching in VectorDB")
        res = self.vectordb.search(
            collection_name="collection",
            data=[embeddings],
            limit=top_k,
            output_fields=["doc_id", "text"],
        )
        
        # logger.info(f"Search results: {res}")
        
        semantic_results = []
        for hits in res:
            for hit in hits:
                hit["id"] = str(hit["id"])
                semantic_results.append(hit)

        logger.info(f"Semantic results: {semantic_results}")
    
        return semantic_results
    
    def contextual_search(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        return list of top_k documents
        """
            
        semantic_results = self.sematic_search(query, top_k)
        combined_nodes = [
            NodeWithScore(
                node=TextNode(
                    text=hit["entity"]["text"],
                    metadata={
                        "doc_id": hit["entity"]["doc_id"],
                    },
                ),
                # score is L2 distance so we need to invert it
                score=1 / (1e-6 + hit["distance"]),
            ) for hit in semantic_results
        ]
            
        # logger.info(f"Combined nodes: {combined_nodes}")
        
        reranked_nodes = self.reranker.postprocess_nodes(
            nodes=combined_nodes, query_bundle=QueryBundle(query_str=query)
        )
        
        # logger.info(f"Reranked nodes: {reranked_nodes}")
        
        context = "\n\n".join([
            node.get_text() for node in reranked_nodes
        ])
        
        messages = [
            ChatMessage(
                role="system",
                content="You are a helpful assistant.",
            ),
            ChatMessage(
                role="user",
                content=QA_PROMPT.format(QUERY=query, CONTEXT=context)
            ),
        ]
        response = None
        retry = 0
        data = None
        while True:
            if retry > 3:
                break
            logger.info(f"Starting chat with LLM")
            response = self.llm.chat(messages=messages)
            logger.info(f"LLM Response: {response}")
            
            data, ok = extract_json(response.message.content)
            if ok:
                break
            try: 
                data = json.loads(response.message.content)
                break
            except json.JSONDecodeError:
                retry += 1
                continue
            
        logger.info(f"LLM final Response: {response}")
        
        return data
        
    def get_vector_store_index(self):
        vector_store = MilvusVectorStore(
            uri=self.config.vectordb_uri,
            collection_name="collection",
            dim=len(self.embedder.get_text_embedding("test")),
        )
        
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
        )
        
        return VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
            embed_model=self.embedder,
        )