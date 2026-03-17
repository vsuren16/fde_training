# Architectural Decision Records

## ADR-001: FastAPI for the Backend API

### Decision

Use `FastAPI` as the backend framework.

### Why

- strong fit for Python-based AI integration
- first-class Pydantic validation
- fast iteration and clean async I/O support

### Tradeoff

- less enterprise convention than Spring Boot

## ADR-002: MongoDB + ChromaDB Split

### Decision

Use MongoDB for canonical incident data and ChromaDB for vector retrieval.

### Why

- MongoDB fits operational documents, admin users, and feedback
- ChromaDB fits semantic search
- source of truth stays separate from derived vector index

### Tradeoff

- requires store synchronization strategy

## ADR-003: Hybrid Search Over Pure Semantic Search

### Decision

Use keyword + semantic retrieval.

### Why

- IT support queries contain exact operational terms that keyword search handles well
- semantic retrieval captures paraphrased incidents

### Tradeoff

- score merging and relevance tuning are required

## ADR-004: RAG Over Direct LLM Answering

### Decision

Generate answers from retrieved incident evidence first.

### Why

- grounded answers are safer for support workflows
- historical incidents and resolution notes are the knowledge asset

### Tradeoff

- retrieval quality directly impacts answer quality

## ADR-005: Disclosed AI-Model Fallback for Weak Internal Evidence

### Decision

If internal evidence is not sufficiently relevant, do not force a KB-backed answer. Disclose the limitation and route the request to AI-model fallback guidance.

### Why

- irrelevant KB matches are misleading
- explicit disclosure preserves trust
- users still receive actionable best-effort guidance

### Tradeoff

- fallback guidance is less grounded in internal historical evidence

## ADR-006: LLM-as-Judge Plus Deterministic Guardrails

### Decision

Combine Pydantic validation, relevance gating, and judge-based validation.

### Why

- deterministic checks are cheap and reliable for basic API safety
- judge evaluation helps reduce hallucinations and weakly grounded responses

### Tradeoff

- adds latency and extra model cost on the answer path

## ADR-007: Modular Monolith for Current Delivery

### Decision

Implement the system as a modular monolith with explicit service boundaries.

### Why

- lower operational complexity
- easier local development and testing
- preserves clean boundaries for later extraction

### Tradeoff

- not independently deployable microservices yet

## ADR-008: In-Process Reranking and Guardrails

### Decision

Keep reranking and guardrail execution inside the FastAPI process.

### Why

- these sit on the hot path
- in-process execution lowers latency

### Tradeoff

- less independent scaling than a dedicated inference service

## ADR-009: Real 10K Incident Dataset Replaced Synthetic-First Flow

### Decision

Adopt the 10K dataset with native `description` and `resolution_notes` as the active corpus.

### Why

- real incident text materially improves retrieval quality and grounding
- removes dependency on synthetic resolution notes for the main path

### Tradeoff

- required schema migration and ingestion refactor

## ADR-010: Mongo-Backed Hashed Admin Auth

### Decision

Store admin users in MongoDB with hashed passwords.

### Why

- better than plaintext demo credentials in env
- supports signup, duplicate checks, and persistent auth state

### Tradeoff

- still lighter than production SSO / OIDC

## ADR-011: Real Connectivity Checks in Admin Diagnostics

### Decision

Admin diagnostics should report actual connectivity, not only whether config values exist.

### Why

- non-empty keys and URIs do not prove working integrations
- operational diagnostics must be truthful

### Tradeoff

- slight runtime overhead when diagnostics are refreshed

## ADR-012: Engineer-Focused UI Over Maximal Field Density

### Decision

Optimize the UI for scanability and clear operational signals.

### Why

- support engineers need quick interpretation
- redundant metadata reduces usability

### Tradeoff

- some low-signal fields moved out of the main workflow
