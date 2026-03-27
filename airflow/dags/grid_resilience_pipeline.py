from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="grid_resilience_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 1},
    tags=["grid", "resilience", "phase-11"],
) as dag:
    start = EmptyOperator(task_id="start")
    bronze_ingestion = EmptyOperator(task_id="bronze_ingestion")
    dbt_staging = EmptyOperator(task_id="dbt_staging")
    dbt_intermediate = EmptyOperator(task_id="dbt_intermediate")
    dbt_dimensions_facts = EmptyOperator(task_id="dbt_dimensions_facts")
    dbt_marts = EmptyOperator(task_id="dbt_marts")
    forecast_phase9 = EmptyOperator(task_id="forecast_phase9")
    dashboard_smoke = EmptyOperator(task_id="dashboard_smoke")
    monitor_phase11 = EmptyOperator(task_id="monitor_phase11")
    end = EmptyOperator(task_id="end")

    (
        start
        >> bronze_ingestion
        >> dbt_staging
        >> dbt_intermediate
        >> dbt_dimensions_facts
        >> dbt_marts
        >> forecast_phase9
        >> dashboard_smoke
        >> monitor_phase11
        >> end
    )
