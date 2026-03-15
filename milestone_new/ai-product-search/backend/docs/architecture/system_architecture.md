# Architecture Overview

```mermaid
flowchart LR
  U[User/Frontend] --> G[API Gateway or Ingress]
  G --> A[FastAPI Service Pods]
  A --> E[Embedding Manager]
  E --> O[OpenAI Embedding API]
  E --> L[Local Transformer Model]
  A --> V[Vector Store Adapter]
  V --> VI[(Vector Index)]
  A --> D[(SQL Database - Search History)]
  A --> M[Metrics/Logs Collector]
  M --> OBS[Observability Stack]
```

## POC vs Production

- POC: single FastAPI container + in-memory vector store.
- Production: API gateway, load balancer, multi-replica K8s deployment, managed DB, external vector DB.

## MLOps/Observability

- Structured logs with query, model version, latency, scores.
- Health endpoints for liveness/readiness.
- Model version surfaced in responses and logs.
