import asyncio
import json
import os
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "ecommerce")
COLLECTION = os.getenv("MONGO_PRODUCTS_COLLECTION", "products")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"

async def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    col = db[COLLECTION]

    # Create indexes
    # 1) Text index for title/description (enables $text queries later)
    await col.create_index([("title", "text"), ("description", "text")], name="text_title_desc")

    # 2) Useful filter/sort indexes
    await col.create_index("brand", name="idx_brand")
    await col.create_index("category", name="idx_category")
    await col.create_index("price", name="idx_price")

    # Load data
    products = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    # Optional: clear existing docs (dev only)
    await col.delete_many({})

    # Insert
    if products:
        result = await col.insert_many(products)
        print(f"Inserted {len(result.inserted_ids)} products into {MONGO_DB}.{COLLECTION}")
    else:
        print("No products found in JSON.")

    client.close()

if __name__ == "__main__":
    asyncio.run(main())