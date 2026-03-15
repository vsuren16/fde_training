# Ingestion Data Flow (Implemented)

1. Build Spark session.
2. Load 20 raw, unstructured mock records.
3. Normalize inconsistent field names to canonical schema.
4. Parse numeric text into integers and sanitize null/invalid values.
5. Validate required fields and timestamp parseability.
6. Split dataset into valid and invalid sets.
7. Persist invalid records with rejection reasons.
8. Upsert valid records into MongoDB by `inventory_id`.
9. Persist execution metrics summary.
10. Emit structured logs for start/success/failure.
