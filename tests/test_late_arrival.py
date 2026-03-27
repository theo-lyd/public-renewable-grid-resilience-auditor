from pathlib import Path

from src.ingestion.late_arrival import (
    classify_record_arrival,
    is_late_against_watermark,
    load_watermark,
    summarize_late_arrivals,
    update_watermark,
)


def test_classify_record_arrival() -> None:
    assert (
        classify_record_arrival(
            event_time_utc="2026-03-26T00:00:00+00:00",
            ingestion_time_utc="2026-03-26T02:00:00+00:00",
            allowed_lag_hours=6,
        )
        == "on_time"
    )
    assert (
        classify_record_arrival(
            event_time_utc="2026-03-24T00:00:00+00:00",
            ingestion_time_utc="2026-03-26T02:00:00+00:00",
            allowed_lag_hours=24,
        )
        == "late"
    )


def test_summarize_late_arrivals() -> None:
    records = [
        {
            "event_time_utc": "2026-03-26T00:00:00+00:00",
            "ingestion_time_utc": "2026-03-26T02:00:00+00:00",
        },
        {
            "event_time_utc": "2026-03-24T00:00:00+00:00",
            "ingestion_time_utc": "2026-03-26T02:00:00+00:00",
        },
    ]

    summary = summarize_late_arrivals(records, allowed_lag_hours=24)
    assert summary["record_count"] == 2
    assert summary["late_count"] == 1


def test_watermark_round_trip(tmp_path: Path) -> None:
    watermark_path = tmp_path / "watermark.json"
    update_watermark(watermark_path, "entsoe_transparency", "2026-03-26T03:00:00+00:00")

    payload = load_watermark(watermark_path)
    assert payload["entsoe_transparency"] == "2026-03-26T03:00:00+00:00"


def test_late_against_watermark() -> None:
    assert is_late_against_watermark("2026-03-25T23:00:00+00:00", "2026-03-26T00:00:00+00:00")
    assert not is_late_against_watermark("2026-03-26T01:00:00+00:00", "2026-03-26T00:00:00+00:00")
