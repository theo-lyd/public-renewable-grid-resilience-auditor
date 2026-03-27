from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricNarrativeCard:
    metric_id: str
    title: str
    plain_language_explanation: str
    technical_definition: str
    caveat: str


METRIC_CATALOG: dict[str, MetricNarrativeCard] = {
    "renewable_share_pct": MetricNarrativeCard(
        metric_id="renewable_share_pct",
        title="Renewable Share (%)",
        plain_language_explanation="Shows how much of generation comes from renewable sources.",
        technical_definition=("100 * renewable_gen_mwh / nullif(total_gen_mwh, 0)"),
        caveat="Can be sensitive to fuel mapping quality and sparse source history.",
    ),
    "carbon_intensity_proxy_tco2_per_mwh": MetricNarrativeCard(
        metric_id="carbon_intensity_proxy_tco2_per_mwh",
        title="Carbon Intensity Proxy",
        plain_language_explanation=(
            "Estimates emissions intensity using available generation mix proxies."
        ),
        technical_definition="co2_proxy_tonnes / nullif(total_gen_mwh, 0)",
        caveat="Proxy only; not a legal-grade verified emissions inventory.",
    ),
    "supply_demand_stress_index": MetricNarrativeCard(
        metric_id="supply_demand_stress_index",
        title="Supply-Demand Stress Index",
        plain_language_explanation=(
            "Measures how tight supply appears relative to expected demand pressure."
        ),
        technical_definition=(
            "total_gen_mwh / nullif(renewable_gen_mwh + (0.25 * total_gen_mwh), 0)"
        ),
        caveat=(
            "Interpreted as a proxy because full load and reserve inputs are not " "yet integrated."
        ),
    ),
    "ramping_risk_index": MetricNarrativeCard(
        metric_id="ramping_risk_index",
        title="Ramping Risk Index",
        plain_language_explanation=(
            "Highlights rapid hour-to-hour generation change that can stress balancing operations."
        ),
        technical_definition=(
            "abs(total_gen_mwh_t - total_gen_mwh_t-1) / nullif(total_gen_mwh_t, 0)"
        ),
        caveat="Sensitive to granularity and short historical windows.",
    ),
    "curtailment_proxy_pct": MetricNarrativeCard(
        metric_id="curtailment_proxy_pct",
        title="Curtailment Proxy (%)",
        plain_language_explanation=(
            "Estimates potential renewable spill where modeled potential exceeds observed output."
        ),
        technical_definition=(
            "100 * curtailment_proxy_mwh / nullif(renewable_gen_mwh + curtailment_proxy_mwh, 0)"
        ),
        caveat="Represents inferred spill risk, not measured curtailment telemetry.",
    ),
    "weather_sensitivity_score": MetricNarrativeCard(
        metric_id="weather_sensitivity_score",
        title="Weather Sensitivity Score",
        plain_language_explanation=(
            "Indicates how strongly renewable outcomes move with weather variation."
        ),
        technical_definition=("abs(corr(renewable_gen_mwh, weather_index)) at daily zone grain"),
        caveat="Can be unstable with short history and sparse weather variability.",
    ),
    "resilience_composite_baseline": MetricNarrativeCard(
        metric_id="resilience_composite_baseline",
        title="Grid Resilience Composite (Baseline)",
        plain_language_explanation=(
            "Combines multiple KPI dimensions into a single 0-100 resilience score."
        ),
        technical_definition=(
            "Weighted sum of normalized KPI components using baseline policy weights"
        ),
        caveat="Weighting is normative; compare with sensitivity variants before decisions.",
    ),
}


def get_metric_cards() -> list[MetricNarrativeCard]:
    return list(METRIC_CATALOG.values())


def validate_metric_catalog(required_metric_ids: set[str]) -> dict[str, object]:
    available = set(METRIC_CATALOG)
    missing = sorted(required_metric_ids - available)

    return {
        "required_count": len(required_metric_ids),
        "available_count": len(available),
        "missing_metric_ids": missing,
        "is_valid": len(missing) == 0,
    }
