import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------- Config --------
XLSX_PATH = os.getenv("XLSX_PATH", "./data/walmart-products.xlsx")
SHEET_NAME = os.getenv("XLSX_SHEET_NAME")  # no default None

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "walmart_products")

OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
BATCH_SIZE = int(os.getenv("INGEST_BATCH_SIZE", "64"))

# Caps to control cost/noise
MAX_REVIEWS_CHARS = int(os.getenv("MAX_REVIEWS_CHARS", "3000"))
MAX_SPECS_CHARS = int(os.getenv("MAX_SPECS_CHARS", "2000"))
MAX_OTHER_ATTRS_CHARS = int(os.getenv("MAX_OTHER_ATTRS_CHARS", "2000"))

# Your schema column names (EXACT)
COL_PRODUCT_ID = "product_id"
COL_PRODUCT_NAME = "product_name"
COL_DESCRIPTION = "description"
COL_CUSTOMER_REVIEWS = "customer_reviews"
COL_SPECIFICATIONS = "specifications"
COL_OTHER_ATTRS = "other_attributes"
COL_INGREDIENTS = "ingredients"

COL_FINAL_PRICE = "final_price"
COL_CURRENCY = "currency"
COL_UNIT_PRICE = "unit_price"
COL_RATING = "rating"
COL_REVIEW_COUNT = "review_count"

COL_BRAND = "brand"
COL_CATEGORY = "category_name"
COL_ROOT_CATEGORY = "root_category_name"
COL_COLORS = "colors"
COL_SELLER = "seller"

COL_DELIVERY = "available_for_delivery"
COL_PICKUP = "available_for_pickup"

COL_MAIN_IMAGE = "main_image"
COL_IMAGE_URLS = "image_urls"


def clean_text(val: Any) -> str:
    if val is None:
        return ""
    try:
        if isinstance(val, float) and pd.isna(val):
            return ""
    except Exception:
        pass
    s = str(val)
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", s)
    return s


def truncate(s: str, max_chars: int) -> str:
    s = s.strip()
    if len(s) <= max_chars:
        return s
    return s[:max_chars].rstrip() + "…"


def safe_float(val: Any) -> Optional[float]:
    try:
        if val is None:
            return None
        if isinstance(val, float) and pd.isna(val):
            return None
        s = str(val).strip()
        if not s:
            return None
        s = s.replace(",", "")
        s = re.sub(r"[^\d.\-]", "", s)
        return float(s) if s else None
    except Exception:
        return None


def safe_int(val: Any) -> Optional[int]:
    try:
        if val is None:
            return None
        if isinstance(val, float) and pd.isna(val):
            return None
        s = str(val).strip()
        if not s:
            return None
        s = s.replace(",", "")
        s = re.sub(r"[^\d\-]", "", s)
        return int(s) if s else None
    except Exception:
        return None


def normalize_boolish(val: Any) -> Optional[bool]:
    s = clean_text(val).lower()
    if not s:
        return None
    if s in {"true", "yes", "y", "1", "available"}:
        return True
    if s in {"false", "no", "n", "0", "unavailable"}:
        return False
    return None


def build_document(row: Dict[str, Any]) -> str:
    # Core fields
    product_name = clean_text(row.get(COL_PRODUCT_NAME))
    brand = clean_text(row.get(COL_BRAND))
    root_cat = clean_text(row.get(COL_ROOT_CATEGORY))
    cat = clean_text(row.get(COL_CATEGORY))
    description = clean_text(row.get(COL_DESCRIPTION))

    # Large fields with caps
    specs = truncate(clean_text(row.get(COL_SPECIFICATIONS)), MAX_SPECS_CHARS)
    other_attrs = truncate(clean_text(row.get(COL_OTHER_ATTRS)), MAX_OTHER_ATTRS_CHARS)
    reviews = truncate(clean_text(row.get(COL_CUSTOMER_REVIEWS)), MAX_REVIEWS_CHARS)
    ingredients = clean_text(row.get(COL_INGREDIENTS))

    # Commerce fields
    final_price = clean_text(row.get(COL_FINAL_PRICE))
    currency = clean_text(row.get(COL_CURRENCY))
    unit_price = clean_text(row.get(COL_UNIT_PRICE))
    rating = clean_text(row.get(COL_RATING))
    review_count = clean_text(row.get(COL_REVIEW_COUNT))

    colors = clean_text(row.get(COL_COLORS))
    seller = clean_text(row.get(COL_SELLER))

    delivery = clean_text(row.get(COL_DELIVERY))
    pickup = clean_text(row.get(COL_PICKUP))

    main_image = clean_text(row.get(COL_MAIN_IMAGE))
    image_urls = clean_text(row.get(COL_IMAGE_URLS))

    # Important: DO NOT dump huge image url lists into the embedding doc
    # We only include a small hint for relevance; keep main_image (single) and count-like info.
    image_urls_hint = ""
    if image_urls:
        # A lightweight heuristic: count separators
        approx_count = image_urls.count("http")
        if approx_count <= 0:
            approx_count = image_urls.count(",") + 1
        image_urls_hint = f"IMAGE_URLS_COUNT_APPROX: {approx_count}"

    parts = [
        f"PRODUCT_NAME: {product_name}",
        f"BRAND: {brand}" if brand else "",
        f"CATEGORY: {root_cat} > {cat}" if (root_cat or cat) else "",
        f"FINAL_PRICE: {final_price} {currency}".strip() if (final_price or currency) else "",
        f"UNIT_PRICE: {unit_price}" if unit_price else "",
        f"RATING: {rating}" if rating else "",
        f"REVIEW_COUNT: {review_count}" if review_count else "",
        f"AVAILABLE_FOR_DELIVERY: {delivery}" if delivery else "",
        f"AVAILABLE_FOR_PICKUP: {pickup}" if pickup else "",
        f"COLORS: {colors}" if colors else "",
        f"SELLER: {seller}" if seller else "",
        f"DESCRIPTION: {description}" if description else "",
        f"SPECIFICATIONS: {specs}" if specs else "",
        f"OTHER_ATTRIBUTES: {other_attrs}" if other_attrs else "",
        f"INGREDIENTS: {ingredients}" if ingredients else "",
        f"CUSTOMER_REVIEWS: {reviews}" if reviews else "",
        f"MAIN_IMAGE: {main_image}" if main_image else "",
        image_urls_hint,
    ]

    return "\n".join([p for p in parts if p]).strip()


def chunked_indices(n: int, batch_size: int):
    for i in range(0, n, batch_size):
        yield list(range(i, min(i + batch_size, n)))


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in .env / environment")

    if not os.path.exists(XLSX_PATH):
        raise RuntimeError(f"XLSX file not found: {XLSX_PATH}")

    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME or 0, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    required = [COL_PRODUCT_ID, COL_PRODUCT_NAME]
    for col in required:
        if col not in df.columns:
            raise RuntimeError(f"Missing required column '{col}'. Found: {list(df.columns)}")

    # Clean IDs/names and drop invalid rows
    df[COL_PRODUCT_ID] = df[COL_PRODUCT_ID].apply(clean_text)
    df[COL_PRODUCT_NAME] = df[COL_PRODUCT_NAME].apply(clean_text)
    df = df[(df[COL_PRODUCT_ID] != "") & (df[COL_PRODUCT_NAME] != "")].copy()

    # Deduplicate product_id
    before = len(df)
    df = df.drop_duplicates(subset=[COL_PRODUCT_ID], keep="first")
    after = len(df)
    if after != before:
        print(f"⚠ Dedup: removed {before - after} duplicate product_id rows")

    if df.empty:
        print("No valid rows to ingest after cleanup.")
        return

    ids: List[str] = []
    docs: List[str] = []
    metas: List[dict] = []

    for _, r in df.iterrows():
        row = r.to_dict()
        pid = clean_text(row.get(COL_PRODUCT_ID))

        doc = build_document(row)

        # Metadata: keep it small + filterable
        meta = {
            "product_id": pid,
            "product_name": clean_text(row.get(COL_PRODUCT_NAME)),
            "brand": clean_text(row.get(COL_BRAND)),
            "category_name": clean_text(row.get(COL_CATEGORY)),
            "root_category_name": clean_text(row.get(COL_ROOT_CATEGORY)),
            "final_price": safe_float(row.get(COL_FINAL_PRICE)),
            "currency": clean_text(row.get(COL_CURRENCY)),
            "unit_price": safe_float(row.get(COL_UNIT_PRICE)),
            "rating": safe_float(row.get(COL_RATING)),
            "review_count": safe_int(row.get(COL_REVIEW_COUNT)),
            "available_for_delivery": normalize_boolish(row.get(COL_DELIVERY)),
            "available_for_pickup": normalize_boolish(row.get(COL_PICKUP)),
            "main_image": clean_text(row.get(COL_MAIN_IMAGE)),
        }

        ids.append(pid)
        docs.append(doc)
        metas.append(meta)

    print(f"✅ Prepared {len(ids)} products for Chroma ingestion")

    chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma.get_or_create_collection(name=CHROMA_COLLECTION)

    client = OpenAI(api_key=api_key)

    for batch_num, idxs in enumerate(chunked_indices(len(ids), BATCH_SIZE), start=1):
        batch_ids = [ids[i] for i in idxs]
        batch_docs = [docs[i] for i in idxs]
        batch_metas = [metas[i] for i in idxs]

        emb = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=batch_docs)
        vectors = [e.embedding for e in emb.data]

        collection.upsert(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_metas,
            embeddings=vectors,
        )
        print(f"Batch {batch_num}: upserted {len(batch_ids)}")

    print("🎉 Ingestion complete.")
    print(f"Chroma path: {CHROMA_PATH}")
    print(f"Collection: {CHROMA_COLLECTION}")


if __name__ == "__main__":
    main()