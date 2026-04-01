---
name: "targeted-test-runner"
description: "Run a focused subset of tests related to recently changed files to validate behavior quickly."
allowed-tools: ["read", "execute", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Targeted Test Runner

Use this skill to execute a **focused subset of tests** related to files changed in the current cycle.

This skill helps validate changes quickly without running the entire test suite. **Prefer this skill** before running full project test suites.

## Purpose

* **Validate behavior changes** by running tests that are likely affected by the modified files.
* Provide **rapid feedback** during the implementation phase.

## Gating Policy

* **Cost Class**: MEDIUM.
* **Skip Conditions**:
    * Skip if **no code files** changed.
    * Skip if **no test framework** is detected in `docs/STACK_PROFILE.md`.
    * Skip if the **repository fingerprint** is unchanged.
    * **Never run** before code implementation.
* **Budget**: Check `local skill budget metadata` (Broader validation limits apply).

## Required Inputs (via current Codex thread)

As context is isolated, the **Team Lead** must ensure access to these artifacts:
* `local metadata state file` (For fingerprint and cycle changes).
* `docs/STACK_PROFILE.md` (For test commands and framework detection).
* `docs/INVENTORY.md` (For structural mapping).

**Note**: Do not read full source files unless necessary for discovery.

## Test Framework Detection

Supported test frameworks include: **Jest, Vitest, Mocha, Pytest, Go test, and Cargo test**. Always use the specific commands defined in `docs/STACK_PROFILE.md`.

## Changed File Detection

Determine changed files using the **fingerprint state** and **current cycle changes**.
* **Focus on**: Application code, API handlers, route handlers, libraries, and utilities.
* **Ignore**: Documentation files and configuration-only changes (unless tests explicitly depend on them).

## Test Discovery Strategy

Attempt to find tests related to changed files using:
1.  **Same directory** test files.
2.  Adjacent `*.test.*` or `*.spec.*` files.
3.  **Test folders** referencing the specific module.
4.  Framework-specific test discovery patterns.

### Discovery Limits
* Maximum **10 test files** executed.
* Maximum runtime per command: **5 minutes**.

## Execution Rules

* Run tests **only** for discovered files.
* **Continue execution** even if earlier tests fail.
* Capture only the **first 50 lines** of failure output.
* **Fallback**: If targeted execution is not supported by the framework, run a minimal subset or skip with an explanation.

## Result Classification

Classify each execution as:
* **PASS**: Tests completed successfully.
* **FAIL**: Tests failed with assertion or runtime errors.
* **SKIP**: No relevant tests discovered.
* **TIMEOUT**: Execution exceeded 5 minutes.

## Output & Communication

The **qa-engineer** (or the agent assigned to the task) is the owner of this output.
1.  **Persistence**: Write results to `docs/TEST_REPORT.md`.
2.  **Decision Log**: Append a summary entry to `docs/DECISIONS.md`.
3.  **Communicate**: Post the test results to the **current Codex thread**.

### Required Output Structure (docs/TEST_REPORT.md)
* **Summary**: Short overview of the targeted test run.
* **Changed Files**: Table with | File | Reason |.
* **Selected Tests**: Table with | Test File | Discovery Method |.
* **Test Results**: Table with | Test File | Result | Notes |.
* **Failures**: List of Test Files and their **50-line error snippets**.
* **Limitations**: Document skipped tests, discovery issues, or framework limitations.

## Completion Rules

* **No tests discovered**: Mark as `SKIP` and document discovery limitations.
* **Tests fail**: Record failures; **do not attempt fixes** within this skill.
* **Tests pass**: Mark the change as **validated** for the tested scope.