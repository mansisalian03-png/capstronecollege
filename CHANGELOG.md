# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Phase 8: CI/CD, Containerization, and Final Docs
  - Added GitHub Actions workflow (`.github/workflows/ci.yml`) to run linting and `pytest` on every push to main.
  - Added `Dockerfile` using `python:3.11-slim` to resolve native C-compiler constraints and install the full ML/GIS stack.
  - Added `docker-compose.yml` for unified one-command startup (FastAPI + Streamlit).
  - Wrote comprehensive documentation: Administrator Guide, User Guide, and Model/System Card.
  - Created a reproducible 5-minute video demo script (`docs/demo_script.md`).
- Phase 7: MLflow Tracking and Evaluation Dossier
  - Installed `mlflow-skinny` and wired it into `tests/test_evaluation_metrics.py`.
  - Automatically generated the evaluation dossier at `docs/evaluation.md`.
  - Added a security/PII-scrubber module to intercept sensitive scraped text.
  - Wrote a rapid-fire load test confirming the FastAPI ingestion route executes in <5ms per request.
- Phase 6: FastAPI Backend and UI
  - Built the `api/main.py` FastAPI backend utilizing `Pydantic` validation and Mock Auth.
  - Generated the `ui/app.py` Streamlit Analyst UI capable of interacting with the API.
  - Added comprehensive End-to-End integration tests (`tests/test_api_integration.py`).
- Phase 5: Graph Engine and Geospatial Scoring
  - Implemented `graph/engine.py` using `networkx` to traverse dependencies.
  - Implemented `scoring/score.py` to calculate exposure scores and explainable paths.
  - Implemented an audit logger (`audit_log.txt`).
  - Wrote comprehensive unit tests (`tests/test_graph_scoring.py`).
- Phase 4: NLP Event Extraction and Deduplication
  - Implemented `nlp/extract.py` featuring a `BaselineExtractor` and `NLPExtractor` (spaCy).
  - Implemented near-duplicate string clustering via `difflib`.
  - Added an evaluation script (`nlp/evaluate.py`).
- Phase 3: Ingestion and Filtering
  - Implemented feed ingestion module (`ingestion/ingest.py`) and relevance classifier (`ingestion/filter.py`).
- Phase 2: Design Pack
  - Created C4 component and sequence diagrams.
  - Defined PostgreSQL and NetworkX schemas, Threat Model, and Test Strategy.
- Phase 1: Data Layer setup.
  - Curated a synthetic news corpus and generated reproducible synthetic graph data.
- Phase 0: Project skeleton initialization.
  - Initialized directory structure, `requirements.txt`, and `.env.example`.
