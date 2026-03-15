from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv(".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "genai-ecommerce"
    env: str = "dev"  # dev/stage/prod
    log_level: str = "INFO"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "ecommerce"
    mongo_products_collection: str = "products"

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_embed_model: str = "text-embedding-3-small"

    chroma_path: str = "./chroma_data"
    chroma_collection: str = "walmart_products"
    chroma_reviews_collection: str = "walmart_reviews"
    

settings = Settings()