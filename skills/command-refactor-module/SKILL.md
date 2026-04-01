---
name: "command-refactor-module"
description: "Safe, behavior-preserving refactor workflow for a specific module or file set. Includes planning, scoped implementation, and validation."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `refactor-module`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /refactor-module <path>

You are the **Main Agent (Team Lead)**. Run a focused, safe refactor.

## Principles
- Preserve existing behavior. No unrelated cleanup.
- Keep the change reviewable. Prefer small, sequential edits.

## Orchestration Phases

### Phase 1 — Planning
Assign to **solution-architect** (or `context-manager` for scope reduction):
- Identify boundaries via `code-search`.
- Classify: Extract, Rename, Simplify, or Restructure.
- Produce Refactor Plan: Files affected, Files NOT to change, Rollback and Test strategy.
*Wait for user confirmation.*

### Phase 2 — Implementation
Assign to **software-engineer**:
- Implement ONLY the refactor plan. No feature work.
- Atomic change sets: Structural changes first, then logic simplification.
- Do not reformat unrelated code.

### Phase 3 — Validation
Assign to **qa-engineer**:
- Run targeted tests first.
- Escalate to `ci-checks` only if shared utilities or public APIs were touched.

## Hard Rules
1. No behavior changes. No touching files outside scope.
2. If a bug is revealed, stop and report.
3. Log the refactor in `docs/DECISIONS.md`.
