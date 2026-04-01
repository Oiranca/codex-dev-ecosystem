---
name: "env-consistency"
description: "Check whether environment variables are documented, referenced in code, and visible in deployment-related configuration."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Env Consistency

Use this skill to compare environment variable documentation against source usage patterns and deployment-related configuration.

This skill detects likely consistency gaps.
It does not prove that deployment variables are missing from external platform UIs.

## Purpose

Identify environment variable issues such as:
- **undocumented variables**: Used in code but missing from templates.
- **documented but unreferenced variables**: Present in templates but not in code.
- **deployment visibility gaps**: Present in code/templates but missing from deployment configs.
- **suspicious naming mismatches**: Inconsistent naming for the same purpose.

## Gating Policy

- **Cost Class**: EXPENSIVE (High-cost).
- **Authorization**: Requires explicit playbook justification naming this skill.
- **Budget**: Check `local skill budget metadata`. Max 1 run per cycle; requires explicit justification.
- **Skip Conditions**:
  - Skip if the repository fingerprint is unchanged.
  - Skip if no env example/template file exists.
  - Never run on every cycle.

## Hard Rules

- **Maximum 3 documentation reads**:
  - `local metadata state file`.
  - `docs/STACK_PROFILE.md`.
  - `docs/INVENTORY.md`.
- **Maximum 1 env template read** (Priority order):
  - `.env.example`, `.env.sample`, `.env.template`.
  - Fallback: `.env.local.example`, `.env.development.example`, `.env.production.example`.
- **Maximum 2 deployment config reads** (First 2 found):
  - `netlify.toml`, `vercel.json`, `docker-compose.yml`.
- **Maximum 20 source files scanned** via grep-like pattern search.
- **Prohibitions**:
  - Do not read full source file contents.
  - Do not scan: `node_modules/`, `.git/`, `dist/`, `build/`, `vendor/`.

## Required Inputs (via current Codex thread)

As context is isolated, the **Team Lead** must ensure the agent has access to the following artifacts:
- `AGENT_STATE.json`.
- `docs/STACK_PROFILE.md`.
- `docs/INVENTORY.md`.

## Data Extraction & Source Usage

### Documented variables
Extract variable names from the env template file.

### Deployment-visible variables
Extract names visible in the 2 reviewed deployment config files only.

### Source usage patterns
Scan source paths only for environment variable patterns:
- `process.env.`
- `import.meta.env.`
- `os.environ["..."]`
- `os.getenv("...")`
- `env("...")`

Search only in likely app code paths: `src/`, `lib/`, `app/`, `pages/`.

## Issue Categories

Classify findings as:
- **undocumented**: Used in code but not in templates.
- **unused-documentation**: Documented in templates but not referenced in scanned code.
- **deployment-visibility-gap**: Used/documented but not visible in deployment configs.
- **naming-mismatch**: Likely same variable purpose with inconsistent names (evidence must be strong).

## Output & Communication

The **security-reviewer** owns the generated artifact.
1. **Persistence**: Write the report to `docs/ENV_REPORT.md`.
2. **Decision Log**: Append a short entry to `docs/DECISIONS.md`.
3. **Communicate**: Post the summary to the **current Codex thread**.

### Required Output Structure (docs/ENV_REPORT.md)
- **Summary**: Short overview.
- **Documented Variables**: | Variable | Source |
- **Referenced Variables**: | Variable | Evidence Pattern |
- **Deployment-Visible Variables**: | Variable | Config Source |
- **Issues Tables**: (Undocumented, Unused, Visibility Gaps, Mismatches).
- **Recommendations**: Short practical next steps.
- **Limitations**: Missing configs, partial coverage, platform secret uncertainty.

## Completion Rules

- **If no env template exists**: Skip skill and log reason in `docs/DECISIONS.md`.
- **If no issues are found**: Still write `docs/ENV_REPORT.md` and mark as clean.