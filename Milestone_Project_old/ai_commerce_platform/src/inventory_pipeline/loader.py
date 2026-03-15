"""MongoDB load helpers for inventory ingestion."""

from __future__ import annotations

from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from pyspark.sql import DataFrame


def upsert_inventory(final_df: DataFrame, mongo_uri: str, mongo_db: str) -> tuple[int, int, int]:
    client = MongoClient(mongo_uri)
    inventory = client[mongo_db].inventory

    operations = []
    for row in final_df.select(
        "inventory_id",
        "product_id",
        "warehouse_id",
        "available_stock",
        "reserved_stock",
        "damaged_stock",
        "reorder_level",
        "last_updated",
        "batch_number",
    ).toLocalIterator():
        operations.append(UpdateOne({"inventory_id": row["inventory_id"]}, {"$set": row.asDict()}, upsert=True))

    inserted = 0
    updated = 0
    failed = 0

    if operations:
        try:
            result = inventory.bulk_write(operations, ordered=False)
            inserted = int(result.upserted_count)
            updated = int(result.modified_count)
        except BulkWriteError as exc:
            details = exc.details or {}
            inserted = int(details.get("nUpserted", 0))
            updated = int(details.get("nModified", 0))
            failed = len(details.get("writeErrors", []))

    client.close()
    return inserted, updated, failed
