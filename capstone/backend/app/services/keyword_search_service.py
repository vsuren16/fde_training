from __future__ import annotations

import math
import re
from collections import defaultdict


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")
STOPWORDS = {
    "the",
    "is",
    "a",
    "an",
    "and",
    "or",
    "for",
    "with",
    "from",
    "to",
    "of",
    "are",
    "this",
    "that",
    "what",
    "how",
    "can",
    "be",
    "it",
    "when",
    "during",
    "after",
    "into",
}

QUERY_EXPANSIONS = {
    "remote": {"vpn", "citrix", "network", "access", "authentication"},
    "denied": {"blocked", "access", "authentication"},
    "freeze": {"timeout", "hang", "unresponsive", "latency"},
    "slow": {"latency", "performance", "timeout"},
    "database": {"postgresql", "sql", "query", "connection"},
    "login": {"authentication", "access", "credentials"},
    "credentials": {"authentication", "login", "access"},
    "proxy": {"network", "blocked", "access"},
    "boot": {"reboot", "startup", "device"},
}

CATEGORY_HINTS = {
    "network": {"vpn", "citrix", "proxy", "switch", "port", "latency"},
    "database": {"database", "postgresql", "sql", "connection", "query", "pool"},
    "hardware": {"workstation", "laptop", "printer", "boot", "ssd", "device"},
    "security": {"access", "authentication", "denied", "credential"},
}


def tokenize(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_PATTERN.findall(text)
        if token.lower() not in STOPWORDS
    ]


def expand_query_tokens(tokens: set[str]) -> set[str]:
    expanded = set(tokens)
    for token in list(tokens):
        expanded.update(QUERY_EXPANSIONS.get(token, set()))
    return expanded


class KeywordSearchService:
    def __init__(self) -> None:
        self._documents: dict[str, dict] = {}
        self._postings: dict[str, set[str]] = defaultdict(set)

    def load(self, incidents: list[dict]) -> None:
        self._documents = {item["incident_id"]: item for item in incidents}
        self._postings = defaultdict(set)
        for item in incidents:
            combined_text = " ".join(
                [
                    str(item.get("title", "")),
                    str(item.get("category", "")),
                    str(item.get("status", "")),
                    str(item.get("team", "")),
                    str(item.get("description", "")),
                    str(item.get("resolution_notes", "")),
                    str(item.get("incident_text", "")),
                ]
            )
            for token in set(tokenize(combined_text)):
                self._postings[token].add(item["incident_id"])

    def is_loaded(self) -> bool:
        return bool(self._documents)

    def search(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        if not self._documents:
            return []
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        expanded_tokens = expand_query_tokens(set(query_tokens))
        candidate_ids: set[str] = set()
        for token in expanded_tokens:
            candidate_ids.update(self._postings.get(token, set()))

        scored: list[tuple[float, dict]] = []
        preferred_category = self._infer_preferred_category(expanded_tokens)
        for incident_id in candidate_ids:
            item = self._documents[incident_id]
            if not self._passes_filters(item, filters):
                continue

            document_tokens = set(
                tokenize(
                    " ".join(
                        [
                            str(item.get("title") or ""),
                            str(item.get("description") or ""),
                            str(item.get("resolution_notes") or ""),
                            str(item.get("category") or ""),
                            str(item.get("team") or ""),
                        ]
                    )
                )
            )
            overlap = len(expanded_tokens & document_tokens)
            if overlap == 0:
                continue
            score = overlap / math.sqrt(max(len(document_tokens), 1))
            if preferred_category and str(item.get("category") or "").lower() == preferred_category:
                score += 0.45
            score += self._field_hint_boost(item, expanded_tokens)
            scored.append((score, item))

        scored.sort(key=lambda entry: entry[0], reverse=True)
        return [
            {"incident_id": item["incident_id"], "score": float(score)}
            for score, item in scored[:top_k]
        ]

    @staticmethod
    def _passes_filters(item: dict, filters: dict | None) -> bool:
        if not filters:
            return True
        for key, expected in filters.items():
            if expected is None:
                continue
            if item.get(key) != expected:
                return False
        return True

    @staticmethod
    def _infer_preferred_category(tokens: set[str]) -> str | None:
        for category, hints in CATEGORY_HINTS.items():
            if tokens & hints:
                return category
        if tokens & {"slow", "freeze", "timeout", "unresponsive"}:
            return "database"
        return None

    @staticmethod
    def _field_hint_boost(item: dict, tokens: set[str]) -> float:
        boost = 0.0
        category = str(item.get("category") or "").lower()
        title = str(item.get("title") or "").lower()
        description = str(item.get("description") or "").lower()
        combined = " ".join([category, title, description])

        for hint in tokens:
            if hint in combined:
                boost += 0.03

        if tokens & {"remote", "vpn", "citrix", "authentication", "access"} and any(
            hint in combined for hint in {"vpn", "citrix", "proxy", "network"}
        ):
            boost += 0.4
        if tokens & {"slow", "freeze", "timeout", "database", "query"} and any(
            hint in combined for hint in {"database", "query", "postgresql", "connection"}
        ):
            boost += 0.4
        if tokens & {"boot", "reboot", "device", "workstation"} and any(
            hint in combined for hint in {"boot", "workstation", "ssd", "device"}
        ):
            boost += 0.35
        return boost
