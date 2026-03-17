from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.domain.incident import CanonicalIncident


REQUIRED_SOURCE_COLUMNS = [
    "incident_id",
    "title",
    "category",
    "priority",
    "priority_label",
    "status",
    "description",
    "resolution_notes",
    "team",
    "assigned_to",
    "resolution_time_hours",
    "created_at",
    "created_by",
    "updated_at",
    "updated_by",
    "closed_at",
    "closed_by",
]


def _clean_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = " ".join(str(value).replace("\u2014", "-").replace("\u00d7", "x").split())
    return text.strip() or None


def _clean_float(value: object) -> float | None:
    if pd.isna(value):
        return None
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def _clean_int(value: object) -> int | None:
    if pd.isna(value):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _build_incident_text(row: pd.Series) -> str:
    segments = [
        row.get("title"),
        row.get("category"),
        row.get("status"),
        row.get("description"),
        f"Owned by {row['team']}" if row.get("team") else None,
        f"Priority {row['priority']} {row['priority_label']}".strip()
        if row.get("priority") is not None
        else row.get("priority_label"),
    ]
    return ". ".join(part for part in segments if part)


def load_and_clean_incidents(dataset_path: str | Path) -> list[CanonicalIncident]:
    dataframe = pd.read_csv(dataset_path, low_memory=False)
    missing_columns = sorted(set(REQUIRED_SOURCE_COLUMNS) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"dataset is missing required columns: {missing_columns}")

    dataframe = dataframe[REQUIRED_SOURCE_COLUMNS].copy()

    text_columns = [
        "incident_id",
        "title",
        "category",
        "priority_label",
        "status",
        "description",
        "resolution_notes",
        "team",
        "assigned_to",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "closed_at",
        "closed_by",
    ]
    for column in text_columns:
        dataframe[column] = dataframe[column].map(_clean_text)

    dataframe["priority"] = dataframe["priority"].map(_clean_int)
    dataframe["resolution_time_hours"] = dataframe["resolution_time_hours"].map(_clean_float)

    dataframe = dataframe.dropna(subset=["incident_id", "title", "description", "resolution_notes"])
    dataframe = dataframe.drop_duplicates(subset=["incident_id"], keep="first")
    dataframe["incident_text"] = dataframe.apply(_build_incident_text, axis=1)
    dataframe = dataframe[dataframe["incident_text"].str.len() > 0]

    records = [
        {key: (None if pd.isna(value) else value) for key, value in record.items()}
        for record in dataframe.to_dict(orient="records")
    ]
    return [CanonicalIncident.model_validate(record) for record in records]
