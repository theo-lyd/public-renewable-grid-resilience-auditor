# System Overview (Brief)

This system is a local-first data engineering and analytics pipeline for public renewable-grid monitoring.

## How it works, briefly
1. It ingests public-source data (weather, generation, and grid-related feeds) into raw storage using contract-checked ingestion jobs.
2. It transforms data through layered modeling (staging -> harmonized intermediate -> dimensions/facts -> KPI marts) using dbt on DuckDB/Parquet.
3. It computes resilience and renewable KPIs, then runs simple forecasting/scenario logic for short-horizon outlooks.
4. It exposes results in a dashboard plus monitoring checks, so you can validate data quality, pipeline health, and stakeholder-facing metrics.
5. It is operated through standardized Make commands, so setup, validation, and runs are reproducible locally and in CI.

In short: ingest trusted public data, normalize/model it, calculate KPIs + forecasts, then present and monitor everything in a repeatable workflow.
