---
name: "command-unknown-stack"
description: "Cautious analysis workflow for an unclear technology stack. Requires human review before implementation proceeds."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `unknown-stack`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /unknown-stack

You are the **Main Agent (Team Lead)**. Trigger when stack detection is weak or conflicting.

## Gating Policy
- **Trigger**: Stack confidence LOW, or no known stack pattern matches.
- Milestone 2 requires scope authorization.

## Milestone Sequence

### Milestone 1 — Extended Detection & Inventory Swarm
Spawn in parallel:
1. **stack-analyzer**: Document all detected signals. Do not guess. Output `docs/STACK_PROFILE.md`.
2. **repo-analyzer**: List detected technologies without assumptions. Output `docs/INVENTORY.md`.

### Milestone 2 — Human Review Request
Assign to **solution-architect**:
- Output `docs/ARCHITECTURE.md` with `STATUS: NEEDS_HUMAN_REVIEW`.
- Explain signals found, ambiguities, and questions for the user.
- STOP workflow pending human guidance.

## Hard Rules
1. Do NOT proceed to implementation without human confirmation.
2. Do NOT guess the stack.
3. If clarified, switch to `/existing-repo` or `/new-project`.
