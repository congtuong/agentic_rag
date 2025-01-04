from services.cloud import CloudService
from services.agent import AgentService
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

AGENTIC_SERVICE = AgenticRAG(config=config)

DATABASE = SQLiteDatabaseRepository(db_path=config.get("SQLITE_DB_PATH"))