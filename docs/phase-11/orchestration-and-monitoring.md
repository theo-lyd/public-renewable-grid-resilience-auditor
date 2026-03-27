# Phase 11 — Orchestration and Monitoring

## Purpose
Phase 11 operationalizes the pipeline with an explicit DAG dependency graph, a backfill/rerun policy, and threshold-based monitoring with alert routing.

## DAG dependency graph finalized
The Airflow DAG `grid_resilience_pipeline` now follows this ordered chain:
1. `bronze_ingestion`
2. `dbt_staging`
3. `dbt_intermediate`
4. `dbt_dimensions_facts`
5. `dbt_marts`
6. `forecast_phase9`
7. `dashboard_smoke`
8. `monitor_phase11`

Operational controls:
- `schedule=@daily`
- `max_active_runs=1`
- `retries=1`
- `catchup=false` (manual controlled backfills)

## Rerun and backfill policy
Policy source: `data/reference/monitoring/phase11_policy.yaml`
- Max backfill window: 30 days
- Rerun on failure: enabled
- Partial backfill: disabled

## SLA and drift thresholds
Policy values implemented:
- Freshness SLA: 72 hours max lag
- Drift thresholds:
  - Stress index: warn 0.35, critical 0.70
  - Renewable share: warn 0.25, critical 0.50

## Alert routing logic
- `critical` → `pagerduty://grid-ops-critical`
- `warning` → `slack://grid-ops-warnings`
- `info` → `email://grid-analytics-digest`

## Monitoring outputs
`make monitor-phase11` emits a JSON report containing:
- overall status (`ok`, `warning`, `critical`)
- freshness metrics
- alerts per zone
- DAG dependency graph snapshot
- active backfill policy snapshot

## Why this matters
- Non-technical: clear operational accountability when data quality degrades.
- Technical: deterministic orchestration sequence and codified response thresholds.
