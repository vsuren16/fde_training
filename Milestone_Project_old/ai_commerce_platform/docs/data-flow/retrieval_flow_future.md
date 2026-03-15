# Retrieval Data Flow (Future - M3)

1. Query arrives at API gateway.
2. Product/search service validates request schema.
3. Query embedding generated via configured embedding provider.
4. Vector retrieval performed through adapter interface.
5. Optional lexical fallback merged with vector results.
6. Re-ranking applied if enabled.
7. Fallback path returns keyword-only results if vector retrieval fails.
8. Response includes model_version and embedding_version metadata.
9. Request/response traces logged for evaluation.
