from __future__ import annotations

import json
from datetime import UTC, datetime

import duckdb
import pandas as pd

from src.common.config import get_project_paths
from src.monitoring.phase11_policy import Phase11Policy, load_phase11_policy


def compute_relative_drift(current_value: float, baseline_value: float) -> float:
    if baseline_value == 0:
        return abs(current_value - baseline_value)

    return abs(current_value - baseline_value) / abs(baseline_value)


def classify_severity(drift_value: float, warn_threshold: float, critical_threshold: float) -> str:
    if drift_value >= critical_threshold:
        return "critical"
    if drift_value >= warn_threshold:
        return "warning"
    return "info"


def evaluate_zone_drift(zone_frame: pd.DataFrame, policy: Phase11Policy) -> list[dict[str, object]]:
    ordered = zone_frame.sort_values("date_utc").reset_index(drop=True)
    if ordered.empty:
        return []

    latest = ordered.iloc[-1]
    history = ordered.iloc[:-1]

    if history.empty:
        return [
            {
                "metric": "history",
                "severity": "info",
                "status": "insufficient_history",
                "route": policy.alert_routing.info,
            }
        ]

    stress_baseline = float(history["supply_demand_stress_index"].mean())
    renewable_baseline = float(history["renewable_share_pct"].mean())

    stress_drift = compute_relative_drift(
        current_value=float(latest["supply_demand_stress_index"]),
        baseline_value=stress_baseline,
    )
    renewable_drift = compute_relative_drift(
        current_value=float(latest["renewable_share_pct"]),
        baseline_value=renewable_baseline,
    )

    stress_severity = classify_severity(
        drift_value=stress_drift,
        warn_threshold=policy.drift.stress_index_warn,
        critical_threshold=policy.drift.stress_index_critical,
    )
    renewable_severity = classify_severity(
        drift_value=renewable_drift,
        warn_threshold=policy.drift.renewable_share_warn,
        critical_threshold=policy.drift.renewable_share_critical,
    )

    return [
        {
            "metric": "supply_demand_stress_index",
            "current": float(latest["supply_demand_stress_index"]),
            "baseline": stress_baseline,
            "drift_ratio": stress_drift,
            "severity": stress_severity,
            "route": getattr(policy.alert_routing, stress_severity),
        },
        {
            "metric": "renewable_share_pct",
            "current": float(latest["renewable_share_pct"]),
            "baseline": renewable_baseline,
            "drift_ratio": renewable_drift,
            "severity": renewable_severity,
            "route": getattr(policy.alert_routing, renewable_severity),
        },
    ]


def _load_daily_mart_frame() -> pd.DataFrame:
    paths = get_project_paths()
    query = """
        select
            zone_code,
            cast(date_utc as date) as date_utc,
            renewable_share_pct,
            supply_demand_stress_index
        from main_marts.mart_zone_day_kpi_scorecard
        order by zone_code, date_utc
    """

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        return conn.execute(query).df()


def run_phase11_monitoring() -> dict[str, object]:
    policy = load_phase11_policy()
    frame = _load_daily_mart_frame()

    if frame.empty:
        raise RuntimeError("Daily mart is empty. Run `make dbt-marts` before monitoring checks.")

    latest_date = pd.to_datetime(frame["date_utc"].max())
    now_utc = datetime.now(UTC)
    freshness_delta = now_utc - latest_date.to_pydatetime().replace(tzinfo=UTC)
    freshness_hours = freshness_delta.total_seconds() / 3600.0

    freshness_ok = freshness_hours <= policy.sla.freshness_hours_max

    zone_alerts: dict[str, list[dict[str, object]]] = {}
    for zone_code, zone_frame in frame.groupby("zone_code"):
        zone_alerts[str(zone_code)] = evaluate_zone_drift(zone_frame, policy)

    severities = [
        alert["severity"]
        for alerts in zone_alerts.values()
        for alert in alerts
        if "severity" in alert
    ]
    critical_count = sum(1 for severity in severities if severity == "critical")
    warning_count = sum(1 for severity in severities if severity == "warning")

    overall_status = "ok"
    if not freshness_ok or critical_count > 0:
        overall_status = "critical"
    elif warning_count > 0:
        overall_status = "warning"

    dag_dependency_graph = [
        "bronze_ingestion",
        "dbt_staging",
        "dbt_intermediate",
        "dbt_dimensions_facts",
        "dbt_marts",
        "forecast_phase9",
        "dashboard_smoke",
        "monitor_phase11",
    ]

    return {
        "overall_status": overall_status,
        "freshness_hours": round(freshness_hours, 2),
        "freshness_ok": freshness_ok,
        "sla_hours_max": policy.sla.freshness_hours_max,
        "alerts_by_zone": zone_alerts,
        "critical_alert_count": critical_count,
        "warning_alert_count": warning_count,
        "dag_dependency_graph": dag_dependency_graph,
        "backfill_policy": policy.backfill.model_dump(),
    }


def main() -> None:
    result = run_phase11_monitoring()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
