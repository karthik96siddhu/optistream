from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Define your variables and their types
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False  # Default value if not provided

    # Tell pydantic to read from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Instantiate the settings to be used accross the app
settings = Settings()
