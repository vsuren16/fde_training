import pytest
from pydantic import ValidationError

from app.schemas.admin import AdminSignupRequest
from app.services.admin_auth_service import AdminAuthService


class FakeAdminRepository:
    def __init__(self) -> None:
        self.admins: dict[str, dict] = {}

    def ensure_indexes(self) -> None:
        return None

    def count(self) -> int:
        return len(self.admins)

    def find_by_username(self, username: str) -> dict | None:
        return self.admins.get(username)

    def create_admin(self, admin: dict) -> bool:
        if admin["username"] in self.admins:
            return False
        self.admins[admin["username"]] = admin
        return True


def test_admin_signup_stores_hash_and_enables_login() -> None:
    service = AdminAuthService()
    service.repository = FakeAdminRepository()
    service.settings.admin_session_secret = "test-secret"

    created = service.signup("alice", "strong-password")

    assert created is True
    stored = service.repository.find_by_username("alice")
    assert stored is not None
    assert stored["password_hash"] != "strong-password"
    assert "password_salt" in stored

    token, expires_in = service.login("alice", "strong-password")

    assert token
    assert expires_in == service.settings.admin_session_ttl_seconds


def test_admin_login_uses_env_bootstrap_when_no_persisted_admin_exists() -> None:
    service = AdminAuthService()
    service.repository = FakeAdminRepository()
    service.settings.admin_username = "admin"
    service.settings.admin_password = "admin"
    service.settings.admin_session_secret = "test-secret"

    token, _ = service.login("admin", "admin")

    assert token


def test_admin_signup_rejects_reserved_username() -> None:
    with pytest.raises(ValidationError) as exc_info:
        AdminSignupRequest(username="admin_test", password="StrongPass1!")

    assert "reserved terms" in str(exc_info.value)


def test_admin_signup_rejects_weak_password() -> None:
    with pytest.raises(ValidationError) as exc_info:
        AdminSignupRequest(username="alice.ops", password="weakpassword")

    assert "uppercase" in str(exc_info.value).lower() or "number" in str(exc_info.value).lower()


def test_admin_signup_normalizes_username_before_storage() -> None:
    service = AdminAuthService()
    service.repository = FakeAdminRepository()
    service.settings.admin_session_secret = "test-secret"

    created = service.signup("Alice.Ops", "StrongPass1!")

    assert created is True
    assert service.repository.find_by_username("alice.ops") is not None
