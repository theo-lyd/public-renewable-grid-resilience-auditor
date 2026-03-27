# Phase 3 — Source Inventory and API Contracts

## Objective(s)
1. Establish a complete source inventory for ENTSO-E, Open-Meteo, and Ember.
2. Define explicit API contracts (required fields, expected types, response shape assumptions).
3. Define source-level data quality rules and failure mode expectations.

## Deliverable(s)
- Versioned source inventory contract file in YAML.
- Contract validation module and execution command.
- Test coverage to ensure contract completeness.

## Scope covered
- Core sources for the capstone MVP:
  - ENTSO-E Transparency API
  - Open-Meteo API
  - Ember Electricity Data

## Contract standard used
For each endpoint, the contract includes:
1. Endpoint metadata (path, method, format, parameters)
2. Required fields (name, type, nullable policy, meaning)
3. Quality rules (rule ID, severity, dimension, expression)
4. Known failure modes (operational and schema risks)

## Quality rule dimensions
- **Completeness:** Required fields present.
- **Validity:** Value ranges and non-negative constraints.
- **Conformance:** Mapping/reference alignment (zone/country codes).
- **Timeliness:** Freshness windows and latency constraints.
- **Consistency:** Expected temporal continuity at target grain.

## Why this matters for policy analytics
- Reduces ambiguity before ingestion implementation begins.
- Makes quality expectations explicit and auditable for thesis defense.
- Improves reliability by identifying likely source failures early.
