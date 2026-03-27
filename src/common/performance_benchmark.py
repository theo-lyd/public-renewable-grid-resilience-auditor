from __future__ import annotations

import json
import statistics
import time

import duckdb

from src.common.config import get_project_paths


def _run_timed_query(conn: duckdb.DuckDBPyConnection, query: str) -> tuple[float, int]:
    start = time.perf_counter()
    frame = conn.execute(query).df()
    elapsed = time.perf_counter() - start
    return elapsed, len(frame)


def calculate_speedup(full_scan_seconds: float, filtered_seconds: float) -> float:
    if filtered_seconds <= 0:
        return 0.0
    return full_scan_seconds / filtered_seconds


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    last_index = len(sorted_values) - 1
    rank = (percentile / 100.0) * last_index
    lower_index = int(rank)
    upper_index = min(lower_index + 1, last_index)
    blend = rank - lower_index
    return sorted_values[lower_index] * (1.0 - blend) + sorted_values[upper_index] * blend


def _coefficient_of_variation(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    mean_value = statistics.mean(values)
    if mean_value <= 0:
        return 0.0

    return statistics.stdev(values) / mean_value


def run_performance_benchmark(repetitions: int = 7, warmup_runs: int = 2) -> dict[str, object]:
    paths = get_project_paths()

    full_query = """
        select
            zone_code,
            avg(renewable_share_pct) as renewable_share_avg,
            avg(supply_demand_stress_index) as stress_avg
        from main_marts.mart_zone_day_kpi_scorecard
        group by 1
    """

    filtered_query = """
        select
            zone_code,
            avg(renewable_share_pct) as renewable_share_avg,
            avg(supply_demand_stress_index) as stress_avg
        from main_marts.mart_zone_day_kpi_scorecard
        where date_utc >= current_date - interval '7 day'
        group by 1
    """

    repetitions = max(1, repetitions)
    warmup_runs = max(0, warmup_runs)

    full_timings: list[float] = []
    filtered_timings: list[float] = []
    speedup_samples: list[float] = []
    full_rows = 0
    filtered_rows = 0

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        for _ in range(warmup_runs):
            _run_timed_query(conn, full_query)
            _run_timed_query(conn, filtered_query)

        for _ in range(repetitions):
            full_seconds, full_rows = _run_timed_query(conn, full_query)
            filtered_seconds, filtered_rows = _run_timed_query(conn, filtered_query)
            full_timings.append(full_seconds)
            filtered_timings.append(filtered_seconds)
            speedup_samples.append(calculate_speedup(full_seconds, filtered_seconds))

    full_scan_median = statistics.median(full_timings)
    filtered_scan_median = statistics.median(filtered_timings)
    speedup_median = statistics.median(speedup_samples)

    tactics = [
        "Date-window filtering for partition pruning behavior",
        "Aggregation pushdown in DuckDB SQL",
        "Keep marts at daily grain to reduce repeated heavy joins",
    ]

    return {
        "full_scan_seconds": round(full_scan_median, 6),
        "filtered_scan_seconds": round(filtered_scan_median, 6),
        "speedup_ratio": round(speedup_median, 4),
        "full_result_rows": full_rows,
        "filtered_result_rows": filtered_rows,
        "repetitions": repetitions,
        "warmup_runs": warmup_runs,
        "speedup_ratio_min": round(min(speedup_samples), 4),
        "speedup_ratio_max": round(max(speedup_samples), 4),
        "speedup_ratio_p95": round(_percentile(speedup_samples, 95), 4),
        "speedup_ratio_cv": round(_coefficient_of_variation(speedup_samples), 4),
        "tactics": tactics,
    }


def main() -> None:
    print(json.dumps(run_performance_benchmark(), indent=2))


if __name__ == "__main__":
    main()
