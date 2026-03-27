# 5-Minute Interview Script (v0.2)

## Goal of this version
This version is designed for hiring manager and technical interviews where you need to show business understanding, architecture choices, and engineering discipline in one coherent story.

## Suggested timing
- 0:00–0:40: business context
- 0:40–2:00: architecture and implementation
- 2:00–3:30: reliability and quality discipline
- 3:30–4:30: current status and next steps
- 4:30–5:00: role alignment

## Script

I’m building an industry-style capstone called the Public Renewable Grid Resilience Auditor.

The business problem is that energy planners and policy teams often operate with fragmented data and inconsistent metrics, which makes renewable integration and reliability decisions harder than they need to be.

To solve this, I designed a full analytics lifecycle project using free public APIs, so the system is both practical and reproducible. I’m using ENTSO-E, Open-Meteo, and Ember as primary sources, and a medallion-style architecture with DuckDB and Parquet.

In Bronze, I ingest raw snapshots with deterministic operation keys, retry/backoff for API resilience, and metadata sidecars for traceability. In Silver and Gold, the plan is to standardize, model, and publish policy KPIs with explicit formulas and caveats.

So far, I’ve completed governance and KPI contracts, environment and CI standards, source inventory with machine-validated API contracts, and Phase 4 ingestion jobs that are idempotent and tested. That means rerunning the same ingestion request does not duplicate output, and each run is auditable.

A key principle in this project is that quality is a first-class feature. I enforce linting, formatting, tests, smoke checks, and contract checks before push. I also document issues and resolutions phase by phase so the project remains defensible for both industry interviews and academic review.

My trade-off decisions have been intentional. For example, I split dependencies by purpose to reduce conflict risk and keep core workflows lightweight, while isolating orchestration dependencies for the phase where they are actually needed.

From here, the next steps are staging and harmonization models, dimensional/fact layers, KPI marts, forecasting and scenarios, then dashboard narrative and orchestration monitoring.

What I want you to take away is that I can build beyond isolated scripts: I can structure reliable analytics systems that connect data engineering, analytics engineering, and stakeholder outcomes.

## Optional technical deepening (if interviewer asks)
- Why contract-first ingestion? To catch schema and quality risks early and reduce downstream breakage.
- Why idempotency? To make reruns safe and operationally predictable.
- Why strong documentation? To improve handover, reproducibility, and decision accountability.

## Role emphasis cues

### Data Analyst emphasis
Highlight KPI interpretation, policy narrative quality, and caveat communication.

### Analytics Engineer emphasis
Highlight modeling discipline, semantic consistency, and test-driven data transformations.

### Data Engineer emphasis
Highlight ingestion reliability, retry strategy, idempotency design, and lineage metadata.

### Stack Analytics Engineer emphasis
Highlight full lifecycle ownership and trade-off decisions from ingestion to business-facing outputs.

## Update notes
- Version `v0.2` reflects project state through Phase 4.
- Next update target: after Phase 8, final polish in Phase 12.
