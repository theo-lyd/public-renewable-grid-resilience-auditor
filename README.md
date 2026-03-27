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

## Repository layout
- `data/`: Bronze/Silver/Gold storage roots
- `src/`: ingestion, cleaning, forecasting, monitoring, shared utilities
- `dbt/`: dbt-duckdb models and configs
- `airflow/`: orchestration DAGs
- `reports/dashboards/`: Streamlit and stakeholder-facing outputs

