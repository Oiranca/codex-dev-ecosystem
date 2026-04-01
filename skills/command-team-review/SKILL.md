---
name: "command-team-review"
description: "Parallel multi-agent code review workflow. Coordinates Security, Performance, and QA review lanes and produces a structured final report."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `team-review`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /team-review [scope]

You are the **Main Agent (Team Lead)**. Orchestrate a parallel review over staged changes or modified files.

## Review Lanes (Parallel Execution)
Spawn all three lanes in parallel via the **current Codex thread**:

### Lane 1 — Security Specialist (security-reviewer)
- Focus: Exposed secrets, unsafe input, dependency vulnerabilities, permissive configs.
- Rule: Never reproduce secret values.

### Lane 2 — Performance Expert (software-engineer)
- Focus: Expensive operations, missing caching, bundle size, complexity.
- Rule: No micro-optimizations without clear scale evidence.

### Lane 3 — QA Engineer (qa-engineer)
- Focus: Missing/broken test coverage, edge cases, build/type issues, milestone compliance.

## Final Report
Consolidate results into the structured Team Review Report (Scope, Security, Performance, QA, Consolidated Verdict, Required Actions).

## Hard Rules
1. Never auto-merge. Do not reproduce secret values.
2. Scope stays on changed files only.
