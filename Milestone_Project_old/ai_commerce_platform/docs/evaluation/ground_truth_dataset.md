# Ground Truth Dataset

## Milestone 1
Ground truth for ingestion validation is the in-script 20-record mock source in:
- `src/inventory_pipeline/mock_data.py`

Expected outcomes:
- 20 raw records total
- known invalid cases (missing IDs, invalid timestamp, blank required fields)
- known duplicate inventory ID for idempotency check

## Milestone 3 (Future)
Ground-truth search query-to-product relevance dataset will be provided under `requirements/`.
