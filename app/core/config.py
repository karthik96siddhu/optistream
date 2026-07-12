from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Define your variables and their types
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str
    DEBUG: bool = False  # Default value if not provided

    # Tell pydantic to read from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

# Instantiate the settings to be used accross the app
settings = Settings()
