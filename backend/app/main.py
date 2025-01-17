import time
import dotenv

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from utils.config import get_config
from utils.logger import get_logger

from const import (
    ContextualRAGConfig,
)


config = get_config()
# print(config['logdir'])
logger = get_logger()


description = """
This is API.
"""

# tags_metadata = [
#     {
#         "name": "queries",
#         "description": "API endpoints for query",
#     },
#     {
#         "name": "keyframes",
#         "description": "API endpoints for get keyframe info, eg. get all shot's keyframes",
#     },
# ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up")
    logger.info("Start application in %s mode" % config["MODE"])
    yield

    # Shutdown
    logger.info("Shutting down")
    # singletons.shutdown()


app = FastAPI(
    docs_url=config["DOCS_URL"] if config["MODE"] == "development" else None,
    redoc_url=config["REDOC_URL"] if config["MODE"] == "development" else None,
    lifespan=lifespan,
    description=description,
    version="v0.1",
    contact={
        "name": "Cong Tuong",
        "email": "22521624@gm.uit.edu.vn",
    },
    debug=True,
    # openapi_tags=tags_metadata,
)


# Turn middleware off if performance is affected
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_exception_handler(request: Request, exc: Exception):
    # Handle 500 exception
    log_request(request, logger)
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": True, "message": "Internal Server Error"},
    )


@app.get("/")
async def root():
    return {
        "message": "Application is running",
    }


@app.get("/healh_check")
async def healh_check():
    logger.info("Health check")

    return {
        "status": "Running (Healthy)",
    }


from routers.agents.controller import router as agents_router
from routers.auth.controller import router as auth_router
from routers.documents.controller import router as documents_router
from routers.knowledges.controller import router as knowledges_router

app.include_router(agents_router, prefix="/agents", tags=["agents"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(knowledges_router, prefix="/knowledges", tags=["knowledges"])

from middleware.authentication import AuthMiddleware

app.add_middleware(
    AuthMiddleware,
    auth_secret_key=config["AUTH_SECRET_KEY"],
    # Add protected prefix here, if only an endpoint of a specific prefix needs to be protected, simply add the whole endpoint
    protected_prefix=[
        "/agents",
        "/auth/refresh",
        "/auth/profile",
        "/documents",
        "/knowledges",
    ],
)

if config["CORS"] == "true":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:30000", "http://localhost:30001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=config["HOST"], port=int(config["PORT"]))
