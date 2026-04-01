---
name: "secret-scan-lite"
description: "Run a lightweight regex-based scan for accidentally committed secrets, tokens, credentials, and unsafe secret hygiene signals."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Secret Scan Lite

Use this skill to perform a lightweight secret hygiene scan before opening a pull request.

This skill is intentionally lightweight and uses pattern matching and repository hygiene checks. It does not replace dedicated secret scanning tools.

## Purpose

Detect likely accidental exposure of:
- API keys.
- tokens.
- credentials.
- private keys.
- unsafe secret hygiene patterns.

## Gating Policy

- **Cost Class**: EXPENSIVE (High-cost).
- **Authorization**: Requires explicit playbook justification naming this skill.
- **Skip Conditions**:
  - Skip if repository fingerprint is unchanged.
  - Skip if no code or config changes were made in the current cycle.
  - Never run on every cycle.
- **Budget**: Check `local skill budget metadata` (Max 1 run per skill per cycle; requires explicit justification).

## Hard Rules

- **Redaction**: Redact secret-like values in all outputs. Never print the actual matched secret value.
- **Read Limits**: Maximum 4 document reads total:
  - `local metadata state file`.
  - `docs/STACK_PROFILE.md`.
  - `docs/SECURITY_REPORT.md`.
  - `.gitignore`.
- **Scan Limits**:
  - Maximum 30 files scanned via grep/pattern matching only.
  - Do not perform full source reads.
  - If more than 50 findings exist, report the first 50 and note truncation.
- **Exclusions**: Do not scan `node_modules/`, `.git/`, `dist/`, `build/`, binary files, images, lockfiles, or minified files.

## Pre-flight Repository Hygiene Checks

Check whether the following are ignored in `.gitignore` and classify accordingly:
- **CRITICAL**: `.env` not ignored.
- **HIGH**: `.env.local` not ignored.
- **MEDIUM**: Other sensitive env variants (`.env.*.local`, `.env.production`, `.env.development`, `.env.test`) not ignored.

## Pattern Severity Categories

- **CRITICAL**: Private key headers (e.g., `BEGIN PRIVATE KEY`) or obvious live credentials with strong indicators.
- **HIGH**: API key assignments with long literals, AWS access keys (`AKIA...`), JWT secrets, or database URLs with embedded credentials.
- **MEDIUM**: Generic `secret=`, `password=`, or `token=` assignments with non-trivial literals, bearer tokens, or suspicious auth headers.
- **LOW**: TODO/FIXME notes mentioning secrets, localhost credentials in examples, or weak hygiene indicators.

## Output Redaction Policy

For every finding, record **only**:
- File path, line number, pattern category, and severity.
- **10-character redacted context snippet**.

**Never record** full secret values, full tokens, private key material, or full credential strings.

## Output & Communication

The **security-reviewer** is the owner of this artifact.
1. **Persistence**: Write results to `docs/SECURITY_REPORT.md`.
2. **Decision Log**: Append a short completion entry to `docs/DECISIONS.md`.
3. **Communicate**: Post the scan summary to the **current Codex thread**.

### Required Report Structure (docs/SECURITY_REPORT.md)
- **Summary**: Overview of the scan outcome.
- **Repository Hygiene Issues**: | Issue | Severity | Evidence |
- **Potential Secret Findings**: | File | Line | Pattern Type | Severity | Redacted Context |
- **Severity Summary**: Counts for Critical, High, Medium, and Low.
- **Recommendations**: Short practical next steps.
- **Limitations**: Regex-only, false positives/negatives possible, and coverage limits.

## Completion Rules

- **No eligible files**: Still write `docs/SECURITY_REPORT.md`, mark as clean with limitations.
- **No findings**: Still write the report and include hygiene check results.
- **Errors**: If a pattern-matching error occurs, skip that pattern, continue, and note the limitation.