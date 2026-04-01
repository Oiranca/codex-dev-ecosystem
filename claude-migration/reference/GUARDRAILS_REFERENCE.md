# Guardrails Reference

## Overview

This global guardrail system defines the operating boundaries shared by all Claude Code agents. It exists to keep agent execution focused, predictable, and safe.

The guardrails are split into two layers:
- `GUARDRAILS.md` — the concise operational version for agents.
- `GUARDRAILS_REFERENCE.md` — the longer human-oriented explanation of how those rules should be interpreted.

These files are ecosystem configuration artifacts. They are not repository docs and should not be confused with generated knowledge files such as `docs/STACK_PROFILE.md`, `docs/INVENTORY.md`, `docs/ARCHITECTURE.md`, or `docs/DECISIONS.md` inside a specific project.

## Global Execution Rules

All agents should operate within the same execution envelope:

- Only one active milestone per cycle.
- Read repository documentation before modifying code.
- Prefer low-cost work first and spend broader validation budget deliberately within a cycle.
- Require explicit justification before high-cost specialized validation.
- Avoid repeating high-cost specialized validation in the same cycle unless the repository fingerprint changes.
- Never modify unrelated files.
- Never expand scope beyond the active milestone.

These rules reduce churn, minimize repeated analysis, and keep multi-agent workflows aligned around a single bounded objective.

## Budget-Aware Execution

Operational budgeting is documented in `reference/BUDGETS.md` and tracked per repository in `.agent-cache/skill_budget_state.json` when the local scaffold is adopted.

- Low-cost work can run freely when directly relevant.
- Broader validation should stay limited per cycle.
- High-cost specialized validation requires explicit justification and should not repeat in the same cycle without new fingerprint evidence.

## Lock Behavior

Repositories using the local scaffold may keep active execution locks under `.agent-cache/locks/`.

Lock expectations:
- Use simple file locks.
- Prefer artifact-level or validation-level lock names.
- Clean up stale locks when they exceed a safe age threshold.
- Record stale lock cleanup in `.agent-cache/lock_events.log`.

Locks exist to prevent duplicate artifact generation, overlapping validation runs, and concurrent writes to the same repository knowledge file.

## Artifact Freshness Behavior

Artifact freshness metadata may be stored in `.agent-cache/artifact_freshness.json`.

Freshness should be evaluated using:
- Current repository fingerprint.
- Last generation timestamp.
- Owning agent.
- Optional source scope patterns tied to the artifact.

Expected states: `fresh`, `missing`, `stale`, `probably-stale`.

`probably-stale` is the preferred signal when relevant files changed but the system has not yet regenerated the artifact.

## Artifact Ownership

| Artifact | Owner |
|----------|-------|
| docs/STACK_PROFILE.md | stack-analyzer |
| docs/INVENTORY.md | repo-analyzer |
| docs/ARCHITECTURE.md | solution-architect |
| docs/QA_REPORT.md | qa-engineer |
| docs/SECURITY_REPORT.md | security-reviewer |
| README / CHANGELOG | tech-writer |

Ownership does not prevent other agents from reading these files. It clarifies who is responsible for producing or updating them.

## Escalation Rules

- Missing prerequisites or operational ambiguity → `product-manager`
- Architecture redesign or boundary changes → `solution-architect`

## Validation Ladder

Preferred order:
1. `targeted-test-runner`
2. `ci-checks`
3. `smoke-journeys`

Start with targeted validation closest to the changed files. Broaden only when scope or risk justifies it.

## Guardrails Per Agent

### product-manager
- Keep exactly one active milestone in motion.
- Confirm prerequisites before delegating.
- Avoid unnecessary skill fan-out.
- Escalate architecture changes to `solution-architect`.
- Check budget state before authorizing broader validation.

### context-manager
- Produce a reading plan, not an implementation.
- Never read more than 5 files.
- Keep the reading plan to 20 files maximum.
- If scope is too broad, hand off to product-manager.

### stack-analyzer
- Produce evidence-backed stack detection only.
- Avoid implementation advice outside its detection role.
- Re-run only when repository fingerprint or relevant stack files changed.

### repo-analyzer
- Inventory only what is supported by repository evidence.
- Avoid architectural assumptions.
- Keep structural output aligned with stack findings.

### solution-architect
- Design the smallest valid implementation path.
- Avoid over-scoping a milestone.
- Escalate unresolved operational ambiguity to `product-manager`.

### software-engineer
- Implement only the approved milestone.
- Prefer localized edits.
- Follow the validation ladder instead of jumping directly to broad checks.

### qa-engineer
- Validate the milestone against existing repository tooling.
- Prefer targeted validation before broader checks.
- Report failures without redesigning implementation scope.

### security-reviewer
- Review for evidence-backed risks only.
- Never expose secrets in reports.
- Escalate architectural security changes to `solution-architect`.

### tech-writer
- Update documentation only when validated changes require it.
- Respect artifact ownership boundaries.
- Avoid inventing behavior not supported by implementation or repo docs.

### migration-engineer
- Apply migrations incrementally.
- Preserve system stability where possible.
- Use the validation ladder to avoid unnecessary high-cost validation.

## Migration Safety Rules

Migration work requires stronger execution discipline:
- Keep changes incremental.
- Preserve compatibility where possible.
- Avoid rewriting unrelated modules.
- Validate after meaningful migration steps.
- Escalate architecture redesign or subsystem boundary changes to `solution-architect`.

## Security Rules

Security guardrails apply to all agents, not only the security-reviewer:
- Never expose secrets in outputs.
- Never commit credentials or tokens.
- Never normalize or echo discovered secrets into generated docs.
- Report secret exposure as a finding without reproducing sensitive values.

## Documentation Ownership

- Generated repository knowledge docs belong to their assigned agents.
- Human-facing project docs (README, CHANGELOG) belong to `tech-writer`.
- Global ecosystem policy files are separate from repository docs and should not be written into project `docs/` folders.
