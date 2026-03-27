# Phase 5 — Staging Models and Quality Gates

## Objective(s)
1. Implement dbt staging models over Bronze Parquet ingestion outputs.
2. Add schema/data tests for core field integrity and value quality.
3. Add source freshness gates using ingestion metadata timeliness checks.

## Deliverable(s)
- Staging models for ENTSO-E, Open-Meteo, Ember, and ingestion metadata
- dbt schema tests (`not_null`, `unique`, `accepted_values`)
- Singular dbt tests for value ranges and freshness-gate enforcement
- dbt staging build/test automation commands

## Design choices

### Why stage from Bronze Parquet directly?
Phase 4 already lands idempotent Bronze files with metadata. Reading those files in dbt creates a clean bridge from ingestion to model-driven quality enforcement.

### Why freshness gate model (instead of only source freshness command)?
In this DuckDB + Parquet setup, freshness logic is derived from Bronze metadata sidecars. Modeling freshness in dbt gives explicit, testable, and explainable freshness logic at source-endpoint granularity.

### What quality rules are enforced now?
- Structural integrity: required key fields are non-null.
- Row-level uniqueness: deterministic record IDs are unique.
- Domain validity:
  - ENTSO-E generation is non-negative,
  - Ember generation is non-negative,
  - Open-Meteo wind values remain in accepted bounds.
- Timeliness: source freshness gate fails if lag exceeds threshold by source/endpoint.

## Operational commands
- Prepare Bronze sample inputs (local/dev): `make ingest-mock`
- Build + test staging layer: `make dbt-staging`
- Direct build command: `make dbt-build-staging`
- Direct test command: `make dbt-test-staging`

## Notes for stakeholders
- This phase turns raw ingestion into auditable staging quality controls.
- It reduces downstream risk before harmonization and marts work in later phases.
