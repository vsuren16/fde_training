# Architecture

## POC vs Production

### POC

- Single FastAPI deployable with clear internal service boundaries
- React frontend served independently
- MongoDB and ChromaDB as managed or local services
- LangSmith plus structured logs for traceability

### Production

- API Gateway for auth, rate limiting, and edge policy enforcement
- Load Balancer in front of stateless FastAPI replicas
- Kubernetes deployment for horizontal scaling
- Managed MongoDB and persistent Chroma deployment
- Centralized metrics/logging/tracing stack
- Optional async workers for bulk ingestion and evaluation jobs

## Logical Components

- `Frontend UI`
  - Support engineer search experience
  - Filter controls and incident detail views
- `API Layer`
  - FastAPI routes
  - Pydantic validation
  - Health and readiness endpoints
- `AI Orchestration Layer`
  - Hybrid retrieval
  - Reranking
  - Triage classification
  - Resolution suggestion
  - Guardrails
  - LLM-as-judge hooks
  - Troubleshooting validation
  - Root cause summary
  - Agent handoff orchestration
  - Feedback capture hooks
- `Data Access Layer`
  - Mongo repositories
  - Vector store abstraction
  - OpenAI adapter
- `Platform Layer`
  - Structured logging
  - Rotating file logs
  - LangSmith tracing
  - Metrics and retry policy
  - Startup warmup

## Decoupling Principle

The vector store is accessed through an abstraction so ChromaDB can later be replaced by another backend without changing API handlers or orchestration services. The same principle applies to OpenAI-facing code and persistence repositories.
