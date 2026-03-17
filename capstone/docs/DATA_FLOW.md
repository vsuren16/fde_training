# Data Flow

## Ingestion Flow

1. Load CSV from `backend/data/raw/ITSM_data.csv`.
2. Select only required columns.
3. Normalize mixed types and categorical values.
4. Remove invalid or duplicate incidents.
5. Derive retrieval text from structured fields.
6. Store normalized incident documents in MongoDB.
7. Generate embeddings with OpenAI.
8. Persist vectors and metadata in ChromaDB.

## Retrieval Flow

1. User submits a natural-language query.
2. Input guardrails validate size, emptiness, and unsafe prompt-like content.
3. System runs keyword retrieval plus semantic retrieval.
4. Results are merged and reranked using recency and resolution-success heuristics.
5. Token-optimized evidence is selected for generation and judge evaluation.
6. Retrieved incidents are passed to the RAG layer.
7. LLM-as-judge or heuristic fallback validates grounding and troubleshooting relevance.
8. Agent handoff path and RCA summary are generated from the ranked evidence.
9. API returns incidents, triage signal, route target, handoff path, metrics, and grounded guidance.

## Failure and Degradation Flow

1. If embeddings or vector search fail, fall back to keyword-only retrieval.
2. If OpenAI generation fails, return retrieval-only evidence and a degraded response flag.
3. If the judge does not approve the answer, downgrade to a safer grounded fallback summary.
4. If ingestion data is empty or malformed, fail fast with structured validation errors.

## Feedback and Evaluation Flow

1. Search responses can be rated through the feedback endpoint.
2. Feedback is stored in MongoDB for later tuning and analysis.
3. DeepEval readiness is exposed through an evaluation endpoint for benchmark integration.
