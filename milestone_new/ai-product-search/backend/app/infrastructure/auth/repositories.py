from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from app.core.security.crypto import encrypt_text, hash_password, hash_username


class InMemoryUserRepository:
    def __init__(self) -> None:
        admin_hash, admin_salt = hash_password("admin")
        self.users: dict[str, dict] = {
            hash_username("admin"): {
                "id": "u-admin",
                "username_hash": hash_username("admin"),
                "username_encrypted": encrypt_text("admin"),
                "password_hash": admin_hash,
                "password_salt": admin_salt,
                "role": "admin",
            }
        }

    async def find_by_username(self, username: str) -> dict | None:
        return self.users.get(hash_username(username))

    async def create_user(self, username: str, password: str, role: str = "user") -> dict:
        uhash = hash_username(username)
        pwd_hash, pwd_salt = hash_password(password)
        user = {
            "id": f"u-{len(self.users) + 1}",
            "username_hash": uhash,
            "username_encrypted": encrypt_text(username),
            "password_hash": pwd_hash,
            "password_salt": pwd_salt,
            "role": role,
        }
        self.users[uhash] = user
        return user

    async def update_password(self, username: str, password: str) -> None:
        user = self.users.get(hash_username(username))
        if user:
            pwd_hash, pwd_salt = hash_password(password)
            user["password_hash"] = pwd_hash
            user["password_salt"] = pwd_salt


class InMemorySessionRepository:
    def __init__(self) -> None:
        self.sessions: dict[str, dict] = {}

    def create_session(self, user: dict, ttl_minutes: int = 240) -> str:
        token = token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
        self.sessions[token] = {
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "expires_at": expires_at,
        }
        return token

    def get_session(self, token: str) -> dict | None:
        session = self.sessions.get(token)
        if not session:
            return None
        if datetime.now(timezone.utc) > session["expires_at"]:
            self.sessions.pop(token, None)
            return None
        return session


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: list[dict] = []

    async def create_order(self, order: dict) -> dict:
        self.orders.append(order)
        return order

    async def list_user_orders(self, user_id: str) -> list[dict]:
        return [o for o in self.orders if o["user_id"] == user_id]
