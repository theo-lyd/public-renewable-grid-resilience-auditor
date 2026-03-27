# Phase 1 — KPI Dictionary (Gold Layer)

## Purpose
This document defines each policy KPI in a way that is:
- **Computable** from modeled data,
- **Interpretable** for policy audiences,
- **Auditable** during thesis review.

All KPI formulas below are written at a default grain of **zone-hour**, then aggregated to daily/weekly/monthly reporting where needed.

---

## Common notation
- `renewable_gen_mwh`: Renewable generation (MWh)
- `total_gen_mwh`: Total generation (MWh)
- `demand_mwh`: Electricity demand/load (MWh)
- `imports_mwh`: Net imports (MWh)
- `exports_mwh`: Exports (MWh)
- `curtailment_proxy_mwh`: Estimated curtailed renewable energy proxy (MWh)
- `co2_proxy_tonnes`: Estimated carbon emissions proxy (tonnes)
- `weather_index`: Composite weather signal (wind/irradiance/temp features)

---

## KPI 1) Renewable Share (%)
### Policy meaning
Share of electricity generation attributable to renewables.

### Formula
`renewable_share_pct = 100 * renewable_gen_mwh / nullif(total_gen_mwh, 0)`

### Inputs
- `fct_generation` by zone-time
- Renewable fuel mapping table (technology classification)

### Interpretation
- Higher is generally better for transition progress.
- Must be interpreted with reliability and import context.

### Caveats
- Technology mapping quality affects precision.
- Imports can mask domestic renewable shortfalls.

---

## KPI 2) Carbon Intensity Proxy
### Policy meaning
Estimated emissions per unit electricity, used when full verified emissions are unavailable.

### Formula (proxy)
`carbon_intensity_proxy = co2_proxy_tonnes / nullif(total_gen_mwh, 0)`

### Inputs
- Generation by fuel/technology
- Reference emissions factors (country/open datasets)

### Interpretation
- Lower is better.
- Best used as trend signal, not legal-grade emissions inventory.

### Caveats
- Emissions factors can be static and imperfect.
- Imports emissions treatment must be stated explicitly.

---

## KPI 3) Supply-Demand Stress Index
### Policy meaning
Measures tightness between available supply and demand.

### Example formula
`stress_index = demand_mwh / nullif(available_supply_mwh, 0)`

Where `available_supply_mwh` may include domestic generation + net import capability proxy.

### Interpretation bands (example)
- `< 0.85`: low stress
- `0.85–0.95`: moderate
- `0.95–1.05`: high
- `> 1.05`: critical (shortfall risk)

### Caveats
- Requires clear definition of “available supply.”
- Planned outages and reserve margins should be documented if excluded.

---

## KPI 4) Ramping Risk Index
### Policy meaning
Captures intra-day volatility and rapid net-load change risk.

### Example formula
`ramping_risk_index = abs(net_load_t - net_load_t_minus_1) / nullif(demand_mwh, 0)`

Where `net_load = demand_mwh - variable_renewable_gen_mwh`.

### Interpretation
- Higher values indicate more operational balancing pressure.

### Caveats
- Sensitive to time granularity.
- Should be compared within consistent zones and periods.

---

## KPI 5) Curtailment Proxy / Spill Risk
### Policy meaning
Estimates potential renewable energy not utilized due to system constraints.

### Example proxy formula
`curtailment_proxy_pct = 100 * curtailment_proxy_mwh / nullif(potential_variable_renewable_mwh, 0)`

### Inputs
- Variable renewable generation
- Weather-derived potential proxy
- Constraint heuristics (if explicit curtailment not available)

### Caveats
- Proxy uncertainty must be surfaced in dashboard notes.
- Distinguish measured curtailment from inferred curtailment.

---

## KPI 6) Import Dependency Ratio
### Policy meaning
Share of demand met via imports; indicates external dependency risk.

### Formula
`import_dependency_ratio = imports_mwh / nullif(demand_mwh, 0)`

### Interpretation
- Higher ratio may indicate flexibility support or vulnerability, depending on context.

### Caveats
- Interpret together with interconnection reliability and geopolitics.
- Net vs gross imports must be stated.

---

## KPI 7) Weather Sensitivity Score
### Policy meaning
Measures degree to which renewable output (or net load) responds to weather variation.

### Example implementation
- Train interpretable baseline model: `renewable_gen ~ wind + irradiance + temperature`
- Derive sensitivity score from standardized coefficients or partial dependence deltas.

### Interpretation
- Higher score implies stronger weather dependence and planning sensitivity.

### Caveats
- Model drift and seasonal changes affect stability.
- Requires regular recalibration windows.

---

## KPI 8) Grid Resilience Composite Score
### Policy meaning
Single index combining multiple risk/progress signals for executive tracking.

### Example construction
1. Normalize KPI components to 0–100 scale.
2. Direction-correct metrics (higher-is-better vs lower-is-better).
3. Apply policy weights.
4. Compute weighted sum.

`resilience_composite = Σ(weight_i * normalized_component_i)`

### Suggested component set
- Renewable Share
- Carbon Intensity Proxy (inverted)
- Stress Index (inverted)
- Ramping Risk (inverted)
- Curtailment Proxy (inverted)
- Import Dependency (context-dependent weighting)
- Weather Sensitivity (context-dependent weighting)

### Caveats
- Weight choice is normative and must be justified.
- Include sensitivity analysis for alternative weight schemes.

---

## Data quality and governance requirements per KPI
For each KPI production model, enforce:
1. Null checks on key numerator/denominator fields.
2. Zero-denominator protection.
3. Accepted range tests for normalized outputs.
4. Timestamp continuity checks at target grain.
5. Source freshness thresholds.

---

## Reporting grain policy
- **Compute grain:** zone-hour (default)
- **Publish grains:** daily, weekly, monthly aggregates
- **Aggregation policy:**
  - Ratios: recompute from aggregated numerators/denominators (avoid averaging percentages when possible)
  - Volatility metrics: preserve distributional context (p50/p90)

---

## KPI ownership and change control
- KPI definitions are versioned.
- Any formula change requires:
  1. rationale,
  2. expected impact note,
  3. backfill/restate decision,
  4. dashboard annotation.

Use this changelog table:

| Date | KPI | Change | Reason | Impact |
|---|---|---|---|---|
| YYYY-MM-DD |  |  |  |  |
