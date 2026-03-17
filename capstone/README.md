# AI-Powered Incident Knowledge Base Assistant

Production-oriented capstone for an IT support incident retrieval assistant built with:

- `FastAPI` for REST APIs
- `React` + CSS for the operator UI
- `MongoDB` for incident documents and operational metadata
- `ChromaDB` for vector storage
- `OpenAI SDK` for embeddings and generation
- `LangSmith` for tracing and observability

## Scope

This repository is intentionally structured for `Requirement 1` while preserving clean extension points for `Requirement 2`.

Implemented:

- Modular backend/frontend layout
- Canonical incident schema and cleansing pipeline
- Production-ready logging/configuration foundations
- API boundaries for health, ingestion, and search
- Native-resolution ingestion from a 10K incident dataset with real descriptions and resolution notes
- Architecture, data flow, and ADR documentation
- UI connected to ingestion and search APIs
- Requirement 2 scaffold for reranking, custom metrics, agent handoff, RCA, feedback, and DeepEval readiness
- Judge transparency in the UI and persistent rotating JSON logs
- Admin / Observability panel with backend-validated login and gated diagnostics links

## Active Dataset

The active ingestion path now uses `it_incidents_10k.csv`, which includes native `description` and `resolution_notes` fields. That removes the earlier dependency on synthetic resolution generation and gives the retrieval stack substantially better grounding.

The older ITSM + seed-template path is no longer the primary flow.

## Project Layout

- `backend/`: FastAPI service, ingestion pipeline, adapters, repositories, evaluation hooks
- `frontend/`: React application for search, triage, and incident review
- `docs/`: architecture, data flow, ADRs, and scaling notes

## Why Both MongoDB and ChromaDB

- `MongoDB` stores the canonical cleaned incident document, metadata, provenance, and future feedback/evaluation data.
- `ChromaDB` stores embeddings for semantic retrieval.

Keeping both is still the right design because vector search alone is a poor source of truth, while MongoDB alone is weaker for dense semantic search at Requirement 1 scale.

## Current Core Flow

1. Clean `it_incidents_10k.csv`.
2. Materialize native incident text and resolution evidence.
3. Materialize `backend/data/processed/incidents_cleaned.csv`.
4. Load incidents into MongoDB.
5. Build Chroma vectors when `OPENAI_API_KEY` is configured.
6. Run hybrid retrieval:
   keyword search in memory + semantic retrieval in Chroma.
7. Rerank incidents using retrieval score, recency, and resolution-success heuristics.
8. Validate the generated answer with LLM-as-judge or heuristic fallback.
9. Return triage, route target, handoff path, RCA summary, custom metrics, and grounded resolution guidance.

## Requirement 2 Extensions

- Reranking by recency and historical resolution-success heuristics
- Predicted resolution time and fix-accuracy metrics
- LLM-as-judge validation for troubleshooting steps
- Token-optimized evidence selection for judge and resolution calls
- Multi-tier handoff path such as `L1 -> L2 -> L3`
- Agent-to-agent context messages for specialist escalation
- Root cause summary generated from retrieved evidence and handoff context
- Feedback endpoint for continuous improvement data capture
- DeepEval readiness endpoint for benchmark integration

Current limitation:
- these Requirement 2 features are implemented as a working vertical slice, not a full autonomous multi-agent production platform yet

## Run Locally

### Prerequisites

- Python 3.10+
- Node.js 20+
- Local MongoDB running on `mongodb://localhost:27017`
- Optional: OpenAI API key for embeddings and LLM summaries

### Backend

1. Open a terminal in [backend](/c:/Users/Administrator/Documents/GenAI%20Training/capstone/backend).
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   `.\.venv\Scripts\activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Create `.env` from [.env.example](/c:/Users/Administrator/Documents/GenAI%20Training/capstone/backend/.env.example).
6. Start the API:
   `uvicorn app.main:app --reload --port 8010`

### Frontend

1. Open a second terminal in [frontend](/c:/Users/Administrator/Documents/GenAI%20Training/capstone/frontend).
2. Install dependencies:
   `npm install`
3. Start the UI:
   `npm run dev`

### First Use

1. Start MongoDB locally.
2. Start the backend.
3. Start the frontend.
4. If the dataset is not initialized yet, click `Initialize dataset`.
5. Run a natural-language search query.

## Notes

- Without `OPENAI_API_KEY`, the system still works in degraded mode using keyword retrieval and heuristic resolution guidance.
- With `OPENAI_API_KEY`, the system adds OpenAI embeddings for Chroma semantic retrieval, LLM-based resolution summaries, and OpenAI-backed judge validation.
- Structured JSON logs are written to `backend/logs/application.log` by default, with rotation.
- The main user workflow now favors free-text search; metadata filters are still supported by the backend but are no longer central to the UI workflow.
- Admin credentials can be supplied through `.env` for local/demo use. This is acceptable for development and demos, but not sufficient as a production-grade authentication strategy on its own.
