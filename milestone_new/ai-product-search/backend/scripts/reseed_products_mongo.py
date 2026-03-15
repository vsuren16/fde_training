import asyncio

from app.core.config import settings
from app.infrastructure.mongodb.client import MongoClientManager
from app.infrastructure.mongodb.product_repository import MongoProductRepository
from app.seed.mock_products import generate_mock_products


async def main() -> None:
    manager = MongoClientManager()
    db = await manager.connect()
    repo = MongoProductRepository.from_database(db)
    await repo.create_indexes()

    collection = db[settings.mongodb_products_collection]
    await collection.delete_many({})
    await repo.bulk_insert(generate_mock_products(settings.seed_products_count))
    await manager.close()
    print("Mongo products reseeded successfully")


if __name__ == "__main__":
    asyncio.run(main())

