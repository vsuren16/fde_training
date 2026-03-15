"""In-script mock records for Milestone 1 ingestion."""

from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType


RAW_INVENTORY_RECORDS = [
    {"inventory_id": " INV-1001 ", "product id": " P-101 ", "warehouse": " WH-A ", "available": "120", "reserved": "10", "damaged": "1", "reorder": "20", "last_updated": "2026-02-26T10:00:00Z", "batch": None},
    {"inv_id": "INV-1002", "product_id": "P-102", "warehouse_id": "wh-b", "available_stock": "75", "reserved_stock": "4", "damaged_stock": "0", "reorder_level": "15", "lastUpdated": "2026-02-26 10:10:00"},
    {"inventory": "INV-1003", "product": "P-103", "warehouseId": "WH-C", "avail": "50units", "reserved": None, "damaged": None, "reorder": None, "last_updated": "2026/02/26 10:20:00"},
    {"inventory_id": "INV-1004", "product_id": "P-104", "warehouse_id": "WH-A", "available_stock": -7, "reserved_stock": 2, "damaged_stock": 0, "reorder_level": 5, "last_updated": "2026-02-26T10:30:00Z"},
    {"inventory_id": "INV-1005", "product_id": "P-105", "warehouse_id": "WH-B", "available_stock": "20", "reserved_stock": "1", "damaged_stock": "0", "reorder_level": "5", "last_updated": ""},
    {"inventory_id": "INV-1006", "product_id": "P-106", "warehouse_id": "WH-C", "available_stock": " 40 ", "reserved_stock": " 3 ", "damaged_stock": "0", "reorder_level": "10", "last_updated": "2026-02-26T10:40:00Z"},
    {"inventory_id": "INV-1007", "product_id": "P-107", "warehouse_id": "  ", "available_stock": "60", "reserved_stock": "6", "damaged_stock": "1", "reorder_level": "8", "last_updated": "2026-02-26T10:50:00Z"},
    {"inventory_id": "INV-1008", "product_id": "", "warehouse_id": "WH-D", "available_stock": "45", "reserved_stock": "4", "damaged_stock": "0", "reorder_level": "7", "last_updated": "2026-02-26T11:00:00Z"},
    {"inventory_id": "INV-1009", "product_id": "P-109", "warehouse_id": "WH-E", "available_stock": "N/A", "reserved_stock": "2", "damaged_stock": "0", "reorder_level": "6", "last_updated": "2026-02-26T11:10:00Z"},
    {"inventory_id": "INV-1010", "product_id": "P-110", "warehouse_id": "WH-F", "available_stock": "35", "reserved_stock": "two", "damaged_stock": "none", "reorder_level": "5", "last_updated": "2026-02-26T11:20:00Z"},
    {"inventory_id": None, "product_id": "P-111", "warehouse_id": "WH-G", "available_stock": "15", "reserved_stock": "1", "damaged_stock": "0", "reorder_level": "3", "last_updated": "2026-02-26T11:30:00Z"},
    {"inventory_id": "INV-1012", "product_id": "P-112", "warehouse_id": "WH-H", "available_stock": "22", "reserved_stock": "2", "damaged_stock": "0", "reorder_level": "4", "last_updated": "bad-date"},
    {"inventory_id": "INV-1013", "product_id": "P-113", "warehouse_id": "WH-I", "available_stock": "-12", "reserved_stock": "-1", "damaged_stock": "-3", "reorder_level": "-5", "last_updated": "2026-02-26T11:40:00Z"},
    {"inventory_id": "INV-1014", "product_id": "P-114", "warehouse_id": "WH-J", "available_stock": "90", "reserved_stock": None, "damaged_stock": None, "reorder_level": None, "last_updated": "2026-02-26T11:45:00Z", "batch_number": "BATCH-LEGACY-01"},
    {"inventory_id": "INV-1015", "product_id": "P-115", "warehouse_id": "WH-K", "available_stock": "100", "reserved_stock": "10", "damaged_stock": "0", "reorder_level": "20", "last_updated": "2026-02-26T11:50:00Z"},
    {"inventory_id": "INV-1016", "product_id": "P-116", "warehouse_id": "WH-L", "available_stock": "49", "reserved_stock": "5", "damaged_stock": "1", "reorder_level": "9", "last_updated": "2026-02-26T11:55:00Z"},
    {"inventory_id": "INV-1017", "product_id": "P-117", "warehouse_id": "WH-M", "available_stock": "33", "reserved_stock": "3", "damaged_stock": "0", "reorder_level": "7", "last_updated": "2026-02-26T12:00:00Z"},
    {"inventory_id": "INV-1018", "product_id": "P-118", "warehouse_id": "WH-N", "available_stock": "25", "reserved_stock": "2", "damaged_stock": "0", "reorder_level": "6", "last_updated": "2026-02-26T12:05:00Z"},
    {"inventory_id": "INV-1019", "product_id": "P-119", "warehouse_id": "WH-O", "available_stock": "17", "reserved_stock": "1", "damaged_stock": "0", "reorder_level": "5", "last_updated": "2026-02-26T12:10:00Z"},
    {"inventory_id": "INV-1001", "product_id": "P-101", "warehouse_id": "WH-A", "available_stock": "121", "reserved_stock": "11", "damaged_stock": "1", "reorder_level": "21", "last_updated": "2026-02-26T12:15:00Z"},
]


def build_raw_dataframe(spark: SparkSession):
    keys = sorted({k for record in RAW_INVENTORY_RECORDS for k in record.keys()})
    schema = StructType([StructField(k, StringType(), True) for k in keys])

    rows = []
    for record in RAW_INVENTORY_RECORDS:
        row = []
        for key in keys:
            value = record.get(key)
            row.append(None if value is None else str(value))
        rows.append(tuple(row))

    return spark.createDataFrame(rows, schema=schema)
