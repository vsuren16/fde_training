import os
import re
import json
from typing import Any, Optional, List

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne, ASCENDING

load_dotenv()

# ---------------- CONFIG ----------------

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "ecommerce")
MONGO_PRODUCTS_COLLECTION = os.getenv("MONGO_PRODUCTS_COLLECTION", "products")

XLSX_PATH = os.getenv("XLSX_PATH", "./data/walmart-products.xlsx")
SHEET_NAME = os.getenv("XLSX_SHEET_NAME")  # optional

COL_PRODUCT_ID = "product_id"
COL_PRODUCT_NAME = "product_name"

# ----------------------------------------


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


def safe_float(val: Any) -> Optional[float]:
    try:
        s = clean_text(val)
        if not s:
            return None
        s = s.replace(",", "")
        s = re.sub(r"[^\d.\-]", "", s)
        return float(s) if s else None
    except Exception:
        return None


def safe_int(val: Any) -> Optional[int]:
    try:
        s = clean_text(val)
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


def make_short_description(description: str, max_len: int = 180) -> str:
    d = clean_text(description)
    if len(d) <= max_len:
        return d
    cut = d[:max_len].rsplit(" ", 1)[0]
    return (cut if cut else d[:max_len]).rstrip() + "…"


# ---------------- IMAGE HANDLING ----------------

def parse_image_urls(val: Any) -> List[str]:
    """
    Converts image_urls column into a clean list of URLs.
    Handles:
    - JSON string: ["url1","url2"]
    - comma-separated string
    - already a list
    """
    if val is None:
        return []

    try:
        if isinstance(val, float) and pd.isna(val):
            return []
    except Exception:
        pass

    if isinstance(val, list):
        raw = val
    else:
        s = clean_text(val)
        if not s:
            return []
        try:
            raw = json.loads(s)
            if not isinstance(raw, list):
                raw = [s]
        except Exception:
            raw = [x.strip() for x in s.split(",") if x.strip()]

    seen = set()
    cleaned: List[str] = []
    for u in raw:
        u = clean_text(u)
        if not u:
            continue
        if u in seen:
            continue
        seen.add(u)
        cleaned.append(u)
    return cleaned


# ---------------- INDEX SAFETY ----------------

def ensure_index(col, keys, name: str, unique: bool = False):
    """
    Create an index only if an equivalent index doesn't already exist (any name).
    keys: list of tuples, e.g. [("brand", ASCENDING)]
    """
    existing = list(col.list_indexes())
    wanted_key = tuple(keys)

    for idx in existing:
        # idx["key"] is an OrderedDict like {"brand": 1}
        idx_key = tuple(idx["key"].items())
        if idx_key == wanted_key:
            # Equivalent index already exists (maybe different name)
            return

    col.create_index(keys, name=name, unique=unique)


def main():
    if not os.path.exists(XLSX_PATH):
        raise RuntimeError(f"XLSX not found: {XLSX_PATH}")

    sheet = SHEET_NAME or 0
    df = pd.read_excel(XLSX_PATH, sheet_name=sheet, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    if COL_PRODUCT_ID not in df.columns or COL_PRODUCT_NAME not in df.columns:
        raise RuntimeError(f"Missing required columns. Found: {list(df.columns)}")

    df[COL_PRODUCT_ID] = df[COL_PRODUCT_ID].apply(clean_text)
    df[COL_PRODUCT_NAME] = df[COL_PRODUCT_NAME].apply(clean_text)
    df = df[(df[COL_PRODUCT_ID] != "") & (df[COL_PRODUCT_NAME] != "")].copy()

    before = len(df)
    df = df.drop_duplicates(subset=[COL_PRODUCT_ID], keep="first")
    after = len(df)
    if after != before:
        print(f"⚠ Removed {before - after} duplicate product_id rows")

    mongo = MongoClient(MONGO_URI)
    col = mongo[MONGO_DB][MONGO_PRODUCTS_COLLECTION]

    # ✅ Safe, idempotent index creation (won't crash if index exists under another name)
    ensure_index(col, [(COL_PRODUCT_ID, ASCENDING)], name="idx_product_id", unique=True)
    ensure_index(col, [("brand", ASCENDING)], name="idx_brand")
    ensure_index(col, [("category_name", ASCENDING)], name="idx_category_name")
    ensure_index(col, [("root_category_name", ASCENDING)], name="idx_root_category_name")

    ops = []

    for _, r in df.iterrows():
        row = r.to_dict()

        product_id = clean_text(row.get("product_id"))
        product_name = clean_text(row.get("product_name"))
        description = clean_text(row.get("description"))
        short_description = make_short_description(description)

        # Images
        main_image = clean_text(row.get("main_image"))
        other_images = parse_image_urls(row.get("image_urls"))

        images: List[str] = []
        if main_image:
            images.append(main_image)
        for img in other_images:
            if img != main_image:
                images.append(img)

        doc = {
            # Core identifiers
            "product_id": product_id,
            "product_name": product_name,

            # List view fields
            "short_description": short_description,
            "main_image": main_image,
            "images": images,  # ✅ swipe-ready array
            "brand": clean_text(row.get("brand")),
            "rating": safe_float(row.get("rating")),
            "review_count": safe_int(row.get("review_count")),
            "price": {
                "final_price": safe_float(row.get("final_price")),
                "currency": clean_text(row.get("currency")),
                "unit_price": safe_float(row.get("unit_price")),
            },
            "availability": {
                "delivery": normalize_boolish(row.get("available_for_delivery")),
                "pickup": normalize_boolish(row.get("available_for_pickup")),
            },

            # Categories
            "category_name": clean_text(row.get("category_name")),
            "root_category_name": clean_text(row.get("root_category_name")),

            # Detail view fields
            "description": description,
            "colors": clean_text(row.get("colors")),
            "ingredients": clean_text(row.get("ingredients")),
            "specifications": clean_text(row.get("specifications")),
            "other_attributes": clean_text(row.get("other_attributes")),
            "customer_reviews": clean_text(row.get("customer_reviews")),
            "seller": clean_text(row.get("seller")),
        }

        ops.append(
            UpdateOne(
                {"product_id": product_id},
                {"$set": doc},
                upsert=True
            )
        )

    if not ops:
        print("No valid rows to insert.")
        return

    res = col.bulk_write(ops, ordered=False)

    print("✅ Mongo load complete")
    print(f"Upserted: {res.upserted_count}")
    print(f"Modified: {res.modified_count}")
    print(f"Matched: {res.matched_count}")


if __name__ == "__main__":
    main()