from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(
    r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}|\b\d{3}-\d{4}\b)"
)
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,16}\b")


@dataclass(frozen=True)
class PiiSanitizationResult:
    original_text: str
    sanitized_text: str
    detected_entities: list[str]

    @property
    def pii_found(self) -> bool:
        return bool(self.detected_entities)


class _RegexEntity:
    def __init__(self, entity_type: str, start: int, end: int, score: float = 1.0):
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.score = score


_PRESIDIO_READY = False
_PRESIDIO_INIT_ATTEMPTED = False
_ANALYZER: Any = None
_ANONYMIZER: Any = None
_OPERATOR_CONFIG: Any = None


def _init_presidio() -> None:
    global _PRESIDIO_READY, _PRESIDIO_INIT_ATTEMPTED
    global _ANALYZER, _ANONYMIZER, _OPERATOR_CONFIG

    if _PRESIDIO_INIT_ATTEMPTED:
        return

    _PRESIDIO_INIT_ATTEMPTED = True

    try:
        from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
        from presidio_anonymizer import AnonymizerEngine
        from presidio_anonymizer.entities import OperatorConfig

        analyzer = AnalyzerEngine()

        phone_pattern = Pattern(
            name="phone_number_pattern",
            regex=r"(\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\(\d{3}\)\s*\d{3}-\d{4}|\+?\d{1,3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{4})",
            score=0.8,
        )
        ssn_pattern = Pattern(
            name="ssn_pattern",
            regex=r"\b\d{3}-\d{2}-\d{4}\b",
            score=0.85,
        )

        analyzer.registry.add_recognizer(
            PatternRecognizer(supported_entity="PHONE_NUMBER", patterns=[phone_pattern])
        )
        analyzer.registry.add_recognizer(
            PatternRecognizer(supported_entity="US_SSN", patterns=[ssn_pattern])
        )

        _ANALYZER = analyzer
        _ANONYMIZER = AnonymizerEngine()
        _OPERATOR_CONFIG = OperatorConfig
        _PRESIDIO_READY = True
    except Exception:
        _PRESIDIO_READY = False


def _dedupe_entities(entities: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for entity in entities:
        if entity not in seen:
            seen.add(entity)
            ordered.append(entity)
    return ordered


def _fallback_entities(text: str) -> list[_RegexEntity]:
    matches: list[_RegexEntity] = []
    for regex, entity_type in (
        (EMAIL_RE, "EMAIL_ADDRESS"),
        (PHONE_RE, "PHONE_NUMBER"),
        (SSN_RE, "US_SSN"),
        (CARD_RE, "CREDIT_CARD"),
    ):
        for match in regex.finditer(text):
            matches.append(_RegexEntity(entity_type, match.start(), match.end()))

    matches.sort(key=lambda item: (item.start, -(item.end - item.start)))
    filtered: list[_RegexEntity] = []
    last_end = -1
    for match in matches:
        if match.start >= last_end:
            filtered.append(match)
            last_end = match.end
    return filtered


def _fallback_mask(text: str) -> PiiSanitizationResult:
    matches = _fallback_entities(text)
    if not matches:
        return PiiSanitizationResult(
            original_text=text,
            sanitized_text=text,
            detected_entities=[],
        )

    parts: list[str] = []
    cursor = 0
    for match in matches:
        parts.append(text[cursor:match.start])
        parts.append(f"<{match.entity_type}>")
        cursor = match.end
    parts.append(text[cursor:])

    return PiiSanitizationResult(
        original_text=text,
        sanitized_text="".join(parts),
        detected_entities=_dedupe_entities(match.entity_type for match in matches),
    )


def sanitize_text_for_llm(text: str) -> PiiSanitizationResult:
    clean_text = (text or "").strip()
    if not clean_text:
        return PiiSanitizationResult(
            original_text=text or "",
            sanitized_text="",
            detected_entities=[],
        )

    _init_presidio()
    if not _PRESIDIO_READY:
        return _fallback_mask(clean_text)

    try:
        analysis_results = _ANALYZER.analyze(
            text=clean_text,
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SSN", "CREDIT_CARD"],
            language="en",
            score_threshold=0.4,
        )

        if not analysis_results:
            return PiiSanitizationResult(
                original_text=clean_text,
                sanitized_text=clean_text,
                detected_entities=[],
            )

        operators = {
            entity.entity_type: _OPERATOR_CONFIG(
                "replace",
                {"new_value": f"<{entity.entity_type}>"},
            )
            for entity in analysis_results
        }
        anonymized = _ANONYMIZER.anonymize(
            text=clean_text,
            analyzer_results=analysis_results,
            operators=operators,
        )
        return PiiSanitizationResult(
            original_text=clean_text,
            sanitized_text=anonymized.text,
            detected_entities=_dedupe_entities(
                entity.entity_type for entity in analysis_results
            ),
        )
    except Exception:
        return _fallback_mask(clean_text)
