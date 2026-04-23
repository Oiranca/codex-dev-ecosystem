# Ecosystem Boundaries

Use this file when creating, revising, or deleting agents and skills.

## Single Source Of Truth

- `agents/*.toml` owns delegated role behavior.
- `skills/` owns reusable capabilities and multi-step playbooks.
- Do not mirror the same role in both places.

## Classification Rule

Before adding a new artifact, classify it:

- Role: persistent specialist with ownership and delegation semantics.
- Capability: narrow reusable technique or tool-driven operation.
- Playbook: reusable multi-step workflow that may invoke several capabilities or agents.

Map each class to one home only:

- Role -> `agents/*.toml`
- Capability -> `skills/<name>/SKILL.md`
- Playbook -> `skills/<name>/SKILL.md`

## Anti-Duplication Rules

- Do not create duplicate skill wrappers for roles already owned by agents.
- Do not duplicate the same workflow text in multiple files unless one file is a short pointer.
- If a skill and an agent overlap, keep the role contract in the agent and reduce the skill to reusable procedure only.
- If two playbooks compete for the same top-level job, pick one as primary and scope the other to a narrower mode.
- If two skills touch the same area, assign one top-level owner and force the other to consume the owner's artifact instead of rediscovering the same facts.

## Functional Ownership Matrix

- Orchestration owner: `product-manager`
- Discovery owner: `scoped-discovery`
- Repository profile owner: `repo-profile`
- Review lane owners: `qa-engineer`, `security-reviewer`
- Review-only aggregation playbook: `command-team-review`
- Migration owner for React + Vite -> Astro: `astro-migration-playbook`

## Precedence Rules

- `product-manager` owns orchestration decisions. Do not create a second orchestration playbook that restates its workflow.
- `scoped-discovery` owns task scoping, reading plans, and exact symbol, usage, import/export, route, and config-key lookup.
- `repo-profile` owns stack classification, tooling detection, deployment signals, run-command extraction, repository shape, project surfaces, and structural path inventory.
- `command-team-review` owns review-only aggregation across lanes. It must not act as a general implementation orchestrator.
- `astro-migration-playbook` owns the full React + Vite -> Astro migration workflow, including batch execution rules.

## Preferred Architecture

- Main orchestration: `product-manager`
- Parallel split helper: `parallel-subagent-orchestration`
- Review-only orchestration: `command-team-review`
- Discovery: `scoped-discovery`, `repo-profile`, `route-mapper`
- Validation: `targeted-test-runner`, `ci-checks`, `smoke-journeys`, `completion-gate`

## Change Policy

When changing agents or skills:

1. Search for overlapping artifacts first.
2. Update the existing owner before creating a new artifact.
3. Remove stale references in docs, preferred skills, and examples.
4. Validate that every referenced skill exists.
5. Prefer deletion over keeping duplicate artifacts once references are gone.
