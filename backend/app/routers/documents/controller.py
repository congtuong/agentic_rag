import uuid
import textract
import shutil
import os
import json

from fastapi import APIRouter,Depends,File,UploadFile

from fastapi.responses import JSONResponse

from typing import Annotated,List
from fastapi import Request, Depends
from fastapi.security import HTTPBearer

from llama_index.core import Document

from utils.logger import get_logger
from utils.checker import check_upload_file

from routers.schemas import ResponseModel

from bootstrap import (
    CLOUD_SERVICE,
    AGENTIC_SERVICE,
    AUTH_SERVICE,
    KNOWLEDGE_SERVICE,
)

router = APIRouter()

logger = get_logger()

security = HTTPBearer()

@router.post("/upload", dependencies=[Depends(security)])
async def upload_documents(
    request: Request,
    document: UploadFile = File(...),
):
    """
    Upload documents to the cloud
    """
    logger.info(f"Upload request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={})
        )
        
    
    if not check_upload_file(document):
        return JSONResponse(
            status_code=400,
            content=ResponseModel(status=400, message="Invalid file format", data={})
        )
        
    doc_id = str(uuid.uuid4())
    
    temp_file_path = f"/tmp/{doc_id}.{document.filename.split('.')[-1]}"
    with open(temp_file_path, "wb") as temp_file:
        shutil.copyfileobj(document.file, temp_file)
    
    if CLOUD_SERVICE.cloud_repository.upload(
        object_name=f"documents/{doc_id}.{document.filename.split('.')[-1]}",
        file_path=temp_file_path,
        bucket_name=CLOUD_SERVICE.bucket_name,
    ):
        logger.info(f"Document uploaded: {document.filename}")
        
        if AGENTIC_SERVICE.add_document(
            file_path=temp_file_path,
            doc_id=doc_id,
            username=request.state.user["username"],
            object_name=f"documents/{doc_id}.{document.filename.split('.')[-1]}",
            file_name=document.filename,
            file_type=document.filename.split('.')[-1],
            file_size=os.path.getsize(temp_file_path),
        ):
            logger.info(f"Document processed: {document.filename}")
            return JSONResponse(
                status_code=200,
                content=ResponseModel(status=200, message="Upload successful", data={})
            )
        else:
            logger.error(f"Document processing failed: {document.filename}")
            CLOUD_SERVICE.cloud_repository.delete(
                object_name=f"documents/{doc_id}.{document.filename.split('.')[-1]}",
                bucket_name=CLOUD_SERVICE.bucket_name
            )
            return JSONResponse(
                status_code=500,
                content=ResponseModel(status=500, message="Processing failed", data={})
            )
    else:
        logger.error(f"Document upload failed: {document.filename}")
        return JSONResponse(
            status_code=500,
            content=ResponseModel(status=500, message="Upload failed", data={})
        )
        
    return JSONResponse(
        status_code=500,
        content={"message": "Upload failed"},
    )

@router.get("/list", dependencies=[Depends(security)])
async def list_documents(
    request: Request,
):
    """
    List documents
    """
    logger.info(f"List documents request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={})
        )
    
    documents = KNOWLEDGE_SERVICE.list_documents(
        username=request.state.user["username"]
    )
    if not documents:
        return JSONResponse(
            status_code=404,
            content=ResponseModel(status=404, message="No documents found", data={})
        )
    
    return JSONResponse(
        status_code=200,
        content=ResponseModel(status=200, message="Documents found", data=documents)
    )