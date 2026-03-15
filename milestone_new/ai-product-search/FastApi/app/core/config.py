from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Outfit Recommendation API"
    app_version: str = "1.0.0"
    environment: str = "dev"

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model_version: str = "openai:text-embedding-3-small|local:all-MiniLM-L6-v2"
    embedding_timeout_seconds: int = 3
    embedding_max_retries: int = 0

    database_url: str = "sqlite+aiosqlite:///./app.db"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "ai_outfit_store"
    mongodb_products_collection: str = "products"
    mongodb_users_collection: str = "users"
    mongodb_orders_collection: str = "orders"
    seed_products_count: int = 1000
    auth_secret_key: str = "dev-auth-secret-change-me"
    chroma_persist_dir: str = "./chroma_data"
    chroma_products_collection: str = "products_embeddings"
    chroma_policy_collection: str = "policy_embeddings"
    policy_docs_path: str = "./docs/policies"
    top_k: int = 5
    request_timeout_seconds: int = 8
    use_fake_embeddings: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = "ai-product-search"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_tracing: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
