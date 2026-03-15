import base64
import hashlib
import os
from cryptography.fernet import Fernet

from app.core.config import settings


def _fernet_key_from_secret(secret: str) -> bytes:
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


fernet = Fernet(_fernet_key_from_secret(settings.auth_secret_key))


def hash_username(username: str) -> str:
    normalized = username.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def encrypt_text(value: str) -> str:
    return fernet.encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_text(value: str) -> str:
    return fernet.decrypt(value.encode("utf-8")).decode("utf-8")


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    salt_bytes = salt or os.urandom(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        210000,
    )
    return derived.hex(), salt_bytes.hex()


def verify_password(password: str, stored_hash: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    computed, _ = hash_password(password, salt=salt)
    return computed == stored_hash

