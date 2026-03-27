#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "[1/16] Installing dependencies"
make bootstrap PYTHON=.venv/bin/python

echo "[2/16] Running lint and tests"
make check PYTHON=.venv/bin/python

echo "[3/16] Validating source contracts"
make contracts PYTHON=.venv/bin/python

echo "[4/16] Running mock ingestion"
make ingest-mock PYTHON=.venv/bin/python

echo "[5/16] Building/testing dbt staging"
make dbt-staging PYTHON=.venv/bin/python

echo "[6/16] Building/testing dbt intermediate"
make dbt-intermediate PYTHON=.venv/bin/python

echo "[7/16] Building/testing dbt dimensions and facts"
make dbt-dimensions-facts PYTHON=.venv/bin/python

echo "[8/16] Building/testing dbt marts"
make dbt-marts PYTHON=.venv/bin/python

echo "[9/16] Running forecasting"
make forecast-phase9 PYTHON=.venv/bin/python

echo "[10/16] Running dashboard smoke checks"
make dashboard-smoke PYTHON=.venv/bin/python

echo "[11/16] Running monitoring checks"
make monitor-phase11 PYTHON=.venv/bin/python

echo "[12/16] Running late-arrival smoke"
make late-arrival-smoke PYTHON=.venv/bin/python

echo "[13/16] Running security smoke"
make security-smoke PYTHON=.venv/bin/python

echo "[14/16] Running performance benchmark smoke"
make benchmark-performance PYTHON=.venv/bin/python

echo "[15/16] Starting dashboard"
echo "Dashboard will run until you press Ctrl+C."

echo "[16/16] Launching Streamlit dashboard"
exec .venv/bin/python -m streamlit run reports/dashboards/streamlit_app.py
