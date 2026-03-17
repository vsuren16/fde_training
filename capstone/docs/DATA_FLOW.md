# Data Flow

## Ingestion Flow

1. Load `backend/data/raw/it_incidents_10k.csv`.
2. Validate the required columns and normalize fields.
3. Drop invalid or duplicate rows.
4. Materialize canonical incident records and processed CSV output.
5. Replace incident documents in MongoDB.
6. If OpenAI is reachable, generate embeddings in batches.
7. Reset and rebuild the Chroma collection.
8. Warm the in-memory keyword index from MongoDB.
9. Record ingestion progress through structured logs.

## Retrieval Flow

1. User submits a natural-language query.
2. Input guardrails validate query length and quality.
3. Optional metadata filters narrow retrieval by `category` and `team`.
4. System runs:
   - keyword retrieval
   - semantic retrieval
5. Results are merged and reranked.
6. Token-optimized evidence is selected for generation and judging.
7. If internal evidence is sufficiently relevant:
   - generate grounded resolution guidance
   - run LLM-as-judge or heuristic judge
8. If grounding is weak:
   - downgrade to a conservative evidence-backed fallback
9. If internal evidence is not sufficiently relevant:
   - disclose that the knowledge base is insufficient
   - route the request to an AI-model fallback response
10. Generate triage, route target, handoff path, RCA summary, and metrics.
11. Return incidents, guidance, diagnostics fields, and response mode.

## Failure and Degradation Flow

1. If vector indexing is unavailable, fall back to keyword-only retrieval.
2. If OpenAI summary generation fails, use conservative fallback behavior.
3. If the judge does not approve a KB-backed answer, downgrade it.
4. If the internal evidence itself is weak or mismatched, switch to disclosed AI-model fallback guidance.
5. If the fallback LLM path is also unavailable, return a clear refinement/escalation message.

## Feedback and Evaluation Flow

1. User can submit feedback on a returned incident result.
2. Feedback is stored in MongoDB.
3. Feedback can later be used for tuning, evaluation, and continuous improvement.
4. DeepEval readiness is exposed through the evaluation service for future benchmark integration.

## Admin / Observability Flow

1. Admin logs in through Mongo-backed hashed credentials.
2. Admin panel requests runtime observability data.
3. Backend performs real connectivity checks for:
   - MongoDB
   - LangSmith
   - ChromaDB
   - OpenAI
4. Backend returns status, diagnostics, and log file path.
5. Admin can open LangSmith or download logs.
