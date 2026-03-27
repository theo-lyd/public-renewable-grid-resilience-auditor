# Phase 12 — Final Q&A Strategy

## Q1) Why this architecture?
**Answer strategy:** emphasize medallion separation, testability, and reproducibility.

## Q2) How do you ensure trust in KPI outputs?
**Answer strategy:** mention schema tests, singular tests, freshness checks, and caveat cards.

## Q3) Why simple forecasting methods first?
**Answer strategy:** highlight interpretability, baseline benchmarking, and controlled iteration.

## Q4) What is production-ready vs prototype?
**Answer strategy:**
- Production-aligned: contracts, quality gates, semantic models, monitoring policy.
- Prototype areas: richer data breadth, advanced forecasting models, full Airflow operators.

## Q5) How do you handle missing or sparse data?
**Answer strategy:** point to idempotent ingestion, fallback forecast behavior, and explicit status flags.

## Q6) How are alerts prioritized?
**Answer strategy:** explain severity classification with policy thresholds and route mapping.

## Q7) What are the strongest limitations?
**Answer strategy:** acknowledge proxy assumptions, mock-context coverage, and explain near-term mitigation path.

## Q8) If you had two more weeks, what next?
**Answer strategy:**
1. add flow/import datasets for import dependency KPI,
2. convert Airflow placeholders to executable operators,
3. add seasonal regression baseline and compare against current methods,
4. enhance dashboard with trend annotations and alert history.

## Q9) How does this map to your target roles?
**Answer strategy:**
- Data Analyst: KPI interpretation and stakeholder narrative.
- Analytics Engineer: dbt semantic layer and quality gates.
- Data Engineer: ingestion reliability and orchestration controls.
- Full-stack Analytics Engineer: end-to-end ownership and trade-off decisions.

## Q10) What does success look like for adoption?
**Answer strategy:**
- reliable weekly refreshes,
- explainable KPI scorecards,
- reduced decision ambiguity,
- clear escalation pathways for data/metric anomalies.
