import jwt
import uuid
from datetime import datetime, timedelta

from repository.database import (
    BaseDatabaseRepository,
    PostgresDatabaseRepository,
    SQLiteDatabaseRepository,
)
from utils.encoder import hash_password, verify_password
from utils.logger import get_logger

logger = get_logger()

class AuthService:
    def __init__(
        self,
        database_instance: BaseDatabaseRepository,
        secret_key: str,
        access_token_expires: int = 15,
        refresh_token_expires: int = 60,
    ):
        self.secret = secret_key
        self.database_instance = database_instance
        self.access_token_expiration = access_token_expires
        self.refresh_token_expiration = refresh_token_expires
    
    def _generate_token(self, username: str, expiration: int, token_id: str):
        payload = {
            "token_id": token_id,
            "username": username,
            "exp": datetime.utcnow() + timedelta(minutes=expiration),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def _is_exists(self, table: str, column: str, value: str):
        return self.database_instance.read_by(table, column, value)
    
    def refresh(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            session = self.database_instance.read("sessions", payload["token_id"])
            logger.info(f"Refreshing token for user: {payload}")
            if payload['exp'] < int(datetime.utcnow().timestamp()):
                return 410
            if session:
                user = self.database_instance.read("users", session["user_id"])
                if user:
                    access_token = self._generate_token(user["username"], self.access_token_expiration, str(uuid.uuid4()))
                    logger.info(f"Refreshed token success for user: {user['username']}")
                    return {"access_token": access_token}
        except jwt.ExpiredSignatureError:
            logger.error(f"Token expired")
            return 410
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
        return None
    
    def login(self, username: str, password: str):
        # try:
        user = self.database_instance.read_by("users", "username", username)
        if user:
            if verify_password(password, user["password"]):
                refresh_token_id = str(uuid.uuid4())
                logger.info(f"Generating token for user: {self.access_token_expiration}, {refresh_token_id}")
                refresh_token = self._generate_token(username, self.refresh_token_expiration, refresh_token_id)
                access_token = self._generate_token(username, self.access_token_expiration, refresh_token_id)
                
                self.database_instance.create("sessions", id=refresh_token_id, user_id=user["id"])
                logger.info(f"Login success for user: {username}")
                return {"access_token": access_token, "refresh_token": refresh_token}
            else:
                logger.error(f"Invalid password for user: {username}")
        else:
            logger.error(f"User not found: {username}")
        return 403
        # except Exception as e:
        #     return None
    
    def register(self, username: str, email: str, password: str, user_fullname: str):
        logger.info(f"Registering user: {username}, {email}, {user_fullname}")
        try:
            if self._is_exists("users", "username", username) or self._is_exists("users", "email", email):
                return 409
            
            hashed_password = hash_password(password)
            user = self.database_instance.create(
                "users",
                username=username,
                email=email,
                password=hashed_password,
                user_fullname=user_fullname,
                user_role="user",
            )
            if user:
                logger.info(f"User registered: {username}")
                return user
            return None
        except Exception as e:
            return None
    
    