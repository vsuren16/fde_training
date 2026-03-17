from __future__ import annotations

from functools import lru_cache

from pymongo import ASCENDING, MongoClient, ReplaceOne
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.core.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(
        settings.mongodb_uri,
        maxPoolSize=settings.mongodb_max_pool_size,
        minPoolSize=5,
        serverSelectionTimeoutMS=5000,
        retryWrites=True,
    )


class IncidentRepository:
    def __init__(self) -> None:
        settings = get_settings()
        self.collection: Collection = get_mongo_client()[settings.mongodb_db]["incidents"]

    def ensure_indexes(self) -> None:
        self.collection.create_index([("incident_id", ASCENDING)], unique=True)
        self.collection.create_index([("priority", ASCENDING)])
        self.collection.create_index([("category", ASCENDING)])
        self.collection.create_index([("status", ASCENDING)])
        self.collection.create_index([("team", ASCENDING)])

    def upsert_many(self, incidents: list[dict]) -> int:
        operations = [
            ReplaceOne({"incident_id": item["incident_id"]}, item, upsert=True)
            for item in incidents
        ]
        if not operations:
            return 0
        result = self.collection.bulk_write(operations, ordered=False)
        return result.upserted_count + result.modified_count

    def count(self) -> int:
        return self.collection.count_documents({})

    def fetch_all(self) -> list[dict]:
        return list(self.collection.find({}, {"_id": 0}))

    def fetch_by_ids(self, incident_ids: list[str]) -> list[dict]:
        if not incident_ids:
            return []
        documents = list(
            self.collection.find({"incident_id": {"$in": incident_ids}}, {"_id": 0})
        )
        order = {incident_id: index for index, incident_id in enumerate(incident_ids)}
        return sorted(documents, key=lambda item: order.get(item["incident_id"], 999999))

    def distinct_values(self, field_name: str) -> list[str]:
        values = self.collection.distinct(field_name)
        return sorted(
            [str(value).strip() for value in values if value is not None and str(value).strip()]
        )

    def replace_all(self, incidents: list[dict]) -> int:
        self.collection.delete_many({})
        return self.upsert_many(incidents)

    def store_feedback(self, feedback: dict) -> None:
        self.collection.database["feedback"].insert_one(feedback)


class AdminRepository:
    def __init__(self) -> None:
        settings = get_settings()
        self.collection: Collection = get_mongo_client()[settings.mongodb_db]["admins"]

    def ensure_indexes(self) -> None:
        self.collection.create_index([("username", ASCENDING)], unique=True)

    def count(self) -> int:
        return self.collection.count_documents({})

    def find_by_username(self, username: str) -> dict | None:
        return self.collection.find_one({"username": username})

    def create_admin(self, admin: dict) -> bool:
        try:
            self.collection.insert_one(admin)
            return True
        except DuplicateKeyError:
            return False
