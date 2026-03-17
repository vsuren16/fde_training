from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.container import get_admin_repository
from app.core.config import get_settings
from app.schemas.admin import _normalize_username


class AdminAuthService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.repository = get_admin_repository()

    @staticmethod
    def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
        salt_bytes = salt or os.urandom(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt_bytes,
            120_000,
        )
        return base64.b64encode(salt_bytes).decode("utf-8"), base64.b64encode(digest).decode("utf-8")

    def signup(self, username: str, password: str) -> bool:
        self.repository.ensure_indexes()
        username = _normalize_username(username)
        salt, password_hash = self._hash_password(password)
        return self.repository.create_admin(
            {
                "username": username,
                "password_salt": salt,
                "password_hash": password_hash,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    def has_persisted_admins(self) -> bool:
        return self.repository.count() > 0

    def _verify_persisted_user(self, username: str, password: str) -> bool:
        username = _normalize_username(username)
        admin = self.repository.find_by_username(username)
        if not admin:
            return False
        salt = base64.b64decode(admin["password_salt"].encode("utf-8"))
        _, expected_hash = self._hash_password(password, salt=salt)
        return hmac.compare_digest(expected_hash, admin["password_hash"])

    def login(self, username: str, password: str) -> tuple[str, int]:
        username = _normalize_username(username)
        using_persisted = self._verify_persisted_user(username, password)
        using_env_fallback = (
            not self.has_persisted_admins()
            and username == _normalize_username(self.settings.admin_username)
            and password == self.settings.admin_password
        )
        if not using_persisted and not using_env_fallback:
            raise HTTPException(status_code=401, detail="invalid admin credentials")

        expires_at = int(time.time()) + self.settings.admin_session_ttl_seconds
        payload = f"{username}:{expires_at}"
        signature = hmac.new(
            self.settings.admin_session_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        token = base64.urlsafe_b64encode(
            f"{payload}:{signature}".encode("utf-8")
        ).decode("utf-8")
        return token, self.settings.admin_session_ttl_seconds

    def verify_token(self, token: str) -> str:
        try:
            decoded = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
            username, expires_at, signature = decoded.split(":", maxsplit=2)
        except Exception as exc:
            raise HTTPException(status_code=401, detail="invalid admin token") from exc

        payload = f"{username}:{expires_at}"
        expected = hmac.new(
            self.settings.admin_session_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=401, detail="invalid admin token signature")
        if int(expires_at) < int(time.time()):
            raise HTTPException(status_code=401, detail="admin token expired")
        return username
