import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import coalesce, col, current_timestamp, lit

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.common.structured_logging import get_logger
from src.common.runtime_config import load_runtime_settings
from src.inventory_pipeline.loader import upsert_inventory
from src.inventory_pipeline.mock_data import RAW_INVENTORY_RECORDS, build_raw_dataframe
from src.inventory_pipeline.transform import clean_and_validate, normalize_raw

logger = get_logger("inventory_pipeline")


def parse_args():
    parser = argparse.ArgumentParser(description="Inventory PySpark ingestion job")
    parser.add_argument("--environment", default=None, choices=["dev", "prod"], help="Runtime environment profile")
    parser.add_argument(
        "--output-log-dir",
        default=None,
        help="Directory for pipeline artifacts/logs",
    )
    parser.add_argument("--run-id", default=None, help="Optional run identifier for deterministic log naming")
    return parser.parse_args()


def build_spark() -> SparkSession:
    return SparkSession.builder.appName("inventory-ingestion-mock").getOrCreate()


def main():
    args = parse_args()
    settings = load_runtime_settings(profile=args.environment, output_log_dir_override=args.output_log_dir)
    run_ts = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    batch_id = f"BATCH-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"
    logs_dir = Path(settings.output_log_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger.info(
        "starting ingestion run",
        extra={"run_id": run_ts, "environment": settings.environment, "output_log_dir": str(logs_dir)},
    )

    spark = build_spark()

    try:
        raw_df = build_raw_dataframe(spark)
        df = normalize_raw(raw_df)
        valid_df, invalid_df = clean_and_validate(df)

        invalid_path = logs_dir / f"invalid_records_{run_ts}.json"
        invalid_df.select(
            "inventory_id",
            "product_id",
            "warehouse_id",
            "available_stock",
            "reserved_stock",
            "damaged_stock",
            "reorder_level",
            "last_updated",
            "rejection_reason",
        ).coalesce(1).write.mode("overwrite").json(str(invalid_path))

        final_df = valid_df.withColumn("batch_number", coalesce(col("batch_number"), lit(batch_id))).withColumn(
            "processed_at", current_timestamp()
        )

        inserted, updated, failed = upsert_inventory(
            final_df=final_df,
            mongo_uri=settings.mongo_uri,
            mongo_db=settings.mongo_db,
        )

        metrics = {
            "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "run_id": run_ts,
            "environment": settings.environment,
            "data_source": "in_script_mock",
            "raw_record_count": len(RAW_INVENTORY_RECORDS),
            "valid_count": int(final_df.count()),
            "invalid_count": int(invalid_df.count()),
            "inserted": inserted,
            "updated": updated,
            "failed": failed,
            "batch_number": batch_id,
            "invalid_records_path": str(invalid_path),
        }

        metrics_path = logs_dir / f"execution_log_{run_ts}.json"
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        logger.info("ingestion completed", extra=metrics)

    except Exception:
        logger.exception("ingestion failed", extra={"run_id": run_ts})
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
