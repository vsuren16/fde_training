from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class ResolutionSeed:
    category: str
    incident_details: str
    description: str
    solution: str


def load_resolution_seeds(seed_path: str | Path) -> dict[str, ResolutionSeed]:
    dataframe = pd.read_csv(seed_path, low_memory=False)
    seeds: dict[str, ResolutionSeed] = {}
    for record in dataframe.to_dict(orient="records"):
        category = str(record["Category"]).strip().lower()
        seeds[category] = ResolutionSeed(
            category=category,
            incident_details=str(record["Incident Details"]).strip(),
            description=str(record["Description"]).strip(),
            solution=str(record["Solution"]).strip(),
        )
    return seeds


def infer_seed_category(
    ci_category: str | None,
    ci_subcategory: str | None,
    closure_code: str | None,
) -> str:
    ci_category_text = (ci_category or "").lower()
    ci_subcategory_text = (ci_subcategory or "").lower()
    closure_code_text = (closure_code or "").lower()
    combined = " ".join([ci_category_text, ci_subcategory_text, closure_code_text])

    if any(token in combined for token in ["network", "citrix", "exchange", "controller"]):
        return "network"
    if any(token in combined for token in ["database", "sql"]):
        return "database"
    if any(token in combined for token in ["storage", "san", "disk"]):
        return "storage"
    if any(token in combined for token in ["hardware", "laptop", "printer", "monitor"]):
        return "hardware"
    if any(token in combined for token in ["security", "access", "operator error", "user error"]):
        return "security"
    if any(token in combined for token in ["performance", "timeout", "slow"]):
        return "performance"
    return "application"


def generate_synthetic_resolution(
    *,
    ci_category: str | None,
    ci_subcategory: str | None,
    category: str | None,
    impact: int | None,
    urgency: int | None,
    priority: int | None,
    closure_code: str | None,
    kb_number: str | None,
    seed_category: str,
    seeds: dict[str, ResolutionSeed],
) -> str:
    impact = None if pd.isna(impact) else impact
    urgency = None if pd.isna(urgency) else urgency
    priority = None if pd.isna(priority) else priority
    seed = seeds[seed_category]
    triage_phrase = (
        f"Treat this as priority {priority} and stabilize user impact first."
        if priority is not None
        else "Stabilize the affected service first and verify blast radius."
    )
    context_bits = [
        f"Incident type is {category}." if category else None,
        f"Configuration item area is {ci_category}." if ci_category else None,
        f"Sub-area is {ci_subcategory}." if ci_subcategory else None,
        f"Observed impact is {impact}." if impact is not None else None,
        f"Observed urgency is {urgency}." if urgency is not None else None,
        f"Historical closure classification is {closure_code}." if closure_code else None,
        f"Reference knowledge article {kb_number} if available." if kb_number else None,
    ]
    context = " ".join(bit for bit in context_bits if bit)
    return (
        f"{triage_phrase} {context} Start with the seed playbook for {seed.category}: "
        f"Representative symptom pattern: {seed.incident_details}. "
        f"Representative description: {seed.description}. "
        f"Suggested starting action: {seed.solution}. "
        "Validate the fix against the current symptom pattern and document whether the issue is "
        "configuration, software, access, or capacity related."
    )
