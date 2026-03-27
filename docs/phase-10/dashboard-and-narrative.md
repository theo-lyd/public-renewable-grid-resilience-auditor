# Phase 10 — Dashboard and Narrative

## Purpose
Phase 10 delivers stakeholder-facing dashboard views and standardized narrative cards so every KPI is explained in plain language with technical traceability and caveats.

## Stakeholder views implemented
1. **Executive snapshot cards**
   - Renewable Share (%)
   - Supply-Demand Stress Index
   - Grid Resilience Composite (Baseline)
2. **Daily KPI trend view**
   - Renewable, carbon proxy, stress, ramping, and curtailment trend lines.
3. **Composite sensitivity view**
   - Baseline vs security-heavy vs transition-heavy resilience score trajectories.
4. **KPI explanation card panel**
   - For each metric: plain-language explanation, technical definition, caveat text.

## Narrative standardization implemented
- KPI narrative catalog is centralized in `src/monitoring/dashboard_narrative.py`.
- Dashboard renders narrative cards directly from this catalog.
- Smoke validation checks required KPI narrative coverage.

## Why this matters
- Non-technical audiences get clear interpretation and limitations.
- Technical reviewers can trace definitions to explicit formulas.
- Proxy caveats are consistently shown rather than hidden in separate docs.

## Runbook
- Validate dashboard prerequisites: `make dashboard-smoke`
- Launch dashboard: `make dashboard-run`
