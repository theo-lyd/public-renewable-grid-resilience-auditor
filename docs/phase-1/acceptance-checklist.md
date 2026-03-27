# Phase 1 — Acceptance Checklist

Use this checklist as the stage-gate to move from Phase 1 (governance and scope lock) to Phase 2 (environment and standards).

## How to use
- Mark each item as complete only when evidence exists in the repository.
- If any **critical** item is not complete, Phase 1 is not approved.

---

## A) Objective coverage

### O1 — Governance clarity
- [ ] **Critical:** Project problem statement is explicit and policy-focused.
- [ ] **Critical:** In-scope and out-of-scope boundaries are documented.
- [ ] Stakeholders and user groups are identified.
- [ ] Project-level success criteria (technical, analytical, presentation) are documented.
- [ ] Risk register includes impacts and mitigations.

### O2 — KPI contract
- [ ] **Critical:** All 8 required KPIs are defined.
- [ ] **Critical:** Each KPI has formula, inputs, and interpretation.
- [ ] **Critical:** Each KPI lists caveats/limitations.
- [ ] Compute and publish grain policies are documented.
- [ ] KPI change-control/versioning process is documented.

### O3 — Exit criteria
- [ ] **Critical:** Phase 1 deliverables are present in `docs/phase-1/`.
- [ ] Gate criteria for progressing to Phase 2 are explicit.
- [ ] Decision log template exists.

---

## B) Deliverable verification

### Deliverable D1 — Project charter
- [ ] File exists: `docs/phase-1/project-charter.md`
- [ ] Contains objectives and deliverables.
- [ ] Contains assumptions and constraints.
- [ ] Contains governance cadence and risk table.

### Deliverable D2 — KPI dictionary
- [ ] File exists: `docs/phase-1/kpi-dictionary.md`
- [ ] Includes all 8 policy KPIs.
- [ ] Includes formulas and data dependencies.
- [ ] Includes quality requirements and reporting-grain policy.

### Deliverable D3 — Acceptance checklist
- [ ] File exists: `docs/phase-1/acceptance-checklist.md`
- [ ] Includes critical/non-critical checklist items.
- [ ] Includes final sign-off block.

---

## C) Review readiness (for supervisor/experts)
- [ ] You can explain each KPI in plain language in under 60 seconds.
- [ ] You can justify why proxy metrics are used and what their limits are.
- [ ] You can explain the difference between compute grain and publish grain.
- [ ] You can describe top 3 risks and mitigation strategy.

---

## D) Phase 1 sign-off

### Student sign-off
- Name: ____________________
- Date: ____________________
- Status: [ ] Approved  [ ] Needs revision
- Notes:

### Supervisor/mentor sign-off (optional for class workflow)
- Name: ____________________
- Date: ____________________
- Status: [ ] Approved  [ ] Needs revision
- Notes:

---

## E) Gate decision
- [ ] **GO to Phase 2** (all critical items complete)
- [ ] **NO-GO** (critical gaps remain)
