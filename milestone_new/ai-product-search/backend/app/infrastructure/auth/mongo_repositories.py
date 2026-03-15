from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from app.core.config import settings
from app.core.security.crypto import encrypt_text, hash_password, hash_username


class MongoUserRepository:
    def __init__(self, users_collection: AsyncIOMotorCollection) -> None:
        self.users_collection = users_collection

    @classmethod
    def from_database(cls, db) -> "MongoUserRepository":
        return cls(db[settings.mongodb_users_collection])

    async def create_indexes(self) -> None:
        await self.users_collection.create_index("username_hash", unique=True)
        await self.users_collection.create_index("role")

    async def find_by_username(self, username: str) -> dict | None:
        uhash = hash_username(username)
        return await self.users_collection.find_one({"username_hash": uhash}, {"_id": 0})

    async def create_user(self, username: str, password: str, role: str = "user") -> dict:
        pwd_hash, pwd_salt = hash_password(password)
        user = {
            "id": f"u-{hash_username(username)[:12]}",
            "username_hash": hash_username(username),
            "username_encrypted": encrypt_text(username),
            "password_hash": pwd_hash,
            "password_salt": pwd_salt,
            "role": role,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            await self.users_collection.insert_one(user)
        except DuplicateKeyError as exc:
            raise ValueError("User already exists") from exc
        return user

    async def update_password(self, username: str, new_password: str) -> None:
        pwd_hash, pwd_salt = hash_password(new_password)
        await self.users_collection.update_one(
            {"username_hash": hash_username(username)},
            {"$set": {"password_hash": pwd_hash, "password_salt": pwd_salt}},
        )


class MongoOrderRepository:
    def __init__(self, orders_collection: AsyncIOMotorCollection) -> None:
        self.orders_collection = orders_collection

    @classmethod
    def from_database(cls, db) -> "MongoOrderRepository":
        return cls(db[settings.mongodb_orders_collection])

    async def create_indexes(self) -> None:
        await self.orders_collection.create_index("order_id", unique=True)
        await self.orders_collection.create_index("user_id")
        await self.orders_collection.create_index("created_at")

    async def create_order(self, order: dict) -> dict:
        await self.orders_collection.insert_one(order)
        return order

    async def list_user_orders(self, user_id: str) -> list[dict]:
        cursor = self.orders_collection.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1)
        return [row async for row in cursor]
