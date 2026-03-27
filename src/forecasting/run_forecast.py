from __future__ import annotations

import argparse
import json
from datetime import timedelta

import duckdb
import pandas as pd

from src.common.config import get_project_paths
from src.forecasting.baseline import backtest_one_step, forecast_horizon
from src.forecasting.scenarios import apply_scenario_adjustments, resolve_scenario


def _load_daily_series() -> pd.DataFrame:
    paths = get_project_paths()

    query = """
        select
            zone_code,
            cast(date_utc as date) as date_utc,
            renewable_share_pct,
            supply_demand_stress_index,
            weather_sensitivity_score
        from main_marts.mart_zone_day_kpi_scorecard
        order by zone_code, date_utc
    """

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        try:
            frame = conn.execute(query).df()
        except duckdb.Error as err:
            raise RuntimeError(
                "Forecast source mart not found. Run `make dbt-marts` before forecasting."
            ) from err

    if frame.empty:
        raise RuntimeError("Forecast source mart is empty. Forecasting cannot run.")

    return frame


def _build_zone_forecast(
    zone_frame: pd.DataFrame,
    zone_code: str,
    horizon_days: int,
    method: str,
    window: int,
) -> tuple[pd.DataFrame, dict[str, float | str | int | None]]:
    zone_frame = zone_frame.sort_values("date_utc").reset_index(drop=True)

    renewable_series = _coerce_series(zone_frame["renewable_share_pct"], default_value=0.0)
    stress_series = _coerce_series(
        zone_frame["supply_demand_stress_index"],
        default_value=1.0,
    )
    weather_series = _coerce_series(
        zone_frame["weather_sensitivity_score"],
        default_value=0.0,
    )

    renewable_bt = None
    if len(zone_frame) >= 4:
        renewable_bt = backtest_one_step(renewable_series, method=method, window=window)

    last_date = pd.to_datetime(zone_frame["date_utc"].iloc[-1]).date()
    forecast_dates = [last_date + timedelta(days=step) for step in range(1, horizon_days + 1)]

    forecast_frame = pd.DataFrame(
        {
            "zone_code": zone_code,
            "forecast_date": forecast_dates,
            "renewable_share_pct_forecast": forecast_horizon(
                renewable_series,
                horizon_days=horizon_days,
                method=method,
                window=window,
            ),
            "supply_demand_stress_index_forecast": forecast_horizon(
                stress_series,
                horizon_days=horizon_days,
                method=method,
                window=window,
            ),
            "weather_sensitivity_score_forecast": forecast_horizon(
                weather_series,
                horizon_days=horizon_days,
                method=method,
                window=window,
            ),
        }
    )

    if renewable_bt is None:
        backtest_summary = {
            "zone_code": zone_code,
            "method": method,
            "n_obs": 0,
            "mae": None,
            "rmse": None,
            "mape": None,
            "status": "insufficient_history_fallback",
        }
    else:
        backtest_summary = {
            "zone_code": zone_code,
            "method": renewable_bt.method,
            "n_obs": renewable_bt.n_obs,
            "mae": round(renewable_bt.mae, 4),
            "rmse": round(renewable_bt.rmse, 4),
            "mape": round(renewable_bt.mape, 4),
            "status": "ok",
        }

    return forecast_frame, backtest_summary


def _coerce_series(series: pd.Series, default_value: float) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.dropna().empty:
        return pd.Series([default_value], dtype="float64")

    return numeric.ffill().bfill().fillna(default_value).astype("float64")


def run_phase9_forecast(
    horizon_days: int,
    method: str,
    window: int,
    scenario_id: str,
) -> dict[str, object]:
    frame = _load_daily_series()

    scenario, used_fallback = resolve_scenario(scenario_id)

    outputs: list[pd.DataFrame] = []
    backtests: list[dict[str, float | str | int | None]] = []

    for zone_code, zone_frame in frame.groupby("zone_code"):
        zone_forecast, zone_backtest = _build_zone_forecast(
            zone_frame=zone_frame,
            zone_code=zone_code,
            horizon_days=horizon_days,
            method=method,
            window=window,
        )
        outputs.append(zone_forecast)
        backtests.append(zone_backtest)

    if not outputs:
        raise RuntimeError("No forecast rows generated from source mart.")

    forecast = pd.concat(outputs, ignore_index=True)
    forecast = apply_scenario_adjustments(forecast, scenario)

    return {
        "scenario_requested": scenario_id,
        "scenario_applied": scenario.scenario_id,
        "fallback_applied": used_fallback,
        "forecast_rows": len(forecast),
        "forecast_preview": forecast.head(10).to_dict(orient="records"),
        "backtest_summary": backtests,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 9 baseline forecasting and scenario runner")
    parser.add_argument("--horizon-days", type=int, default=7)
    parser.add_argument(
        "--method",
        type=str,
        default="moving_average",
        choices=["moving_average", "naive"],
    )
    parser.add_argument("--window", type=int, default=3)
    parser.add_argument("--scenario", type=str, default="baseline")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = run_phase9_forecast(
        horizon_days=args.horizon_days,
        method=args.method,
        window=args.window,
        scenario_id=args.scenario,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
