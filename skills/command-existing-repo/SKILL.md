---
name: "command-existing-repo"
description: "Full analysis and improvement workflow for an existing repository. Runs stack detection, inventory, dependency audit, architecture review, targeted improvements, and QA."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `existing-repo`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /existing-repo

You are the **Main Agent (Team Lead)**. Trigger this command when starting work on an existing repository with source files and a known structure.

## Gating Policy
- **Trigger**: Stack confidence HIGH and >= 10 source files.
- Milestones 2 and 3 require scope authorization before running.
- Milestone 1 is the default detection pass. Skip if fingerprint unchanged.

## Milestone Sequence (Swarm Orchestration)

### Milestone 1 — Detection & Cache Check
Assign to **stack-analyzer**:
- Run fingerprint first. If no material change is detected, skip the rest of this milestone.
- Output `docs/STACK_PROFILE.md`.

### Milestone 2 — Full Inventory & Audit Swarm
Spawn in parallel via **current Codex thread**:
1. **repo-analyzer**: Run repo-inventory and route-mapper. Output `docs/INVENTORY.md`.
2. **security-reviewer**: Run dependency-audit. Output `docs/SECURITY_REPORT.md`.

### Milestone 3 — Architecture Review
Assign to **solution-architect**:
- Use `code-search` and `architecture-drift-check`. 
- Output `docs/ARCHITECTURE.md`.
*Note: Planning only. No code changes.*

### Milestone 4 — Targeted Improvements
Assign to **software-engineer**:
- Apply `docs/ARCHITECTURE.md` recommendations. One improvement per cycle.
- Use `code-search` and `targeted-test-runner`.

### Milestone 5 — QA & Documentation Swarm
Spawn in parallel:
1. **qa-engineer**: Run `ci-checks`. Output `docs/QA_REPORT.md`.
2. **tech-writer**: Update README when needed using `docs-writer`.

## Hard Rules
1. Execute milestones in order.
2. One milestone per cycle. No batching.
3. Respect existing code — minimal, non-destructive changes only.
4. Never auto-merge PRs.
5. Read repository docs before recommending source changes.
6. Log every cycle in `docs/DECISIONS.md`.
