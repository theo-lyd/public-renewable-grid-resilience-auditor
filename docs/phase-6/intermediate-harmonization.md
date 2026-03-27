# Phase 6 — Intermediate Harmonization

## Objective(s)
1. Harmonize timestamps to a canonical UTC hour grain.
2. Harmonize units to comparable energy units (MWh) where needed.
3. Enforce zone-grain conformance across sources.

## Deliverable(s)
- Intermediate dbt models for ENTSO-E, Open-Meteo, Ember harmonization
- Conformed zone-hour model joining harmonized source outputs
- Zone mapping seed and conformance tests
- Makefile commands for intermediate build/test workflow

## Harmonization standards implemented

### Timezone standard
- Canonical timezone: `UTC`
- Canonical grain: `zone-hour`
- Rule: all timestamps are truncated/expanded to hour-level before conformed joins.

### Unit standard
- ENTSO-E generation (`MW` at hourly granularity) converted to `MWh` via 1-hour equivalence.
- Ember generation (`TWh` daily) converted to hourly `MWh` and expanded across 24 hours.

### Zone conformance standard
- Central zone reference: `zone_conformance_mapping` seed.
- Open-Meteo joins to zone via mapped coordinates.
- Ember joins to zone via country-to-zone mapping.

## Why this phase matters
This phase prevents downstream KPI/model errors caused by incompatible timestamp grains, unit scales, and zone keys.

## Operational commands
1. Ensure Bronze sample data exists: `make ingest-mock`
2. Run staging prerequisites: `make dbt-staging`
3. Run Phase 6 harmonization gates: `make dbt-intermediate`
