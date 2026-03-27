# Phase 7 — Technical Implementation Document

## 1) Objective(s)
1. Implement reusable dimensions with explicit surrogate keys.
2. Implement governed fact tables with fixed analytical grain.
3. Enforce referential integrity and mapping-drift controls before Gold mart build-out.

## 2) Deliverable(s)
- Dimension models (`dim_time_hourly`, `dim_zone`, `dim_fuel_category`, `dim_source_system`)
- Fact models (`fct_zone_hour_resilience_inputs`, `fct_zone_hour_fuel_generation`)
- dbt schema tests and singular tests for dimensions/facts
- Makefile automation for dimensions/facts validation
- Phase 7 implementation documentation

## 3) What was implemented
- Added four dimension models and two fact models in dbt.
- Added dimension and fact schema definitions with key and relationship tests.
- Added singular tests to enforce:
  - no unmapped zones in `dim_zone`
  - fact-to-conformed grain alignment
- Added new Make target `dbt-dimensions-facts`.

## 4) How it was implemented
1. Derived dimensions from intermediate harmonized models to avoid source-level ambiguity.
2. Used deterministic hash surrogate keys for consistent joins.
3. Built facts at explicitly defined grains and joined dimensions by business keys.
4. Added dbt tests for uniqueness, not-null, accepted-values, and relationships.
5. Added singular guardrails for mapping drift and grain integrity.

## 5) Exact commands run
Commands executed during Phase 7 implementation and validation are recorded below.

```bash
make check PYTHON=.venv/bin/python && make contracts PYTHON=.venv/bin/python && make ingest-mock PYTHON=.venv/bin/python && make dbt-staging PYTHON=.venv/bin/python && make dbt-intermediate PYTHON=.venv/bin/python && make dbt-dimensions-facts PYTHON=.venv/bin/python
```

## 6) Files created/updated

### Created
- `dbt/models/dimensions/dim_time_hourly.sql`
- `dbt/models/dimensions/dim_zone.sql`
- `dbt/models/dimensions/dim_fuel_category.sql`
- `dbt/models/dimensions/dim_source_system.sql`
- `dbt/models/dimensions/schema.yml`
- `dbt/models/facts/fct_zone_hour_resilience_inputs.sql`
- `dbt/models/facts/fct_zone_hour_fuel_generation.sql`
- `dbt/models/facts/schema.yml`
- `dbt/tests/test_dim_zone_no_unmapped.sql`
- `dbt/tests/test_fact_zone_hour_alignment.sql`
- `docs/phase-7/dimensions-and-facts-modeling.md`
- `docs/phase-7/technical-implementation.md`

### Updated
- `Makefile`
- `README.md`
- `docs/README.md`

## 7) Validation outcomes
- Final validation status:
  - `make check`: passed
  - `make contracts`: passed
  - `make ingest-mock`: passed (`skipped_existing` for all three mock ingestions)
  - `make dbt-staging`: passed
  - `make dbt-intermediate`: passed
  - `make dbt-dimensions-facts`: passed
- dbt dimensions/facts execution summary:
  - 4 dimensions built
  - 2 facts built
  - 40 dimensions/facts tests passed in targeted run

## 8) Output state
- Dimensions/facts layer is implemented and ready for validation.

## 9) Requirement-to-reality gap log
- Potential gap: zone mapping is seed-driven and currently requires manual expansion as new zones appear.
- Minimal viable path: keep fail-fast test active and update mapping seed before promoting new data domains.

## 10) Problems encountered and resolution log

### Problem P7-01: Intermediate build attempted fact-layer singular test
- **Where observed:** during `make dbt-intermediate` in combined validation chain
- **Root cause:** new `test_fact_zone_hour_alignment` matched selection graph while building only intermediate resources
- **Possible implications:** Phase 6 validation could fail because a Phase 7-only test references `fct_zone_hour_resilience_inputs`, which does not exist during intermediate-only execution
- **Resolution applied:** updated `dbt-build-intermediate` target to exclude Phase 7 singular tests (`--exclude test_dim_* test_fact_*`)
- **Final status:** resolved; intermediate target runs independently again.

### Problem P7-02: Phase 7 test selector returned no nodes
- **Where observed:** initial `make dbt-dimensions-facts` run, dbt message “Nothing to do” for test step
- **Root cause:** comma-separated selection string in `dbt-test-dimensions-facts` was not interpreted as valid node selection
- **Possible implications:** false-positive validation (tests not actually executed)
- **Resolution applied:** changed selector to space-delimited patterns: `models/dimensions/** models/facts/** test_dim_* test_fact_*`
- **Final status:** resolved; targeted Phase 7 dbt test run executed and passed (40 tests).

### Non-blocking warning observed
- dbt reported one unused configuration path for `marts` in `dbt_project.yml`.
- **Implication:** no runtime failure; warning only.
- **Action:** retained intentionally because `marts` belongs to upcoming Phase 8 scope.
