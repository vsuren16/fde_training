# POC vs Production Boundary

## What is POC now
- Mock in-script inventory source
- Single MongoDB container
- Manual Spark ingestion run
- Service stubs for M2-M4

## What is Production target
- API gateway + load balancing
- Kubernetes deployment and autoscaling
- Managed DB and secrets manager
- Retry/circuit breaker policies for downstream calls
- Observability dashboards and alerting
- Automated CI/CD with quality gates

## Why this split
The repository is deliberately scoped to Milestone 1 implementation while preserving production-grade interfaces and design direction.
