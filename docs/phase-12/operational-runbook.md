# Phase 12 — Operational Runbook

## 1) Daily operations checklist
1. Run `make ingest-mock` for deterministic validation (or live ingestion in production context).
2. Run `make dbt-staging`, `make dbt-intermediate`, `make dbt-dimensions-facts`, `make dbt-marts`.
3. Run `make forecast-phase9`.
4. Run `make dashboard-smoke`.
5. Run `make monitor-phase11` and inspect `overall_status`.

## 2) Incident response guidance
### If `overall_status=critical`
- Escalate using route in monitoring output (`pagerduty://grid-ops-critical`).
- Check freshness status and drift metric details by zone.
- Re-run from ingestion onward after root-cause correction.

### If `overall_status=warning`
- Notify analytics channel (`slack://grid-ops-warnings`).
- Track whether warning persists in next cycle.

### If `overall_status=info`
- Include in regular digest (`email://grid-analytics-digest`).

## 3) Rerun/backfill policy
- Maximum backfill window: 30 days.
- Failed jobs should be rerun.
- Partial backfills are disallowed in current policy.

## 4) Common failure categories and first actions
1. **Contract failure**: inspect source fixtures/payload changes and update contract definitions.
2. **dbt test failure**: inspect failing model/test and restore expected grain/constraints.
3. **Forecast runtime warning**: verify data sufficiency and fallback status in output.
4. **Dashboard smoke failure**: ensure mart tables and narrative metric IDs remain aligned.

## 5) Change management rule
Any formula, threshold, or policy change must include:
- rationale,
- expected impact,
- validation evidence,
- phase technical log update,
- CI green status before merge/deploy.
