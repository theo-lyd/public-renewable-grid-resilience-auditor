# Phase 2 — Environment and Standards

## Objective(s)
1. Establish a reproducible development baseline.
2. Standardize project structure for DuckDB + Parquet architecture.
3. Define coding, testing, and execution conventions for all future phases.

## Deliverable(s)
- Python environment and dependency manifests
- `.env.example` for configuration policy
- `Makefile` automation commands
- CI workflow for lint/test
- Source/data/dbt/orchestration scaffold

## Environment standards
- **Python version:** 3.11+
- **Core storage:** DuckDB + Parquet
- **Config management:** `.env` values loaded from `.env.example` template
- **Project entry commands:** `make bootstrap`, `make check`, `make smoke`

## Data standards
- Bronze path: `data/raw/parquet`
- Processed path: `data/processed/parquet`
- Reference path: `data/reference`
- DuckDB file path: `data/processed/grid_resilience.duckdb`

## Code quality standards
- Formatting: Black
- Linting: Ruff
- Testing: Pytest
- CI gate: lint + test on push and pull request

## Orchestration standard (MVP)
- Airflow dependency is separated in `requirements-orchestration.txt`.
- A DAG placeholder exists to formalize dependency flow before full implementation.
