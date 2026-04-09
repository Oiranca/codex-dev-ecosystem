---
name: "astro-migration-playbook"
description: "Use when migrating a React + Vite codebase to Astro and you need one workflow for validation, planning, batched migration, and verification."
---

# Astro Migration Playbook

Single workflow for React + Vite to Astro migrations.

## Preconditions

Abort if any of these are false:
- primary framework is React;
- bundler is Vite;
- Astro is not already the active framework;
- the current build is not already broken for unrelated reasons;
- migration confidence is not `HIGH`.

## Hard Rules

- One milestone per cycle.
- Maximum 5 components per migration batch.
- Prefer this batch order: `STATIC` -> `SHARED` -> `ISLAND`.
- Never delete original React files during migration batches.
- Do not migrate more than one route family in a batch unless explicitly planned.
- Stop immediately if the build breaks.

## Workflow

### Milestone 1 — Validation and inventory

1. Confirm React + Vite preconditions from stack evidence.
2. Build or refresh:
   - `docs/STACK_PROFILE.md`
   - `docs/INVENTORY.md`
   - `docs/ROUTE_MAP.md`

### Milestone 2 — Migration architecture

Create or refresh `docs/ARCHITECTURE.md` with:
- route strategy;
- component classifications;
- hydration policy;
- dependency cleanup plan;
- validation and rollback strategy.

Component classifications:
- `STATIC`: no hooks, no state, no browser interactivity. Convert directly to `.astro`.
- `SHARED`: layout or shell structures. Convert to `.astro` and use `<slot />`.
- `ISLAND`: interactive components. Keep interactive logic in React and wrap from Astro with the lightest viable hydration directive.

### Milestone 3 — Incremental migration batch

For each selected component:
1. confirm classification with evidence;
2. migrate only the planned batch;
3. preserve styling and behavior;
4. create wrappers when interactivity must remain;
5. update `docs/MIGRATION_STATE.md`;
6. append decisions to `docs/DECISIONS.md` when present.

### Milestone 4 — Verification and cleanup

Run the narrowest validation that proves safety:
- `targeted-test-runner` first;
- `smoke-journeys` for runtime route confidence;
- `ci-checks` when broader validation is required.

Then clean up only what the batch made obsolete:
- unused imports;
- dead route wiring;
- no-longer-needed Vite or React dependencies;
- migration notes in docs.

## Output

### Migration Goal
Short description of the current migration objective.

### Preconditions
What was verified and what artifacts were consulted.

### Current Batch
Which routes or components are in scope.

### Migration Results
| Source | Target | Classification | Status | Reason |
|--------|--------|----------------|--------|--------|

### Deferred Items
| Item | Reason |
|------|--------|

### Validation
Commands or checks run and their results.

### Remaining Work
What is left for later milestones.
