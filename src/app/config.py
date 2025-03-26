from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from src.app.common.constants import  LOCAL

load_dotenv(".env")


class MCQAppSettings(BaseSettings):
    """
    MCQ App Settings
    """
    ENVIRONMENT: str = LOCAL

    # Database Configuration
    DB_USER: str = os.getenv("DB_USER", "default_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "default_password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "mcq-fastapi-db")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.getenv("ALGORITHM")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = MCQAppSettings()
