---
name: "smoke-journeys"
description: "Run lightweight end-to-end smoke checks against a running dev or preview server to catch critical route regressions."
allowed-tools: ["read", "execute", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Smoke Journeys

Use this skill to run lightweight runtime smoke checks against a dev or preview server after a successful build.

This skill validates critical route availability and basic runtime health.
It does not perform deep browser automation.

## Purpose

Catch regressions that static checks may miss by validating a small set of critical routes against a live local server.

## Gating Policy

- **Cost Class**: EXPENSIVE (High-cost).
- **Authorization**: Requires explicit playbook justification naming this skill.
- **Skip Conditions**:
  - Skip if no code changes were made.
  - Skip if no web routes exist.
  - Skip if build did not pass.
  - Never run on every cycle.
  - Never run before a successful build.
- **Budget & Locks**:
  - Check `local skill budget metadata` before starting (Max 1 run per skill per cycle; requires explicit justification).
  - Respect `local lock metadata` when present before starting overlapping smoke validation.

## Required Inputs (via current Codex thread)

As context is not shared natively among Agent Teams, the **Team Lead** must ensure access to:
- `local metadata state file`
- `docs/STACK_PROFILE.md`
- `docs/ROUTE_MAP.md`
- `docs/QA_REPORT.md`

*Do not read source files.*

## Preconditions

Before running smoke checks:
- `docs/QA_REPORT.md` must show `build = PASS`.
- `docs/ROUTE_MAP.md` must exist.
- `docs/STACK_PROFILE.md` must provide a dev or preview run command.

If any precondition fails, skip the skill, record the reason, and append it to `docs/DECISIONS.md`.

## Server Startup Policy

- Start the dev or preview server as a background process.
- Use the run command from `docs/STACK_PROFILE.md`.
- Wait up to 60 seconds for readiness.
- **Readiness Strategy**:
  1. Successful HTTP response from the root route.
  2. Successful HTTP response from a known route.
  3. Confirmed listening server process.

**If the server does not become ready within 60 seconds**:
- Kill the process.
- Mark the run as `BLOCKED`.
- Stop execution.

*The server process must always be terminated, even on failure.*

## Route Selection Policy

Select at most 10 routes total from `docs/ROUTE_MAP.md`.
**Priority Order**:
1. Homepage.
2. Primary navigation pages.
3. Important static pages.
4. Resolvable dynamic routes.
5. API endpoints (only if useful for runtime verification).

- **Maximum total requests**: 20.
- **Dynamic Routes**: If no concrete testable path is available, skip it and record the limitation.

## Route Validation Rules

For each selected route, record URL, classification, HTTP status, response size, and result.
**A route PASSES if**:
- HTTP status is 200.
- Response is not empty.
- No obvious error indicators appear (e.g., `500`, `Internal Server Error`, stack traces, framework error overlays).

*Do not parse HTML deeply, take screenshots, or run browser automation.*

## Result Classification

Classify each route as:
- **PASS**: Healthy response.
- **FAIL**: Responded but showed error behavior.
- **BLOCKED**: Server startup failed or test could not run.
- **SKIP**: Route not testable under current constraints.

## Output & Communication

The **qa-engineer** is the primary owner of this artifact.
1. **Persistence**: Write results to `docs/SMOKE_REPORT.md`.
2. **Decision Log**: Append a short decision entry to `docs/DECISIONS.md`.
3. **Communicate**: Post the smoke run summary back to the **current Codex thread**.

### Required Report Structure (docs/SMOKE_REPORT.md)
- **Summary**: Short overview.
- **Server Startup**: | Command | Result | Notes |
- **Selected Routes**: | URL | Classification | Reason Selected |
- **Route Results**: | URL | Status | Response Size | Result |
- **Blocked or Skipped Routes**: | URL | Reason |
- **Overall Result**: PASS | PARTIAL | FAIL | BLOCKED
- **Limitations**: Document skipped dynamic routes, startup uncertainty, or truncation.

## Completion Rules

- **Startup Failure**: Mark all journeys as `BLOCKED`, stop immediately, and append a critical note to `docs/DECISIONS.md`.
- **Total Failure**: If all tested routes fail, mark as `FAIL` and append a critical note to `docs/DECISIONS.md`.
- **Partial/Full Success**: Record accordingly if at least one critical route passes and no blocking startup issue exists.