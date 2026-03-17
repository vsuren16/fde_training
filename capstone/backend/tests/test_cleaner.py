from pathlib import Path

from app.ingestion.cleaner import load_and_clean_incidents


def test_load_and_clean_incidents_returns_canonical_records() -> None:
    root = Path(__file__).resolve().parents[1]
    dataset_path = root / "data" / "raw" / "it_incidents_10k.csv"
    incidents = load_and_clean_incidents(dataset_path)

    assert incidents
    first = incidents[0]
    assert first.incident_id
    assert first.title
    assert first.description
    assert first.resolution_notes
    assert first.incident_text
