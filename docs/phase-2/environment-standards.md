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

## Dependency strategy Q&A (for project defense)

### Q1) Why are there multiple requirements files?
We separate dependencies by purpose to reduce conflicts and make installs predictable:
- `requirements.txt`: core runtime stack (pipeline + data + app dependencies).
- `requirements-dev.txt`: core runtime plus developer tooling (pytest, ruff, black).
- `requirements-orchestration.txt`: orchestration-only stack (Airflow), installed when needed.

This keeps the base environment lean while still supporting full engineering quality gates.

### Q2) Was choosing `requirements.txt` during venv creation correct for Phase 4?
It was a valid choice for running core application code, but not sufficient for Phase 4 quality checks.

Reason:
- `requirements.txt` does not include dev tools (`pytest`, `ruff`, `black`).
- Phase 4 execution required running `make check`, which depends on those tools.

For Phase 4, the best choice is `requirements-dev.txt` (or `make bootstrap`, which installs it).

### Q3) What does each requirements file stand for?
- `requirements.txt` → production/core runtime dependencies.
- `requirements-dev.txt` → development and CI quality dependencies.
- `requirements-orchestration.txt` → optional Airflow dependencies for orchestration phases.

### Q4) How does this differ from using one file across multiple environments?
Your approach (single file + separate environments) works, but has trade-offs:
- Pros: simpler conceptually, one dependency list to remember.
- Cons: tool bloat in all envs, higher conflict risk, slower installs, less clear ownership of dependencies.

Current repository approach (layered requirements) improves this by:
1. **Clarity:** dependency intent is explicit by environment purpose.
2. **Stability:** Airflow is isolated from day-to-day analytics/dev tooling.
3. **Speed:** faster installs for non-orchestration tasks.
4. **CI alignment:** exact tooling used in checks is pinned in dev requirements.

For this capstone, layered requirements are better for reproducibility, reviewer confidence, and maintenance.

### Q5) Should we also use `.devcontainer` and separate environments for Airflow?
Yes, both are good practice for this project.

- `.devcontainer` benefits:
	- consistent tooling across machines,
	- fewer "works on my machine" issues,
	- easier onboarding and demo reproducibility.

- Separate Airflow environment benefits:
	- avoids package conflicts with analytics stack,
	- safer upgrades,
	- cleaner troubleshooting.

Practical recommendation for this repository:
1. Keep layered requirements (already implemented).
2. Use one primary project venv for core + dev (`requirements-dev.txt`).
3. Use a separate Airflow environment (or container service) when orchestration phase work starts.
4. Add `.devcontainer` in a future phase to lock full runtime reproducibility for defense/demo.
