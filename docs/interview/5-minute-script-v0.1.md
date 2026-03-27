# 5-Minute Interview Script (v0.1)

## When to use
- Hiring manager interview
- Technical deep-dive interview
- Portfolio walkthrough

## 1) Project overview (about 45 seconds)
I’m building a capstone project called the Public Renewable Grid Resilience Auditor. The goal is to help public-sector planners monitor renewable integration, reliability risks, and transition progress using only free/public data sources.

The project is designed as an industry-style analytics platform, not just a notebook: contract-defined ingestion, layered modeling, quality gates, and stakeholder communication.

## 2) Business problem and impact (about 45 seconds)
Planners often have fragmented datasets and inconsistent metrics. That creates decision risk when evaluating renewable targets, grid stress, curtailment, or import dependency.

This project addresses that by producing governed policy KPIs with explicit assumptions and caveats, so decisions are explainable and repeatable.

## 3) Technical architecture (about 75 seconds)
The core architecture is Bronze/Silver/Gold on DuckDB + Parquet:
- Bronze stores raw snapshots from APIs.
- Silver standardizes and harmonizes across time, units, and zones.
- Gold publishes policy KPI marts and scorecards.

For reliability and operations:
- Source contracts are versioned and machine-validated.
- Ingestion has retry/backoff.
- Bronze writes are idempotent using deterministic operation keys.
- Every write also stores metadata for lineage and auditability.
- CI enforces lint, tests, and repeatable checks.

## 4) What I have implemented so far (about 60 seconds)
Through Phase 4, I have completed:
1. Governance and KPI definitions,
2. Environment and CI standards,
3. Source inventory and API contracts with quality rules,
4. Raw ingestion jobs for ENTSO-E, Open-Meteo, and Ember with mock-driven deterministic validation.

I also documented implementation decisions and problems/resolutions phase by phase, which is important for both thesis defense and production-style engineering accountability.

## 5) Key trade-offs and engineering choices (about 45 seconds)
I made deliberate choices:
- Chose layered requirements files instead of a single dependency file to reduce conflicts and improve reproducibility.
- Kept orchestration dependencies isolated to avoid unnecessary base-environment complexity.
- Prioritized interpretable and testable foundations over premature model complexity.

These choices optimize for maintainability, reviewability, and delivery reliability.

## 6) Current limitations and mitigation (about 40 seconds)
Current limitations are expected at this stage:
- Some source schemas can drift over time.
- KPI marts and forecasting layers are still in future phases.

Mitigations already in place:
- Contract-first ingestion,
- explicit quality rules,
- reproducible validation workflow,
- documented gaps and minimal viable paths.

## 7) What comes next (about 30 seconds)
Next phases implement staging and harmonization models, dimensional/fact modeling, KPI marts, forecasting/scenarios, dashboard narrative, and orchestration/monitoring.

By the final phase, this becomes a full, interview-ready demonstration of analytics engineering from source ingestion to decision-support delivery.

## Role-specific emphasis cheatsheet

### Data Analyst
- Emphasize KPI interpretation, caveat communication, and policy trend storytelling.

### Analytics Engineer / Analytic Engineer
- Emphasize contracts, tested transformations, semantic consistency, and documentation quality.

### Data Engineer
- Emphasize idempotency, resilience, metadata lineage, partition strategy, and CI discipline.

### Stack Analytics Engineer
- Emphasize full lifecycle ownership and trade-off decisions across data, modeling, and product communication.

## Update notes
- Version `v0.1` reflects project state through Phase 4.
- Refresh after Phase 8 and finalize in Phase 12.
