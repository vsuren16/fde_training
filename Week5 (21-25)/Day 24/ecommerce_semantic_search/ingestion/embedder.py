from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str, embeddings_file: Path, chunks_file: Path):
        self.model_name = model_name
        self.embeddings_file = embeddings_file
        self.chunks_file = chunks_file
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        vectors = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return vectors.astype(np.float32)

    def build_or_load(
        self,
        chunks: list[dict[str, Any]],
        force_rebuild: bool = False,
    ) -> tuple[list[dict[str, Any]], np.ndarray]:
        if (
            not force_rebuild
            and self.embeddings_file.exists()
            and self.chunks_file.exists()
        ):
            cached_chunks = self._load_chunks(self.chunks_file)
            embeddings = np.load(self.embeddings_file)
            return cached_chunks, embeddings

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.encode(texts)
        np.save(self.embeddings_file, embeddings)
        self._save_chunks(self.chunks_file, chunks)
        return chunks, embeddings

    @staticmethod
    def _save_chunks(path: Path, chunks: list[dict[str, Any]]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _load_chunks(path: Path) -> list[dict[str, Any]]:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
