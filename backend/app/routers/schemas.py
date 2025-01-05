from pydantic import BaseModel, EmailStr

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
