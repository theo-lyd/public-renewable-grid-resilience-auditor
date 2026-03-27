from __future__ import annotations

from src.common.config import bootstrap_directories


def run_healthcheck() -> str:
    paths = bootstrap_directories()

    checks = {
        "raw_parquet_dir": paths.raw_parquet_dir.exists(),
        "processed_parquet_dir": paths.processed_parquet_dir.exists(),
        "reference_data_dir": paths.reference_data_dir.exists(),
        "duckdb_parent_dir": paths.duckdb_path.parent.exists(),
    }

    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        raise RuntimeError(f"Healthcheck failed for: {', '.join(failed_checks)}")

    return "Phase 2 smoke-check passed: environment paths and data directories are ready."


if __name__ == "__main__":
    print(run_healthcheck())
