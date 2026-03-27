# public-renewable-grid-resilience-auditor
Public-sector analytics capstone using DuckDB + Parquet to monitor renewable integration, grid resilience, and policy risk with free API data (ENTSO-E, Open-Meteo, Ember).

## Documentation
- Project documentation index: [docs/README.md](docs/README.md)
- System overview (brief): [docs/system-overview-brief.md](docs/system-overview-brief.md)
- System run commands and dashboard startup: [docs/system-run-commands-and-dashboard.md](docs/system-run-commands-and-dashboard.md)

## Command references
- Git commands: [docs/commands/git-commands.md](docs/commands/git-commands.md)
- Bash and shell commands: [docs/commands/bash-shell-commands.md](docs/commands/bash-shell-commands.md)
- Make commands: [docs/commands/make-commands.md](docs/commands/make-commands.md)

## One-click Startup
- Full run + dashboard script: [scripts/run_full_system_and_dashboard.sh](scripts/run_full_system_and_dashboard.sh)
- Desktop launcher file: [Launch-Public-Renewable-Grid-Dashboard.desktop](Launch-Public-Renewable-Grid-Dashboard.desktop)

## Quickstart (Phase 2 baseline)
1. Create and activate a Python virtual environment.
2. Install dependencies:
	- `make bootstrap`
3. Run checks:
	- `make check`
4. Run smoke check:
	- `make smoke`
5. Validate source contracts:
	- `make contracts`
6. Run mock Bronze ingestion jobs (Phase 4):
	- `make ingest-mock`
7. Run dbt staging quality gates (Phase 5):
	- `make dbt-staging`
8. Run intermediate harmonization quality gates (Phase 6):
	- `make dbt-intermediate`
9. Run dimensions/facts quality gates (Phase 7):
	- `make dbt-dimensions-facts`
10. Run Gold marts and scorecard quality gates (Phase 8):
	- `make dbt-marts`
11. Run baseline forecasting + scenario engine (Phase 9):
	- `make forecast-phase9`
12. Run dashboard narrative smoke validation (Phase 10):
	- `make dashboard-smoke`
13. Launch stakeholder dashboard (Phase 10):
	- `make dashboard-run`
14. Run orchestration and monitoring policy checks (Phase 11):
	- `make monitor-phase11`
15. Run late-arrival handling smoke check (post-Phase-12 hardening):
	- `make late-arrival-smoke`
16. Run security controls smoke check (post-Phase-12 hardening):
	- `make security-smoke`
17. Run performance benchmark smoke check (post-Phase-12 hardening):
	- `make benchmark-performance`

Notes:
- Bronze writes are idempotent by operation key (same request window + params will be skipped if already written).
- Live ENTSO-E ingestion requires `ENTSOE_API_KEY` in your local `.env`.

## Repository layout
- `data/`: Bronze/Silver/Gold storage roots
- `src/`: ingestion, cleaning, forecasting, monitoring, shared utilities
- `dbt/`: dbt-duckdb models and configs
- `airflow/`: orchestration DAGs
- `reports/dashboards/`: Streamlit and stakeholder-facing outputs

