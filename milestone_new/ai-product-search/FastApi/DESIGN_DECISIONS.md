# Design Decisions

## 1. FastAPI for the Application Layer

FastAPI was chosen because the requirement explicitly targets a structured FastAPI backend and because it provides async support, validation, and generated API docs with low ceremony.

## 2. Embedding Provider Chain with Exact Attribution

The system supports an embedding chain:

- `openai:text-embedding-3-small` when configured
- `local:sentence-transformers/all-MiniLM-L6-v2` as fallback

Instead of returning the configured provider chain, the implementation records the exact provider that successfully generated the embedding for each request. This satisfies the requirement to track model version usage accurately.

## 3. Vector Store Abstraction

The recommendation engine is written against a `VectorStore` interface. This keeps semantic search logic independent from ChromaDB and allows in-memory fallback for local development.

## 4. Cosine Similarity Retrieval

Both Chroma and the in-memory store use cosine similarity semantics. This aligns directly with the requirement for similarity-based ranking.

## 5. Business Filtering After Retrieval

The system separates semantic retrieval from business constraints. After nearest-neighbor retrieval, results are filtered by availability, category, and pricing rules. This keeps recommendation quality and business logic independently tunable.

## 6. Graceful Degradation

If vector retrieval fails or returns nothing useful, the platform degrades to keyword ranking so the user still receives recommendations instead of a hard failure.

## 7. LangSmith as Optional Observability Layer

LangSmith tracing is integrated as an optional capability, activated only through environment variables. This preserves local simplicity while enabling trace-level observability for recommendation workflows during demos, debugging, and review.

## 8. Requirement-Aligned Compatibility Structure

The project is actively developed in `backend/` and `frontend/`, but this `FastApi/` submission tree is retained to satisfy strict folder-structure evaluation without duplicating the running backend logic.
