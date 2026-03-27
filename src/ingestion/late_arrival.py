from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _parse_iso8601(ts: str) -> datetime:
    normalized = ts.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def classify_record_arrival(
    event_time_utc: str,
    ingestion_time_utc: str,
    allowed_lag_hours: float,
) -> str:
    event_dt = _parse_iso8601(event_time_utc)
    ingestion_dt = _parse_iso8601(ingestion_time_utc)

    lag_hours = (ingestion_dt - event_dt).total_seconds() / 3600.0
    return "late" if lag_hours > allowed_lag_hours else "on_time"


def summarize_late_arrivals(
    records: list[dict[str, Any]],
    allowed_lag_hours: float,
) -> dict[str, Any]:
    if not records:
        return {
            "record_count": 0,
            "late_count": 0,
            "negative_lag_count": 0,
            "late_ratio": 0.0,
            "min_lag_hours": 0.0,
            "max_lag_hours": 0.0,
        }

    late_count = 0
    negative_lag_count = 0
    min_lag_hours = float("inf")
    max_lag_hours = float("-inf")

    for record in records:
        event_dt = _parse_iso8601(str(record["event_time_utc"]))
        ingestion_dt = _parse_iso8601(str(record["ingestion_time_utc"]))
        lag_hours = (ingestion_dt - event_dt).total_seconds() / 3600.0
        min_lag_hours = min(min_lag_hours, lag_hours)
        max_lag_hours = max(max_lag_hours, lag_hours)

        if lag_hours < 0:
            negative_lag_count += 1

        if lag_hours > allowed_lag_hours:
            late_count += 1

    record_count = len(records)
    return {
        "record_count": record_count,
        "late_count": late_count,
        "negative_lag_count": negative_lag_count,
        "late_ratio": late_count / record_count,
        "min_lag_hours": round(min_lag_hours, 2),
        "max_lag_hours": round(max_lag_hours, 2),
    }


def load_watermark(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    return json.loads(path.read_text(encoding="utf-8"))


def update_watermark(path: Path, source_id: str, max_event_time_utc: str) -> dict[str, str]:
    payload = load_watermark(path)
    existing_value = payload.get(source_id)

    if existing_value is None or (
        _parse_iso8601(max_event_time_utc) >= _parse_iso8601(existing_value)
    ):
        payload[source_id] = max_event_time_utc

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def is_late_against_watermark(event_time_utc: str, current_watermark_utc: str) -> bool:
    return _parse_iso8601(event_time_utc) < _parse_iso8601(current_watermark_utc)


def main() -> None:
    sample_records = [
        {
            "event_time_utc": "2026-03-26T00:00:00+00:00",
            "ingestion_time_utc": "2026-03-26T02:00:00+00:00",
        },
        {
            "event_time_utc": "2026-03-24T00:00:00+00:00",
            "ingestion_time_utc": "2026-03-26T02:00:00+00:00",
        },
    ]

    print(json.dumps(summarize_late_arrivals(sample_records, allowed_lag_hours=24), indent=2))


if __name__ == "__main__":
    main()
