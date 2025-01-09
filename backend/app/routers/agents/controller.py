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

from routers.schemas import ResponseModel

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
            content=ResponseModel(status=401, message="Unauthorized", data={}).dict(),
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

@router.get("/conversation/{conversation_id}", dependencies=[Depends(security)])
async def get_conversation(
    conversation_id: str,
    request: Request,
):
    """
    Get conversation
    """
    logger.info(f"Get conversation request incoming")
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={}).dict(),
        )
    
    data = AGENTIC_SERVICE.get_conversation(conversation_id)
    
    if not data:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "message": "Conversation not found",
                "data": {},
            },
        )
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Get conversation successfully",
            "data": data,
        },
    )
    
@router.post("/conversation/{conversation_id}/chat", dependencies=[Depends(security)])
async def chat(
    conversation_id: str,
    query: str,
    request: Request,
):
    """
    Chat
    """
    logger.info(f"Chat request incoming")
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={}).dict(),
        )
    try:
        data = AGENTIC_SERVICE.chat(query, conversation_id).response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": f"Error: {e}",
                "data": {},
            },
        )
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Chat successfully",
            "data": data,
        },
    )

@router.post("/conversation/create", dependencies=[Depends(security)])
async def create_conversation(
    chatbot_id: str,
    request: Request,
):
    """
    Create conversation
    """
    logger.info(f"Create conversation request incoming")
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={}).dict(),
        )
    
    conversaton_id = str(uuid.uuid4())
    
    data = AGENTIC_SERVICE.create_conversation(chatbot_id, conversaton_id, request.state.user['username'])
    
    if not data:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "message": "Failed to create conversation",
                "data": {},
            },
        )
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Create conversation successfully",
            "data": {"conversation_id": conversaton_id},
        },
    )

@router.get("/{chatbot_id}/conversations/list", dependencies=[Depends(security)])
async def list_conversations(
    chatbot_id: str,
    request: Request,
):
    """
    Get conversations
    """
    logger.info(f"Get conversations request incoming")
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={}).dict(),
        )
    
    data = AGENTIC_SERVICE.list_conversations(chatbot_id)
    
    if not data:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "message": "Conversations not found",
                "data": {},
            },
        )
        
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "Get conversations successfully",
            "data": data,
        },
    )