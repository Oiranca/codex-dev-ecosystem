# Usage Guide

This guide describes how to use the normalized Copilot CLI setup.

---

## How to Work

Use Copilot CLI directly from the terminal.

The typical interaction pattern is:

1. Start from the current milestone.
2. Let the appropriate agent coordinate the task.
3. Use repository documentation as shared context.
4. Implement only the current milestone.
5. Validate changes before expanding scope.
6. Record outcomes in repository docs.

---

## Core Concepts

Agents coordinate work across different responsibilities:

- planning
- architecture
- implementation
- QA
- security review
- documentation
- migration tasks

Each agent owns a specific responsibility in the workflow.

---

Skills provide reusable capabilities such as:

- repository fingerprinting
- stack detection
- repository inventory
- code search
- route mapping
- targeted validation
- CI-style checks
- smoke journeys
- security review helpers

Agents invoke skills when deeper inspection or validation is needed.

---

Playbooks define milestone-based workflows.

They guide execution depending on the repository type:

- existing repository
- new project
- unknown stack
- migration scenarios

Playbooks help agents choose the smallest valid next step.

---

Guardrails define:

- scope boundaries
- escalation rules
- validation order
- security expectations

They ensure the workflow remains safe and predictable.

See GUARDRAILS.md.

---

## Repository Workflow

A typical repository workflow looks like this:

1. Read repository knowledge docs first.
2. Detect stack and repository inventory when necessary.
3. Plan the current milestone.
4. Implement the milestone with minimal changes.
5. Validate using targeted checks first.
6. Escalate to broader validation only when needed.
7. Record outcomes in docs/DECISIONS.md.

---

## Local Validation and Helpers

Some repositories may include helper scripts provided by the scaffold.

Examples:

- scripts/validate-local.sh
- scripts/autopilot.sh

These scripts are optional helpers and are not the primary interface.

Runtime state and local cache belong in `.agent-cache/`.

Examples:

- .agent-cache/AGENT_STATE.json
- .agent-cache/agent_config.json
- .agent-cache/last-run/
- .agent-cache/skill_budget_state.json
- .agent-cache/artifact_freshness.json
- .agent-cache/locks/

---

## Budget-aware Execution

Execution should prefer:

1. low-cost analysis first
2. targeted validation
3. broader validation only when needed

Avoid rerunning expensive operations within the same cycle without new evidence.

---

## Locks and Artifact Freshness

Before regenerating repository knowledge:

- check `.agent-cache/locks/`
- check `.agent-cache/artifact_freshness.json`

This prevents unnecessary regeneration.

Stale locks should be cleaned up and recorded in:

.agent-cache/lock_events.log

---

## MCP and Secrets

Repositories may include MCP configuration templates:

- mcp/mcp.config.json
- mcp/mcp.allowlist.json
- mcp/mcp.secrets.example

Actual secrets must never be committed and should be stored locally or provided through environment variables.

---

## Notes

- Pull requests are never auto-merged.
- Repository knowledge lives in docs/.
- Runtime state lives in .agent-cache/.
- Scripts are helpers, not the primary workflow.