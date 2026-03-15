import os

os.environ["USE_FAKE_EMBEDDINGS"] = "true"
os.environ["OPENAI_API_KEY"] = ""
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
