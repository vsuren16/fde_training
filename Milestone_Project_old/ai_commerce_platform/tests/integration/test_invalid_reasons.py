from __future__ import annotations

from pyspark.sql import SparkSession

from src.inventory_pipeline.mock_data import build_raw_dataframe
from src.inventory_pipeline.transform import clean_and_validate, normalize_raw


def test_invalid_reason_presence():
    spark = SparkSession.builder.master("local[1]").appName("integration-test").getOrCreate()
    try:
        raw_df = build_raw_dataframe(spark)
        normalized = normalize_raw(raw_df)
        _, invalid_df = clean_and_validate(normalized)

        reasons = {row["rejection_reason"] for row in invalid_df.select("rejection_reason").collect()}
        assert "missing_product_id" in reasons or "missing_warehouse_id" in reasons
    finally:
        spark.stop()
