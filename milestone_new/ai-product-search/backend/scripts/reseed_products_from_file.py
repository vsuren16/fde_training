import asyncio
import sys
from pathlib import Path

from app.core.config import settings
from app.infrastructure.embedding.manager import EmbeddingManager
from app.infrastructure.mongodb.client import MongoClientManager
from app.infrastructure.mongodb.product_repository import MongoProductRepository
from app.infrastructure.vector_store.chroma_store import ChromaVectorStore
from app.seed.external_products import load_external_products
from app.services.ingestion_service import IngestionService
from app.services.product_service import ProductService


async def main() -> None:
    source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "mongodb_mockdata.txt"
    if not source.exists():
        raise FileNotFoundError(f"Dataset file not found: {source}")

    products = load_external_products(source)
    if not products:
        raise ValueError(f"No products parsed from {source}")

    manager = MongoClientManager()
    embedding_manager = EmbeddingManager()
    try:
        db = await manager.connect()
        repo = MongoProductRepository.from_database(db)
        await repo.create_indexes()
        await db[settings.mongodb_products_collection].delete_many({})
        await repo.bulk_insert(products)

        product_service = ProductService(repo)
        vector_store = ChromaVectorStore(
            persist_dir=settings.chroma_persist_dir,
            collection_name=settings.chroma_products_collection,
        )
        ingestion_service = IngestionService(product_service, embedding_manager, vector_store)
        await ingestion_service.build_index()
    finally:
        await embedding_manager.close()
        await manager.close()

    print(f"Replaced Mongo products with {len(products)} records from {source}")


if __name__ == "__main__":
    asyncio.run(main())
