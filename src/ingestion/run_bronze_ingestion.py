from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.ingestion.bronze_writer import BronzeWriteRequest, serialize_result, write_bronze_parquet
from src.ingestion.source_fetchers import fetch_ember_mix, fetch_entsoe_generation, fetch_open_meteo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Bronze raw ingestion jobs")
    subparsers = parser.add_subparsers(dest="job", required=True)

    open_meteo = subparsers.add_parser("open-meteo", help="Ingest Open-Meteo weather covariates")
    open_meteo.add_argument("--latitude", type=float, required=True)
    open_meteo.add_argument("--longitude", type=float, required=True)
    open_meteo.add_argument("--start-date", required=True)
    open_meteo.add_argument("--end-date", required=True)
    open_meteo.add_argument("--mock-file", type=Path)

    ember = subparsers.add_parser("ember", help="Ingest Ember country electricity mix")
    ember.add_argument("--country-code", required=True)
    ember.add_argument("--year", type=int, required=True)
    ember.add_argument("--mock-file", type=Path)

    entsoe = subparsers.add_parser("entsoe", help="Ingest ENTSO-E generation data")
    entsoe.add_argument("--in-domain", required=True)
    entsoe.add_argument("--period-start-utc", required=True)
    entsoe.add_argument("--period-end-utc", required=True)
    entsoe.add_argument("--mock-file", type=Path)

    return parser


def run() -> dict:
    parser = build_parser()
    args = parser.parse_args()

    if args.job == "open-meteo":
        fetched = fetch_open_meteo(
            latitude=args.latitude,
            longitude=args.longitude,
            start_date=args.start_date,
            end_date=args.end_date,
            mock_file=args.mock_file,
        )
        write_request = BronzeWriteRequest(
            source_id="open_meteo",
            endpoint_id="historical_forecast_weather",
            window_start_utc=fetched.window_start_utc,
            window_end_utc=fetched.window_end_utc,
            request_params=fetched.request_params,
            records=fetched.records,
        )
    elif args.job == "ember":
        fetched = fetch_ember_mix(
            country_code=args.country_code,
            year=args.year,
            mock_file=args.mock_file,
        )
        write_request = BronzeWriteRequest(
            source_id="ember_electricity",
            endpoint_id="national_generation_mix",
            window_start_utc=fetched.window_start_utc,
            window_end_utc=fetched.window_end_utc,
            request_params=fetched.request_params,
            records=fetched.records,
        )
    else:
        fetched = fetch_entsoe_generation(
            in_domain=args.in_domain,
            period_start_utc=args.period_start_utc,
            period_end_utc=args.period_end_utc,
            mock_file=args.mock_file,
        )
        write_request = BronzeWriteRequest(
            source_id="entsoe_transparency",
            endpoint_id="generation_actual_per_type",
            window_start_utc=fetched.window_start_utc,
            window_end_utc=fetched.window_end_utc,
            request_params=fetched.request_params,
            records=fetched.records,
        )

    result = write_bronze_parquet(write_request)
    return serialize_result(result)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
