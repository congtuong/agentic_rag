import uuid
import textract
import shutil
import os
import json

from fastapi import APIRouter, Depends,File,UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import Annotated,List

from llama_index.core import Document

from utils.logger import get_logger
from utils.checker import check_upload_file

from bootstrap import (
    CLOUD_SERVICE,
    AGENTIC_SERVICE,
    AUTH_SERVICE,
)


router = APIRouter()

logger = get_logger()

security = HTTPBearer()

@router.post("/chat", dependencies=[Depends(security)])
async def search_vector(
    query: str,
    request: Request,
):
    """
    Search vector
    """
    logger.info(f"Chat request incoming")
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={})
        )
    
    data = AGENTIC_SERVICE.chat(query).response
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Search vector successfully",
            "data": data,
        },
    )