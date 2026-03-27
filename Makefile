PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
DBT ?= $(dir $(PYTHON))dbt

.PHONY: bootstrap bootstrap-orchestration lint format test check smoke contracts ingest-open-meteo-mock ingest-ember-mock ingest-entsoe-mock ingest-mock dbt-seed dbt-build-staging dbt-test-staging dbt-staging dbt-build-intermediate dbt-test-intermediate dbt-intermediate dbt-build-dimensions-facts dbt-test-dimensions-facts dbt-dimensions-facts dbt-build-marts dbt-test-marts dbt-marts forecast-phase9 dashboard-smoke dashboard-run monitor-phase11 late-arrival-smoke security-smoke benchmark-performance

bootstrap:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

bootstrap-orchestration:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt -r requirements-orchestration.txt

lint:
	$(PYTHON) -m ruff check src tests
	$(PYTHON) -m black --check src tests

format:
	$(PYTHON) -m ruff check src tests --fix
	$(PYTHON) -m black src tests

test:
	$(PYTHON) -m pytest

check: lint test

smoke:
	$(PYTHON) -m src.ingestion.healthcheck

contracts:
	$(PYTHON) -m src.ingestion.validate_contracts

ingest-open-meteo-mock:
	$(PYTHON) -m src.ingestion.run_bronze_ingestion open-meteo --latitude 52.52 --longitude 13.41 --start-date 2026-03-26 --end-date 2026-03-26 --mock-file data/reference/contracts/samples/open_meteo_sample.json

ingest-ember-mock:
	$(PYTHON) -m src.ingestion.run_bronze_ingestion ember --country-code DE --year 2026 --mock-file data/reference/contracts/samples/ember_sample.csv

ingest-entsoe-mock:
	$(PYTHON) -m src.ingestion.run_bronze_ingestion entsoe --in-domain 10Y1001A1001A83F --period-start-utc 202603260000 --period-end-utc 202603260300 --mock-file data/reference/contracts/samples/entsoe_sample.xml

ingest-mock: ingest-open-meteo-mock ingest-ember-mock ingest-entsoe-mock

dbt-seed:
	DBT_PROFILES_DIR=dbt $(DBT) seed --full-refresh --project-dir dbt --select zone_conformance_mapping zone_conformance_mapping_history

dbt-build-staging:
	DBT_PROFILES_DIR=dbt $(DBT) build --project-dir dbt --select models/staging/**

dbt-test-staging:
	DBT_PROFILES_DIR=dbt $(DBT) test --project-dir dbt --select models/staging/**,test_type:singular

dbt-staging: dbt-build-staging dbt-test-staging

dbt-build-intermediate:
	DBT_PROFILES_DIR=dbt $(DBT) build --project-dir dbt --select models/intermediate/** --exclude test_dim_* test_fact_*

dbt-test-intermediate:
	DBT_PROFILES_DIR=dbt $(DBT) test --project-dir dbt --select models/intermediate/**,test_intermediate*

dbt-intermediate: dbt-seed dbt-build-intermediate dbt-test-intermediate

dbt-build-dimensions-facts:
	DBT_PROFILES_DIR=dbt $(DBT) build --project-dir dbt --select models/dimensions/** models/facts/**

dbt-test-dimensions-facts:
	DBT_PROFILES_DIR=dbt $(DBT) test --project-dir dbt --select models/dimensions/** models/facts/** test_dim_* test_fact_*

dbt-dimensions-facts: dbt-seed dbt-build-dimensions-facts dbt-test-dimensions-facts

dbt-build-marts:
	DBT_PROFILES_DIR=dbt $(DBT) build --project-dir dbt --select models/marts/**

dbt-test-marts:
	DBT_PROFILES_DIR=dbt $(DBT) test --project-dir dbt --select models/marts/** test_mart_*

dbt-marts: dbt-seed dbt-build-marts dbt-test-marts

forecast-phase9:
	$(PYTHON) -m src.forecasting.run_forecast --horizon-days 7 --method moving_average --window 3 --scenario baseline

dashboard-smoke:
	$(PYTHON) -m src.monitoring.dashboard_smoke

dashboard-run:
	streamlit run reports/dashboards/streamlit_app.py

monitor-phase11:
	$(PYTHON) -m src.monitoring.phase11_monitoring

late-arrival-smoke:
	$(PYTHON) -m src.ingestion.late_arrival

security-smoke:
	$(PYTHON) -m src.common.security_controls

benchmark-performance:
	$(PYTHON) -m src.common.performance_benchmark
