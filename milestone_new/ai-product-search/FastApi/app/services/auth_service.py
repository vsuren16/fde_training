import re

from app.core.security.crypto import verify_password
from app.domain.auth.schemas import UserSession
from app.infrastructure.auth.repositories import InMemorySessionRepository


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
MOBILE_RE = re.compile(r"^\d{10}$")


class AuthService:
    def __init__(self, users, sessions: InMemorySessionRepository) -> None:
        self.users = users
        self.sessions = sessions

    def _validate_username(self, username: str) -> None:
        if username == "admin":
            return
        if not (EMAIL_RE.match(username) or MOBILE_RE.match(username)):
            raise ValueError("Username must be a valid email or 10-digit mobile number")

    async def ensure_admin(self) -> None:
        admin = await self.users.find_by_username("admin")
        if not admin:
            await self.users.create_user("admin", "admin", role="admin")

    async def signup(self, username: str, password: str) -> None:
        self._validate_username(username)
        if username == "admin":
            raise ValueError("Reserved username")
        existing = await self.users.find_by_username(username)
        if existing:
            raise ValueError("User already exists")
        await self.users.create_user(username=username, password=password, role="user")

    async def login(self, username: str, password: str) -> tuple[str, UserSession]:
        self._validate_username(username)
        user = await self.users.find_by_username(username)
        if user is None:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user["password_hash"], user["password_salt"]):
            raise ValueError("Invalid credentials")

        session_payload = {"id": user["id"], "username": username, "role": user["role"]}
        token = self.sessions.create_session(session_payload)
        session = UserSession(user_id=user["id"], username=username, role=user["role"])
        return token, session

    async def forgot_password(self, username: str) -> dict:
        self._validate_username(username)
        user = await self.users.find_by_username(username)
        if not user or user["role"] == "admin":
            return {"message": "If account exists, reset instructions were processed", "temp_password": None}
        temp_password = "Reset@123"
        await self.users.update_password(username, temp_password)
        return {"message": "Password reset successful for demo", "temp_password": temp_password}

    def authenticate_token(self, token: str) -> UserSession | None:
        session = self.sessions.get_session(token)
        if not session:
            return None
        return UserSession(
            user_id=session["user_id"],
            username=session["username"],
            role=session["role"],
        )

