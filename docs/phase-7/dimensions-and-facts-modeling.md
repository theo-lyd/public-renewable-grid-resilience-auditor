# Phase 7 — Dimensions and Facts Modeling

## Purpose
Phase 7 turns harmonized intermediate data into reusable analytical dimensions and governed fact tables. This provides stable keys and explicit grain definitions for downstream KPI marts.

## Scope delivered
1. Defined dimension keys for time, zone, fuel category, and source system.
2. Defined fact grains for:
   - zone-hour resilience inputs
   - zone-hour-fuel generation
3. Added quality gates to verify key integrity, grain conformance, and mapping completeness.
4. Added automation target to run dimensions/facts build and tests.

## Model grain decisions
- `dim_time_hourly`: one row per UTC hour (`timestamp_hour_utc`).
- `dim_zone`: one row per conformed `zone_code` observed in intermediate data.
- `dim_fuel_category`: one row per normalized `fuel_category`.
- `dim_source_system`: one row per `source_system`.
- `fct_zone_hour_resilience_inputs`: one row per `zone_code` + `timestamp_hour_utc`.
- `fct_zone_hour_fuel_generation`: one row per `zone_code` + `timestamp_hour_utc` + `fuel_category`.

## Mapping drift strategy
- Current strategy is **fail-fast conformance**:
  - model records mapping status in `dim_zone` (`mapped` vs `unmapped`)
  - singular test fails if any `unmapped` zone appears
- Operational implication: reference mapping must be updated before new zones can be promoted into facts.

## Why this matters
- Non-technical: dashboards can rely on consistent definitions and avoid hidden metric mismatches.
- Technical: downstream marts can use stable surrogate keys and enforce referential integrity.

## Validation entry point
- `make dbt-dimensions-facts`
