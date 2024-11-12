"""
Configuration module for the application.
Handles all environment variables and application settings.
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    Automatically reads environment variables from .env file.
    """

    # Database settings
    SQL_SERVER_HOST: str
    SQL_DATABASE: str

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SQL Server FastAPI"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
