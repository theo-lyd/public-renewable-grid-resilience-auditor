# Make Commands Reference

This document explains Make commands used in this project, including what each command does and why Make is used instead of directly typing every underlying command.

## Why Make commands are used instead of direct commands

### Main reasons
1. Consistency: one command path for all contributors and reviewers.
2. Reproducibility: the same target runs the same sequence every time.
3. Readability: project operations become discoverable as named targets.
4. Safety: grouped targets reduce skipped steps and ordering mistakes.
5. Maintainability: command changes are centralized in one file.
6. CI alignment: local workflow can mirror automated pipeline steps.

### Essence and benefits of Makefile in this repository
- Makefile is the project command orchestrator.
- It defines standards for setup, linting, tests, ingestion, dbt, monitoring, dashboard checks, and hardening smoke tasks.
- It encodes dependencies between tasks, for example staging or marts pipelines that chain seed, build, and test.
- It reduces cognitive load for both technical and non-technical collaborators by exposing clear operational names.

## Scope and context
- Source of truth for these commands: Makefile at repository root.
- Typical execution location: local terminal at repository root.
- Typical use moments: environment bootstrap, phase validation, smoke checks, demo readiness, CI parity runs.

## Command log

| Make target | What command was used | Why command was used | Where command was used | When command was used | How command was used | What the command did exactly |
| --- | --- | --- | --- | --- | --- | --- |
| make bootstrap | Development dependency bootstrap | Prepare baseline local environment | Local terminal and onboarding flow | At setup and clean environment rebuilds | Direct target invocation | Upgraded pip and installed requirements-dev.txt |
| make bootstrap-orchestration | Orchestration-capable bootstrap | Include airflow and orchestration dependencies | Local terminal for orchestration phases | Before phase 11 orchestration work | Direct target invocation | Upgraded pip and installed dev plus orchestration requirements |
| make lint | Static quality checks | Catch style and lint issues early | Local and CI quality pass | Before commit and in CI | Direct target invocation | Ran ruff checks and black formatting checks |
| make format | Auto-format and fix style | Normalize code formatting and simple lint fixes | Local terminal before validation | When lint reported fixable issues | Direct target invocation | Ran ruff with fix mode and black formatter |
| make test | Unit and integration test pass | Validate behavior and regressions | Local and CI | Before commit, after fixes | Direct target invocation | Executed pytest suite |
| make check | Combined quality gate | Single gate for lint plus tests | Local and CI | Standard pre-commit and pre-push gate | Invokes lint then test | Ensured code quality and test success in sequence |
| make smoke | Health smoke check | Confirm baseline runtime viability | Local terminal | Early phase checks and quick diagnostics | Direct target invocation | Ran ingestion healthcheck module |
| make contracts | Contract validation | Verify source contracts before ingestion | Local terminal | Contract-first phase and regression checks | Direct target invocation | Ran contract validator module |
| make ingest-open-meteo-mock | Mock Open-Meteo ingestion | Deterministic ingestion validation | Local terminal | Bronze ingestion phase and regressions | Direct target invocation | Executed run_bronze_ingestion for open-meteo with sample payload |
| make ingest-ember-mock | Mock Ember ingestion | Deterministic ingestion validation | Local terminal | Bronze ingestion phase and regressions | Direct target invocation | Executed run_bronze_ingestion for ember with sample payload |
| make ingest-entsoe-mock | Mock ENTSO-E ingestion | Deterministic ingestion validation | Local terminal | Bronze ingestion phase and regressions | Direct target invocation | Executed run_bronze_ingestion for entsoe with sample payload |
| make ingest-mock | Aggregate mock ingestion target | Run all mock ingestions in one command | Local terminal | Full ingestion validation | Depends on three mock ingestion targets | Completed all mock source ingestions |
| make dbt-seed | Seed dbt reference tables | Load conformance mappings and history for models | Local terminal and dbt workflows | Before dbt model builds/tests | Direct target invocation | Ran dbt seed with full refresh for two seed datasets |
| make dbt-build-staging | Build staging models | Materialize staging transformations | Local terminal in dbt phase flows | During phase 5 and regression runs | Direct target invocation | Ran dbt build for staging model selectors |
| make dbt-test-staging | Test staging models | Validate staging model quality gates | Local terminal in dbt phase flows | During phase 5 and regressions | Direct target invocation | Ran dbt test on staging selectors and singular tests |
| make dbt-staging | Full staging pipeline | Ensure staging build and tests run together | Local terminal | Phase 5 validation | Depends on staging build and test targets | Completed staging build plus test sequence |
| make dbt-build-intermediate | Build intermediate models | Materialize harmonized intermediate layer | Local terminal in dbt phase flows | During phase 6 and regressions | Direct target invocation | Ran dbt build on intermediate selectors |
| make dbt-test-intermediate | Test intermediate models | Validate harmonization and data quality assertions | Local terminal in dbt phase flows | During phase 6 and regressions | Direct target invocation | Ran dbt tests on intermediate selectors |
| make dbt-intermediate | Full intermediate pipeline | Keep seed, build, and tests ordered together | Local terminal | Phase 6 validation | Depends on seed, intermediate build, intermediate test | Completed ordered intermediate pipeline checks |
| make dbt-build-dimensions-facts | Build dimensions and facts | Materialize dimensional and fact layer | Local terminal in dbt phase flows | During phase 7 and hardening | Direct target invocation | Ran dbt build on dimensions and facts selectors |
| make dbt-test-dimensions-facts | Test dimensions and facts | Validate keys, relationships, and singular assertions | Local terminal in dbt phase flows | During phase 7 and hardening | Direct target invocation | Ran dbt tests for dimensions/facts and named singular test groups |
| make dbt-dimensions-facts | Full dimensions/facts pipeline | Keep seed, build, test flow consistent | Local terminal | Phase 7 and hardening validation | Depends on seed, dimensions-facts build, dimensions-facts test | Completed full dimensions/facts validation chain |
| make dbt-build-marts | Build marts | Materialize gold KPI marts | Local terminal in dbt phase flows | During phase 8 and regressions | Direct target invocation | Ran dbt build on marts selectors |
| make dbt-test-marts | Test marts | Validate KPI marts and mart-level assertions | Local terminal in dbt phase flows | During phase 8 and regressions | Direct target invocation | Ran dbt tests on marts selectors and mart singular tests |
| make dbt-marts | Full marts pipeline | Keep seed, build, test flow consistent for marts | Local terminal | Phase 8 validation and release checks | Depends on seed, marts build, marts test | Completed full mart validation chain |
| make forecast-phase9 | Forecast/scenario run | Generate forecast outputs with scenario engine | Local terminal | Phase 9 execution and regressions | Direct target invocation | Ran forecasting module with moving-average baseline and configured horizon |
| make dashboard-smoke | Dashboard smoke validation | Verify dashboard dependencies and narrative checks | Local terminal | Phase 10 and release checks | Direct target invocation | Ran dashboard smoke module |
| make dashboard-run | Launch dashboard app | Start stakeholder-facing interface | Local terminal | Demonstrations and manual review | Direct target invocation | Started Streamlit app |
| make monitor-phase11 | Monitoring policy evaluation | Evaluate monitoring rules and routing decisions | Local terminal | Phase 11 and operations checks | Direct target invocation | Ran phase11 monitoring module |
| make late-arrival-smoke | Late-arrival utility smoke | Validate late-arrival module behavior and output | Local terminal | Post-phase hardening checks | Direct target invocation | Executed late_arrival module main output |
| make security-smoke | Security utility smoke | Validate security controls module behavior | Local terminal | Post-phase hardening checks | Direct target invocation | Executed security_controls module main output |
| make benchmark-performance | Performance utility smoke | Validate benchmark utility behavior | Local terminal | Post-phase hardening checks | Direct target invocation | Executed performance_benchmark module main output |

## Practical guidance
- Prefer make check as first validation gate after edits.
- Use grouped dbt targets for layer-level validation instead of ad hoc dbt command fragments.
- Use smoke targets for quick confidence before longer end-to-end runs.
- Use command chaining only when intentionally building a full release validation trail.
