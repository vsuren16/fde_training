# AI Commerce Platform (Senior+ Checklist Aligned)

This repository is currently implemented for **Milestone 1** with production-grade engineering scaffolding for future milestones.

## Repository Structure
- `requirements/`: original requirements, checklist mapping
- `docs/architecture/`: system architecture and POC-vs-production boundaries
- `docs/data-flow/`: ingestion/retrieval logic flows
- `docs/decisions/`: ADRs and trade-off decisions
- `docs/evaluation/`: methodology, ground-truth, metrics summaries
- `docs/stakeholder/`: stakeholder PPT source content
- `src/`: production implementation modules by domain (`inventory_pipeline`, `common`, `ai`)
- `data-engineering/inventory_pipeline/`: ingestion entrypoint
- `tests/`: unit, integration, performance suites

## Current Runtime Scope
Implemented now:
- Local MongoDB
- PySpark ingestion pipeline (mock in-script raw data: 20 records)
- Structured logging and artifact outputs

Scaffold only:
- M2, M3, M4 service behavior

## Local Setup (No Docker)
1. Install MongoDB Community Edition and start it locally (`mongodb://localhost:27017`).
2. Create and activate a Python venv.
3. Install dependencies:
```bash
pip install -r requirements-dev.txt
pip install -r data-engineering/inventory_pipeline/requirements.txt
```
4. Set environment variables (recommended: copy from `.env.example` into your shell/session).

## Environment Profiles (Parameterized)
- `ENVIRONMENT=dev` or `ENVIRONMENT=prod`
- Resolution order for each setting:
  - `<KEY>_<ENV>` (for example `MONGO_URI_PROD`)
  - `<KEY>`
  - internal default

Keys used by ingestion:
- `MONGO_URI`
- `MONGO_DB`
- `INVENTORY_LOG_DIR`

## Run Ingestion
```bash
python data-engineering/inventory_pipeline/spark_job.py
```
Optional:
```bash
python data-engineering/inventory_pipeline/spark_job.py --environment prod --run-id demo_run_001 --output-log-dir data-engineering/inventory_pipeline/logs
```

## Verify Results
```bash
mongosh --eval "db.getSiblingDB('ai_commerce').inventory.countDocuments()"
```

## Generated Artifacts
- `data-engineering/inventory_pipeline/logs/execution_log_<run_id>.json`
- `data-engineering/inventory_pipeline/logs/invalid_records_<run_id>.json/part-*.json`

## Testing
```bash
python -m pytest -q
```

Performance/load script (future service runtime):
- `tests/performance/locustfile.py`

## Documentation Index
- Architecture: `docs/architecture/system_architecture.md`
- Data flow: `docs/data-flow/ingestion_flow.md`
- Decisions: `docs/decisions/DECISIONS.md`
- Evaluation: `docs/evaluation/accuracy_methodology.md`
- Stakeholder deck source: `docs/stakeholder/stakeholder_briefing_ppt.md`
