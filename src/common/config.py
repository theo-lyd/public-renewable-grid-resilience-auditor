from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ProjectPaths:
    project_root: Path
    raw_parquet_dir: Path
    processed_parquet_dir: Path
    reference_data_dir: Path
    duckdb_path: Path


def _resolve_path(project_root: Path, env_key: str, default_value: str) -> Path:
    return project_root / Path(os.getenv(env_key, default_value))


def get_project_paths(project_root: Path | None = None) -> ProjectPaths:
    root = project_root or Path(__file__).resolve().parents[2]

    raw_parquet_dir = _resolve_path(root, "RAW_PARQUET_DIR", "data/raw/parquet")
    processed_parquet_dir = _resolve_path(root, "PROCESSED_PARQUET_DIR", "data/processed/parquet")
    reference_data_dir = _resolve_path(root, "REFERENCE_DATA_DIR", "data/reference")
    duckdb_path = _resolve_path(root, "DUCKDB_PATH", "data/processed/grid_resilience.duckdb")

    return ProjectPaths(
        project_root=root,
        raw_parquet_dir=raw_parquet_dir,
        processed_parquet_dir=processed_parquet_dir,
        reference_data_dir=reference_data_dir,
        duckdb_path=duckdb_path,
    )


def bootstrap_directories(paths: ProjectPaths | None = None) -> ProjectPaths:
    resolved_paths = paths or get_project_paths()

    resolved_paths.raw_parquet_dir.mkdir(parents=True, exist_ok=True)
    resolved_paths.processed_parquet_dir.mkdir(parents=True, exist_ok=True)
    resolved_paths.reference_data_dir.mkdir(parents=True, exist_ok=True)
    resolved_paths.duckdb_path.parent.mkdir(parents=True, exist_ok=True)

    return resolved_paths
