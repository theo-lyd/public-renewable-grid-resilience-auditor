# Phase 9 — Forecasting and Scenarios

## Purpose
Phase 9 introduces a practical forecasting baseline and scenario engine so policy stakeholders can compare expected KPI trajectories under alternative assumptions.

## Scope delivered
1. Baseline forecasting methods selected:
   - Naive last-observation carry-forward
   - Moving average (default)
2. Backtest policy implemented:
   - Rolling one-step backtest
   - Report MAE, RMSE, MAPE
   - Require minimum training history before forecast generation
3. Scenario catalog implemented:
   - `baseline`
   - `security_stress`
   - `transition_acceleration`
4. Fallback behavior implemented:
   - Unknown or empty scenario input automatically falls back to `baseline`
   - Output explicitly flags fallback usage

## Why this is interview-defensible
- Uses transparent baseline methods before introducing high-complexity ML.
- Backtest metrics are explicit and reproducible.
- Scenario assumptions are codified and auditable.

## Operational entry point
- `make forecast-phase9`

## Current caveat
- Forecasting currently targets daily KPI outputs from `mart_zone_day_kpi_scorecard`.
- More advanced models (seasonal decomposition/regression) can be layered in Phase 9+ iterations while retaining this baseline as fallback.
