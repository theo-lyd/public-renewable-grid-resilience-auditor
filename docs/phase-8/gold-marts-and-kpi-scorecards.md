# Phase 8 — Gold Marts and KPI Scorecards

## Purpose
Phase 8 converts modeled facts into policy-facing scorecards and composite resilience indicators.

## Scope delivered
1. Implemented Gold marts for zone-hour KPI scorecard and zone-day KPI scorecard.
2. Implemented zone-day composite resilience scores using baseline and sensitivity weight variants.
3. Finalized stress threshold bands in SQL (`low`, `moderate`, `high`, `critical`).
4. Added automated quality checks for threshold correctness and composite score ranges.

## Implemented KPI set (current data-supported)
- Renewable Share (%)
- Carbon Intensity Proxy
- Supply-Demand Stress Index (proxy)
- Ramping Risk Index
- Curtailment Proxy (%)
- Weather Sensitivity Score (daily correlation proxy)
- Grid Resilience Composite Score (3 weighting variants)

## Weighting methodology and sensitivity variants
- **Baseline composite:** balanced transition and reliability weighting.
- **Security-heavy composite:** increases stress/ramping emphasis.
- **Transition-heavy composite:** increases renewable/carbon emphasis.

## Threshold bands finalized
Supply-Demand Stress Index bands:
- `< 0.85` → `low`
- `0.85–0.95` → `moderate`
- `0.95–1.05` → `high`
- `> 1.05` → `critical`

## Important caveats
- Import dependency remains `NULL` pending interconnection flow inputs in later phases.
- KPI formulas are explicit proxies built from currently integrated free datasets.
- Composite scores are governance artifacts and should be interpreted with documented caveats.

## Validation entry point
- `make dbt-marts`
