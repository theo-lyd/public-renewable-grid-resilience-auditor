from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ScenarioDefinition:
    scenario_id: str
    renewable_share_multiplier: float
    stress_index_multiplier: float
    weather_sensitivity_multiplier: float
    description: str


SCENARIO_CATALOG: dict[str, ScenarioDefinition] = {
    "baseline": ScenarioDefinition(
        scenario_id="baseline",
        renewable_share_multiplier=1.00,
        stress_index_multiplier=1.00,
        weather_sensitivity_multiplier=1.00,
        description="Reference outlook with no exogenous uplift or shock.",
    ),
    "security_stress": ScenarioDefinition(
        scenario_id="security_stress",
        renewable_share_multiplier=0.92,
        stress_index_multiplier=1.10,
        weather_sensitivity_multiplier=1.05,
        description="Stress case: lower renewable output and tighter supply-demand balance.",
    ),
    "transition_acceleration": ScenarioDefinition(
        scenario_id="transition_acceleration",
        renewable_share_multiplier=1.08,
        stress_index_multiplier=0.95,
        weather_sensitivity_multiplier=0.95,
        description="Policy acceleration case: higher renewable deployment and smoother balancing.",
    ),
}


def resolve_scenario(scenario_id: str | None) -> tuple[ScenarioDefinition, bool]:
    if not scenario_id:
        return SCENARIO_CATALOG["baseline"], True

    scenario = SCENARIO_CATALOG.get(scenario_id)
    if scenario is None:
        return SCENARIO_CATALOG["baseline"], True

    return scenario, False


def apply_scenario_adjustments(
    forecast_frame: pd.DataFrame,
    scenario: ScenarioDefinition,
) -> pd.DataFrame:
    adjusted = forecast_frame.copy()

    adjusted["renewable_share_pct_forecast"] = (
        adjusted["renewable_share_pct_forecast"] * scenario.renewable_share_multiplier
    ).clip(lower=0.0, upper=100.0)

    adjusted["supply_demand_stress_index_forecast"] = (
        adjusted["supply_demand_stress_index_forecast"] * scenario.stress_index_multiplier
    ).clip(lower=0.0)

    adjusted["weather_sensitivity_score_forecast"] = (
        adjusted["weather_sensitivity_score_forecast"] * scenario.weather_sensitivity_multiplier
    ).clip(lower=0.0, upper=1.0)

    adjusted["scenario_id"] = scenario.scenario_id
    adjusted["scenario_description"] = scenario.description

    return adjusted
