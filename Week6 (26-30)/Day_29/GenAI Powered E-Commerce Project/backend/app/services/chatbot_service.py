import json
import re
from typing import Any, Dict, Optional

from app.core.config import settings
from app.db.mongodb import get_collection as get_products_collection # <-- adjust if your path differs
from app.llm.chat_models import extract_text_content, get_chat_model
from app.security.pii import sanitize_text_for_llm
from langchain_core.messages import HumanMessage, SystemMessage


# -------------------------
# Intent detection
# -------------------------
def detect_intent(q: str) -> str:
    ql = (q or "").lower()

    if any(k in ql for k in ["price", "cost", "how much", "mrp", "pricing"]):
        return "price"
    if any(k in ql for k in ["review", "reviews", "rating", "feedback", "what people say", "summary", "summarize"]):
        return "reviews"
    if any(k in ql for k in ["ingredient", "ingredients", "contains", "allergen"]):
        return "ingredients"
    if any(k in ql for k in ["delivery", "deliver", "shipping", "ship", "available for delivery"]):
        return "delivery"

    return "general"


# -------------------------
# Output clamps
# -------------------------
def clamp_words(text: str, max_words: int = 120) -> str:
    words = (text or "").strip().split()
    if len(words) <= max_words:
        return (text or "").strip()
    return " ".join(words[:max_words]).strip() + "…"


def clamp_lines(text: str, max_lines: int = 8) -> str:
    lines = [(l or "").rstrip() for l in (text or "").splitlines() if (l or "").strip()]
    if len(lines) <= max_lines:
        return "\n".join(lines).strip()
    return "\n".join(lines[:max_lines]).strip() + "\n…"


# -------------------------
# Helpers for Mongo fields
# -------------------------
def safe_json_loads(s: Any) -> Any:
    if not isinstance(s, str):
        return s
    t = s.strip()
    if not t:
        return []
    try:
        return json.loads(t)
    except Exception:
        return []


def extract_price(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Your Mongo example:
    price: { final_price: 34.97, currency: "USD", ... }
    """
    p = product.get("price") or {}
    if isinstance(p, str):
        # sometimes stored as json string
        try:
            p = json.loads(p)
        except Exception:
            p = {}

    final_price = (
        p.get("final_price")
        or p.get("value")
        or p.get("amount")
        or p.get("price")
    )
    currency = p.get("currency") or "USD"
    return {"final_price": final_price, "currency": currency}


async def get_product_by_id(product_id: str):
    col = get_products_collection(settings.mongo_products_collection)  # ✅ name required

    doc = await col.find_one({"product_id": product_id})
    if not doc:
        doc = await col.find_one({"id": product_id})

    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# -------------------------
# Prompts
# -------------------------
SYSTEM_BASE = """
You are a concise e-commerce product assistant.

Global rules (must follow):
- Be brief and skimmable.
- Never dump raw JSON.
- Never include internal fields (e.g., product_snapshot, need_product_id).
- If information is missing, say so clearly.
"""

SYSTEM_PRICE = SYSTEM_BASE + """
User asked about PRICE.
Rules:
- Answer in 1–2 lines only.
- Return only price + currency (and unit price if available).
- Do NOT include reviews or description.
"""

SYSTEM_REVIEWS = SYSTEM_BASE + """
User asked about REVIEWS.
Rules:
- Max 120 words.
- Use at most 6 bullets.
- Start with a 1-line verdict, then bullets.
- Use ONLY the review data provided. Do NOT use product description.
- Do NOT paste full reviews; summarize themes (pros/cons).
If no reviews: say "No reviews available for this product."
"""

SYSTEM_DELIVERY = SYSTEM_BASE + """
User asked about DELIVERY.
Rules:
- Answer in max 3 bullets.
- Mention delivery availability and any known shipping info.
- If unknown, say "Delivery info not available."
"""

SYSTEM_INGREDIENTS = SYSTEM_BASE + """
User asked about INGREDIENTS.
Rules:
- Answer in max 4 bullets.
- Use only ingredients field; if missing, say "Ingredients not available."
"""

SYSTEM_GENERAL = SYSTEM_BASE + """
Rules:
- Max 120 words.
- Answer only what user asked.
"""


# -------------------------
# LLM call
# -------------------------
def call_llm(system: str, user: str, max_output_tokens: int = 220) -> str:
    llm = get_chat_model()
    resp = llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(content=user),
        ],
        config={"max_tokens": max_output_tokens},
    )
    return extract_text_content(resp.content)


# -------------------------
# Main handler
# -------------------------
async def handle_chat(message: str, product_id: Optional[str] = None) -> Dict[str, str]:
    msg = (message or "").strip()
    if not msg:
        return {"answer": "Please enter a question."}

    sanitized = sanitize_text_for_llm(msg)
    llm_message = sanitized.sanitized_text or msg

    # If no product selected, ask for it (short)
    if not product_id:
        return {"answer": "Please select a product first (Product ID) so I can answer accurately."}

    product = await get_product_by_id(str(product_id))
    if not product:
        return {"answer": f"I couldn't find product {product_id}. Please select a valid product."}

    intent = detect_intent(msg)

    if intent == "price":
        price = extract_price(product)
        user_prompt = f"""
Question: {llm_message}
Product name: {product.get("product_name") or product.get("title") or product.get("name") or "Unknown"}
Price data:
final_price: {price.get("final_price")}
currency: {price.get("currency")}
"""
        answer = call_llm(SYSTEM_PRICE, user_prompt, max_output_tokens=120)
        answer = clamp_lines(answer, 4)
        answer = clamp_words(answer, 50)
        return {"answer": answer}

    if intent == "reviews":
        reviews = safe_json_loads(product.get("customer_reviews", ""))
        # cap to avoid long context
        reviews = reviews[:30] if isinstance(reviews, list) else []
        user_prompt = f"""
Question: {llm_message}
Product name: {product.get("product_name") or product.get("title") or product.get("name") or "Unknown"}

Customer reviews (JSON array, may be empty):
{json.dumps(reviews, ensure_ascii=False)}
"""
        answer = call_llm(SYSTEM_REVIEWS, user_prompt, max_output_tokens=220)
        answer = clamp_lines(answer, 8)
        answer = clamp_words(answer, 120)
        return {"answer": answer}

    if intent == "ingredients":
        ingredients = (product.get("ingredients") or "").strip()
        user_prompt = f"""
Question: {llm_message}
Product name: {product.get("product_name") or product.get("title") or product.get("name") or "Unknown"}
Ingredients field:
{ingredients if ingredients else "MISSING"}
"""
        answer = call_llm(SYSTEM_INGREDIENTS, user_prompt, max_output_tokens=140)
        answer = clamp_lines(answer, 6)
        answer = clamp_words(answer, 80)
        return {"answer": answer}

    if intent == "delivery":
        delivery = {
            "delivery": product.get("delivery"),
            "shipping": product.get("shipping"),
            "delivery_available": product.get("delivery_available") or product.get("delivery_eligible"),
            "pickup": product.get("pickup"),
        }
        user_prompt = f"""
Question: {llm_message}
Product name: {product.get("product_name") or product.get("title") or product.get("name") or "Unknown"}
Delivery fields:
{json.dumps(delivery, ensure_ascii=False)}
"""
        answer = call_llm(SYSTEM_DELIVERY, user_prompt, max_output_tokens=160)
        answer = clamp_lines(answer, 6)
        answer = clamp_words(answer, 90)
        return {"answer": answer}

    # general
    user_prompt = f"""
Question: {llm_message}
Product name: {product.get("product_name") or product.get("title") or product.get("name") or "Unknown"}
Known fields:
- brand: {product.get("brand")}
- rating: {product.get("rating")}
- description: {(product.get("description") or "")[:600]}
"""
    answer = call_llm(SYSTEM_GENERAL, user_prompt, max_output_tokens=220)
    answer = clamp_lines(answer, 8)
    answer = clamp_words(answer, 120)
    return {"answer": answer}
