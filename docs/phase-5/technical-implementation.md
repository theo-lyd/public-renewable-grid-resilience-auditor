# Phase 5 — Technical Implementation Document

## 1) Objective(s)
1. Build dbt staging models from Bronze outputs.
2. Enforce schema and quality tests at staging layer.
3. Implement source freshness gates based on ingestion metadata.

## 2) Deliverable(s)
- Staging dbt models for source datasets and ingestion metadata
- dbt schema tests and singular quality tests
- Freshness gate model and assertion test
- dbt execution automation targets in Makefile
- Phase 5 documentation

## 3) What was implemented
- Added source staging models under `dbt/models/staging/sources/`.
- Added ingestion metadata staging model used for freshness checks.
- Added `stg_source_freshness_gate` model for timeliness enforcement.
- Added schema and singular tests under `dbt/models/staging/` and `dbt/tests/`.
- Added local dbt profile (`dbt/profiles.yml`) and Makefile dbt targets.

## 4) How it was implemented
1. Mapped each Bronze dataset to a typed staging model.
2. Added deterministic `record_id` fields for uniqueness tests.
3. Added rule-based singular tests for value-range and non-negative checks.
4. Built freshness gate from Bronze metadata with source-specific thresholds.
5. Integrated dbt build/test commands into project automation.

## 5) Exact commands run
Commands executed during Phase 5 implementation and validation are recorded below.

```bash
make check PYTHON=.venv/bin/python && make contracts PYTHON=.venv/bin/python && make dbt-staging PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python && make contracts PYTHON=.venv/bin/python && make dbt-staging PYTHON=.venv/bin/python
make dbt-staging PYTHON=.venv/bin/python
make ingest-mock PYTHON=.venv/bin/python && make dbt-staging PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python && make contracts PYTHON=.venv/bin/python
```

## 6) Files created/updated

### Created
- `dbt/profiles.yml`
- `dbt/models/staging/sources/stg_open_meteo_weather.sql`
- `dbt/models/staging/sources/stg_ember_generation_mix.sql`
- `dbt/models/staging/sources/stg_entsoe_generation.sql`
- `dbt/models/staging/sources/stg_ingestion_metadata.sql`
- `dbt/models/staging/sources/schema.yml`
- `dbt/models/staging/stg_source_freshness_gate.sql`
- `dbt/models/staging/schema.yml`
- `dbt/tests/test_entsoe_generation_non_negative.sql`
- `dbt/tests/test_ember_generation_non_negative.sql`
- `dbt/tests/test_open_meteo_wind_speed_range.sql`
- `dbt/tests/test_source_freshness_gate.sql`
- `docs/phase-5/staging-models-and-quality-gates.md`
- `docs/phase-5/technical-implementation.md`

### Updated
- `.gitignore`
- `Makefile`
- `README.md`
- `docs/README.md`
- `dbt/profiles.yml.example`
- `dbt/models/staging/sources/stg_open_meteo_weather.sql`
- `dbt/models/staging/sources/stg_ember_generation_mix.sql`
- `dbt/models/staging/sources/stg_entsoe_generation.sql`
- `dbt/models/staging/sources/stg_ingestion_metadata.sql`
- `dbt/models/staging/sources/schema.yml`

## 7) Validation outcomes
- Final validation status:
	- `make check`: passed
	- `make contracts`: passed
	- `make dbt-staging`: passed (`dbt build` + `dbt test`)
- dbt staging execution summary:
	- 5 staging models built
	- 32 data tests + 4 singular tests passed

## 8) Output state
- Phase 5 staging layer and quality gates are implemented and executable.

## 9) Requirement-to-reality gap log
- **Potential gap:** dbt staging models read local Bronze parquet files; if Bronze is absent, dbt build cannot materialize source staging.
- **Minimal viable path:** run `make ingest-mock` before `make dbt-staging` in local/dev environments.

## 10) Problems encountered and resolution log

### Problem P5-01: dbt invocation failed via `python -m dbt`
- **Where observed:** `make dbt-staging`
- **Root cause:** Installed dbt package does not expose runnable `dbt.__main__` module in this environment.
- **Possible implications if unresolved:**
	1. dbt build/test commands cannot run from automation.
	2. Phase 5 quality gates cannot be validated.
- **Resolution applied:**
	1. Updated Makefile to call dbt CLI executable directly (`$(dir $(PYTHON))dbt`).
	2. Re-ran dbt staging commands successfully.
- **Final status:** Resolved.

### Problem P5-02: DuckDB path resolved outside repository
- **Where observed:** dbt connection initialization
- **Root cause:** `dbt/profiles.yml` used `../data/...`, which resolved to `/workspaces/data/...` in this execution context.
- **Possible implications if unresolved:**
	1. dbt cannot open/create target DuckDB file.
	2. Staging models and tests never execute.
- **Resolution applied:**
	1. Updated profile path to `data/processed/grid_resilience.duckdb`.
	2. Synced `profiles.yml.example` with same path behavior.
- **Final status:** Resolved.

### Problem P5-03: Parquet schema mismatch in staging model globs
- **Where observed:** dbt tests for staging models
- **Root cause:** Data model globs (`op_*.parquet`) also matched metadata files (`op_*_metadata.parquet`) with different schemas.
- **Possible implications if unresolved:**
	1. Staging models fail intermittently at runtime.
	2. Quality tests produce false negatives due to schema collisions.
- **Resolution applied:**
	1. Enabled `union_by_name=true` and `filename=true` in data staging models.
	2. Added `where filename not like '%_metadata.parquet'` to keep only data files.
	3. Re-ran dbt staging build/tests successfully.
- **Final status:** Resolved.

### Problem P5-04: Missing Bronze files before dbt staging execution
- **Where observed:** initial dbt run in environments without complete Bronze sample files.
- **Root cause:** Phase 5 staging models depend on existing Bronze parquet artifacts.
- **Possible implications if unresolved:**
	1. dbt staging cannot materialize source views.
	2. Teams may interpret failures as model bugs instead of missing inputs.
- **Resolution applied:**
	1. Executed `make ingest-mock` before `make dbt-staging`.
	2. Documented this dependency in phase docs as minimal viable path.
- **Final status:** Resolved.
