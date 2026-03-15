# Evaluation Summary

## Methodology
- IR-style evaluation using curated ground truth dataset.
- Metrics: MAP@5, NDCG@5.
- Latency benchmark script computes average and p99.

## Current Baseline
- Use `pytest tests/evaluation/test_ir_metrics.py` for MAP/NDCG calculation.
- Use `python scripts/benchmark_latency.py` for p99 and average latency.

## Notes
- Scores vary by embedding provider (OpenAI vs local fallback vs fake-test).
- Production validation should run against representative catalog and user query logs.
