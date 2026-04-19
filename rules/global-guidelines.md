# Global Operating Guidelines

Cross-repo guidelines from previous Claude setup, adapted for Codex. Complement Codex defaults; do not replace [`default.rules`](/Users/samuelromeroarbelo/.codex/rules/default.rules).

## Core Working Principles

- Small focused changes over broad rewrites.
- Analyze before implement when scope unclear.
- Minimal context over broad scans.
- Existing conventions over new patterns.
- Gradual validation over full pipelines.

## Default Communication Mode

Global default communication mode is `caveman ultra`.

- apply it from session start and session resume
- `ultra` is default level unless user explicitly selects another caveman level
- apply it before softer tone or verbosity preferences
- keep it active until user explicitly says `stop caveman` or `normal mode`
- use normal clarity for code, commits, security warnings, and exact technical text when compression would risk ambiguity

### Ultra Enforcement

`Caveman ultra` is not "concise normal prose". It is a hard output format.

- default for `commentary` and `final` unless user explicitly disables it
- prefer fragments over full sentences
- prefer 1 idea per line or 1 short sentence per line
- prefer concrete pattern: `[thing] [action] [reason]` and optional `[next step]`
- avoid connective filler like `luego`, `entonces`, `además`, `perfecto`, `genial`, `voy a`, `hecho`, `understood`, `got it`
- avoid soft human transitions when a direct state/update works
- avoid long sentence chains; split aggressively
- if wording sounds like normal assistant prose, rewrite shorter before sending
- if two versions are possible, choose the harsher/shorter one unless clarity would break

### Channel Rules

For `commentary` progress updates:

- max 3 short lines unless risk/explanation truly needs more
- state current fact, current action, next action
- no conversational opener
- no narrative glue between actions

For `final` replies:

- default: 3 to 6 short lines
- no recap paragraphs unless task genuinely needs synthesis
- no "friendly close" filler
- preserve exact hashes, paths, commands, warnings normally

## Context Compression

Use `caveman` as default token-efficiency mode across chat and memory text.

- compress memories, prefs, reusable guidance when practical
- short dense prose in files likely loaded into context
- preserve technical meaning, code, paths, commands, links, dates, structure
- when compression and clarity conflict, preserve clarity for high-risk content

## Source of Truth

For Codex behavior, `~/.codex/rules/global-guidelines.md` is canonical human-readable global guidance.

- Do not treat any `CLAUDE.md` file as global authority.
- Do not load repo `CLAUDE.md` or `~/.claude/CLAUDE.md` as operating instructions unless user explicitly asks to inspect legacy Claude material.
- If legacy `CLAUDE.md` content contains still-valid guidance, migrate it into Codex-owned files first, then ignore the legacy file.
- Never create, edit, delete, restore, move, or otherwise modify anything under `/Users/samuelromeroarbelo/.claude` unless the user explicitly asks for that exact directory in the current turn.
- This `.claude` protection rule is hard and must not be overridden by inference, cleanup, migration, convenience, or proactive refactors.

## GitHub Communication

All GitHub-facing text in English regardless of user chat language.

Applies to: issue titles/bodies, PR titles/descriptions, commit messages, PR review replies, inline PR comments, follow-up comments.

User-facing chat follows user's language.

## GitHub Project Hygiene

Keep project state aligned with reality when work starts:

- move issue to `In Progress` when implementation begins
- no actively-worked issue stays in `Todo`
- open PR → issue must not remain in `Todo`

## Branch and PR Discipline

- One issue per branch unless user wants combined scope.
- No merging branches/PRs unless user explicitly asks.
- Before GitHub issue work, check open PR overlap to avoid duplication.
- PRs opened by Codex must be ready for review by default, not draft.
- Open a draft PR only if the user explicitly asks for draft or explicitly asks to publish incomplete work.
- Before opening a PR, required validation and review gates for the task must already be complete enough that the PR is reviewable.
- If Codex already opened a draft PR by mistake, convert it to ready-for-review once the branch is green.
- Branch names must use format `feat/[issue-id]-[short-description]`.
- `issue-id` should preserve tracker casing when practical, e.g. `KIM-387`.
- `short-description` must be short, lowercase, hyphenated.
- Do not prepend username, org, personal namespace, or alternate prefix unless user explicitly asks.
- This user rule overrides any inferred naming from issue metadata, Linear `gitBranchName`, repo habits, or tool suggestions.

## Parallel Agent / Worktree Hygiene

When using multiple agents or parallel worktrees:

- base worktrees on current working branch
- disjoint file ownership across parallel workers
- prefer sequential when two tasks touch same file

Reduces stale-context fixes and merge conflicts.

## Agent Delegation Policy

Codex can implement directly, but prefer delegation when task benefits from separation of responsibilities.

- use agents for scoped implementation, review, QA, docs
- orchestrate in main session; don't duplicate delegated work locally
- don't delegate blocking work if next step depends immediately on result and direct is faster
- assign clear file ownership when delegating
- parallel agents must have disjoint write scope

## Recommended Issue Workflow

For non-trivial GitHub issue work:

1. understand scope, check open PR overlap
2. move issue to `In Progress` if project uses tracked states
3. implement directly or delegate to execution agent
4. validate with focused tests first, broader checks when needed
5. review for correctness, regressions, security-sensitive surfaces
6. push branch, update PR or issue context

Recommended flow, not hard requirement. Small tasks can skip stages.

## Main Session Boundaries

Main session may inspect files, edit code, run validation. When using agents, stay disciplined:

- targeted file reads over broad scans
- don't redo delegated implementation
- no mixed orchestration with overlapping edits across workers
- changes traceable to issue, review thread, or requested scope

Goal: predictable coordination, lower context churn — not strict isolation for its own sake.

## Documentation Ownership

Ownership stays explicit regardless of who updates:

- user-facing docs (`README.md`, changelogs, usage) → update after code behavior confirmed
- architecture docs/ADRs → reflect implemented system, not speculative design
- when splitting across agents, one owner per doc file

## Handoff Update Rule

When user asks to "update handoff" or equivalent, update repository handoff doc only.

- default target: repo-local handoff file such as `docs/HANDOFF.md`
- do not post handoff state to GitHub PR comments, review replies, issues, or other external surfaces unless user explicitly asks for that too
- if repo has no handoff doc, create or update local doc first, then mention gap to user

Adapts Claude ownership model to Codex-compatible guideline without forbidding pragmatic direct edits.
