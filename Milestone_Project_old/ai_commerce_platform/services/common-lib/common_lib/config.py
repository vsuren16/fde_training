from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://mongo:27017"
    mongo_db: str = "ai_commerce"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    user_service_url: str = "http://user-service:8001"
    product_service_url: str = "http://product-service:8002"
    cart_service_url: str = "http://cart-service:8003"
    order_service_url: str = "http://order-service:8004"
    search_service_url: str = "http://search-service:8005"
    active_embed_model_version: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
