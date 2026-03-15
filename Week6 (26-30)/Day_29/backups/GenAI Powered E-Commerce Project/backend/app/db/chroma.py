import os
import chromadb

_client = None
_collection = None

def get_chroma_collection():
    """
    Singleton Chroma Persistent collection.
    Chroma client is sync, so we will call it via asyncio.to_thread in services.
    """
    global _client, _collection
    if _collection is not None:
        return _collection

    chroma_path = os.getenv("CHROMA_PATH", "./chroma_data")
    collection_name = os.getenv("CHROMA_COLLECTION", "walmart_products")

    _client = chromadb.PersistentClient(path=chroma_path)
    _collection = _client.get_or_create_collection(name=collection_name)
    return _collection