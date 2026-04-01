---
name: "fingerprint"
description: "Detect repository changes using a git-first fingerprint strategy and classify them as none, non-material, or material to control downstream agent execution."
allowed-tools: ["read", "execute", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Fingerprint

Use this skill as the **mandatory first step of every cycle**.

Its job is to detect whether the repository changed in a meaningful way and decide whether downstream agents should run. This skill does not analyze code; it only detects and classifies change.

## Purpose

- Prevent redundant analysis when no changes exist.
- Control the execution scope of the Agent Team.
- Maintain the source of truth for repository state in `local metadata state file`.

## Gating Policy

- **Cost Class**: CHEAP (Low-cost).
- **Mandatory**: Always run at the beginning of every cycle; never skip.
- **Authorization**: No explicit authorization needed.
- **Recovery**: If `local metadata state file` is missing or corrupt, run anyway and rebuild state.

## Primary Goals

1. **Update State**: Update `local metadata state file`.
2. **Log Decision**: Append a short decision entry to `docs/DECISIONS.md`.

## Detection Strategy

Use a git-first working-tree strategy.

### Preferred Commands
1. `git diff --name-only --cached`.
2. `git diff --name-only`.
3. `git ls-files --others --exclude-standard`.

Combine results to detect staged files, unstaged files, and untracked files.

## Change Classification

Classify the cycle as one of the following:

### 1. none
- **Definition**: No changed files detected.
- **Behavior**: Stop downstream execution; return exit code 2; set `material_change = false`.

### 2. non-material
- **Definition**: Changed files detected, but none match material patterns.
- **Behavior**: Allow downstream execution with limited scope; set `material_change = false`.

### 3. material
- **Definition**: At least one changed file matches material patterns, or legacy fallback is used.
- **Behavior**: Allow full downstream execution; set `material_change = true`.

## Material File Categories

Treat these as material signals:

### Dependency and package signals
- `package.json`.
- Lockfiles.
- Workspace manifests.

### Build and stack signals
- `tsconfig.*`.
- `astro.config.*`.
- `vite.config.*`.
- `next.config.*`.
- `nuxt.config.*`.
- `svelte.config.*`.

### Container and runtime signals
- `Dockerfile`.
- `docker-compose.*`.

### Deployment signals
- `netlify.toml`.
- `vercel.json`.
- `.github/workflows/*`.

### App surface signals
- `src/pages/**`.
- `src/routes/**`.
- `app/**`.

## Fingerprint Generation

For changed files only:
- Prioritize material files first.
- Hash at most 15 files.
- Hash raw bytes only; do not parse file contents.
- Sort file hashes, concatenate them, and compute a final SHA-256 fingerprint.
- **Deleted files**: Must still count as changes and be recorded in `changed_files`.

## Legacy Fallback Mode

Use fallback mode if not inside a git repository, git commands fail, or changed file count exceeds 200.

### Fallback Behavior
- Use legacy 15 high-signal files.
- Treat all fallback detections as material.
- Set `detection_mode = "legacy-fallback"`.
- Otherwise, set `detection_mode = "git-working-tree"`.

## State File Behavior

- **Read Policy**: Read only `local metadata state file`. Do not read source files for context.
- **Corrupt State**: If `local metadata state file` is corrupt JSON, delete it and treat the cycle as a first run.
- **Workspace**: If `docs/` does not exist, create it.
- **Errors**: If a file cannot be hashed due to permissions, skip it, continue, and record the limitation.

## Required State Output

Write the following fields to `local metadata state file`:
- `fingerprint`
- `previous_fingerprint`
- `cycle_count`
- `last_run`
- `material_change`
- `change_type`
- `detection_mode`
- `changed_files`
- `files_hashed`

## Console Output Rules

Print only short structured summary lines:
- Changed files count.
- Change type.
- Material change (yes/no).
- Fingerprint hash.

*Do not print inline code or verbose debug output.*

## Completion Rules & Communication

Upon completion, the agent (typically **stack-analyzer**) must **Communicate** the result to the **current Codex thread**.

- **If `change_type = "none"`**: Stop downstream execution; return exit code 2; log the skip in `docs/DECISIONS.md`.
- **If `change_type = "non-material"`**: Continue with limited downstream scope; log the reduced-scope path in `docs/DECISIONS.md`.
- **If `change_type = "material"`**: Continue with full downstream evaluation; log the full path in `docs/DECISIONS.md`.