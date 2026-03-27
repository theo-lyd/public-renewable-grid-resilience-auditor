from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="grid_resilience_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["grid", "resilience", "phase-scaffold"],
) as dag:
    start = EmptyOperator(task_id="start")
    bronze_ingestion = EmptyOperator(task_id="bronze_ingestion")
    silver_transform = EmptyOperator(task_id="silver_transform")
    gold_publish = EmptyOperator(task_id="gold_publish")
    monitoring = EmptyOperator(task_id="monitoring")
    end = EmptyOperator(task_id="end")

    start >> bronze_ingestion >> silver_transform >> gold_publish >> monitoring >> end
