from pathlib import Path

import pandas as pd

from src.monitoring.phase11_monitoring import (
    classify_severity,
    compute_relative_drift,
    evaluate_zone_drift,
)
from src.monitoring.phase11_policy import load_phase11_policy


def test_phase11_policy_loads() -> None:
    policy = load_phase11_policy()
    assert policy.sla.freshness_hours_max > 0
    assert policy.backfill.max_backfill_days > 0


def test_compute_relative_drift() -> None:
    assert compute_relative_drift(120.0, 100.0) == 0.2
    assert compute_relative_drift(5.0, 0.0) == 5.0


def test_classify_severity() -> None:
    assert classify_severity(0.8, warn_threshold=0.3, critical_threshold=0.7) == "critical"
    assert classify_severity(0.5, warn_threshold=0.3, critical_threshold=0.7) == "warning"
    assert classify_severity(0.1, warn_threshold=0.3, critical_threshold=0.7) == "info"


def test_evaluate_zone_drift() -> None:
    policy = load_phase11_policy()

    frame = pd.DataFrame(
        {
            "zone_code": ["DE", "DE", "DE", "DE"],
            "date_utc": pd.to_datetime(["2026-03-24", "2026-03-25", "2026-03-26", "2026-03-27"]),
            "renewable_share_pct": [40.0, 41.0, 39.0, 50.0],
            "supply_demand_stress_index": [0.9, 0.95, 0.92, 1.2],
        }
    )

    alerts = evaluate_zone_drift(frame, policy)
    assert len(alerts) == 2
    assert {alert["metric"] for alert in alerts} == {
        "supply_demand_stress_index",
        "renewable_share_pct",
    }


def test_policy_file_exists() -> None:
    policy_path = Path("data/reference/monitoring/phase11_policy.yaml")
    assert policy_path.exists()
