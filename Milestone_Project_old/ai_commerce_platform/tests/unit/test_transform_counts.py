from __future__ import annotations

from pyspark.sql import SparkSession

from src.inventory_pipeline.mock_data import build_raw_dataframe
from src.inventory_pipeline.transform import clean_and_validate, normalize_raw


def test_normalize_and_validate_counts():
    spark = SparkSession.builder.master("local[1]").appName("unit-test").getOrCreate()
    try:
        raw_df = build_raw_dataframe(spark)
        normalized = normalize_raw(raw_df)
        valid_df, invalid_df = clean_and_validate(normalized)

        assert raw_df.count() == 20
        assert normalized.count() <= 20
        assert valid_df.count() > 0
        assert invalid_df.count() > 0
    finally:
        spark.stop()
