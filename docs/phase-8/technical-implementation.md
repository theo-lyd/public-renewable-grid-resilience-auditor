# Phase 8 — Technical Implementation Document

## 1) Objective(s)
1. Finalize KPI SQL implementations in Gold marts.
2. Finalize threshold bands for stress-score interpretation.
3. Implement composite resilience scoring with sensitivity variants.

## 2) Deliverable(s)
- Gold mart models for zone-hour and zone-day KPI scorecards
- Gold mart model for daily composite resilience scoring
- Mart schema and singular tests
- Makefile marts automation target
- Phase 8 implementation documentation

## 3) What was implemented
- Added `mart_zone_hour_kpi_scorecard` with KPI proxy logic and stress bands.
- Added `mart_zone_day_kpi_scorecard` with aggregation-safe ratio recomputation.
- Added `mart_zone_day_resilience_composite` with three weighting variants.
- Added mart schema tests and singular tests for threshold and score-range integrity.
- Added `make dbt-marts` pipeline target.

## 4) How it was implemented
1. Started from Phase 7 governed facts as the Gold mart source layer.
2. Encoded KPI formulas directly in SQL with denominator guards.
3. Implemented threshold banding in SQL for auditability.
4. Normalized KPI components to 0–100 and computed weighted composites.
5. Added singular validation for stress band consistency and score range bounds.

## 5) Exact commands run
Commands executed during Phase 8 implementation and validation are recorded below.

```bash
make check PYTHON=.venv/bin/python && make contracts PYTHON=.venv/bin/python && make ingest-mock PYTHON=.venv/bin/python && make dbt-staging PYTHON=.venv/bin/python && make dbt-intermediate PYTHON=.venv/bin/python && make dbt-dimensions-facts PYTHON=.venv/bin/python && make dbt-marts PYTHON=.venv/bin/python
```

## 6) Files created/updated

### Created
- `dbt/models/marts/mart_zone_hour_kpi_scorecard.sql`
- `dbt/models/marts/mart_zone_day_kpi_scorecard.sql`
- `dbt/models/marts/mart_zone_day_resilience_composite.sql`
- `dbt/models/marts/schema.yml`
- `dbt/tests/test_mart_composite_range.sql`
- `dbt/tests/test_mart_stress_band_thresholds.sql`
- `docs/phase-8/gold-marts-and-kpi-scorecards.md`
- `docs/phase-8/technical-implementation.md`

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
	- `make dbt-marts`: passed
- dbt marts execution summary:
	- 3 mart models built
	- 20 marts-layer tests passed in targeted run

## 8) Output state
- Gold mart KPI scorecard layer is implemented and ready for validation.

## 9) Requirement-to-reality gap log
- Import dependency KPI remains data-gapped because import/export flow inputs are not integrated yet.
- Minimal viable path: preserve field as null with explicit caveat; activate once flow data is onboarded.

## 10) Problems encountered and resolution log

### Problem P8-01: Null KPI percentages at zero-generation hours
- **Where observed:** first `make dbt-marts` run, `not_null_mart_zone_hour_kpi_scorecard_renewable_share_pct` failed with 24 rows.
- **Root cause:** percentage formulas used division by `nullif(denominator, 0)`, which produced `NULL` when denominator was zero.
- **Possible implications:** downstream scorecards could show missing KPI values and violate non-null quality contracts.
- **Resolution applied:** added explicit `coalesce(..., 0.0)` denominator-safe defaults in hourly/day KPI marts for ratio-derived fields.
- **Final status:** resolved; full validation chain and targeted marts tests passed.

### Problem P8-02: Downstream mart tests skipped after upstream failure
- **Where observed:** initial `dbt build --select models/marts/**` execution.
- **Root cause:** dbt halted dependent mart resources after first test failure.
- **Possible implications:** false sense of completion if skip states are not reviewed.
- **Resolution applied:** fixed root KPI null issue and re-ran complete standing validation chain.
- **Final status:** resolved; no skips and all marts tests executed in final run.
