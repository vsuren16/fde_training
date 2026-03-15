# System Architecture

## POC Runtime (Current)
- MongoDB
- PySpark ingestion container
- In-script mock data source

## Service Boundaries (Future)
- API Gateway
- User Service
- Product Service
- Cart Service
- Order Service
- Search Service

## Production Target Architecture
- API Gateway behind Load Balancer
- Stateless microservices on Kubernetes (HPA-enabled)
- Managed MongoDB cluster with pooled clients
- Vector DB abstraction layer (FAISS/Milvus/pgvector swappable)
- Observability stack (metrics, logs, traces)
- MLOps layer (embedding versions, model versions, rollout controls)

## Observability & MLOps Layers
- Structured JSON logs with correlation IDs
- Metrics: p99 latency, throughput, error rates
- Model/version registry metadata on each retrieval event
- Controlled rollout with health gates and rollback criteria
