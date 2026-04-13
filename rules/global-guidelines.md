# Global Operating Guidelines

These are the cross-repository operating guidelines preserved from the previous Claude setup and adapted for Codex.

They complement the existing Codex defaults and do not replace tool-specific configuration such as [`default.rules`](/Users/samuelromeroarbelo/.codex/rules/default.rules).

## Core Working Principles

- Prefer small, focused changes over broad rewrites.
- Prefer analysis before implementation when scope is unclear.
- Prefer minimal context usage over broad repository scans.
- Prefer existing project conventions over introducing new patterns.
- Prefer gradual validation over running full pipelines unnecessarily.

## Context Compression

Use `caveman` primarily for context/token reduction, not as a forced chat persona.

- keep global memories, preference docs, and reusable guidance compressed when practical
- prefer short, information-dense prose in files likely to be loaded into context
- preserve exact technical meaning, code, paths, commands, links, dates, and structure
- response style can still vary by user request; context compression is separate from chat tone

## GitHub Communication

All GitHub-facing communication should be written in English, regardless of the language used by the user in chat.

This applies to:

- issue titles and bodies
- pull request titles and descriptions
- commit messages
- PR review replies
- inline PR comments
- issue or PR follow-up comments

The user-facing chat response can still follow the user's language.

## GitHub Project Hygiene

When work starts on a tracked GitHub issue, keep the project state aligned with reality:

- move the issue to `In Progress` when implementation begins
- do not leave an actively worked issue in `Todo`
- if an issue already has an open PR, it should not remain in `Todo`

## Branch and PR Discipline

- Default to one issue per branch unless the user explicitly wants combined scope.
- Do not merge branches or PRs unless the user explicitly asks for it.
- Before implementing GitHub issue work, check for open PR overlap so existing in-flight work is not duplicated.

## Parallel Agent / Worktree Hygiene

When explicitly using multiple agents or parallel worktrees:

- base worktrees on the current working branch
- keep file ownership disjoint across parallel workers
- prefer sequential execution when two tasks would touch the same file

These are best practices to reduce stale-context fixes and merge conflicts.

## Agent Delegation Policy

Codex can implement work directly, but delegation should be the default when the task clearly benefits from separation of responsibilities.

- use agents for well-scoped implementation, review, QA, or documentation tasks
- keep orchestration in the main session and avoid duplicating delegated work locally
- do not delegate blocking work if the next step depends immediately on the result and it is faster to do it directly
- when delegating code changes, assign clear file ownership
- when multiple agents run in parallel, each agent must have a disjoint write scope

This keeps Codex practical while preserving most of the coordination discipline from the previous Claude setup.

## Recommended Issue Workflow

For non-trivial GitHub issue work, prefer this execution order:

1. understand scope and check for overlap with open PRs
2. move the issue to `In Progress` if the project uses tracked states
3. implement the change directly or delegate implementation to an execution agent
4. validate with focused tests first, then broader checks when needed
5. perform a review pass for correctness, regressions, and security-sensitive surfaces
6. push the branch and update the PR or issue context

This is a recommended flow, not a hard requirement. Small tasks can skip stages when that would only add overhead.

## Main Session Boundaries

The main Codex session may inspect files, edit code, and run validation commands. However, when using agents, the main session should still stay disciplined:

- avoid broad reads when a few targeted files are enough
- avoid redoing implementation that was already delegated
- avoid mixing orchestration and overlapping edits across multiple workers
- keep changes traceable to the issue, review thread, or requested scope

The goal is not strict isolation for its own sake, but predictable coordination and lower context churn.

## Documentation Ownership

Documentation can be updated by the main session or by an agent, depending on the task, but ownership should stay explicit:

- user-facing docs such as `README.md`, changelogs, and usage docs should usually be updated after code behavior is confirmed
- architecture docs and ADR-style decisions should reflect the implemented system, not speculative design
- when splitting work across agents, assign documentation files to exactly one owner

This adapts the stricter Claude ownership model into a Codex-compatible guideline without forbidding pragmatic direct edits.
