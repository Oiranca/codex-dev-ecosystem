# Agent Guidelines

Load when using multiple agents, worktrees, or delegated execution/review flows.

## Parallel Agent and Worktree Hygiene

- base worktrees on the current working branch
- assign disjoint file ownership across parallel workers
- prefer sequential work when tasks touch the same file

## Delegation Policy

- prefer delegation when the task benefits from separation of responsibilities
- use agents for scoped implementation, review, QA, or docs
- orchestrate in the main session; do not duplicate delegated work locally
- do not delegate blocking work if the next step depends on that result and direct work is faster
- assign clear file ownership when delegating
- parallel agents must have disjoint write scope

## Main Session Boundaries

- prefer targeted file reads over broad scans
- do not redo delegated implementation
- avoid overlapping edits across workers
- keep changes traceable to the issue, review thread, or requested scope

## Documentation Ownership

- update user-facing docs only after behavior is confirmed
- architecture docs and ADRs should reflect the implemented system, not speculative design
- when splitting work across agents, keep one owner per doc file
