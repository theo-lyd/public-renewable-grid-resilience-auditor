# System Run Commands and Dashboard Startup

This document details the command sequence needed to get the system running and the dashboard visible.

## Preconditions
1. Open terminal at repository root.
2. Ensure Python is available.
3. Ensure internet access for package install and optional live-source behavior.

## Full command sequence (recommended first run)

```bash
python3 -m venv .venv
source .venv/bin/activate
make bootstrap PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python
make contracts PYTHON=.venv/bin/python
make ingest-mock PYTHON=.venv/bin/python
make dbt-staging PYTHON=.venv/bin/python
make dbt-intermediate PYTHON=.venv/bin/python
make dbt-dimensions-facts PYTHON=.venv/bin/python
make dbt-marts PYTHON=.venv/bin/python
make forecast-phase9 PYTHON=.venv/bin/python
make dashboard-smoke PYTHON=.venv/bin/python
make monitor-phase11 PYTHON=.venv/bin/python
make late-arrival-smoke PYTHON=.venv/bin/python
make security-smoke PYTHON=.venv/bin/python
make benchmark-performance PYTHON=.venv/bin/python
make dashboard-run PYTHON=.venv/bin/python
```

## What this sequence does
1. Creates and activates isolated Python runtime.
2. Installs dependencies.
3. Runs lint and tests.
4. Validates source data contracts.
5. Performs deterministic mock ingestion.
6. Builds/tests dbt layers from staging to marts.
7. Runs forecasting and monitoring checks.
8. Runs hardening smoke checks (late-arrival, security, performance).
9. Launches Streamlit dashboard.

## Dashboard visibility notes
1. After `make dashboard-run`, Streamlit prints a local URL in terminal.
2. Keep terminal open while using the dashboard.
3. To stop dashboard, press `Ctrl+C` in the dashboard terminal.

## Faster subsequent run (if data and models are already built)

```bash
source .venv/bin/activate
make dashboard-run PYTHON=.venv/bin/python
```
