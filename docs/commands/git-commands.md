# Git Commands Reference

This document lists individual Git commands used in this project lifecycle.

## Scope and context
- Repository: public-renewable-grid-resilience-auditor
- Main branch used during implementation: master
- Typical places where these commands are run: local project terminal and CI-related verification flows
- Typical periods when used: every phase completion, hotfixes, post-validation release, CI verification

## Command log

| Command | What command was used | Why command was used | Where command was used | When command was used | How command was used | What the command did exactly |
| --- | --- | --- | --- | --- | --- | --- |
| git status --short | Quick working tree inspection | Confirm modified or untracked files before commit | Local terminal at project root | Before staging and after commit validation | Run directly after edits or tests | Printed compact list of changed files |
| git add <files> | Stage selected files | Ensure only intended files are included in a commit | Local terminal at project root | After successful checks and before commit | Explicit file list was provided | Added file snapshots to the index |
| git commit -m "..." | Create a versioned checkpoint | Preserve atomic phase or hardening change with clear message | Local terminal at project root | After passing validation for a phase or patch | Single-line message with scope in commit title | Wrote a commit object with staged changes |
| git push | Publish local commits | Sync local validated work to remote repository | Local terminal at project root | After each phase and post-fix completion | Standard push to tracked upstream branch | Uploaded commits and updated remote branch reference |
| git rev-parse <short-sha> | Resolve full SHA | Ensure exact commit identity for CI watch commands | Local terminal at project root | During CI investigation and run filtering | Used short hash as input | Returned canonical full commit hash |

## Usage notes
- Project flow used non-interactive Git commands to keep automation and logs reproducible.
- Commit messages were phase-specific and change-scoped to improve traceability.
- Push followed successful local validation to reduce CI churn.

## Good practice in this repository
- Stage intentionally, avoid broad add operations unless all changes are validated.
- Keep commits focused on one technical objective.
- Verify working tree state before and after commits.
