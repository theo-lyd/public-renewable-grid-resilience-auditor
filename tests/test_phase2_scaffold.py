from pathlib import Path

from src.common.config import get_project_paths


def test_required_directories_exist() -> None:
    root = Path(__file__).resolve().parents[1]

    required_dirs = [
        root / "data/raw/parquet",
        root / "data/processed/parquet",
        root / "data/reference",
        root / "src/ingestion",
        root / "src/cleaning",
        root / "src/forecasting",
        root / "src/monitoring",
        root / "dbt/models/staging",
        root / "dbt/models/intermediate",
        root / "dbt/models/dimensions",
        root / "dbt/models/facts",
        root / "dbt/models/marts",
        root / "airflow/dags",
        root / "reports/dashboards",
        root / "docs/phase-1",
        root / "docs/phase-2",
    ]

    missing_dirs = [str(path) for path in required_dirs if not path.exists()]
    assert not missing_dirs, f"Missing required directories: {missing_dirs}"


def test_project_path_defaults() -> None:
    paths = get_project_paths()

    assert paths.raw_parquet_dir.as_posix().endswith("data/raw/parquet")
    assert paths.processed_parquet_dir.as_posix().endswith("data/processed/parquet")
    assert paths.reference_data_dir.as_posix().endswith("data/reference")
    assert paths.duckdb_path.as_posix().endswith("data/processed/grid_resilience.duckdb")
