# Bash and Shell Commands Reference

This document records common Bash and shell commands used while building, validating, and operating this project.

## Scope and context
- Shell environment: bash in VS Code dev container
- Typical execution location: project root terminal
- Typical use moments: setup, diagnostics, log inspection, CI monitoring, targeted probes

## Command log

| Command | What command was used | Why command was used | Where command was used | When command was used | How command was used | What the command did exactly |
| --- | --- | --- | --- | --- | --- | --- |
| source .venv/bin/activate | Activate Python virtual environment | Ensure Python, pip, and tools resolve from project environment | Local terminal at project root | Before Python, pytest, dbt, and helper executions | Invoked once per terminal session | Updated shell environment variables to use project virtual environment |
| set -e | Enable fail-fast shell behavior | Stop command chains immediately on first error | Local terminal in multi-step validation runs | During scripted validation pipelines | Added at start of shell sequence | Caused shell to exit on non-zero command status |
| grep -RIn "pattern" <path> | Recursive text search with line numbers | Locate configuration, references, and debug sources quickly | Local terminal at project root | During root cause analysis and config tracing | Pattern and path were provided explicitly | Searched files recursively and printed matching lines with file and line number |
| find <path> -type f ... | Structured file discovery | Constrain searches to specific file types and folders | Local terminal at project root | During targeted diagnostics and inventory checks | Combined with include filters and exclusions | Enumerated files matching constraints |
| nl -ba <file> | Print file with line numbers | Support precise audit and review references | Local terminal at project root | During residual-risk audit and evidence capture | Piped into sed for specific ranges when needed | Output file contents with absolute line numbering |
| sed -n 'start,endp' <file> | Print selected line ranges | Inspect only relevant sections to reduce noise | Local terminal at project root | During audits and quick reviews | Used with nl output and line range arguments | Printed only requested lines from a file |
| gh run list --commit <sha> --json ... | List GitHub Actions runs for commit | Map a commit to workflow runs and status | Local terminal at project root | Post-push CI monitoring | Used with exact commit hash and JSON fields | Returned run metadata such as status, conclusion, URL |
| gh run watch <run-id> --exit-status | Watch a workflow run | Wait for run completion and detect pass/fail | Local terminal at project root | During CI watch pass for release confirmation | Run against known workflow run ID | Streamed run state and exited with status code matching run conclusion |
| gh run view <run-id> --json ... | Retrieve detailed run/job/step summary | Produce exact CI report for stakeholders | Local terminal at project root | After run completion | Queried selected JSON fields including jobs and steps | Returned detailed workflow, job, and step conclusions |
| python - <<'PY' ... PY | Inline Python script execution in shell | Run focused probes without creating temporary files | Local terminal at project root | During post-hardening evidence checks | Heredoc block passed to project Python interpreter | Executed multi-line Python snippet and printed probe results |

## Usage notes
- Commands were intentionally plain and script-friendly for reproducibility.
- Investigation commands were read-only unless explicitly running a build or check.
- CI commands were used to produce exact status evidence, not only visual confirmation.
