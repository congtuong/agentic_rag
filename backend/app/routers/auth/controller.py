from utils.logger import get_logger
from utils.config import get_config
from routers.schemas import (
    LoginResponse,
    LoginRequest,
    ResponseModel,
    RegisterRequest,
    RefreshTokenRequest,
    RegisterResponse,
    ProfileResponse,
)
from bootstrap import AUTH_SERVICE

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, APIKeyCookie

router = APIRouter()

logger = get_logger()
config = get_config()

security = HTTPBearer()
cookie_security = APIKeyCookie(name="refresh_token")


@router.post("/login")
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
            content=ResponseModel(
                status=403, message="Invalid username or password", data={}
            ),
        )

    if isinstance(res, dict):
        response = JSONResponse(
            status_code=200,
            content=ResponseModel(status=200, message="Login successfully", data=res),
        )

        response.set_cookie(
            key="refresh_token",
            value=res["refresh_token"],
            httponly=True,
            max_age=int(config["REFRESH_TOKEN_EXPIRES"]) * 60,
            expires=int(config["REFRESH_TOKEN_EXPIRES"]) * 60,
            secure=True,
        )

        response.set_cookie(
            key="access_token",
            value=res["access_token"],
            httponly=False,
            max_age=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            expires=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            secure=False,
        )

        return response

    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={}),
    )


@router.post("/register")
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
            content=ResponseModel(status=404, message="User not found", data={}),
        )

    if res == 409:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(
                status=409, message="Username or email already exists", data={}
            ),
        )

    if res:
        return JSONResponse(
            status_code=200,
            content=ResponseModel(
                status=200,
                message="Register successfully",
                data={
                    "username": register_request.username,
                    "email": register_request.email,
                    "user_fullname": register_request.user_fullname,
                },
            ),
        )

    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={}),
    )


@router.post("/refresh", dependencies=[Depends(cookie_security)])
async def refresh(
    request: Request,
):
    """
    Refresh token
    """

    payload = request.state.user

    logger.info(f"Refresh token request incoming")
    # res = AUTH_SERVICE.refresh(**refresh_token_request.dict())
    res = AUTH_SERVICE.refresh(payload)

    if res is None:
        return JSONResponse(
            status_code=400,
            content=ResponseModel(status=400, message="Invalid refresh token", data={}),
        )

    if res == 410:
        return JSONResponse(
            status_code=410,
            content=ResponseModel(status=410, message="Refresh token expired", data={}),
        )

    if isinstance(res, dict):
        response = JSONResponse(
            status_code=200,
            content=ResponseModel(
                status=200, message="Refresh token successfully", data=res
            ),
        )
        response.set_cookie(
            key="access_token",
            value=res["access_token"],
            httponly=False,
            max_age=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            expires=int(config["ACCESS_TOKEN_EXPIRES"]) * 60,
            secure=False,
        )
        return response

    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={}),
    )


@router.get("/profile", dependencies=[Depends(security)])
async def profile(
    request: Request,
):
    """
    Profile
    """

    if not AUTH_SERVICE.is_access_token(request.state.user):
        return JSONResponse(
            status_code=401,
            content=ResponseModel(status=401, message="Unauthorized", data={}),
        )

    payload = request.state.user

    logger.info(f"Profile request incoming")
    res = AUTH_SERVICE.get_profile(payload["username"])

    if res is None:
        return JSONResponse(
            status_code=400,
            content=ResponseModel(status=400, message="Invalid access token", data={}),
        )

    if res == 410:
        return JSONResponse(
            status_code=410,
            content=ResponseModel(status=410, message="Access token expired", data={}),
        )

    if isinstance(res, dict):
        return JSONResponse(
            status_code=200,
            content=ResponseModel(
                status=200,
                message="Profile successfully",
                data=ProfileResponse(
                    username=res["username"],
                    email=res["email"],
                    user_fullname=res["user_fullname"],
                    user_role=res["user_role"],
                    created_at=res["created_at"],
                    updated_at=res["updated_at"],
                ).dict(),
            ),
        )
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status=500, message="Internal server error", data={}),
    )


@router.get("/logout")
async def logout(
    request: Request,
):
    """
    Logout
    """

    response = RedirectResponse(url=f"{config['FRONTEND_URL']}/auth/login")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return response
