from services.cloud import CloudService
from services.agent import AgentService
from services.auth import AuthService
from services.knowledge import KnowledgeService
from src import AgenticRAG
from repository.database import SQLiteDatabaseRepository
from utils.logger import get_logger
from utils.config import get_config

config = get_config()
logger = get_logger()

logger.info("Initializing cloud service")
CLOUD_SERVICE = CloudService(
    type="s3",
    bucket_name=config.get("AWS_BUCKET_NAME"),
    access_key=config.get("AWS_ACCESS_KEY_ID"),
    secret_key=config.get("AWS_SECRET_ACCESS_KEY"),
    region_name=config.get("AWS_REGION_NAME"),
)

logger.info("Initialized agent service")
# AGENT_SERVICE = AgentService()
AGENT_SEVICE=""

DATABASE = SQLiteDatabaseRepository(
    db_path=config.get("SQLITE_DB_PATH"),
    init_db_path=config.get("SQLITE_INIT_DB_PATH"),   
    reinit_db=True if 
    config.get("SQLITE_REINIT_DB") == "true" else False,
)

AGENTIC_SERVICE = AgentService(
    config=config,
    database_instance=DATABASE,
)

AUTH_SERVICE = AuthService(
    database_instance=DATABASE,
    secret_key=config.get("AUTH_SECRET_KEY"),
    access_token_expires=int(config.get("ACCESS_TOKEN_EXPIRES")),
    refresh_token_expires=int(config.get("REFRESH_TOKEN_EXPIRES")),
)

KNOWLEDGE_SERVICE = KnowledgeService(
    database_instance=DATABASE,
)