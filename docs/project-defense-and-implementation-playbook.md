# Project Defense and Implementation Playbook

## Purpose of this document
This document is a single reference for:
1. Business/theoretical logic behind the project,
2. Technical rules and implementation standards,
3. Decisions already made and decisions planned by phase,
4. Interview-ready framing across multiple analytics and data engineering job roles.

---

## A) Why lint issues appeared repeatedly in early phases

### Short answer
Lint issues appeared because the project was evolving rapidly across new files and modules, and style/quality rules were intentionally strict from the beginning.

### Root causes
1. New modules were introduced quickly each phase (normal in early build stages).
2. Ruff/Black rules enforce strict import ordering, line length, and modern Python idioms.
3. Some formatting issues are not fully auto-fixable and required manual refactoring.

### Implications if ignored
1. CI fails repeatedly.
2. Code quality confidence drops in reviews/interviews.
3. Delivery speed slows later due to technical debt.

### Why this is still a good signal
Frequent early lint failures can be healthy when they are:
- caught quickly,
- documented,
- fixed consistently,
- prevented with automation.

This project already enforces that pattern via `make check`, CI gates, and problem logs in each phase technical document.

---

## B) Business/theoretical rules (program-level)

## B1) Policy problem framing
The system exists to support public-sector energy decisions, not only technical reporting.

Guiding rule:
- Every data product must answer a policy question (risk, reliability, transition progress, or equity implication).

## B2) KPI governance and interpretability
All KPIs must include:
1. Plain-language meaning,
2. Formula and data dependencies,
3. Assumptions and caveats,
4. Appropriate grain and aggregation policy.

Guiding rule:
- No KPI is published without explicit caveats, especially proxy metrics.

## B3) Decision-usefulness over model novelty
Forecasting and scorecards must be defensible and interpretable before they become complex.

Guiding rule:
- Start with robust baselines, then improve only when measurable benefit is clear.

## B4) Reproducibility as a thesis and industry requirement
The project must be repeatable by evaluators and teammates.

Guiding rule:
- Environment, commands, outputs, and decisions are always documented and versioned.

## B5) Risk and transparency discipline
Operational and analytical risks are expected and explicitly managed.

Guiding rule:
- Every phase includes risk notes and a problem log (cause, implications, resolution).

---

## C) Technical/implementation rules (program-level)

## C1) Architecture rule
- Bronze: raw snapshots (Parquet)
- Silver: standardized conformed data
- Gold: policy marts and KPI outputs

Guiding rule:
- Preserve raw truth first, transform later.

## C2) Contract-first ingestion rule
Before large ingestion logic, define source contracts.

Guiding rule:
- Required fields, quality rules, and failure modes are versioned and machine-validated.

## C3) Idempotency and metadata rule
Ingestion operations must be safe to rerun.

Guiding rule:
- Deterministic operation keys + sidecar metadata per run are mandatory.

## C4) Reliability rule
External calls are unreliable by default.

Guiding rule:
- Use retry/backoff, explicit status handling, and controlled mock fixtures for deterministic tests.

## C5) Quality gate rule
Code is not complete without validation.

Guiding rule:
- Lint, format, tests, smoke checks, and contract checks must pass before push.

## C6) Documentation rule
Each phase must include technical implementation documentation.

Guiding rule:
- Include what/how, commands, files changed, validation outcomes, output state, gaps, and problems/resolutions.

## C7) Dependency management rule
Dependencies are separated by concern.

- `requirements.txt` for runtime core,
- `requirements-dev.txt` for developer/CI tooling,
- `requirements-orchestration.txt` for Airflow stack.

Guiding rule:
- Keep base workflows lightweight and isolate heavy orchestration dependencies.

---

## D) Decisions made so far (implemented)

## Phase 1 — Governance and scope lock
- Project charter, KPI dictionary, and acceptance checklist created.
- Scope and constraints fixed for an academically defensible MVP.

## Phase 2 — Environment and standards
- Full project scaffold created.
- Dependency strategy standardized.
- CI quality gates established.

## Phase 3 — Source inventory and contracts
- Versioned source inventory created.
- Explicit endpoint schemas and quality rules implemented.
- Contract validation introduced.

## Phase 4 — Bronze ingestion jobs
- Retry/backoff HTTP layer implemented.
- Source fetchers and Bronze writer implemented.
- Idempotent writes with metadata sidecar verified.
- Mock ingestion workflows added for deterministic validation.

---

## E) Decisions to be made (planned by remaining phases)

## Phase 5 — Staging + schema tests
- Finalize dbt source/staging model granularity and naming.
- Implement source freshness and schema tests in dbt.

## Phase 6 — Intermediate harmonization
- Lock timezone, unit, and zone harmonization policy.
- Define canonical zone-hour grain rules.

## Phase 7 — Dimensions/facts
- Confirm dimensional model keys and fact grains.
- Choose strategy for reference updates and mapping drift.

## Phase 8 — Gold marts and KPI scorecards
- Finalize KPI SQL implementations and threshold bands.
- Decide composite score weighting methodology and sensitivity variants.

## Phase 9 — Forecasting and scenarios
- Select baseline forecasting methods and backtest policy.
- Define scenario catalog and fallback behavior.

## Phase 10 — Dashboard and narrative
- Decide final stakeholder views and KPI explanation cards.
- Standardize plain-language caveats next to each metric.

## Phase 11 — Orchestration and monitoring
- Finalize DAG dependency graph and rerun/backfill policy.
- Decide SLA targets, drift thresholds, and alert routing logic.

## Phase 12 — Defense package
- Finalize thesis narrative, demo script, and Q&A strategy.
- Package reproducibility evidence and operational runbook.

---

## F) Interview framing by potential role

## F1) Data Analyst
Emphasize:
- KPI logic, stakeholder readability, trend interpretation,
- policy insight generation,
- caveat communication and metric trustworthiness.

## F2) Analytics Engineer / Analytic Engineer
Emphasize:
- semantic layer design,
- dbt-ready contract-to-model workflow,
- data quality testing and documentation discipline.

## F3) Data Engineer
Emphasize:
- idempotent ingestion,
- retry/backoff resilience,
- partition strategy,
- metadata lineage and operational reliability.

## F4) Stack Analytics Engineer
Emphasize:
- full-lifecycle ownership (source contracts → ingestion → marts → dashboard → CI/ops),
- trade-off decisions between speed, reliability, and interpretability,
- reproducible delivery under governance controls.

---

## G) Interview-ready narrative (compact)
Use this structure:
1. **Problem:** public-sector renewable planning needs reliable, explainable indicators.
2. **Approach:** contract-first ingestion + medallion modeling + policy KPI marts.
3. **Reliability:** retries, idempotency, metadata tracing, CI quality gates.
4. **Outcome:** reproducible analytics platform with decision-oriented KPI outputs.
5. **Learning:** strict quality rules surfaced issues early; documented fixes improved delivery discipline.

---

## H) Program-wide operating checklist
For each remaining phase:
1. Implement only phase scope.
2. Validate with project quality gates.
3. Document implementation and all problems/resolutions.
4. Update docs index.
5. Commit with clear phase message and push.
