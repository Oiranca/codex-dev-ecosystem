---
name: "docs-writer"
description: "Synchronize human-facing documentation such as README and CHANGELOG using existing agent-generated documentation as the source of truth."
allowed-tools: ["read", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Docs Writer

Use this skill to update human-facing documentation after a cycle that produced or changed repository documentation.

This skill does not generate documentation from scratch.
It only summarizes and synchronizes information from existing agent-generated docs.

## Purpose

Keep the following documentation aligned with the latest validated repository state:
- `README.md`.
- `CHANGELOG.md`.
- Selected human-facing documentation sections.

## Gating Policy

- **Cost Class**: CHEAP.
- **Trigger**: Run only after a cycle that produced or updated docs.
- **Skip Conditions**:
  - Skip if no docs changed in the current cycle.
  - Skip if the repository fingerprint is unchanged.
  - Never run as a standalone cycle without upstream documentation changes.

## Required Inputs (via current Codex thread)

As context is isolated, the agent must be provided with the paths to the source of truth artifacts:
- `AGENT_STATE.json`.
- `docs/STACK_PROFILE.md`.
- `docs/INVENTORY.md`.
- `docs/ARCHITECTURE.md`.
- `docs/DECISIONS.md`.
- `README.md`.
- `CHANGELOG.md`.

## Hard Rules

- **Never read source code**.
- **Never read config files**.
- **Maximum 7 file reads total** (the files listed in Required Inputs).
- **Never rewrite the entire README**.
- **Never delete existing README content**.
- **Never invent undocumented features**.
- **Never summarize from memory**: Use existing docs only.
- **Ownership**: This skill is primary for the **tech-writer** agent.

## Managed README Sections

Only update agent-managed sections when the following markers are present:
- `` / ``.
- `` / ``.
- `` / ``.
- `` / ``.

**If markers are absent**: Append a new `## Agent-managed project summary` section at the end of `README.md`.

## CHANGELOG Policy

- Update `CHANGELOG.md` only with a minimal new entry for the current cycle.
- Do not rewrite historical entries.
- If `CHANGELOG.md` is missing, create a minimal one.
- **Structure**:
  ## [YYYY-MM-DD]
  ### Added
  ### Changed
  ### Fixed
  ### Security
  *(Only include sections relevant to the current cycle)*.

## Missing File Behavior

- **If README.md is missing**: Create a minimal `README.md` with agent-managed sections only.
- **If any docs file is missing**:
  - Skip the corresponding summary section.
  - Add a warning to the output.
  - Append a short warning note to `docs/DECISIONS.md`.

## Output & Communication

Upon execution, the agent must:
1. **Edit**: Update `README.md` and `CHANGELOG.md` (when relevant).
2. **Persistence**: Append a short entry to `docs/DECISIONS.md` recording the documentation sync.
3. **Communicate**: Post a confirmation to the **current Codex thread** once human-facing docs are synchronized.

## Completion Rules

The skill is successful if:
- Documentation was updated non-destructively.
- No undocumented claims were introduced.
- `README.md` existing content was preserved.