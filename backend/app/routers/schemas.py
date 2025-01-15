from pydantic import BaseModel, EmailStr, Field

from typing import List


def ResponseModel(data, message, status):
    return {
        "data": data,
        "message": message,
        "status": status,
    }


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_fullname: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegisterResponse(BaseModel):
    username: str
    email: str
    user_fullname: str


class CreateKnowledgeRequest(BaseModel):
    name: str
    documents: List[str] = Field(..., min_items=1)


class CreateKnowledgeResponse(BaseModel):
    name: str
    knowledge_id: str


class CreateChatBotRequest(BaseModel):
    name: str
    knowledges: List[str] = Field(..., min_items=1)


class CreateChatBotResponse(BaseModel):
    name: str
    chatbot_id: str


class ProfileResponse(BaseModel):
    username: str
    email: str
    user_fullname: str
    user_role: str
    created_at: str
    updated_at: str


class ChatRequest(BaseModel):
    query: str
    conversation_id: str
