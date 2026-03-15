"""Transform and validation logic for inventory ingestion."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql.functions import coalesce, col, lit, lower, regexp_extract, to_timestamp, trim, when


def _pick(df: DataFrame, candidates: list[str]):
    existing = [c for c in candidates if c in df.columns]
    if not existing:
        return lit(None)
    return coalesce(*[col(c) for c in existing])


def _to_int(expr):
    return regexp_extract(trim(expr.cast("string")), r"-?\\d+", 0).cast("int")


def normalize_raw(df: DataFrame) -> DataFrame:
    normalized = (
        df.withColumn("inventory_id", trim(_pick(df, ["inventory_id", "inv_id", "inventory", "Inventory Id"])))
        .withColumn("product_id", trim(_pick(df, ["product_id", "product", "product id", "ProductID"])))
        .withColumn("warehouse_id", lower(trim(_pick(df, ["warehouse_id", "warehouseId", "warehouse", "Warehouse ID"]))))
        .withColumn("available_stock", _to_int(_pick(df, ["available_stock", "available", "avail"])))
        .withColumn("reserved_stock", _to_int(_pick(df, ["reserved_stock", "reserved"])))
        .withColumn("damaged_stock", _to_int(_pick(df, ["damaged_stock", "damaged"])))
        .withColumn("reorder_level", _to_int(_pick(df, ["reorder_level", "reorder"])))
        .withColumn("last_updated", trim(_pick(df, ["last_updated", "lastUpdated", "updated_at"])))
        .withColumn("batch_number", trim(_pick(df, ["batch_number", "batch"])))
        .select(
            "inventory_id",
            "product_id",
            "warehouse_id",
            "available_stock",
            "reserved_stock",
            "damaged_stock",
            "reorder_level",
            "last_updated",
            "batch_number",
        )
    )
    return normalized.dropDuplicates(["inventory_id"])


def clean_and_validate(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    clean = (
        df.withColumn("available_stock", coalesce(col("available_stock"), lit(0)))
        .withColumn("reserved_stock", coalesce(col("reserved_stock"), lit(0)))
        .withColumn("damaged_stock", coalesce(col("damaged_stock"), lit(0)))
        .withColumn("reorder_level", coalesce(col("reorder_level"), lit(0)))
        .withColumn("available_stock", when(col("available_stock") < 0, lit(0)).otherwise(col("available_stock")))
        .withColumn("reserved_stock", when(col("reserved_stock") < 0, lit(0)).otherwise(col("reserved_stock")))
        .withColumn("damaged_stock", when(col("damaged_stock") < 0, lit(0)).otherwise(col("damaged_stock")))
        .withColumn("reorder_level", when(col("reorder_level") < 0, lit(0)).otherwise(col("reorder_level")))
        .withColumn("last_updated_ts", to_timestamp(col("last_updated")))
    )

    rejection_reason = when(col("inventory_id").isNull() | (col("inventory_id") == ""), lit("missing_inventory_id"))
    rejection_reason = rejection_reason.when(col("product_id").isNull() | (col("product_id") == ""), lit("missing_product_id"))
    rejection_reason = rejection_reason.when(col("warehouse_id").isNull() | (col("warehouse_id") == ""), lit("missing_warehouse_id"))
    rejection_reason = rejection_reason.when(col("last_updated").isNull() | (col("last_updated") == ""), lit("missing_last_updated"))
    rejection_reason = rejection_reason.when(col("last_updated_ts").isNull(), lit("invalid_last_updated_format"))

    validated = clean.withColumn("rejection_reason", rejection_reason)
    invalid_df = validated.filter(col("rejection_reason").isNotNull())
    valid_df = validated.filter(col("rejection_reason").isNull())
    return valid_df, invalid_df
