# Phase 12 — Final Demo Script

## 1) 60-second opening
"This system is a public renewable grid resilience auditor built end-to-end for transparent policy analytics. It ingests public energy data with contract validation, standardizes and models it through dbt, computes governance-backed KPI scorecards, runs baseline forecasts and scenarios, serves stakeholder dashboards, and monitors freshness/drift with explicit alert policies."

## 2) Demo flow (8-10 minutes)
1. **Quality gates and reproducibility (1 min)**
   - Show core commands in `README.md` and CI passing state.
2. **Data model and KPI marts (2 min)**
   - Explain Bronze/Silver/Gold progression and KPI scorecard outputs.
3. **Forecasting and scenarios (2 min)**
   - Run forecast command and show scenario fallback behavior.
4. **Dashboard narrative cards (2 min)**
   - Launch dashboard and show plain-language + technical + caveat card pattern.
5. **Operational monitoring (2 min)**
   - Run monitoring command and explain severity routing and policy thresholds.
6. **Close with limitations + next steps (1 min)**
   - State current constraints and practical roadmap.

## 3) Live commands sequence
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

## 4) What to say at each command milestone
- `make check`: "Code quality and tests are enforced before analytics output is trusted."
- `make dbt-marts`: "Policy KPIs are generated from governed semantic layers."
- `make forecast-phase9`: "Forecasting is interpretable and includes fallback behavior."
- `make dashboard-smoke`: "Stakeholder narrative coverage is validated, not assumed."
- `make monitor-phase11`: "Operational thresholds are policy-configured and machine-enforced."

## 5) Closing statement
"The final deliverable is not just a dashboard; it is a reproducible, testable, and explainable analytics product with explicit governance and operational controls."
