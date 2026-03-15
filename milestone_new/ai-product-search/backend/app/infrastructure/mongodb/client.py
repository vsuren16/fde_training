import logging
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)


class MongoClientManager:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> AsyncIOMotorDatabase:
        self.client = AsyncIOMotorClient(
            settings.mongodb_uri,
            maxPoolSize=100,
            minPoolSize=5,
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000,
            socketTimeoutMS=2000,
        )
        await asyncio.wait_for(self.client.admin.command("ping"), timeout=3)
        self.db = self.client[settings.mongodb_db]
        logger.info("mongodb_connected", extra={"db": settings.mongodb_db})
        return self.db

    async def close(self) -> None:
        if self.client:
            self.client.close()
            logger.info("mongodb_closed")
