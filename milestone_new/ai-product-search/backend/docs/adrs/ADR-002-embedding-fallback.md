# ADR-002: Embedding Fallback Chain

Decision: primary OpenAI embeddings with local transformer fallback.

- Why: balances quality and resiliency.
- Tradeoff: local model cold-start memory/time overhead.
