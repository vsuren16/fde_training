"""Environment/profile-aware runtime settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


VALID_ENVIRONMENTS = {"dev", "prod"}


@dataclass(frozen=True)
class RuntimeSettings:
    environment: str
    mongo_uri: str
    mongo_db: str
    output_log_dir: str



def _resolve_env(profile: str | None) -> str:
    value = (profile or os.getenv("ENVIRONMENT", "dev")).strip().lower()
    return value if value in VALID_ENVIRONMENTS else "dev"



def _get_profiled(key: str, env_name: str, default: str) -> str:
    # Priority: KEY_<ENV> -> KEY -> default
    return os.getenv(f"{key}_{env_name.upper()}") or os.getenv(key) or default



def load_runtime_settings(
    profile: str | None = None,
    output_log_dir_override: str | None = None,
) -> RuntimeSettings:
    env_name = _resolve_env(profile)
    default_log_dir = str(Path(__file__).resolve().parents[2] / "data-engineering" / "inventory_pipeline" / "logs")

    mongo_uri = _get_profiled("MONGO_URI", env_name, "mongodb://localhost:27017")
    mongo_db = _get_profiled("MONGO_DB", env_name, "ai_commerce")
    output_log_dir = output_log_dir_override or _get_profiled("INVENTORY_LOG_DIR", env_name, default_log_dir)

    return RuntimeSettings(
        environment=env_name,
        mongo_uri=mongo_uri,
        mongo_db=mongo_db,
        output_log_dir=output_log_dir,
    )
