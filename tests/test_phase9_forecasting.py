import pandas as pd

from src.forecasting.baseline import backtest_one_step, forecast_horizon, forecast_next
from src.forecasting.scenarios import SCENARIO_CATALOG, apply_scenario_adjustments, resolve_scenario


def test_forecast_next_methods() -> None:
    series = [10.0, 12.0, 14.0]

    assert forecast_next(series, method="naive") == 14.0
    assert forecast_next(series, method="moving_average", window=2) == 13.0


def test_forecast_horizon_and_backtest() -> None:
    series = [10.0, 12.0, 14.0, 16.0, 18.0]

    horizon = forecast_horizon(series, horizon_days=3, method="moving_average", window=2)
    assert len(horizon) == 3
    assert all(value >= 0 for value in horizon)

    result = backtest_one_step(series, method="naive", min_train_size=3)
    assert result.n_obs == 2
    assert result.mae >= 0
    assert result.rmse >= 0


def test_scenario_resolution_and_fallback() -> None:
    baseline_scenario, used_fallback = resolve_scenario("baseline")
    assert baseline_scenario.scenario_id == "baseline"
    assert used_fallback is False

    fallback_scenario, fallback_used = resolve_scenario("unknown_scenario")
    assert fallback_scenario.scenario_id == "baseline"
    assert fallback_used is True


def test_apply_scenario_adjustments() -> None:
    frame = pd.DataFrame(
        {
            "zone_code": ["DE"],
            "forecast_date": [pd.Timestamp("2026-01-02")],
            "renewable_share_pct_forecast": [50.0],
            "supply_demand_stress_index_forecast": [1.0],
            "weather_sensitivity_score_forecast": [0.5],
        }
    )

    adjusted = apply_scenario_adjustments(frame, SCENARIO_CATALOG["transition_acceleration"])

    assert adjusted.loc[0, "renewable_share_pct_forecast"] > 50.0
    assert adjusted.loc[0, "scenario_id"] == "transition_acceleration"
