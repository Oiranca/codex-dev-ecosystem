---
name: "repo-profile"
description: "Build or refresh the repository profile by generating both `docs/STACK_PROFILE.md` and `docs/INVENTORY.md` from manifests, configuration, and high-signal structure."
allowed-tools: ["read", "search", "edit"]
---

# Repo Profile

Use this skill to generate the two core repository context artifacts in one pass:
- `docs/STACK_PROFILE.md`
- `docs/INVENTORY.md`

This skill is the single owner of:
- stack classification;
- runtime and package manager detection;
- tooling and deployment signals;
- primary run commands;
- repository shape;
- project surfaces;
- key configuration paths.

## Hard Rules

- Read only manifests, config files, and existing docs.
- Do not read source file contents except for path-level discovery.
- Maximum 15 file reads total.
- Maximum directory depth: 3 levels.
- Stop early when evidence is already high-confidence.
- Reuse existing artifacts when the fingerprint is unchanged.

## Workflow

### 1. Detect stack facts

Determine:
- language;
- framework;
- runtime;
- bundler;
- package manager;
- testing and validation tooling;
- deployment signals;
- primary run commands for `dev`, `build`, `test`, and `lint`.

### 2. Detect repository structure

Determine:
- repository shape;
- top-level directories;
- project surfaces;
- important configuration paths;
- notable structural patterns or ambiguities.

### 3. Write both artifacts

Write:
- `docs/STACK_PROFILE.md`
- `docs/INVENTORY.md`

Keep the two artifacts consistent with each other.

## Output

### Stack Profile
Short summary plus evidence-backed stack table and run commands.

### Inventory
Short summary plus repository shape, directory structure, project surfaces, and configuration paths.

### Open Uncertainties
Anything still ambiguous after the evidence pass.
