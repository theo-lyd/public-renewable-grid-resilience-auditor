PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap bootstrap-orchestration lint format test check smoke

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
