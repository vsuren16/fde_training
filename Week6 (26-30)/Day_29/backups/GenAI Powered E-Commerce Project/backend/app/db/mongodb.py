import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None


async def connect_mongo() -> None:
    global client
    client = AsyncIOMotorClient(settings.mongo_uri)
    logger.info("MongoDB connection initialized")


async def close_mongo() -> None:
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")
        client = None


def get_db() -> AsyncIOMotorDatabase:
    if not client:
        raise RuntimeError("Mongo client not initialized")
    return client[settings.mongo_db]


def get_collection(name: str):
    return get_db()[name]