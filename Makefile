PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap bootstrap-orchestration lint format test check smoke contracts ingest-open-meteo-mock ingest-ember-mock ingest-entsoe-mock ingest-mock

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
