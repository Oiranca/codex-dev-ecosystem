---
name: "repo-inventory"
description: "Build or update a lightweight repository inventory covering directory structure, manifests, dependencies, scripts, tooling, and key configuration files."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Repo Inventory

Use this skill to build or update `docs/INVENTORY.md` so downstream agents can understand the repository structure without exploring blindly.

This skill is structural only.
It does not read source file contents.

## Purpose

Document the repository's internal organization and surfaces:
- repository shape.
- directory structure.
- project surfaces.
- dependency signals.
- scripts and tooling.
- key configuration files.

## Gating Policy

- **Cost Class**: LOW-COST (CHEAP).
- **Authorization**: Requires an active milestone.
- **Trigger**: Run during **Milestone 1** (Detection & Inventory) or **Milestone 2** (Full Inventory) depending on the playbook.
- **Skip Conditions**:
  - Skip if the repository fingerprint is unchanged and `docs/INVENTORY.md` already exists.
  - Never run on every cycle.

## Hard Rules

- **Maximum directory depth**: 3 levels.
- **Maximum file reads**: 10.
- **Read policy**: Read only manifests, config files, and existing documentation.
- **No source**: Do not read source code contents.
- **Exclusions**:
  - `node_modules/`, `.git/`, `dist/`, `build/`, `vendor/`, `.next/`, `.turbo/`.
- **Persistence**: If `docs/INVENTORY.md` exists, use incremental update mode.
- **Integrity**: Preserve any `` annotations. If the file is corrupt, discard and rebuild from scratch.

## Inventory Goals

The agent must document the following:
1. **Repository Shape**: Single app, Monorepo, etc.
2. **Directory Structure**: Tree view (up to 3 levels).
3. **Project Surfaces**: Classification as frontend, backend, library, etc.
4. **Dependency Signals**: Major frameworks and tool signals.
5. **Scripts**: Key runnable commands.
6. **Tooling Signals**: Detection of eslint, prettier, jest, turbo, nx, etc.
7. **Key Configuration Files**: Path and purpose.

## What to Inspect (High-Signal Files)

- `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`.
- `tsconfig.json`, `vite.config.*`, `astro.config.*`, `next.config.*`.
- `Dockerfile`, `docker-compose.*`.
- `.husky/*` (first relevant file).
- `README.md` (only if needed for context).

## Output & Communication

The **repo-analyzer** is the owner of this artifact. Upon completion:

1. **Persistence**: Write the results to `docs/INVENTORY.md`.
2. **Decision Log**: Append a short completion note to `docs/DECISIONS.md`.
3. **Communicate**: Post the inventory summary to the **current Codex thread** so the Team Lead can update the project context.

### Required Inventory Structure (docs/INVENTORY.md)
- **Summary**: Overview of repository shape.
- **Repository Shape**: Single application | Multi-application | Monorepo | Hybrid.
- **Directory Structure**: Tree view up to 3 levels.
- **Project Surfaces**: Table with Surface, Path, and Type.
- **Dependency Signals**: Framework and tool signals.
- **Scripts**: Key scripts and their commands.
- **Tooling Signals**: Status of linters, testers, and monorepo tools.
- **Key Configuration Files**: List of paths and locations.
- **Limitations**: Record truncation or missing manifests.

## Completion Rules

- **If no manifest is found**: Catalog the directory structure only and add a warning to the report and `docs/DECISIONS.md`.
- **If Monorepo detected**: Record it explicitly, stop traversal at 3 levels, and note truncation.
- **Incremental mode**: Update only changed sections and preserve manual annotations.