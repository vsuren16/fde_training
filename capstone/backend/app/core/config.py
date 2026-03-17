from functools import lru_cache
from pathlib import Path
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "incident-kb-assistant"
    app_env: str = "local"
    log_level: str = "INFO"
    log_dir: str = str(Path(__file__).resolve().parents[2] / "logs")
    log_file_name: str = "application.log"
    log_max_bytes: int = 5_242_880
    log_backup_count: int = 5
    api_prefix: str = "/api/v1"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "incident_kb"
    mongodb_max_pool_size: int = 50
    chroma_persist_dir: str = str(Path(__file__).resolve().parents[2] / "chroma")
    chroma_collection: str = "incidents"
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4.1-mini"
    openai_timeout_seconds: int = 20
    embedding_batch_size: int = 500
    langsmith_api_key: str = ""
    langsmith_project: str = "incident-kb-assistant"
    langsmith_project_url: str = ""
    langsmith_tracing: bool = True
    admin_username: str = ""
    admin_password: str = ""
    admin_session_secret: str = secrets.token_urlsafe(32)
    admin_session_ttl_seconds: int = 28800
    raw_dataset_path: str = str(
        Path(__file__).resolve().parents[2] / "data" / "raw" / "it_incidents_10k.csv"
    )
    processed_dataset_path: str = str(
        Path(__file__).resolve().parents[2] / "data" / "processed" / "incidents_cleaned.csv"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
