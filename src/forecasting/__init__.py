"""Forecasting and scenario planning modules."""

from src.forecasting.baseline import (
    BacktestResult,
    backtest_one_step,
    forecast_horizon,
    forecast_next,
)
from src.forecasting.scenarios import (
    SCENARIO_CATALOG,
    apply_scenario_adjustments,
    resolve_scenario,
)

__all__ = [
    "BacktestResult",
    "SCENARIO_CATALOG",
    "apply_scenario_adjustments",
    "backtest_one_step",
    "forecast_horizon",
    "forecast_next",
    "resolve_scenario",
]
