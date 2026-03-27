# Phase 12 — Reproducibility Evidence

## 1) Environment assumptions
- OS: Linux (dev container)
- Python: 3.11
- Runtime dependencies: `requirements.txt`
- Dev/CI dependencies: `requirements-dev.txt`
- Orchestration dependencies: `requirements-orchestration.txt`

## 2) Deterministic execution pathway
Primary validation and execution path:
```bash
make check
make contracts
make ingest-mock
make dbt-staging
make dbt-intermediate
make dbt-dimensions-facts
make dbt-marts
make forecast-phase9
make dashboard-smoke
make monitor-phase11
```

## 3) Artifacts proving reproducibility
- Versioned source contracts and sample fixtures.
- Deterministic mock ingestion flow.
- dbt model/test definitions for each semantic layer.
- Per-phase technical implementation records.
- CI workflow enforcing lint + tests on push and PR.

## 4) Known reproducibility constraints
- Live source variability is expected outside mock mode.
- Some KPI and monitoring outputs vary with data horizon and ingestion date.
- Forecast backtest behavior depends on historical depth; fallback status is emitted when sparse.

## 5) How evaluators should verify
1. Clone repository and install dependencies.
2. Execute the command chain above in order.
3. Confirm all commands complete without error.
4. Confirm dashboard smoke and monitoring JSON outputs are produced.
5. Compare results against phase documentation and latest CI run.
