import json
import logging
import os
from datetime import datetime, timezone

import boto3

bucket = os.getenv("MINIO_BUCKET", "inventory-raw")
endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
access = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
secret = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")

session = boto3.session.Session()
client = session.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=access,
    aws_secret_access_key=secret,
    region_name="us-east-1",
)

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

records = [
    {
        "inventory_id": "INV-1001",
        "product_id": "P-101",
        "warehouse_id": "WH-A",
        "available_stock": 120,
        "reserved_stock": 12,
        "damaged_stock": 1,
        "reorder_level": 20,
        "last_updated": now,
        "batch_number": None,
    },
    {
        "inventory_id": "INV-1002",
        "product_id": "P-102",
        "warehouse_id": "WH-B",
        "available_stock": 75,
        "reserved_stock": 4,
        "damaged_stock": 0,
        "reorder_level": 15,
        "last_updated": now,
        "batch_number": None,
    },
    {
        "inventory_id": "INV-1003",
        "product_id": "P-103",
        "warehouse_id": "WH-A",
        "available_stock": 50,
        "reserved_stock": None,
        "damaged_stock": None,
        "reorder_level": None,
        "last_updated": now,
        "batch_number": None,
    },
    {
        "inventory_id": "INV-1004",
        "product_id": "P-104",
        "warehouse_id": "WH-C",
        "available_stock": -7,
        "reserved_stock": 2,
        "damaged_stock": 0,
        "reorder_level": 5,
        "last_updated": now,
        "batch_number": None,
    },
    {
        "inventory_id": "INV-1005",
        "product_id": "P-105",
        "warehouse_id": "WH-D",
        "available_stock": 20,
        "reserved_stock": 1,
        "damaged_stock": 0,
        "reorder_level": 5,
        "last_updated": "",
        "batch_number": None,
    },
]

payload = "\n".join(json.dumps(r) for r in records)
key = "daily/inventory_20260226.json"
client.put_object(Bucket=bucket, Key=key, Body=payload.encode("utf-8"), ContentType="application/json")
logger.info('uploaded_object bucket=%s key=%s', bucket, key)
logging.basicConfig(level=logging.INFO, format='{"level":"%(levelname)s","message":"%(message)s"}')
logger = logging.getLogger("minio_seed")
