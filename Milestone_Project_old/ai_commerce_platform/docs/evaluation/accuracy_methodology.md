# Accuracy Methodology (Current + Future)

## Current (Milestone 1)
- Data quality accuracy measured by schema compliance and rejection categorization.
- Validation success ratio: `valid_count / raw_record_count`.
- Error auditability: invalid records persisted with rejection_reason.

## Future (Milestone 3)
- Retrieval quality via IR metrics: Recall@K, NDCG@10, MRR.
- Optional LLM-as-Judge for relevance and faithfulness scoring.
- Release gates compare candidate model vs baseline.
