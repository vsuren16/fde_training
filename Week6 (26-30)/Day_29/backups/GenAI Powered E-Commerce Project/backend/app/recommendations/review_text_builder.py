import re
from typing import Any

def _clean(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s

def build_review_text_agg(product: dict[str, Any], max_reviews: int = 60, max_chars: int = 12000) -> str:
    """
    Build a single review-focused text string for embeddings.

    Supports common schemas:
      - product["reviews"] as list[str] OR list[dict] with fields like: title/text/body/comment/content/review
      - product["review_summary"] / ["reviews_summary"]
    Falls back to title/description if reviews absent.
    """
    chunks: list[str] = []

    # 1) explicit summaries if present
    for key in ("review_summary", "reviews_summary", "reviewSummary", "reviewsSummary"):
        v = product.get(key)
        if isinstance(v, str) and v.strip():
            chunks.append(_clean(v))

    # 2) raw reviews list
    reviews = product.get("reviews")
    if isinstance(reviews, list):
        for r in reviews[:max_reviews]:
            if isinstance(r, str):
                t = _clean(r)
                if t:
                    chunks.append(t)
            elif isinstance(r, dict):
                # prioritize longer free-text fields
                for rk in ("text", "body", "content", "comment", "review", "title"):
                    rv = r.get(rk)
                    if isinstance(rv, str) and rv.strip():
                        chunks.append(_clean(rv))
                        break

    # 3) fallback so we still can recommend when reviews are missing
    for key in ("title", "name", "short_description", "description"):
        v = product.get(key)
        if isinstance(v, str) and v.strip():
            chunks.append(_clean(v))

    agg = " | ".join([c for c in chunks if c])
    return agg[:max_chars]