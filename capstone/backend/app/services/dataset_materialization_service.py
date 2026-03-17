from pathlib import Path

import pandas as pd

from app.core.config import get_settings
from app.ingestion.cleaner import load_and_clean_incidents
from app.observability.logging import get_logger


logger = get_logger(__name__)


class DatasetMaterializationService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def write_processed_dataset(self) -> Path:
        logger.info(
            "dataset_cleaning_started",
            extra={"raw_dataset_path": str(self.settings.raw_dataset_path)},
        )
        incidents = load_and_clean_incidents(self.settings.raw_dataset_path)
        output_path = Path(self.settings.processed_dataset_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe = pd.DataFrame([incident.model_dump() for incident in incidents])
        dataframe.to_csv(output_path, index=False)
        logger.info(
            "dataset_cleaning_completed",
            extra={
                "processed_dataset_path": str(output_path),
                "cleaned_records": len(incidents),
            },
        )
        return output_path

    def load_processed_incidents(self) -> list[dict]:
        output_path = Path(self.settings.processed_dataset_path)
        if not output_path.exists():
            logger.info(
                "processed_dataset_missing_rebuilding",
                extra={"processed_dataset_path": str(output_path)},
            )
            self.write_processed_dataset()
        dataframe = pd.read_csv(output_path, low_memory=False)
        dataframe = dataframe.where(pd.notnull(dataframe), None)
        records = dataframe.to_dict(orient="records")
        logger.info(
            "processed_dataset_loaded",
            extra={
                "processed_dataset_path": str(output_path),
                "loaded_records": len(records),
            },
        )
        return records
