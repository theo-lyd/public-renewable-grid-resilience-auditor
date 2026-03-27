from __future__ import annotations

import csv
import json
import os
import xml.etree.ElementTree as et
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from src.ingestion.http_client import RetryHttpClient


@dataclass(frozen=True)
class FetchedPayload:
    records: list[dict]
    request_params: dict[str, str]
    window_start_utc: str
    window_end_utc: str


def fetch_open_meteo(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    mock_file: Path | None = None,
) -> FetchedPayload:
    request_params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "hourly": "wind_speed_10m,shortwave_radiation,temperature_2m",
        "timezone": "UTC",
        "start_date": start_date,
        "end_date": end_date,
    }

    if mock_file:
        payload = json.loads(mock_file.read_text(encoding="utf-8"))
    else:
        client = RetryHttpClient()
        payload = client.get_json("https://api.open-meteo.com/v1/forecast", params=request_params)

    hourly = payload["hourly"]
    hourly_times = hourly["time"]
    wind_values = hourly.get("wind_speed_10m", [None] * len(hourly_times))
    radiation_values = hourly.get("shortwave_radiation", [None] * len(hourly_times))
    temperature_values = hourly.get("temperature_2m", [None] * len(hourly_times))

    records = []
    for index, timestamp in enumerate(hourly_times):
        records.append(
            {
                "timestamp_utc": timestamp,
                "latitude": latitude,
                "longitude": longitude,
                "wind_speed_10m": wind_values[index],
                "shortwave_radiation": radiation_values[index],
                "temperature_2m": temperature_values[index],
            }
        )

    return FetchedPayload(
        records=records,
        request_params=request_params,
        window_start_utc=f"{start_date}T00:00:00+00:00",
        window_end_utc=f"{end_date}T23:59:59+00:00",
    )


def fetch_ember_mix(country_code: str, year: int, mock_file: Path | None = None) -> FetchedPayload:
    request_params = {
        "country": country_code,
        "year": str(year),
        "metric": "generation_mix",
    }

    if mock_file:
        csv_text = mock_file.read_text(encoding="utf-8")
    else:
        url = "https://ember-energy.org/latest-data.csv"
        client = RetryHttpClient()
        csv_text = client.get_text(url)

    rows = list(csv.DictReader(csv_text.splitlines()))
    records: list[dict] = []
    for row in rows:
        if row.get("country_code") == country_code and int(row.get("year", year)) == year:
            records.append(
                {
                    "date": row.get("date"),
                    "country_code": row.get("country_code"),
                    "fuel_category": row.get("fuel_category"),
                    "generation_twh": float(row.get("generation_twh", 0.0)),
                }
            )

    window_start = f"{year}-01-01T00:00:00+00:00"
    window_end = f"{year}-12-31T23:59:59+00:00"
    return FetchedPayload(
        records=records,
        request_params=request_params,
        window_start_utc=window_start,
        window_end_utc=window_end,
    )


def fetch_entsoe_generation(
    in_domain: str,
    period_start_utc: str,
    period_end_utc: str,
    mock_file: Path | None = None,
) -> FetchedPayload:
    token = os.getenv("ENTSOE_API_KEY", "")
    if not token and mock_file is None:
        raise ValueError("ENTSOE_API_KEY is required for live ENTSO-E ingestion")

    request_params = {
        "documentType": "A75",
        "processType": "A16",
        "in_Domain": in_domain,
        "periodStart": period_start_utc,
        "periodEnd": period_end_utc,
        "securityToken": token,
    }

    if mock_file:
        xml_text = mock_file.read_text(encoding="utf-8")
    else:
        client = RetryHttpClient()
        xml_text = client.get_text("https://web-api.tp.entsoe.eu/api", params=request_params)

    root = et.fromstring(xml_text)
    records = _parse_entsoe_points(root, in_domain, period_start_utc)

    window_start = _format_entsoe_period(period_start_utc)
    window_end = _format_entsoe_period(period_end_utc)
    return FetchedPayload(
        records=records,
        request_params=request_params,
        window_start_utc=window_start,
        window_end_utc=window_end,
    )


def _format_entsoe_period(value: str) -> str:
    dt = datetime.strptime(value, "%Y%m%d%H%M")
    return dt.replace(tzinfo=UTC).isoformat()


def _parse_entsoe_points(root: et.Element, zone_code: str, period_start_utc: str) -> list[dict]:
    base_time = datetime.strptime(period_start_utc, "%Y%m%d%H%M").replace(tzinfo=UTC)
    records: list[dict] = []

    for point in root.findall(".//{*}Point"):
        position_text = point.findtext("{*}position")
        quantity_text = point.findtext("{*}quantity")
        if not position_text or not quantity_text:
            continue

        position = int(position_text)
        timestamp = base_time + timedelta(hours=position - 1)
        records.append(
            {
                "timestamp_utc": timestamp.isoformat(),
                "zone_code": zone_code,
                "generation_mw": float(quantity_text),
                "position": position,
            }
        )

    return records
