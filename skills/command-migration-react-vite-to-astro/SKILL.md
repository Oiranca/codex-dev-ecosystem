---
name: "command-migration-react-vite-to-astro"
description: "Incremental migration workflow from React + Vite to Astro using islands architecture. Validates preconditions, inventories routes, plans architecture, migrates components in batches, and validates."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `migration-react-vite-to-astro`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /migration-react-vite-to-astro

You are the **Main Agent (Team Lead)**. Execute a structured incremental migration.

## Gating Policy
- Require HIGH confidence of: 1. React primary framework AND 2. Vite is the bundler.
- Pre-conditions: `docs/STACK_PROFILE.md` exists; Astro is NOT the active framework.
- Milestone 2 requires authorization; Milestone 4 requires explicit justification.

## Milestone Sequence

### Milestone 1 — Validation & Inventory Swarm
Spawn in parallel:
1. **stack-analyzer**: Confirm pre-conditions. STOP if any fail.
2. **repo-analyzer**: Run repo-inventory and route-mapper. Output `docs/INVENTORY.md` and `docs/ROUTE_MAP.md`.

### Milestone 2 — Migration Architecture
Assign to **solution-architect**:
- Classify components (STATIC, ISLAND, SHARED). Define Route Plan.
- Output `docs/ARCHITECTURE.md`.

### Milestone 3 — Incremental Migration
Assign to **migration-engineer**:
- Use `react-vite-to-astro-migration`.
- Migrate **maximum 5 components per cycle**. No exceptions.
- Order: STATIC -> SHARED -> ISLAND.
- Never delete original React files.

### Milestone 4 — Validation & Cleanup Swarm
Spawn in parallel:
1. **qa-engineer**: Run `smoke-journeys` for end-to-end regression.
2. **software-engineer + security-reviewer**: Remove unused Vite/React dependencies and update docs.

## Hard Rules
1. One milestone per cycle. No batching.
2. If migration breaks the build, stop immediately.
3. Never auto-merge PRs.
4. Component classification must be evidence-based.
5. Log every decision in `docs/DECISIONS.md`.
