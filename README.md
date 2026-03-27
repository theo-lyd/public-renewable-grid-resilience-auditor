# public-renewable-grid-resilience-auditor
Public-sector analytics capstone using DuckDB + Parquet to monitor renewable integration, grid resilience, and policy risk with free API data (ENTSO-E, Open-Meteo, Ember).

## Documentation
- Project documentation index: [docs/README.md](docs/README.md)

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

Notes:
- Bronze writes are idempotent by operation key (same request window + params will be skipped if already written).
- Live ENTSO-E ingestion requires `ENTSOE_API_KEY` in your local `.env`.

## Repository layout
- `data/`: Bronze/Silver/Gold storage roots
- `src/`: ingestion, cleaning, forecasting, monitoring, shared utilities
- `dbt/`: dbt-duckdb models and configs
- `airflow/`: orchestration DAGs
- `reports/dashboards/`: Streamlit and stakeholder-facing outputs

