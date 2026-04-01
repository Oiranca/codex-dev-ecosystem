---
name: "architecture-drift-check"
description: "Detect likely drift between documented architecture and the current repository structure, file boundaries, and dependency patterns."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Architecture Drift Check

Use this skill to compare the documented architecture with the current repository structure and identify likely signs of architectural drift.

This skill detects structural inconsistencies and suspicious dependency patterns.
It does not rewrite architecture documents and does not enforce architecture automatically.

## Purpose

Identify signs that the repository may have drifted away from its documented architecture, including:
- Boundary violations.
- Unexpected cross-layer dependencies.
- Missing or outdated architectural assumptions.
- Repository shape changes not reflected in documentation.

## Gating Policy

- **Cost Class**: MEDIUM.
- Run only when a milestone affects architecture-sensitive areas.
- **Skip Conditions**:
  - Skip if `docs/ARCHITECTURE.md` is missing.
  - Skip if fingerprint unchanged and no structural files changed.
  - Never run on every cycle.

## Required Inputs

Because context is not shared natively among Agent Teams, the Team Lead must ensure the following are accessible or provided via the **current Codex thread**:
- `local metadata state file`.
- `docs/STACK_PROFILE.md`.
- `docs/INVENTORY.md`.
- `docs/ARCHITECTURE.md`.
- **Optional**: `docs/DECISIONS.md` if needed for recent architectural changes.

## Hard Rules

- Maximum 8 file reads total.
- Maximum 10 targeted searches.
- Do not read source files in full unless necessary.
- Prefer structure, import, and path-level evidence.
- Do not edit source code.
- Do not rewrite architecture docs.
- Do not guess undocumented architectural rules.

## Drift Detection Areas

### Repository shape drift
Check whether the repository shape described in `docs/ARCHITECTURE.md` still matches:
- Single app vs monorepo.
- Number of applications.
- Service boundaries.
- Presence of libraries or packages.

### Boundary drift
Look for likely violations such as:
- Frontend importing backend-only modules.
- Route handlers depending directly on deep infrastructure internals.
- Shared packages depending on app-specific code.
- Circular-looking coupling signals across boundaries.

### Dependency drift
Look for changes in:
- Major framework signals.
- Bundler/build assumptions.
- Newly introduced tooling that is not reflected in architecture documentation.

### Path drift
Check whether key documented paths still exist and whether new important paths appeared without being reflected in architecture notes.

## Result Classification

Classify findings as:
- **HIGH**: Strong evidence that the current repo shape or dependency flow contradicts documented architecture.
- **MEDIUM**: A likely mismatch exists, but the evidence is partial or indirect.
- **LOW**: Minor architectural inconsistency or outdated documentation signal.

## Output & Communication

Once the analysis is complete, the agent must **Communicate** the results back to the **current Codex thread** and persist them as follows:
1. Write results to `docs/ARCHITECTURE_DRIFT_REPORT.md`.
2. Append a short summary to `docs/DECISIONS.md`.

### Required Output Structure (Report)
- **Summary**: Short overview of whether drift was detected.
- **Repository Shape Drift**: Table with Finding, Severity, and Evidence.
- **Boundary Drift**: Table with Finding, Severity, and Evidence.
- **Dependency Drift**: Table with Finding, Severity, and Evidence.
- **Path Drift**: Table with Finding, Severity, and Evidence.
- **Recommended Follow-up**: Short practical next steps.
- **Limitations**: Document uncertainty, weak signals, or missing evidence.

## Completion Rules

- **If no drift is detected**: Still write the report and mark the architecture as aligned.
- **If `docs/ARCHITECTURE.md` is missing**: Skip the skill and record the reason in `docs/DECISIONS.md`.
- **If evidence is weak**: Record findings as LOW or MEDIUM and do not escalate without clear structural evidence.