# Architecture (Current State)

## Current Implementation
This repository currently runs **Milestone 1 only**:
- MongoDB
- PySpark inventory ingestion job
- In-script mock raw inventory dataset (20 records)

## M1 Data Flow
1. Spark job constructs 20 raw/unstructured mock inventory records in memory.
2. Spark normalizes field names and data types.
3. Spark applies validation and cleansing rules.
4. Invalid records are written under `data-engineering/inventory_pipeline/logs`.
5. Valid records are upserted into `ai_commerce.inventory`.

## Future-Ready Scaffolding (Not Implemented)
- `api-gateway`, `user-service`, `product-service`, `cart-service`, `order-service`, `search-service`.
- Each service currently exposes scaffold behavior only.

## Why This Boundary
The target submission scope is Milestone 1 grading, while preserving explicit contracts and folder structure for Milestones 2–4.
