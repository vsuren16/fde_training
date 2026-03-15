from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProductLoader:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            raise FileNotFoundError(f"Product file not found: {self.path}")
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Product catalog must be a JSON list.")
        return data
