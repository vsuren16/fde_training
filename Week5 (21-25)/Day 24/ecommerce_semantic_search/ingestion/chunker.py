from __future__ import annotations

from typing import Any


def _tokenize(text: str) -> list[str]:
    return text.split()


def _detokenize(tokens: list[str]) -> str:
    return " ".join(tokens)


class Chunker:
    def __init__(self, chunk_size: int = 380, overlap: int = 50):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_products(self, products: list[dict[str, Any]]) -> list[dict[str, Any]]:
        chunks: list[dict[str, Any]] = []
        for product in products:
            text_sections = [
                f"Name: {product.get('name', '')}",
                f"Description: {product.get('description', '')}",
                f"Specifications: {product.get('specifications', '')}",
                f"Reviews: {product.get('reviews', '')}",
            ]
            full_text = "\n".join([s for s in text_sections if s.strip()])
            tokens = _tokenize(full_text)

            start = 0
            chunk_idx = 0
            while start < len(tokens):
                end = min(start + self.chunk_size, len(tokens))
                chunk_tokens = tokens[start:end]
                chunk_text = _detokenize(chunk_tokens)
                chunk = {
                    "product_id": product.get("product_id"),
                    "chunk_id": f"{product.get('product_id')}_{chunk_idx}",
                    "text": chunk_text,
                    "price": product.get("price"),
                    "category": product.get("category"),
                    "name": product.get("name"),
                    "description": product.get("description"),
                    "specifications": product.get("specifications"),
                    "reviews": product.get("reviews"),
                }
                chunks.append(chunk)
                if end == len(tokens):
                    break
                start = end - self.overlap
                chunk_idx += 1
        return chunks
