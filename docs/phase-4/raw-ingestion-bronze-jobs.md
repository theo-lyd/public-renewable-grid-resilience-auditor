# Phase 4 — Raw Ingestion Jobs (API to Bronze Parquet)

## Objective(s)
1. Implement source ingestion jobs that fetch raw data from APIs.
2. Land raw payload records in Bronze Parquet partitions.
3. Enforce idempotent writes and run-level metadata capture.
4. Add retry/backoff handling for transient API failures.

## Deliverable(s)
- Retry-enabled HTTP client layer
- Source fetchers for Open-Meteo, Ember, ENTSO-E
- Idempotent Bronze writer with metadata Parquet
- CLI ingestion runner and Makefile targets
- Tests for idempotency, retries, and mock-source ingestion

## Ingestion design summary
- **Ingestion mode:** Batch pull from API endpoints.
- **Bronze output path:** `data/raw/parquet/source=<source>/endpoint=<endpoint>/ingestion_date=<date>/`
- **Data file naming:** `op_<operation_key>.parquet`
- **Metadata file naming:** `op_<operation_key>_metadata.parquet`

## Idempotency policy
Each ingestion operation computes a deterministic `operation_key` from:
1. source ID,
2. endpoint ID,
3. window start/end,
4. request parameters.

If both data and metadata files for the operation key already exist, the write is skipped with status `skipped_existing`.

## Metadata captured per run
- `run_id`
- `operation_key`
- `source_id`
- `endpoint_id`
- `requested_at_utc`
- `window_start_utc`
- `window_end_utc`
- `request_params_json`
- `record_count`
- `status`

## Retry/backoff policy
- HTTP client uses retry-enabled session adapters.
- Retries apply to transient status codes (`429`, `500`, `502`, `503`, `504`).
- Exponential-style backoff is configured via `backoff_factor`.

## Operational commands
- Validate quality gates: `make check`
- Validate contracts: `make contracts`
- Run mock ingestion batch: `make ingest-mock`

## Live ingestion note
- ENTSO-E live calls require `ENTSOE_API_KEY`.
- Mock fixtures are included for deterministic local and CI validation.
