import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=settings.chroma_path,  # uses CHROMA_PATH=./chroma_data
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _chroma_client

def get_products_collection():
    # existing collection used by /search
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=settings.chroma_collection,  # uses CHROMA_COLLECTION=walmart_products
        metadata={"hnsw:space": "cosine"},
    )

def get_reviews_collection():
    # NEW collection used by recommendations
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=settings.chroma_reviews_collection,  # uses CHROMA_REVIEWS_COLLECTION=walmart_reviews
        metadata={"hnsw:space": "cosine"},
    )