"""
Centralized configuration. Single source of truth for anything that would
otherwise be an os.environ.get() scattered across modules.

Usage:
    from consensus_curator.config import settings
    settings.database_url
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    database_url: str


settings = Settings()
