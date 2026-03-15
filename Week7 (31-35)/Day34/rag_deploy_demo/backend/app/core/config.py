import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    use_openai: bool = parse_bool(os.getenv("USE_OPENAI"), default=False)
    fallback_score_threshold: float = float(os.getenv("FALLBACK_SCORE_THRESHOLD", "0.18"))
    backend_host: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8010"))
    vite_api_base_url: str = os.getenv("VITE_API_BASE_URL", "http://127.0.0.1:8010")
    allowed_origins: list[str] = field(
        default_factory=lambda: ["http://127.0.0.1:5173", "http://localhost:5173"]
    )


settings = Settings()
