# Milestone Boundary

## Implemented Now
- Milestone 1 only: inventory ingestion pipeline using PySpark mock data + MongoDB.

## Scaffold Only (Not Implemented)
- Milestone 2: Core microservices (Auth, Product, Cart, Order)
- Milestone 3: Semantic search embedding and similarity APIs
- Milestone 4: LLM Ops versioning, monitoring, redeployment controls

## Runtime Enforcement
- Local runtime only (no Docker process required).
- Start local MongoDB, then run Spark ingestion directly via Python.
- Future service apps are placeholders and return `501 Not Implemented in Milestone 1`.

## Submission Intent
This repository state is prepared for grading Milestone 1 while keeping a clean and explicit upgrade path for Milestones 2–4.
