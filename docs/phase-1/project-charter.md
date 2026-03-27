# Phase 1 — Project Charter

## 1) Project identity
- **Project name:** Public Renewable Grid Resilience Auditor
- **Project type:** MSc capstone (industry-standard analytics engineering + decision support)
- **Primary users:** Policymakers, public energy planners, grid analysts, academic reviewers
- **Owner (student):** You
- **Delivery mode:** Iterative, phase-gated, reproducible analytics platform

## 2) Problem statement
Public-sector planners need a transparent and repeatable way to monitor renewable integration, reliability risk, and equity-oriented transition progress. Existing reporting is often fragmented across sources and difficult to operationalize for planning decisions.

This project builds a governance-first analytics system that ingests free public data, standardizes it, computes policy KPIs, and supports forecasting/scenario analysis for practical decision-making.

## 3) Vision and outcome
Build a production-style, academically defensible data platform that:
1. Integrates free energy + weather sources into a governed data model.
2. Produces interpretable resilience and transition KPIs.
3. Supports scenario-driven policy planning.
4. Demonstrates operational reliability (orchestration, tests, SLA/drift checks, alerting).

## 4) Objectives (Phase 1 locked)
### Objective O1 — Governance clarity
Define scope, assumptions, decision rights, and success criteria before major engineering work.

### Objective O2 — KPI contract
Define precise KPI formulas, grains, required inputs, caveats, and thresholds to avoid downstream ambiguity.

### Objective O3 — Exit criteria
Define a concrete acceptance checklist for Phase 1 to support stage-gate progression.

## 5) Deliverables (Phase 1)
1. This project charter (`docs/phase-1/project-charter.md`)
2. KPI dictionary (`docs/phase-1/kpi-dictionary.md`)
3. Acceptance checklist (`docs/phase-1/acceptance-checklist.md`)

## 6) Scope definition
### In scope
- Data sources: ENTSO-E, Open-Meteo, Ember (plus optional country portals later).
- Data architecture: Bronze/Silver/Gold with DuckDB + Parquet.
- Transformation/modeling: dbt-duckdb.
- Orchestration: Airflow DAGs.
- Consumption layer: Streamlit dashboard.
- Reliability layer: SLA checks, drift checks, alert severity/dedupe/escalation.
- KPI set: 8 policy KPIs and composite resilience score.

### Out of scope (initially)
- Real-time streaming architecture.
- Proprietary paid data sources.
- Country-specific market bidding optimization.
- Advanced deep learning models as initial baseline.

## 7) Target users and decisions supported
### Policymakers
- Track renewable share and resilience trends.
- Detect risk windows (stress, ramping, curtailment proxy).

### Planning analysts
- Compare regions and periods using standardized scorecards.
- Explore weather-driven sensitivity and import dependency.

### Academic/industry evaluators
- Review reproducibility, methods rigor, and operational maturity.

## 8) Success criteria (project-level)
### Technical
- Reproducible environment setup and runbook.
- Idempotent ingestion and traceable data lineage.
- Tested dbt models with quality gates.
- Automated orchestration and CI checks.

### Analytical
- All 8 KPIs computed from governed models.
- Forecasting baselines outperform naive reference for selected targets.
- Scenario outputs are interpretable and policy-relevant.

### Presentation
- Clear thesis narrative: business context → architecture → methods → results → limitations.
- Dashboard supports a 10–15 minute executive walkthrough.

## 9) Stakeholders and RACI (lightweight)
| Workstream | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Scope/KPI definition | Student | Student | Supervisor | Review panel |
| Data engineering | Student | Student | Supervisor | Review panel |
| Forecasting/scenarios | Student | Student | Domain experts | Review panel |
| Dashboard/storyline | Student | Student | Supervisor | Review panel |
| Governance/testing | Student | Student | Supervisor | Review panel |

## 10) Assumptions
1. Selected source endpoints remain publicly accessible.
2. Data latency and completeness vary by source and are explicitly documented.
3. Time granularity for core marts will be standardized (target: zone-hour baseline).
4. Emissions data may be incomplete; carbon KPI is a proxy when needed.

## 11) Key risks and mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| API rate limits or downtime | Delayed/partial ingestion | Retry/backoff, cached snapshots, rerun windows |
| Schema drift in source payloads | Broken ingestion/transforms | Data contracts + schema tests + alerts |
| Missing intervals | KPI distortion | Gap handling policy + missingness flags |
| Unit/timezone inconsistencies | Wrong KPI values | Harmonization layer with explicit conversion tests |
| Over-complex modeling too early | Delivery risk | Start interpretable baselines; phase advanced models later |

## 12) Constraints
- Must use free/public APIs where possible.
- Must remain reproducible and explainable for thesis defense.
- Must prioritize data quality and operational reliability over model complexity.

## 13) Governance cadence
- **Weekly:** Phase checkpoint (scope, quality, risk review).
- **Per release:** Update assumptions, KPI definitions, and known limitations.
- **Before moving phase:** Pass checklist gate for current phase.

## 14) Decision log template
Use this template for major decisions:

| Date | Decision | Rationale | Alternatives considered | Impact |
|---|---|---|---|---|
| YYYY-MM-DD |  |  |  |  |

## 15) Phase 1 exit definition
Phase 1 is complete when:
1. Governance documents exist and are internally consistent.
2. KPI formulas and assumptions are explicit and reviewable.
3. Acceptance checklist is fully satisfied and signed off by you.
