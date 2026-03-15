from __future__ import annotations


def build_context(products: list[dict]) -> str:
    lines = []
    for p in products:
        lines.extend(
            [
                f"Product ID: {p.get('product_id')}",
                f"Name: {p.get('name')}",
                f"Price: {p.get('price')}",
                f"Category: {p.get('category')}",
                f"Description: {p.get('description')}",
                f"Specifications: {p.get('specifications')}",
                "---",
            ]
        )
    return "\n".join(lines)


def build_generation_messages(query: str, ranked_products: list[dict]) -> list[dict[str, str]]:
    context = build_context(ranked_products)
    system = (
        "You are an e-commerce recommendation assistant. "
        "Use only the products in the provided context. "
        "Do not invent products, prices, features, or IDs. "
        "If context is empty, say no suitable products found."
    )
    user = (
        f"User Query: {query}\n\n"
        "Retrieved Product Context:\n"
        f"{context}\n\n"
        "Return a concise recommendation with ranking rationale and mention price-fit if relevant."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_judge_messages(query: str, ranked_products: list[dict], llm_explanation: str) -> list[dict[str, str]]:
    context = build_context(ranked_products)
    system = (
        "You are a strict evaluator for retrieval-grounded recommendations. "
        "Score from 1 to 5 for relevance, faithfulness, and completeness. "
        "Return JSON only with keys: relevance, faithfulness, completeness, overall_score, reasoning."
    )
    user = (
        f"Query: {query}\n\n"
        f"Retrieved Context:\n{context}\n\n"
        f"Assistant Response:\n{llm_explanation}\n\n"
        "Evaluation rules:\n"
        "- relevance: response matches user intent\n"
        "- faithfulness: response grounded only in context\n"
        "- completeness: response covers major relevant options from context\n"
        "Compute overall_score as average of the three metrics."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
