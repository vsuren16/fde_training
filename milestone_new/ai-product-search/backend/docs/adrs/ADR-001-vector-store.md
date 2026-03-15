# ADR-001: Vector Store Interface

Decision: use `VectorStore` abstraction with in-memory implementation for now.

- Why: allows future migration to FAISS/Milvus/Atlas without API/service rewrite.
- Tradeoff: one extra abstraction layer.
