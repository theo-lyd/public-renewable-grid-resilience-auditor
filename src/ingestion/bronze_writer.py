from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pandas as pd

from src.common.config import bootstrap_directories, get_project_paths


@dataclass(frozen=True)
class BronzeWriteRequest:
    source_id: str
    endpoint_id: str
    window_start_utc: str
    window_end_utc: str
    request_params: dict[str, str]
    records: list[dict]


@dataclass(frozen=True)
class BronzeWriteResult:
    status: str
    operation_key: str
    run_id: str
    data_file: str
    metadata_file: str
    record_count: int


def build_operation_key(request: BronzeWriteRequest) -> str:
    payload = {
        "source_id": request.source_id,
        "endpoint_id": request.endpoint_id,
        "window_start_utc": request.window_start_utc,
        "window_end_utc": request.window_end_utc,
        "request_params": request.request_params,
    }
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:20]


def _build_partition_dir(raw_root: Path, source_id: str, endpoint_id: str) -> Path:
    ingestion_date = datetime.now(UTC).date().isoformat()
    return (
        raw_root
        / f"source={source_id}"
        / f"endpoint={endpoint_id}"
        / f"ingestion_date={ingestion_date}"
    )


def write_bronze_parquet(request: BronzeWriteRequest) -> BronzeWriteResult:
    paths = bootstrap_directories(get_project_paths())
    operation_key = build_operation_key(request)
    run_id = str(uuid4())

    partition_dir = _build_partition_dir(
        paths.raw_parquet_dir,
        request.source_id,
        request.endpoint_id,
    )
    partition_dir.mkdir(parents=True, exist_ok=True)

    data_file = partition_dir / f"op_{operation_key}.parquet"
    metadata_file = partition_dir / f"op_{operation_key}_metadata.parquet"

    if data_file.exists() and metadata_file.exists():
        return BronzeWriteResult(
            status="skipped_existing",
            operation_key=operation_key,
            run_id=run_id,
            data_file=str(data_file),
            metadata_file=str(metadata_file),
            record_count=0,
        )

    data_frame = pd.DataFrame(request.records)
    data_frame.to_parquet(data_file, index=False)

    metadata = {
        "run_id": run_id,
        "operation_key": operation_key,
        "source_id": request.source_id,
        "endpoint_id": request.endpoint_id,
        "requested_at_utc": datetime.now(UTC).isoformat(),
        "window_start_utc": request.window_start_utc,
        "window_end_utc": request.window_end_utc,
        "request_params_json": json.dumps(request.request_params, sort_keys=True),
        "record_count": len(request.records),
        "status": "written",
    }
    pd.DataFrame([metadata]).to_parquet(metadata_file, index=False)

    return BronzeWriteResult(
        status="written",
        operation_key=operation_key,
        run_id=run_id,
        data_file=str(data_file),
        metadata_file=str(metadata_file),
        record_count=len(request.records),
    )


def serialize_result(result: BronzeWriteResult) -> dict:
    return asdict(result)
