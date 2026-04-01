# Agent Guardrails

This document defines the concise operational guardrails used by all Claude Code agents in this ecosystem.

Detailed explanations are in `reference/GUARDRAILS_REFERENCE.md`.
Operational budgeting rules are in `reference/BUDGETS.md`.

---

## Global Execution Rules

- Only one active milestone per cycle.
- Always read repository documentation before modifying code.
- Prefer low-cost skills first and keep broader validation within the current cycle budget.
- High-cost specialized validation requires explicit justification.
- High-cost validation should not repeat in the same cycle unless the repository fingerprint changes.
- Never modify unrelated files.
- Never expand scope beyond the active milestone.
- Check artifact freshness in `.agent-cache/artifact_freshness.json` before regenerating owned artifacts.
- Respect active lock files under `.agent-cache/locks/` when present.

---

## Artifact Ownership

Repository knowledge artifacts are owned by specific agents.

| Artifact | Owner Agent |
|----------|-------------|
| docs/STACK_PROFILE.md | stack-analyzer |
| docs/INVENTORY.md | repo-analyzer |
| docs/ARCHITECTURE.md | solution-architect |
| docs/QA_REPORT.md | qa-engineer |
| docs/SECURITY_REPORT.md | security-reviewer |
| README / CHANGELOG | tech-writer |

Ownership defines responsibility for generating or updating the artifact.
Other agents may read these files but should avoid rewriting them.

---

## Optional Artifacts

The following directories and files are **optional** — they improve agent efficiency but are not required:

- `docs/` — repository knowledge artifacts. Agents create these when missing.
- `.agent-cache/` — runtime state. Always gitignored. Never commit.

Agents must handle the case where these do not exist without failing.

---

## Escalation Rules

- Missing prerequisites or operational ambiguity → product-manager
- Architecture redesign or subsystem boundary changes → solution-architect

---

## Validation Ladder

Validation should escalate gradually.

Preferred order:

1. targeted-test-runner
2. ci-checks
3. smoke-journeys

Always stop at the lowest sufficient validation level.

---

## Security Rules

Security guardrails apply to all agents.

- Never expose secrets in outputs.
- Never commit credentials or tokens.
- Never echo discovered secrets into generated documentation.
- Report potential secret exposure without reproducing sensitive values.
