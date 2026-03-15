from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "genai-ecommerce"
    env: str = "dev"  # dev/stage/prod
    log_level: str = "INFO"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "ecommerce"
    mongo_products_collection: str = "products"

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_embed_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.2

    langsmith_api_key: str = ""
    langsmith_project: str = "genai-ecommerce"
    langsmith_tracing: bool = False
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    chroma_path: str = "./chroma_data"
    chroma_collection: str = "walmart_products"
    chroma_reviews_collection: str = "walmart_reviews"
    

settings = Settings()
