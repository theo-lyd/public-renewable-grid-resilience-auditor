# Phase 3 — Technical Implementation Document

## 1) Objective(s)
1. Build source inventory for target public APIs.
2. Define machine-validated API contracts with explicit schema fields.
3. Define and enforce baseline quality rule requirements per endpoint.

## 2) Deliverable(s)
- Source inventory contract YAML file
- Contract schema and validation module
- Contract validation command (`make contracts`)
- Automated tests for source and quality-rule coverage
- Phase 3 source/contract documentation

## 3) What was implemented
- Added `data/reference/contracts/source_inventory.yaml` with contracts for ENTSO-E, Open-Meteo, and Ember.
- Added Pydantic models in `src/ingestion/contracts.py` to validate contract structure.
- Added CLI validator in `src/ingestion/validate_contracts.py`.
- Added test suite in `tests/test_phase3_contracts.py`.
- Added Makefile `contracts` target and quickstart update.

## 4) How it was implemented
1. Designed a versioned inventory schema for sources and endpoints.
2. Encoded quality rules directly in contract metadata.
3. Added runtime validation using strict Pydantic model checks.
4. Added tests to verify required source presence and critical-rule coverage.

## 5) Exact commands run
Commands executed during implementation and validation are recorded below.

```bash
make check && make smoke && make contracts
make check && make smoke && make contracts
make check && make smoke && make contracts
python3 -m ruff check src/ingestion/contracts.py --fix && make check && make smoke && make contracts
python3 -m black src/ingestion/validate_contracts.py && make check && make smoke && make contracts
```

## 6) Files created/updated

### Created
- `data/reference/contracts/source_inventory.yaml`
- `src/ingestion/contracts.py`
- `src/ingestion/validate_contracts.py`
- `tests/test_phase3_contracts.py`
- `docs/phase-3/source-inventory-and-api-contracts.md`
- `docs/phase-3/technical-implementation.md`

### Updated
- `Makefile`
- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `docs/README.md`

## 7) Validation outcomes
- Initial validation failed on lint/format checks in new Phase 3 files.
- Final validation passed with full stack:
	- Ruff: all checks passed
	- Black: check passed
	- Pytest: 5 passed
	- Smoke check: passed
	- Contract validator: passed (`3 sources, 4 endpoints, 14 quality rules`)

## 8) Output state
- Source inventory and API contracts are versioned and machine-validated.
- Quality-rule expectations are explicit per endpoint.

## 9) Requirement-to-reality gap log
- **Potential gap:** Some ENTSO-E endpoint parameters and XML tags vary by document type and market domain.
- **Minimal viable path:** Keep core endpoint contracts explicit now; refine endpoint-level parameter presets during ingestion implementation (Phase 4) with real payload samples.

## 10) Problems encountered and resolution log

### Problem P3-01: Import-order lint failures in contract module
- **Where observed:** `make check`
- **Root cause:** New `src/ingestion/contracts.py` import ordering did not match Ruff/isort canonical ordering.
- **Possible implications if unresolved:**
	1. CI lint stage fails continuously.
	2. Contract changes cannot be merged cleanly under quality gates.
- **Resolution applied:**
	1. Applied Ruff auto-fix (`python3 -m ruff check src/ingestion/contracts.py --fix`).
	2. Re-ran full validation stack.
- **Final status:** Resolved.

### Problem P3-02: Formatting failure in contract validator module
- **Where observed:** `make check` (Black step)
- **Root cause:** `src/ingestion/validate_contracts.py` did not match Black formatting.
- **Possible implications if unresolved:**
	1. CI fails on formatting gate.
	2. Inconsistent style baseline across ingestion modules.
- **Resolution applied:**
	1. Ran Black on the affected file (`python3 -m black src/ingestion/validate_contracts.py`).
	2. Re-ran full validation stack.
- **Final status:** Resolved.
