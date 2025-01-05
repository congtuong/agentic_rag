from utils.logger import get_logger
from utils.config import get_config
from routers.schemas import LoginResponse, LoginRequest, ResponseModel, RegisterRequest, RefreshTokenRequest, RegisterResponse
from bootstrap import AUTH_SERVICE

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

logger = get_logger()
config = get_config()

@router.post("/auth/login")
async def login(
    login_request: LoginRequest,
):
    """
    Login
    """
    logger.info(f"Login request incoming")
    res = AUTH_SERVICE.login(**login_request.dict())
    logger.info(f"{res}")
    
    if res == 403:
        return JSONResponse(
            status_code=403,
            content=ResponseModel(status=403, message="Invalid username or password", data={})
        )
        
    
    if isinstance(res, dict):
        response = JSONResponse(
            status_code=200,
            content=ResponseModel(status=200, message="Login successfully", data=res)
        )

        response.set_cookie(
            key="refresh_token",
            value=res["refresh_token"],
            httponly=True,
            max_age=int(config["REFRESH_TOKEN_EXPIRES"]) * 60,
            expires=int(config["REFRESH_TOKEN_EXPIRES"]) * 60,
            secure=False
        )
        
        response.set_cookie(
            key="access_token",
            value=res["access_token"],
            httponly=True,
            max_age=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            expires=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            secure=False
        )
        
        return response
    
        
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={})
    )

@router.post("/auth/register")
async def register(
    register_request: RegisterRequest,
):
    """
    Register
    """
    logger.info(f"Register request incoming")
    res = AUTH_SERVICE.register(**register_request.dict())
    logger.info(f"{res}")        

    if res == 404:
        return JSONResponse(
            status_code=404,
            content=ResponseModel(status=404, message="User not found", data={})
        )
        
    if res == 409:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(status=409, message="Username or email already exists", data={})
        )

    if res:
        return JSONResponse(
            status_code=200,
            content=ResponseModel(status=200, message="Register successfully", data={
                "username": register_request.username,
                "email": register_request.email,
                "user_fullname": register_request.user_fullname
            })
        )

        
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={})
    )
    
@router.post("/auth/refresh")
async def refresh(
    refresh_token_request: RefreshTokenRequest,
):
    """
    Refresh token
    """
    logger.info(f"Refresh token request incoming")
    res = AUTH_SERVICE.refresh(**refresh_token_request.dict())
    
    if res is None:
        return JSONResponse(
            status_code=400,
            content=ResponseModel(status=400, message="Invalid refresh token", data={})
        )

    
    if res == 410:
        return JSONResponse(
            status_code=410,
            content=ResponseModel(status=410, message="Refresh token expired", data={})
        )
           
    if isinstance(res, dict):
        return JSONResponse(
            status_code=200,
            content=ResponseModel(status=200, message="Refresh token successfully", data=res)
        ) 
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={})
    )    
