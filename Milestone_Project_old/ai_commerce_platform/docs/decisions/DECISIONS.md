# DECISIONS / ADRs

## ADR-001: Use PySpark for Inventory Ingestion
- Decision: Use PySpark DataFrames for normalization and validation.
- Pros: Scalable to large datasets, robust transformation primitives.
- Cons: Runtime overhead for small datasets.
- Trade-off: Chosen for production-readiness over minimal runtime simplicity.

## ADR-002: Mock Raw Data Embedded in Pipeline for Milestone 1
- Decision: Keep source data in-script for deterministic grading.
- Pros: No external dependency during evaluation, repeatable runs.
- Cons: Not production-realistic source integration.
- Trade-off: Reliability and reproducibility prioritized for milestone scope.

## ADR-003: Structured JSON Logging
- Decision: Replace print statements with structured log events.
- Pros: Easier indexing/searching in observability systems.
- Cons: Slightly more setup than plain logs.

## ADR-004: Vector Store Decoupling Strategy (Future)
- Decision: Define adapter boundary for retrieval engine.
- Pros: Allows FAISS -> Milvus/pgvector migration with no API contract break.
- Cons: Slight abstraction complexity.
