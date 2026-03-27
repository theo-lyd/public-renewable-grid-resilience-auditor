from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingestion.bronze_writer import BronzeWriteRequest, write_bronze_parquet
from src.ingestion.http_client import RetryConfig, RetryHttpClient
from src.ingestion.source_fetchers import fetch_ember_mix, fetch_entsoe_generation, fetch_open_meteo


def test_retry_http_client_has_backoff_and_retry_config() -> None:
    client = RetryHttpClient(RetryConfig(total=3, backoff_factor=0.5, timeout_seconds=10))
    adapter = client.session.get_adapter("https://")
    retries = adapter.max_retries

    assert retries.total == 3
    assert retries.backoff_factor == 0.5


def test_bronze_writer_is_idempotent_for_same_operation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("RAW_PARQUET_DIR", str(tmp_path / "raw"))
    monkeypatch.setenv("PROCESSED_PARQUET_DIR", str(tmp_path / "processed"))
    monkeypatch.setenv("REFERENCE_DATA_DIR", str(tmp_path / "reference"))
    monkeypatch.setenv("DUCKDB_PATH", str(tmp_path / "processed" / "test.duckdb"))

    request = BronzeWriteRequest(
        source_id="open_meteo",
        endpoint_id="historical_forecast_weather",
        window_start_utc="2026-03-26T00:00:00+00:00",
        window_end_utc="2026-03-26T02:59:59+00:00",
        request_params={"latitude": "52.52", "longitude": "13.41"},
        records=[{"timestamp_utc": "2026-03-26T00:00:00+00:00", "wind_speed_10m": 5.8}],
    )

    first = write_bronze_parquet(request)
    second = write_bronze_parquet(request)

    assert first.status == "written"
    assert second.status == "skipped_existing"
    assert first.operation_key == second.operation_key
    assert Path(first.data_file).exists()
    assert Path(first.metadata_file).exists()


def test_open_meteo_fetcher_reads_mock_payload() -> None:
    payload = fetch_open_meteo(
        latitude=52.52,
        longitude=13.41,
        start_date="2026-03-26",
        end_date="2026-03-26",
        mock_file=Path("data/reference/contracts/samples/open_meteo_sample.json"),
    )

    assert len(payload.records) == 3
    assert payload.records[0]["wind_speed_10m"] == 5.8


def test_ember_fetcher_reads_mock_payload() -> None:
    payload = fetch_ember_mix(
        country_code="DE",
        year=2026,
        mock_file=Path("data/reference/contracts/samples/ember_sample.csv"),
    )

    assert len(payload.records) == 2
    assert payload.records[0]["country_code"] == "DE"


def test_entsoe_fetcher_reads_mock_payload(monkeypatch) -> None:
    monkeypatch.delenv("ENTSOE_API_KEY", raising=False)
    payload = fetch_entsoe_generation(
        in_domain="10Y1001A1001A83F",
        period_start_utc="202603260000",
        period_end_utc="202603260300",
        mock_file=Path("data/reference/contracts/samples/entsoe_sample.xml"),
    )

    assert len(payload.records) == 3
    assert payload.records[0]["generation_mw"] == 1034.2


def test_bronze_metadata_contains_request_context(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("RAW_PARQUET_DIR", str(tmp_path / "raw"))
    monkeypatch.setenv("PROCESSED_PARQUET_DIR", str(tmp_path / "processed"))
    monkeypatch.setenv("REFERENCE_DATA_DIR", str(tmp_path / "reference"))
    monkeypatch.setenv("DUCKDB_PATH", str(tmp_path / "processed" / "test.duckdb"))

    request = BronzeWriteRequest(
        source_id="ember_electricity",
        endpoint_id="national_generation_mix",
        window_start_utc="2026-01-01T00:00:00+00:00",
        window_end_utc="2026-12-31T23:59:59+00:00",
        request_params={"country": "DE", "year": "2026"},
        records=[{"date": "2026-01-01", "country_code": "DE", "generation_twh": 2.35}],
    )

    result = write_bronze_parquet(request)
    metadata_df = pd.read_parquet(result.metadata_file)

    assert metadata_df.iloc[0]["source_id"] == "ember_electricity"
    assert metadata_df.iloc[0]["endpoint_id"] == "national_generation_mix"
    assert '"country": "DE"' in metadata_df.iloc[0]["request_params_json"]
