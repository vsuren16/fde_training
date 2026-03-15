from __future__ import annotations

from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int, index_path: Path):
        self.dim = dim
        self.index_path = index_path
        self.index: faiss.IndexFlatIP | None = None

    def build_or_load(self, embeddings: np.ndarray, force_rebuild: bool = False) -> None:
        if not force_rebuild and self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            return

        index = faiss.IndexFlatIP(self.dim)
        index.add(embeddings)
        faiss.write_index(index, str(self.index_path))
        self.index = index

    def search(self, query_vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        if self.index is None:
            raise RuntimeError("FAISS index has not been initialized.")
        return self.index.search(query_vector, k)
