import uuid
import textract
import shutil
import os
import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from fastapi.responses import (
    JSONResponse,
)
from typing import (
    Annotated,
    List,
)

from llama_index.core import Document

from utils.logger import get_logger
from utils.checker import check_upload_file

from routers.schemas import *

from bootstrap import (
    CLOUD_SERVICE,
    AGENTIC_SERVICE,
)


router = APIRouter()

logger = get_logger()

@router.post("/cloud/upload/document")
async def upload_documents(
    document: UploadFile = File(...),
):
    """
    Upload documents to the cloud
    """
    
    if not check_upload_file(document):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid file format"},
        )
        
    doc_id = uuid.uuid4()
    
    temp_file_path = f"/tmp/{str(doc_id)}.{document.filename.split('.')[-1]}"
    with open(temp_file_path, "wb") as temp_file:
        shutil.copyfileobj(document.file, temp_file)
    
    if CLOUD_SERVICE.cloud_repository.upload(
        object_name=f"documents/{str(doc_id)}.{document.filename.split('.')[-1]}",
        file_path=temp_file_path,
        bucket_name=CLOUD_SERVICE.bucket_name,
    ):
        logger.info(f"Document uploaded: {document.filename}")
        
        try:
            content = textract.process(temp_file_path).decode("utf-8")
    
            if AGENTIC_SERVICE.rag.add_new_document(
                doc_id=str(doc_id),
                doc=Document(
                    text=content,
                    metadata={
                        "doc_id": str(doc_id),
                    },
                ),
            ):  
                logger.info(f"Document processed: {doc_id}")
        finally:
            os.remove(temp_file_path)
            
    else:
        logger.error(f"Document failed to upload: {document.filename}")
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to upload documents"},
        )
        
    return JSONResponse(
        status_code=200,
        content={"message": "Documents uploaded successfully"},
    )

@router.get("/vector/search")
async def search_vector(
    query: str,
):
    """
    Search vector
    """
    
    data = AGENTIC_SERVICE.rag.contextual_search(query)
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Search vector successfully",
            "data": data,
        },
    )

@router.post("/agent/chat")
async def search_vector(
    query: str,
):
    """
    Search vector
    """
    
    data = AGENTIC_SERVICE.chat(query).response
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Search vector successfully",
            "data": data,
        },
    )