from __future__ import annotations

import json

import duckdb

from src.common.config import get_project_paths
from src.monitoring.dashboard_narrative import validate_metric_catalog

REQUIRED_METRICS = {
    "renewable_share_pct",
    "carbon_intensity_proxy_tco2_per_mwh",
    "supply_demand_stress_index",
    "ramping_risk_index",
    "curtailment_proxy_pct",
    "weather_sensitivity_score",
    "resilience_composite_baseline",
}

REQUIRED_TABLES = [
    "main_marts.mart_zone_hour_kpi_scorecard",
    "main_marts.mart_zone_day_kpi_scorecard",
    "main_marts.mart_zone_day_resilience_composite",
]


def _table_exists(conn: duckdb.DuckDBPyConnection, full_name: str) -> bool:
    schema_name, table_name = full_name.split(".")

    query = """
        select count(*)
        from information_schema.tables
        where table_schema = ? and table_name = ?
    """
    count = conn.execute(query, [schema_name, table_name]).fetchone()[0]
    return count > 0


def run_dashboard_smoke() -> dict[str, object]:
    paths = get_project_paths()

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        table_status = {table: _table_exists(conn, table) for table in REQUIRED_TABLES}

        latest_zone_count = conn.execute(
            """
            select count(distinct zone_code)
            from main_marts.mart_zone_day_kpi_scorecard
            """
        ).fetchone()[0]

    narrative_status = validate_metric_catalog(REQUIRED_METRICS)

    all_tables_present = all(table_status.values())
    is_valid = all_tables_present and narrative_status["is_valid"]

    return {
        "is_valid": is_valid,
        "tables": table_status,
        "latest_zone_count": latest_zone_count,
        "narrative_status": narrative_status,
    }


def main() -> None:
    result = run_dashboard_smoke()
    print(json.dumps(result, indent=2))

    if not result["is_valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
