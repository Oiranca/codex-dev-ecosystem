---
name: "ci-checks"
description: "Run available lint, type-check, test, and build commands and report results before pull request creation."
allowed-tools: ["read", "execute", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# CI Checks

Use this skill to run available project validation checks before opening a pull request.

The skill executes local validation commands and reports their status.
This skill does not fix failures.

## Purpose

Validate that the repository passes its core quality checks:
- **lint**: code linting.
- **type-check**: static type validation.
- **test**: unit or integration tests.
- **build**: production build.

## Gating Policy

- **Cost Class**: MEDIUM.
- **Authorization**: Requires explicit milestone authorization from the **Team Lead** via the current Codex thread.
- **Skip Conditions**:
  - Skip if no code changes were produced in the current cycle.
  - Skip if repository fingerprint is unchanged.
  - Never run speculatively.
- **Budget & Locks**:
  - Check `local skill budget metadata` before rerunning (Max 2 broader validation runs per cycle; max 1 run per skill per cycle).
  - Respect `local lock metadata` when present before starting overlapping validation.

## Hard Limits

- Max 4 documentation reads.
- Max 2 CI config reads.
- Max 4 command executions.
- Max command runtime: 5 minutes.
- Capture only first 50 lines of failure output.

## Required Inputs (via current Codex thread)

As context is isolated, the **Team Lead** must ensure access to these paths:
- `local metadata state file`.
- `docs/STACK_PROFILE.md` (Command discovery source).
- `docs/INVENTORY.md`.
- `docs/QA_REPORT.md` (If exists).

*Do not read source files.*

## Command Discovery & Environment

- **Source**: Commands must be obtained strictly from `docs/STACK_PROFILE.md`.
- **Missing Commands**: If a command is missing from the stack profile, mark it as `SKIP`.
- **Environment**:
  - Run commands in repository root.
  - Do not install dependencies or modify the environment.
  - Do not execute optional or custom scripts.

## Execution Order

Run checks in the following sequence. Continue execution even if earlier checks fail:
1. **lint**.
2. **type-check**.
3. **test**.
4. **build**.

## Result Classification

Classify each check as:
- **PASS**: Command completed successfully.
- **FAIL**: Command exited with non-zero status.
- **SKIP**: Command not defined in stack profile.
- **TIMEOUT**: Command exceeded 5 minutes.

## CI Pipeline Detection (Optional)

Inspect CI configuration files if present (e.g., `.github/workflows/*.yml`, `gitlab-ci.yml`, `circle.yml`).
- Record only whether a pipeline exists.
- Do not attempt to interpret pipeline logic.

## Output & Ownership

The **qa-engineer** is the owner of the validation results. Upon completion:
1. **Communicate**: Post the result summary to the **current Codex thread**.
2. **Persistence**: Write the full results to `docs/QA_REPORT.md`.
3. **Decision Log**: Append a validation outcome entry to `docs/DECISIONS.md` including the timestamp.

### QA_REPORT Structure
- **Overall Status**: PASS | FAIL.
- **Summary Table**: Check name and Result.
- **Failure Details**: First 50 lines of output for any `FAIL` or `TIMEOUT` status.
- **CI Pipelines**: Existence of external CI configurations.