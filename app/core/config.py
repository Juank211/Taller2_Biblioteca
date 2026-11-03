from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    cors_origins: List[str]
    environment: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
