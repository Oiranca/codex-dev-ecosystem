---
name: "react-vite-to-astro-migration"
description: "Incrementally migrate React + Vite components to Astro using islands architecture while preserving behavior and deferring risky components."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# React Vite to Astro Migration

Use this skill to migrate a React + Vite application incrementally toward Astro using islands architecture.

**Constraint**: This is a migration playbook skill. It must never run outside an approved migration workflow.

## Purpose

Convert selected React + Vite components into Astro-ready structure by classifying them as **STATIC**, **ISLAND**, or **SHARED**, and migrating them in small, reversible batches.

## Gating Policy

- **Cost Class**: EXPENSIVE (High-cost).
- **Authorization**: Requires explicit playbook justification and is only allowed when the `MIGRATION_REACT_VITE_TO_ASTRO` playbook is active.
- **Pre-conditions**:
  - `docs/STACK_PROFILE.md` must confirm React + Vite with HIGH confidence.
  - Must be executed during **Milestone 4: Incremental Migration**.
  - `docs/ROUTE_MAP.md` and `docs/ARCHITECTURE.md` (with migration classification) must exist.
- **Skip Conditions**:
  - Skip if Astro is already detected as the active framework.
  - Skip if the build is currently failing.

## Hard Rules

- **Batch Limit**: Maximum 5 components per cycle.
- **Batch Order**: Prefer batches in this order: 1. STATIC -> 2. SHARED/layout -> 3. ISLAND. (Max 5 per cycle)
- **Read Limits**: Maximum 13 file reads total (6 documentation, 5 source components, 2 config).
- **Safety**: Create new files only; **never delete original React files**.
- **Scope**: Never migrate more than one route surface family in the same batch unless explicitly planned.
- **Integrity**: Never guess interactivity classification. If uncertainty exists, defer the component.

## Required Inputs (via current Codex thread)

As context is not shared natively, the **Team Lead** must ensure the **migration-engineer** has access to these artifacts:
- `local metadata state file`.
- `docs/STACK_PROFILE.md`.
- `docs/ROUTE_MAP.md`.
- `docs/ARCHITECTURE.md`.
- `docs/INVENTORY.md`.
- `docs/MIGRATION_STATE.md` (if present).

## Precondition Check

Abort immediately if any of the following fail:
- Framework is not React.
- Bundler is not Vite.
- Confidence is not HIGH.
- Migration playbook is not active.
- Architecture classification is missing.

## Classification Rules

### STATIC
A component is STATIC if it has no hooks, no local state, no effects, and no required runtime interactivity.
- **Target**: `.astro`.
- **Transformation**: Remove React imports, move props to `Astro.props`, convert JSX to Astro syntax, and `className` to `class`.

### ISLAND
A component must remain an ISLAND if it uses hooks, state, effects, or event-driven browser behavior.
- **Target**: Keep interactive component as `.tsx`/`.jsx` and create an Astro wrapper.
- **Hydration Policy**: Prefer `client:visible` or `client:idle`. Use `client:load` only if immediate interactivity is required.

### SHARED
Structural components (e.g., layouts).
- **Target**: `.astro`.
- **Transformation**: Convert shell to Astro and replace child rendering with `<slot />`.


## Workflow Milestones

1. **Validation & Inventory**: Confirm React + Vite, update `docs/STACK_PROFILE.md` and `docs/INVENTORY.md`.
2. **Architecture**: Classify components in `docs/ARCHITECTURE.md`.
3. **Incremental Migration**: Execute batches of max 5 components.
4. **Verification**: Verify behavior and build integrity.

## Migration Policies

- **Styling**: Preserve existing styling (Tailwind, CSS Modules, etc.). Do not rewrite unless explicitly required.
- **Routes**: Only update route files if the milestone explicitly includes route migration.
- **Defer**: Defer components with complex shared state, router coupling, or animation-heavy behavior. Record reasons.

## Output & Communication

Upon completion of the batch, the **migration-engineer** must:

1. **Update Artifacts**:
   - Write/update migrated `.astro` files and wrappers.
   - Update `docs/MIGRATION_STATE.md` with the required structure.
   - Append a short entry to `docs/DECISIONS.md`.
2. **Communicate**: Post the status of the batch (migrated, deferred, or failed) to the **current Codex thread**.

### Required Migration State Structure (docs/MIGRATION_STATE.md)
- **Current Batch**: Short description.
- **Migrated Components**: | Source | Target | Classification | Reason | Status |
- **Deferred Components**: | Source | Reason |
- **Failed Components**: | Source | Reason | Rollback Performed |
- **Notes**: Progress and blockers.

## Completion Rules

- **Failure**: If a component breaks the batch, mark as failed, record rollback, and **do not delete originals**.
- **No Progress**: If no safe components are available, write an empty result and mark the batch as deferred.
