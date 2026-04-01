---
name: "dependency-audit"
description: "Audit project dependencies for known vulnerabilities and outdated packages using the repository's native package manager tooling."
allowed-tools: ["read", "execute", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Dependency Audit

Use this skill to audit repository dependencies for known vulnerabilities and outdated packages.

**Constraint**: Do not use this skill to detect unused packages. That requires a different workflow and is intentionally out of scope here.

## Purpose

Audit repository dependencies for:
- **Known vulnerabilities**: Security risks identified in the dependency tree.
- **Outdated packages**: Dependencies that have newer versions available.

## Gating Policy

- **Cost Class**: MEDIUM.
- **Trigger**: Run only when the active milestone authorizes dependency review.
- **Skip Conditions**:
  - Skip if the repository fingerprint is unchanged and `docs/DEPENDENCY_AUDIT.md` already exists.
  - Skip if no package manager is detected in `docs/STACK_PROFILE.md`.
  - Never run in every cycle.
- **Budget**: Check `local skill budget metadata` when present. This falls under Broader Validation (Max 2 runs/cycle, max 1/skill).

## Hard Rules

- **Read limits**: Read at most 3 files (dependency manifest, lockfile if present, previous `docs/DEPENDENCY_AUDIT.md` if present).
- **Source exclusion**: Do not read source files.
- **Command limits**: Execute at most 2 commands total (one audit command, one outdated command).
- **Tooling fallback**: If audit tooling is unavailable, record a warning and run only the outdated check.
- **Lockfile policy**: If no lockfile exists, continue with manifest-only evidence.
- **Timeouts**: If any command times out, write partial results and mark them clearly.
- **Output limit**: Limit vulnerability output to the top 20 most critical findings.

## Package Manager Command Mapping

Use the native tool that matches the repository as identified by `stack-analyzer`:

### npm
- **audit**: `npm audit --json`
- **outdated**: `npm outdated`

### yarn
- **audit**: `yarn audit`
- **outdated**: `yarn outdated`

### pnpm
- **audit**: `pnpm audit --json`
- **outdated**: `pnpm outdated`

### pip
- **audit**: `pip-audit`
- **outdated**: `pip list --outdated`

### cargo
- **audit**: `cargo audit`
- **outdated**: `cargo install-update -a` (or report outdated status if available in repo tooling)

*If the package manager is detected but the required command is unavailable, write that limitation into the report.*

## Output & Communication

The **security-reviewer** is the primary owner of this skill's output. Upon completion:

1. **Persistence**: Write full results to `docs/DEPENDENCY_AUDIT.md`.
2. **Decision Log**: Append a short completion note/summary to `docs/DECISIONS.md`.
3. **Communicate**: Post the audit summary to the **current Codex thread** so the Team Lead can review findings.

### Required Report Structure (docs/DEPENDENCY_AUDIT.md)
- **Summary**: Short overview of the dependency health status.
- **Package Manager**: Detected package manager and evidence.
- **Vulnerabilities**: Table with Severity, Package, Version, Issue, and Recommended Action.
  - *Group by: Critical, High, Moderate, Low. Only include top 20.*
- **Outdated Packages**: Table with Package, Current, Latest, and Recommended Action.
- **Recommendations**: Classify as Immediate action, Scheduled update, or Monitor only.
- **Limitations**: Document missing lockfiles, unavailable tooling, timeouts, or partial results.

## Completion Rules

- **No Package Manager**: If none is detected, skip the skill and log the skip in `docs/DECISIONS.md`.
- **Clean Audit**: If no vulnerabilities or outdated packages are found, still write a report and mark the audit as clean.