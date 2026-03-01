from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Slack
    slack_bot_token: str = ""
    slack_app_token: str = ""
    slack_signing_secret: str = ""

    # Translation
    translation_provider: str = "google"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    deepl_api_key: str = ""

    # Defaults
    default_target_language: str = "en"
    database_path: str = "cluely.db"
    log_level: str = "INFO"
    cache_max_size: int = 1000
