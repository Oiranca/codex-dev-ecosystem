---
name: "repo-task-orchestrator"
description: "Use for repository implementation work that is not primarily review, audit, or safe refactor, when you need one Codex-native workflow for triage, scoping, delegation, and closure."
---

# Repo Task Orchestrator

Default workflow for repository work.

## When To Use

Use this for feature work, bugfixes, implementation requests, repository improvements, and scoped architecture changes.
Skip it for review-only, audit-only, or safe-refactor-only work.

## Triage

- **UNKNOWN**: stack confidence is low or conflicting.
- **NEW**: stack confidence is high and the repository has very little source surface.
- **ESTABLISHED**: stack confidence is high and the repository has a normal existing codebase.

## Workflow

### Milestone 1 — Detect and scope

1. Run `fingerprint`.
2. Run `stack-detection` if stack confidence is not already high.
3. Run `repo-inventory` if structural context is missing or stale.
4. Run `scoped-discovery` for the current task.

Refresh when needed:
- `docs/STACK_PROFILE.md`
- `docs/INVENTORY.md`
- `docs/DECISIONS.md`

### Milestone 2 — Decide path

Based on triage:

- **UNKNOWN**:
  - stop before implementation;
  - produce `docs/ARCHITECTURE.md` with `STATUS: NEEDS_HUMAN_REVIEW`;
  - surface concrete ambiguities and ask for direction.

- **NEW**:
  - produce the smallest viable architecture and initial implementation plan;
  - prefer one milestone that leaves the project runnable.

- **ESTABLISHED**:
  - produce the smallest viable architecture and change plan;
  - prefer one milestone that is reviewable and reversible.

### Milestone 3 — Architecture

Use `solution-architect` to write the minimal plan in `docs/ARCHITECTURE.md`.

### Milestone 4 — Implementation

Use `software-engineer` for localized implementation. Prefer `targeted-test-runner`, escalate to `ci-checks` only for shared surfaces.

### Milestone 5 — Review and docs

Run review lanes only when needed:
- `qa-engineer`
- `security-reviewer`
- `tech-writer`

Use `parallel-subagent-orchestration` for independent lanes.
Use `command-team-review` for review-only cycles.

### Milestone 6 — Close safely

Before claiming completion or deciding merge/PR/cleanup actions, use `completion-gate`.

## Hard Rules

1. One milestone per cycle when the task is large or ambiguous.
2. Prefer the smallest valid change set.
3. Never guess the stack.
4. Never skip validation before claiming success.
5. Never run broad multi-agent work when `scoped-discovery` can narrow the file set first.

## Output

### Repository Mode
`UNKNOWN` | `NEW` | `ESTABLISHED`

### Task Scope
What this cycle is trying to achieve.

### Current Milestone
What is being executed now.

### Delegation Plan
Which agent owns what.

### Validation Plan
Which checks prove the change is safe.

### Next Gate
What must happen before moving forward.
