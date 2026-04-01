---
name: "route-mapper"
description: "Map application routes from framework routing conventions and configuration to produce a route inventory for web projects."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Route Mapper

Use this skill to build a route inventory for web applications that use file-based or convention-based routing.

This skill is for route discovery only.
It does not inspect business logic or component internals.

## Purpose

Produce a route map that helps architecture, migration, documentation, and validation workflows understand the exposed route surface of the application.

## Gating Policy

- **Cost Class**: MEDIUM.
- **Authorization**: Requires active milestone authorization from the **Team Lead** via the **current Codex thread**.
- **Skip Conditions**:
  - Skip if the project is not a web project.
  - Skip if `docs/STACK_PROFILE.md` does not confirm a routable framework.
  - Skip if the fingerprint is unchanged and `docs/ROUTE_MAP.md` already exists.
  - Never run speculatively.
- **Budget & Freshness**:
  - Check `local skill budget metadata` (Broader validation: Max 2 runs/cycle, max 1/skill).
  - Check `local artifact freshness metadata` and `local lock metadata` when present before regenerating `docs/ROUTE_MAP.md`.

## Required Inputs (via current Codex thread)

As context is not shared natively among Agent Teams, the **Team Lead** must ensure the agent has access to:
- `local metadata state file`.
- `docs/STACK_PROFILE.md` (To identify routing conventions).
- `docs/INVENTORY.md`.

## Supported Frameworks

Use routing conventions identified in `docs/STACK_PROFILE.md`. Supported routable frameworks include:

- **Astro** → `src/pages/`
- **Next.js** → `app/` or `pages/`
- **Nuxt** → `pages/`
- **SvelteKit** → `src/routes/`
- **Remix** → `app/routes/`

*If no supported routable framework is detected, skip and log the reason in `docs/DECISIONS.md`.*

## Hard Rules

- Scan **only** the route directory identified from the stack profile.
- Do **not** scan `src/`, `lib/`, or `components/` broadly.
- Maximum 50 route files enumerated.
- Maximum 5 file reads for dynamic route interpretation.
- Map file path to URL route.
- Classify each route as: **page**, **api**, **middleware**, or **special file**.
- Identify whether the route is: **static**, **dynamic**, or **catch-all**.
- Flag ambiguous routing conventions (e.g., presence of both `pages/` and `app/`).
- Each listed route must include its source file.
- If no route directory is found, write an empty route map with `confidence = LOW`.
- If more than 50 route files are detected, list the first 50 and note truncation clearly.

## Special File Handling

Recognize and classify framework-specific special files where applicable:
- layout files, loading files, error files, not-found files, middleware, and route handlers.
- **Important**: Do not treat all special files as user-facing pages.

## Output & Communication

The **repo-analyzer** is the primary owner of this skill's output. Upon completion:

1. **Persistence**: Write results to `docs/ROUTE_MAP.md`.
2. **Decision Log**: Append a short completion note to `docs/DECISIONS.md`.
3. **Communicate**: Post the route summary back to the **current Codex thread** so the Team Lead can update the project context.

### Required Output Structure (docs/ROUTE_MAP.md)
- **Summary**: Short overview of the routed application surface.
- **Framework**: Detected framework and route directory used.
- **Confidence**: HIGH | MEDIUM | LOW.
- **Route Counts**:
  - total route files detected
  - total routes listed
  - truncation: yes/no
- **Page Routes**: | URL Route | Type | Dynamic | Source File |
- **API Routes**: | URL Route | Type | Dynamic | Source File |
- **Middleware and Special Files**: | File | Classification | Source File |
- **Ambiguities**: List conflicting routing conventions or unclear cases.
- **Limitations**: Document truncation, missing route directories, or unsupported conventions.

## Completion Rules

- **If no routes are found**: Still write `docs/ROUTE_MAP.md`, mark confidence as LOW, and explain why.
- **If ambiguous routing is detected**: Record the ambiguity explicitly and do not guess a preferred convention without evidence.