from pathlib import Path

import pandas as pd

from app.core.config import get_settings
from app.ingestion.cleaner import REQUIRED_SOURCE_COLUMNS, load_and_clean_incidents
from app.schemas.incident import IngestionPreviewResponse


class IngestionService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def preview_dataset(self) -> IngestionPreviewResponse:
        source_path = Path(self.settings.raw_dataset_path)
        if not source_path.exists():
            raise FileNotFoundError(f"dataset not found: {source_path}")

        dataframe = pd.read_csv(source_path, low_memory=False)
        cleaned = load_and_clean_incidents(source_path)
        return IngestionPreviewResponse(
            source_rows=len(dataframe),
            cleaned_rows=len(cleaned),
            dropped_rows=len(dataframe) - len(cleaned),
            required_columns=REQUIRED_SOURCE_COLUMNS,
            retrieval_strategy=(
                "title_plus_description_keyword_and_semantic_retrieval"
            ),
            resolution_strategy="native_resolution_notes_from_dataset",
        )
