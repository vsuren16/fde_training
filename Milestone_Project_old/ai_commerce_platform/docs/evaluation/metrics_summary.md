# Metrics Summary

## Current Metrics (M1)
- Raw record count
- Valid record count
- Invalid record count
- Inserted/Updated/Failed Mongo upserts

## Performance Baseline (M1 Local)
- Throughput and latency should be captured from execution log timestamp and runtime wrapper script.
- p99 retrieval metrics are deferred to M3 search benchmark.

## Future Metrics (M3/M4)
- Retrieval p99 latency
- Throughput (requests/sec)
- Recall@K, NDCG@10, MRR
- Model fallback rate
- Circuit breaker open-rate
