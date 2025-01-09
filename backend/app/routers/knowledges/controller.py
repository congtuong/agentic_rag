import uuid

from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import List

from utils.logger import get_logger
from routers.schemas import ResponseModel, CreateKnowledgeRequest, CreateKnowledgeResponse
from routers.schemas import CreateChatBotRequest, CreateChatBotResponse
from bootstrap import AUTH_SERVICE, DATABASE, KNOWLEDGE_SERVICE

security = HTTPBearer()
logger = get_logger()
router = APIRouter()

@router.post("/knowledge/create", dependencies=[Depends(security)])
async def create_knowledge(
    request: Request,
    knowledge: CreateKnowledgeRequest,
):
    """
    Create a knowledge
    """
    logger.info(f"Create knowledge request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Unauthorized",
                status=401,
            ),
            status_code=401,
        )

    # Create a knowledge
    knowledge_id = str(uuid.uuid4())

    if not KNOWLEDGE_SERVICE.create_knowledge(
        name=knowledge.name,
        documents=knowledge.documents,
        knowledge_id=knowledge_id,
        username=request.state.user["username"],
    ):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Failed to create knowledge",
                status=400,
            ),
            status_code=400,
        )
        
    return JSONResponse(
        content=ResponseModel(
            data=CreateKnowledgeResponse(
                name=knowledge.name,
                knowledge_id=knowledge_id,
            ).dict(),
            message="Knowledge created",
            status=200,
        ),
        status_code=200,
    )
    
@router.post("/chatbot/create", dependencies=[Depends(security)])
async def create_chatbot(
    request: Request,
    chatbot: CreateChatBotRequest,
):
    """
    Create a chatbot
    """
    logger.info(f"Create chatbot request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Unauthorized",
                status=401,
            ),
            status_code=401,
        )

    # Create a chatbot
    chatbot_id = str(uuid.uuid4())

    if not KNOWLEDGE_SERVICE.create_chatbot(
        name=chatbot.name,
        knowledges=chatbot.knowledges,
        chatbot_id=chatbot_id,
        username=request.state.user["username"],
    ):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Failed to create chatbot",
                status=400,
            ),
            status_code=400,
        )
        
    return JSONResponse(
        content=ResponseModel(
            data=CreateChatBotResponse(
                name=chatbot.name,
                chatbot_id=chatbot_id,
            ).dict(),
            message="Chatbot created",
            status=200,
        ),
        status_code=200,
    )
    
@router.get("/chatbot/{chatbot_id}", dependencies=[Depends(security)])
async def get_chatbot(
    request: Request,
    chatbot_id: str,
):
    """
    Get a chatbot
    """
    logger.info(f"Get chatbot request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Unauthorized",
                status=401,
            ),
            status_code=401,
        )

    chatbot = KNOWLEDGE_SERVICE.get_chatbot(chatbot_id)
    if not chatbot:
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Chatbot not found",
                status=404,
            ),
            status_code=404,
        )
        
    return JSONResponse(
        content=ResponseModel(
            data=chatbot,
            message="Chatbot found",
            status=200,
        ),
        status_code=200,
    )
    
@router.get("/knowledge/list", dependencies=[Depends(security)])
async def list_knowledges(
    request: Request,
):
    """
    List knowledges
    """
    logger.info(f"List knowledges request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Unauthorized",
                status=401,
            ),
            status_code=401,
        )

    knowledges = KNOWLEDGE_SERVICE.list_knowledges(
        username=request.state.user["username"]
    )
    if not knowledges:
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="No knowledges found",
                status=404,
            ),
            status_code=404,
        )
        
    return JSONResponse(
        content=ResponseModel(
            data=knowledges,
            message="Knowledges found",
            status=200,
        ),
        status_code=200,
    )
    
@router.get("/knowledge/{knowledge_id}", dependencies=[Depends(security)])
async def get_knowledge(
    request: Request,
    knowledge_id: str,
):
    """
    Get a knowledge
    """
    logger.info(f"Get knowledge request incoming")
    
    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Unauthorized",
                status=401,
            ),
            status_code=401,
        )

    knowledge = KNOWLEDGE_SERVICE.list_documents_in_knowledge(
        knowledge_id=knowledge_id,
    )
    
    if not knowledge:
        return JSONResponse(
            content=ResponseModel(
                data={},
                message="Knowledge not found",
                status=404,
            ),
            status_code=404,
        )
    
    return JSONResponse(
        content=ResponseModel(
            data=knowledge,
            message="Knowledge found",
            status=200,
        ),
        status_code=200,
    )
