from __future__ import annotations

import json
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


def run_performance_benchmark() -> dict[str, object]:
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

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        full_seconds, full_rows = _run_timed_query(conn, full_query)
        filtered_seconds, filtered_rows = _run_timed_query(conn, filtered_query)

    tactics = [
        "Date-window filtering for partition pruning behavior",
        "Aggregation pushdown in DuckDB SQL",
        "Keep marts at daily grain to reduce repeated heavy joins",
    ]

    return {
        "full_scan_seconds": round(full_seconds, 6),
        "filtered_scan_seconds": round(filtered_seconds, 6),
        "speedup_ratio": round(calculate_speedup(full_seconds, filtered_seconds), 4),
        "full_result_rows": full_rows,
        "filtered_result_rows": filtered_rows,
        "tactics": tactics,
    }


def main() -> None:
    print(json.dumps(run_performance_benchmark(), indent=2))


if __name__ == "__main__":
    main()
