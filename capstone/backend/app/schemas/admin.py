import re

from pydantic import BaseModel, Field, field_validator


USERNAME_PATTERN = re.compile(r"^[a-z][a-z0-9._-]{2,99}$")
RESERVED_USERNAME_TOKENS = {
    "test",
    "dev",
    "demo",
    "temp",
    "admin_test",
    "qa",
    "staging",
}


def _normalize_username(value: str) -> str:
    return value.strip().lower()


def _validate_username(value: str) -> str:
    normalized = _normalize_username(value)
    if not USERNAME_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Username must start with a letter and contain only lowercase letters, numbers, '.', '_' or '-'."
        )
    if any(token in normalized for token in RESERVED_USERNAME_TOKENS):
        raise ValueError(
            "Username cannot contain reserved terms such as test, dev, demo, temp, qa, or staging."
        )
    return normalized


def _validate_password(value: str) -> str:
    password = value.strip()
    if len(password) < 10:
        raise ValueError("Password must be at least 10 characters long.")
    if password.lower() == password:
        raise ValueError("Password must include at least one uppercase letter.")
    if password.upper() == password:
        raise ValueError("Password must include at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must include at least one number.")
    if not any(not char.isalnum() for char in password):
        raise ValueError("Password must include at least one special character.")
    return password


class AdminLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        return _validate_username(value)


class AdminSignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=10, max_length=200)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        return _validate_username(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return _validate_password(value)


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class IntegrationStatus(BaseModel):
    configured: bool
    connected: bool
    detail: str | None = None


class AdminObservabilityResponse(BaseModel):
    tracing_enabled: bool
    langsmith_project: str | None = None
    langsmith_project_url: str | None = None
    mongo: IntegrationStatus
    langsmith: IntegrationStatus
    chroma: IntegrationStatus
    openai: IntegrationStatus
    persisted_admins: bool = False
    vector_store_count: int
    keyword_index_loaded: bool
    log_file_path: str
    last_search_diagnostics: dict | None = None


class AdminSignupResponse(BaseModel):
    status: str
    created: bool
