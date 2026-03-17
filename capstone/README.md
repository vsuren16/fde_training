# AI-Powered Incident Knowledge Base Assistant

Production-shaped capstone for IT support incident retrieval, grounded resolution guidance, and observability-driven operations.

## Stack

- `FastAPI` for REST APIs
- `React` + CSS for the operator UI
- `MongoDB` as the system of record
- `ChromaDB` for vector retrieval
- `OpenAI SDK` for embeddings, generation, fallback guidance, and LLM-as-judge
- `LangSmith` for traceability

## What Is Implemented

### Requirement 1

- Basic RAG for incident similarity search
- Hybrid search: keyword + semantic retrieval
- Triage priority classification
- Metadata filtering by `category` and `team`
- Basic resolution suggestion grounded in retrieved incidents
- Input validation guardrails with Pydantic
- Output guardrails with judge-based downgrade behavior
- Simple ticket routing
- REST API endpoints for ingestion, search, feedback, health, and admin diagnostics
- Frontend for search, evidence review, triage, routing, and fallback disclosure

### Requirement 2 Vertical Slice

- Reranking by recency and historical success heuristics
- Predicted resolution time
- Fix confidence heuristic
- LLM-as-judge troubleshooting validation
- Token optimization for evidence selection
- Multi-tier handoff path such as `L1 -> L2 -> L3`
- A2A-style escalation messages
- Root cause summary
- Feedback loop endpoint and persistence
- DeepEval readiness hook

Current limitation:
- Requirement 2 is implemented as a working vertical slice, not as a fully autonomous multi-agent production platform.

## Active Dataset

The active ingestion path uses `backend/data/raw/it_incidents_10k.csv`.

This dataset includes real:

- `title`
- `description`
- `resolution_notes`
- `team`
- `status`
- `resolution_time_hours`

That replaced the older synthetic-resolution-heavy path and materially improved retrieval quality and answer grounding.

## Current Core Flow

1. Load and clean `it_incidents_10k.csv`.
2. Materialize `backend/data/processed/incidents_cleaned.csv`.
3. Replace canonical incidents in MongoDB.
4. Rebuild vector embeddings in ChromaDB when `OPENAI_API_KEY` is valid.
5. Warm the in-memory keyword index.
6. Run hybrid retrieval: keyword + semantic.
7. Rerank by retrieval score, recency, and success heuristics.
8. Generate grounded resolution guidance from retrieved evidence.
9. Validate the answer with LLM-as-judge or heuristic fallback.
10. If internal evidence is not sufficiently relevant, disclose that and route to an AI-model fallback response.
11. Return incidents, triage priority, route target, handoff path, RCA summary, metrics, and observability metadata.

## Guardrails

- Input guardrails:
  - query validation through Pydantic
  - length and quality validation
  - metadata filter validation
- Retrieval guardrails:
  - internal evidence relevance gate before trusting retrieved incidents
- Output guardrails:
  - LLM-as-judge for grounding and troubleshooting relevance
  - downgrade to conservative evidence-backed fallback when grounding is weak
  - explicit disclosure when the system routes to an AI-model fallback

## Admin / Observability

The Admin panel includes:

- Mongo-backed admin auth with hashed passwords
- Signup/login flow
- LangSmith project link
- Downloadable rotating log file
- Real connectivity diagnostics for:
  - MongoDB
  - LangSmith
  - ChromaDB
  - OpenAI

Connectivity status is based on real checks, not only whether a key or URI exists in config.

## Project Layout

- `backend/`: FastAPI service, ingestion, adapters, repositories, evaluation, admin routes
- `frontend/`: React UI for search, insights, and admin diagnostics
- `docs/`: architecture, data flow, and architectural decisions

## Run Locally

### Prerequisites

- Python 3.10+
- Node.js 20+
- Local MongoDB on `mongodb://localhost:27017`
- Optional but recommended:
  - valid `OPENAI_API_KEY`
  - valid `LANGSMITH_API_KEY`

### Backend

1. Open a terminal in `capstone/backend`
2. Create a virtual environment:
   - `python -m venv .venv`
3. Activate it:
   - `.\.venv\Scripts\activate`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Create `.env` from `.env.example`
6. Start the backend:
   - `uvicorn app.main:app --reload --port 8010`

### Frontend

1. Open a second terminal in `capstone/frontend`
2. Install dependencies:
   - `npm install`
3. Start the UI:
   - `npm run dev`

### First Use

1. Start MongoDB locally.
2. Start backend and frontend.
3. Open the UI.
4. If the dataset is not initialized yet, click `Initialize Dataset`.
5. Run a natural-language incident query.

## Notes

- Without a valid OpenAI key, semantic retrieval and generation degrade gracefully.
- With a valid OpenAI key, the system supports embeddings, grounded summaries, AI-model fallback guidance, and judge evaluation.
- Logs are written to `backend/logs/application.log` with rotation.
- The main workflow favors free-text search with focused metadata filters for `category` and `team`.
- Admin credentials are no longer stored as demo defaults in the codebase.
