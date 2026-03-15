import asyncio

from app.infrastructure.embedding.manager import EmbeddingManager
from app.infrastructure.vector_store.base import VectorStore
from app.services.product_service import ProductService


class IngestionService:
    def __init__(self, product_service: ProductService, embedding_manager: EmbeddingManager, vector_store: VectorStore) -> None:
        self.product_service = product_service
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store

    async def build_index(self) -> None:
        documents = await self.product_service.product_documents()
        if not documents:
            self.vector_store.build([], [])
            return

        semaphore = asyncio.Semaphore(8)

        async def embed_doc(doc: dict) -> tuple[list[float], dict]:
            async with semaphore:
                embedding = await self.embedding_manager.embed(doc["text"])
                payload = {**doc["metadata"], "embedding_model_version": embedding.model_version}
                return embedding.vector, payload

        results = await asyncio.gather(*(embed_doc(doc) for doc in documents))
        embeddings, payloads = zip(*results)
        self.vector_store.build(list(embeddings), list(payloads))
