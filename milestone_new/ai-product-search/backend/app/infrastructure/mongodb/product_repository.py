import uuid

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import UpdateOne

from app.core.config import settings
from app.domain.products.schemas import ProductCreate, ProductResponse


class MongoProductRepository:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    @classmethod
    def from_database(cls, db) -> "MongoProductRepository":
        return cls(db[settings.mongodb_products_collection])

    async def create_indexes(self) -> None:
        await self.collection.create_index("id", unique=True)
        await self.collection.create_index("category")
        await self.collection.create_index("brand")
        await self.collection.create_index("price")
        await self.collection.create_index("availability")

    async def count(self) -> int:
        return await self.collection.count_documents({})

    async def bulk_insert(self, products: list[dict]) -> None:
        if products:
            await self.collection.insert_many(products, ordered=False)

    async def sync_seed_catalog(self, products: list[dict]) -> int:
        operations = []
        for product in products:
            product_id = str(product.get("id", "")).strip()
            if not product_id:
                continue
            payload = {k: v for k, v in product.items() if k != "_id"}
            operations.append(
                UpdateOne(
                    {"id": product_id},
                    {"$set": payload},
                    upsert=True,
                )
            )
        if not operations:
            return 0
        result = await self.collection.bulk_write(operations, ordered=False)
        return int(result.modified_count + result.upserted_count)

    async def create(self, payload: ProductCreate) -> ProductResponse:
        item = {"id": f"p-{uuid.uuid4().hex[:10]}", **payload.model_dump()}
        await self.collection.insert_one(item)
        return ProductResponse(**item)

    async def get_by_id(self, product_id: str) -> ProductResponse | None:
        item = await self.collection.find_one({"id": product_id}, {"_id": 0})
        return ProductResponse(**item) if item else None

    async def list_paginated(self, filters: dict, page: int, page_size: int) -> tuple[list[ProductResponse], int]:
        query: dict = {}
        if filters.get("category"):
            query["category"] = filters["category"]
        if filters.get("brand"):
            query["brand"] = filters["brand"]
        if filters.get("color"):
            query["color"] = filters["color"]
        if filters.get("size"):
            query["size"] = filters["size"]
        if filters.get("availability") is not None:
            query["availability"] = filters["availability"]

        if filters.get("min_price") is not None or filters.get("max_price") is not None:
            query["price"] = {}
            if filters.get("min_price") is not None:
                query["price"]["$gte"] = filters["min_price"]
            if filters.get("max_price") is not None:
                query["price"]["$lte"] = filters["max_price"]

        if filters.get("search"):
            regex = {"$regex": filters["search"], "$options": "i"}
            query["$or"] = [
                {"product_name": regex},
                {"description": regex},
                {"short_description": regex},
            ]

        cursor = (
            self.collection.find(query, {"_id": 0})
            .skip((page - 1) * page_size)
            .limit(page_size)
            .sort("rating", -1)
        )
        items = [ProductResponse(**doc) async for doc in cursor]
        total = await self.collection.count_documents(query)
        return items, total

    async def list_all(self) -> list[ProductResponse]:
        cursor = self.collection.find({}, {"_id": 0})
        return [ProductResponse(**doc) async for doc in cursor]

    async def facet_values(self) -> dict[str, list[str]]:
        brands = await self.collection.distinct("brand")
        categories = await self.collection.distinct("category")
        colors = await self.collection.distinct("color")
        sizes = await self.collection.distinct("size")
        return {
            "brands": sorted(str(x) for x in brands),
            "categories": sorted(str(x) for x in categories),
            "colors": sorted(str(x) for x in colors),
            "sizes": sorted(str(x) for x in sizes),
        }
