import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List

from routers.schemas import ResponseModel
from utils.logger import get_logger

logger = get_logger()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        auth_secret_key: str,
        protected_prefix: List[str],
    ):
        super().__init__(app)
        self.secret = auth_secret_key
        self.protected_prefix = protected_prefix
        
    async def dispatch(self, request: Request, call_next):
        for prefix in self.protected_prefix:
            if request.url.path.startswith(prefix):
                logger.info(f"Protected route: {request.url.path}")
                bearer_token = request.headers.get("Authorization")
                if not bearer_token:
                    return JSONResponse(
                        status_code=401,
                        content=ResponseModel(status=401, message="Unauthorized", data={})
                    )
                
                token = bearer_token.split(" ")[1]
                
                try:
                    payload = jwt.decode(token, self.secret, algorithms=["HS256"])
                    # request.state.user = payload
                except jwt.ExpiredSignatureError:
                    return JSONResponse(
                        status_code=401,
                        content=ResponseModel(status=401, message="Unauthorized", data={})
                    )
                
                response = await call_next(request)
                return response

        return await call_next(request)
        
        