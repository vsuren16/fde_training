from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

from backend.app.core.config import settings
from backend.app.llm.openai_client import get_openai_client


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json"
TOKEN_PATTERN = re.compile(r"\b[a-zA-Z0-9]+\b")


with DATA_FILE.open("r", encoding="utf-8") as file:
    DOCUMENTS = json.load(file)


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def cosine_similarity(query_tokens: list[str], doc_tokens: list[str]) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0

    query_counts = Counter(query_tokens)
    doc_counts = Counter(doc_tokens)
    shared_terms = set(query_counts) & set(doc_counts)

    numerator = sum(query_counts[token] * doc_counts[token] for token in shared_terms)
    query_norm = math.sqrt(sum(value * value for value in query_counts.values()))
    doc_norm = math.sqrt(sum(value * value for value in doc_counts.values()))

    if not query_norm or not doc_norm:
        return 0.0

    return numerator / (query_norm * doc_norm)


def retrieve_context(question: str, top_k: int = 3) -> list[dict]:
    query_tokens = tokenize(question)
    scored_docs = []

    for doc in DOCUMENTS:
        score = cosine_similarity(query_tokens, tokenize(f"{doc['title']} {doc['content']}"))
        if score <= 0:
            continue
        scored_docs.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "score": round(score, 3),
            }
        )

    scored_docs.sort(key=lambda item: item["score"], reverse=True)
    return scored_docs[:top_k]


def build_local_answer(question: str, context_docs: list[dict]) -> str:
    if not context_docs:
        return (
            "No matching document was retrieved from the dummy knowledge base. "
            "Try asking about deployment, chunking, embeddings, or monitoring."
        )

    top_doc = context_docs[0]
    source_titles = ", ".join(doc["title"] for doc in context_docs)
    return (
        f"Best local answer for '{question}': {top_doc['content']} "
        f"Retrieved from: {source_titles}."
    )


def build_openai_answer(question: str, context_docs: list[dict]) -> str:
    client = get_openai_client()
    if not client or not context_docs:
        return build_local_answer(question, context_docs)

    context_text = "\n".join(f"- {doc['title']}: {doc['content']}" for doc in context_docs)
    system_prompt = "Answer only from the provided context. Keep it concise and mention when context is limited."
    user_prompt = f"Question: {question}\n\nContext:\n{context_text}"

    if hasattr(client, "responses"):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or build_local_answer(question, context_docs)


def build_openai_fallback_answer(question: str) -> str:
    client = get_openai_client()
    if not client:
        return (
            "The local knowledge base does not contain enough relevant information, "
            "and OpenAI fallback is not configured."
        )

    system_prompt = (
        "You are a helpful assistant. The local RAG knowledge base was not relevant enough. "
        "Answer from general knowledge, keep it concise, and do not claim the answer came from retrieved documents."
    )
    user_prompt = question

    if hasattr(client, "responses"):
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    return completion.choices[0].message.content or (
        "The fallback model did not return an answer."
    )


def generate_rag_response(question: str) -> dict:
    clean_question = question.strip()
    if not clean_question:
        return {"question": question, "answer": "Question is required.", "sources": []}

    context_docs = retrieve_context(clean_question)
    top_score = context_docs[0]["score"] if context_docs else 0.0

    if settings.use_openai and top_score < settings.fallback_score_threshold:
        answer = build_openai_fallback_answer(clean_question)
        mode = "fallback-openai"
    elif settings.use_openai:
        answer = build_openai_answer(clean_question, context_docs)
        mode = "openai-grounded"
    else:
        answer = build_local_answer(clean_question, context_docs)
        mode = "local"

    return {
        "question": clean_question,
        "answer": answer,
        "sources": context_docs,
        "mode": mode,
        "retrieval_score": top_score,
    }
