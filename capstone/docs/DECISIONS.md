# Architectural Decision Records

## ADR-001: FastAPI for the Backend API

### Decision

Use `FastAPI` as the backend framework.

### Why

- Native async support for I/O-heavy workloads
- Strong Pydantic validation for API contracts
- Good fit for stateless, containerized services
- Faster iteration than a heavier Java stack for this capstone

### Tradeoffs

- Less enterprise convention than Spring Boot
- Team members from Java-heavy environments may prefer Spring ecosystems

### Why not Spring Boot

Spring Boot is viable, but the project already requires Python for OpenAI, ChromaDB, evaluation logic, and data processing. Keeping the AI and API layers in the same language lowers complexity and reduces cross-service overhead for Requirement 1.

## ADR-002: MongoDB + ChromaDB Split

### Decision

Use MongoDB for canonical incident documents and ChromaDB for vector search.

### Why

- Clean separation between source-of-truth data and vector search concerns
- Fits the user constraint directly
- Keeps metadata filtering and document lifecycle management straightforward

### Tradeoffs

- Dual-write complexity during ingestion
- Requires consistency checks between document and vector stores

## ADR-003: Derived Retrieval Text from Structured Data

### Decision

Construct incident search text from available structured columns because the provided dataset lacks `description` and `resolution_notes`.

### Why

- Allows Requirement 1 retrieval to proceed with the available dataset
- Preserves a path to better retrieval once real incident text is available

### Tradeoffs

- Lower semantic richness than true free-text tickets
- Resolution suggestions will be more constrained and should be presented with clear confidence language

## ADR-006: Synthetic Resolution Notes with Provenance

### Decision

Generate a `synthetic_resolution` field for the ITSM dataset using deterministic templates seeded by the smaller resolution dataset.

### Why

- The large ITSM dataset has scale and metadata but lacks explicit resolution text
- The 150-row dataset has solution text but is too small and repetitive to use as the primary incident corpus
- A synthetic field enables Requirement 1 RAG and UI demonstrations while preserving a clean upgrade path to real resolution notes later

### Tradeoffs

- Synthetic resolutions are useful for guidance, not for final truth claims
- Evaluation results must distinguish between real evidence and generated enrichment

## ADR-004: Modular Monolith for Requirement 1

### Decision

Implement Requirement 1 as a modular monolith with explicit service boundaries.

### Why

- Faster to deliver and test
- Avoids premature distributed-system complexity
- Keeps architecture ready for later extraction into microservices

### Tradeoffs

- Not a true independently deployed microservice fleet on day one
- Requires discipline in package boundaries to avoid drift into a monolith blob

## ADR-005: ChromaDB Behind an Abstraction

### Decision

Hide vector search behind a repository interface.

### Why

- Enables future swap to FAISS, Milvus, pgvector, or managed vector backends
- Keeps orchestration logic independent from store-specific APIs

### Tradeoffs

- Slightly more upfront abstraction cost
- Some backend-specific features may need adapter-specific extensions later

## ADR-007: Conservative Degraded Mode for Slow or Weak LLM Paths

### Decision

Use degraded fallback summaries when OpenAI calls fail, time out, or judge confidence is weak.

### Why

- Prevents hallucinated or weakly grounded troubleshooting advice
- Keeps the UI responsive enough for support workflows
- Makes system behavior explicit instead of silently returning low-confidence answers

### Tradeoffs

- Some answers become less polished
- The system may be conservative and downgrade responses that are partly acceptable

## ADR-008: Route Target Should Align With Final Handoff Stage

### Decision

Set `route_to` to the final stage of the computed handoff path.

### Why

- Avoids conflicting UI signals between route recommendation and handoff chain
- Better matches how support teams think about escalation ownership

### Tradeoffs

- Loses the distinction between immediate receiver and eventual owner unless both are displayed
