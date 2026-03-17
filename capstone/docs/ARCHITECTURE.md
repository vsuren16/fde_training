# Architecture

## Intent

This document describes the software architecture, not the step-by-step data movement. Data flow is documented separately in `DATA_FLOW.md`.

## POC vs Production

### Current Implementation

- React frontend served independently
- Single FastAPI deployable with clear internal service boundaries
- MongoDB as canonical store
- ChromaDB as vector retrieval store
- OpenAI SDK for embeddings, generation, fallback guidance, and judging
- LangSmith plus rotating structured logs for observability

### Production Shape

- API Gateway for auth, edge policy, and rate limiting
- Load Balancer in front of stateless FastAPI replicas
- Kubernetes deployment for horizontal scaling
- Managed MongoDB
- Persistent Chroma or swappable managed vector backend
- Optional async workers for ingestion, indexing, and evaluation jobs
- Centralized metrics, logging, and tracing stack

## Logical Layers

### User Layer

- Support engineer
- Admin / observability user

### Frontend Layer

- React search interface
- Retrieved evidence panel
- Resolution insights panel
- Admin / observability panel

### API Layer

- FastAPI routes
- Pydantic request/response validation
- Health and readiness endpoints
- Admin auth endpoints

### AI Orchestration Layer

- Hybrid retrieval
- Reranking
- Triage classification
- Routing
- Resolution generation
- AI-model fallback generation
- LLM-as-judge evaluation
- Troubleshooting validation
- Root cause analysis
- Agent handoff orchestration
- Feedback capture

### Data Access Layer

- Mongo repositories
- Chroma adapter
- OpenAI adapter

### Platform Layer

- Structured logging
- Rotating file logs
- LangSmith tracing
- Runtime diagnostics
- Startup warmup
- Connectivity health checks

## Architectural Boundaries

### MongoDB

Stores:

- incident documents
- admin users with hashed passwords
- feedback records

MongoDB is the source of truth.

### ChromaDB

Stores:

- incident embeddings
- retrieval metadata used by semantic search

ChromaDB is a derived index, not the source of truth.

### OpenAI

Used for:

- embeddings
- grounded resolution summaries
- AI-model fallback guidance when internal evidence is insufficient
- LLM-as-judge evaluation

### LangSmith

Used for:

- tracing retrieval, generation, and judge flows
- debugging model-path behavior

## Decoupling Principles

- The vector layer is abstracted so ChromaDB can later be replaced without rewriting API handlers.
- Repositories isolate Mongo operations from orchestration logic.
- OpenAI calls are isolated behind an adapter.
- The backend is modular even though it is not yet deployed as separate microservices.

## Scalability Position

The current codebase is a modular monolith. That is intentional.

Why:

- lower delivery complexity
- easier testing and local debugging
- preserves clean service boundaries without premature distributed overhead

Production evolution path:

- split ingestion/indexing workers if throughput grows
- externalize heavy inference workloads if needed
- move store synchronization toward CDC plus task queue
