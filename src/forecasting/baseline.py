from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    method: str
    n_obs: int
    mae: float
    rmse: float
    mape: float


def _to_series(values: pd.Series | list[float] | np.ndarray) -> pd.Series:
    series = pd.Series(values, dtype="float64").dropna().reset_index(drop=True)
    if series.empty:
        raise ValueError("Input series is empty after dropping nulls.")
    return series


def forecast_next(
    values: pd.Series | list[float] | np.ndarray,
    method: str = "moving_average",
    window: int = 3,
) -> float:
    series = _to_series(values)

    if method == "naive":
        return float(series.iloc[-1])

    if method == "moving_average":
        win = max(1, min(window, len(series)))
        return float(series.tail(win).mean())

    raise ValueError(f"Unsupported baseline method: {method}")


def forecast_horizon(
    values: pd.Series | list[float] | np.ndarray,
    horizon_days: int,
    method: str = "moving_average",
    window: int = 3,
) -> list[float]:
    if horizon_days <= 0:
        raise ValueError("horizon_days must be > 0")

    history = _to_series(values).tolist()
    forecasts: list[float] = []

    for _ in range(horizon_days):
        prediction = forecast_next(history, method=method, window=window)
        forecasts.append(prediction)
        history.append(prediction)

    return forecasts


def backtest_one_step(
    values: pd.Series | list[float] | np.ndarray,
    method: str = "moving_average",
    window: int = 3,
    min_train_size: int = 3,
) -> BacktestResult:
    series = _to_series(values)

    if len(series) <= min_train_size:
        raise ValueError("Series length must be greater than min_train_size for backtesting.")

    y_true: list[float] = []
    y_pred: list[float] = []

    for idx in range(min_train_size, len(series)):
        train = series.iloc[:idx]
        pred = forecast_next(train, method=method, window=window)
        y_pred.append(pred)
        y_true.append(float(series.iloc[idx]))

    errors = np.array(y_true) - np.array(y_pred)
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(np.square(errors))))

    with np.errstate(divide="ignore", invalid="ignore"):
        pct_errors = np.where(
            np.array(y_true) != 0,
            np.abs(errors) / np.abs(np.array(y_true)),
            np.nan,
        )
    mape = float(np.nanmean(pct_errors) * 100.0) if not np.all(np.isnan(pct_errors)) else 0.0

    return BacktestResult(method=method, n_obs=len(y_true), mae=mae, rmse=rmse, mape=mape)
