from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def inventory_schema() -> StructType:
    return StructType(
        [
            StructField("inventory_id", StringType(), True),
            StructField("product_id", StringType(), True),
            StructField("warehouse_id", StringType(), True),
            StructField("available_stock", IntegerType(), True),
            StructField("reserved_stock", IntegerType(), True),
            StructField("damaged_stock", IntegerType(), True),
            StructField("reorder_level", IntegerType(), True),
            StructField("last_updated", StringType(), True),
            StructField("batch_number", StringType(), True),
        ]
    )
