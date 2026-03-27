# Interview Q&A Companion (v0.2)

## How to use
- Use this with the 2-minute and 5-minute scripts.
- Keep answers concise first, then expand if asked.

## Q1) Why this project?
I chose it because it combines strong social relevance with real technical complexity: multiple APIs, quality variability, time-series integration, and policy-facing metrics.

## Q2) What makes your approach industry-grade?
I implemented contract-first ingestion, idempotent writes, metadata lineage, strict quality gates, and phase-level implementation documentation with problem-resolution logs.

## Q3) Why use Bronze/Silver/Gold?
It separates concerns clearly:
- Bronze preserves raw truth,
- Silver standardizes/harmonizes,
- Gold publishes governed business metrics.
This improves debugging, trust, and maintainability.

## Q4) Why did you separate dependency files?
To reduce conflicts and improve reproducibility:
- core runtime dependencies,
- dev/CI dependencies,
- orchestration-only dependencies.
This avoids heavy package coupling in day-to-day workflows.

## Q5) Why did lint issues appear in early phases?
Because strict quality rules were active while many new files were being added quickly.
The key is that issues were fixed immediately, documented, and prevented from accumulating.

## Q6) How do you handle API unreliability?
I use retries with backoff for transient failures, contract validation for schema expectations, and deterministic mock fixtures for reliable testing.

## Q7) How do you prevent duplicate ingestion output?
I compute a deterministic operation key from source, endpoint, window, and request parameters.
If output files for that key already exist, the write is skipped.

## Q8) How do you ensure your metrics are trustworthy?
I define KPI formulas explicitly, include caveats and assumptions, and enforce quality checks from contracts through model layers.

## Q9) What have you implemented so far vs planned next?
Completed: governance, standards, source contracts, and Bronze ingestion.
Next: staging models, harmonization, dimensions/facts, KPI marts, forecasting, dashboard, and orchestration/monitoring.

## Q10) What role are you best aligned to right now?
I can contribute across Data Analyst, Analytics Engineer, and Data Engineer scopes, but my strongest differentiator is owning cross-functional analytics delivery end-to-end.

## Q11) What is one technical decision you are proud of?
Implementing idempotent ingestion with metadata sidecars early, because it reduced operational risk and made reruns safe from the start.

## Q12) What would you improve next if given more time?
I would add advanced drift monitoring, richer scenario simulation, and stronger dashboard interactivity while preserving interpretability.

## Role-specific mini-answers

### Data Analyst
I turn technically complex data pipelines into decision-ready KPI narratives with clear caveats.

### Analytics Engineer
I focus on semantic consistency, tested transformations, and reliable metric contracts.

### Data Engineer
I focus on resilient ingestion design, idempotency, and traceable pipeline operations.

### Stack Analytics Engineer
I focus on connecting data platform reliability with stakeholder-facing analytics outcomes.

## Update notes
- Version `v0.2` reflects project state through Phase 4.
- Refresh after Phase 8 and final defense prep in Phase 12.
