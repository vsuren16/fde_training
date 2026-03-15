import json
from pathlib import Path


DEFAULT_DIMENSIONS = {
    "length_cm": 30.0,
    "width_cm": 20.0,
    "height_cm": 3.0,
}


def _clamp_rating(value: float | int | None) -> float:
    try:
        rating = float(value if value is not None else 4.0)
    except (TypeError, ValueError):
        rating = 4.0
    return max(1.0, min(5.0, rating))


def _normalize_product(raw: dict, index: int) -> dict:
    image_url = str(raw.get("image_url") or raw.get("image") or "").strip()
    image_urls = raw.get("image_urls") or []
    if isinstance(image_urls, str):
        image_urls = [x.strip() for x in image_urls.split("|") if x.strip()]
    if image_url and image_url not in image_urls:
        image_urls = [image_url, *image_urls]

    description = str(raw.get("description") or raw.get("short_description") or "").strip()
    short_description = str(raw.get("short_description") or description[:180] or "Product description unavailable.").strip()
    availability = raw.get("availability")
    if availability is None:
        availability = raw.get("available")

    dimensions = raw.get("dimensions")
    if not isinstance(dimensions, dict):
        dimensions = DEFAULT_DIMENSIONS.copy()

    return {
        **raw,
        "id": str(raw.get("id") or f"p-import-{index + 1}"),
        "product_name": str(raw.get("product_name") or raw.get("name") or f"Product {index + 1}").strip(),
        "short_description": short_description,
        "description": description or short_description,
        "category": str(raw.get("category") or "general").strip(),
        "brand": str(raw.get("brand") or "Generic").strip(),
        "color": str(raw.get("color") or "standard").strip(),
        "size": str(raw.get("size") or "NA").strip(),
        "price": float(raw.get("price") or 0),
        "image_url": image_url,
        "image_urls": image_urls,
        "rating": _clamp_rating(raw.get("rating")),
        "dimensions": dimensions,
        "availability": bool(True if availability is None else availability),
        "reviews": raw.get("reviews") or [],
    }


def load_external_products(path: str | Path) -> list[dict]:
    source = Path(path)
    text = source.read_text(encoding="utf-8").strip()
    if not text:
        return []

    rows: list[dict] = []
    try:
        payload = json.loads(text)
        if isinstance(payload, list):
            rows = [item for item in payload if isinstance(item, dict)]
        elif isinstance(payload, dict):
            rows = [payload]
    except json.JSONDecodeError:
        rows = []
        for line in text.splitlines():
            line = line.strip().rstrip(",")
            if not line:
                continue
            rows.append(json.loads(line))

    return [_normalize_product(item, idx) for idx, item in enumerate(rows)]


def load_seed_products(default_count: int) -> list[dict]:
    current = Path(__file__).resolve()
    search_roots = [current.parent]
    search_roots.extend(current.parents)

    candidate_paths: list[Path] = []
    seen: set[Path] = set()
    preferred_patterns = (
        ("mongodb_mockdata.txt",),
        ("app", "data", "products.json"),
        ("data", "products.json"),
    )

    for pattern in preferred_patterns:
        for root in search_roots:
            candidate = root.joinpath(*pattern)
            if candidate in seen:
                continue
            seen.add(candidate)
            candidate_paths.append(candidate)

    for candidate in candidate_paths:
        if candidate.exists():
            products = load_external_products(candidate)
            if products:
                return products

    from app.seed.mock_products import generate_mock_products

    return generate_mock_products(default_count)
