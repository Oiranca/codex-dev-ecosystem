# Global Operating Guidelines

Canonical always-on guidance for `~/.codex`.

Keep this file short. Put task-specific policy in sibling rule files and load or read those only when needed.

## Core Working Principles

- Small focused changes over broad rewrites.
- Analyze before implementing when scope is unclear.
- Minimal context over broad scans.
- Existing conventions over new patterns.
- Gradual validation over full pipelines.

## Communication Mode

Communication style comes from installed plugins, project instructions, and the active session.

- avoid duplicating plugin-owned style policy here
- keep global rules tool- and workflow-focused
- if a plugin provides a default prompt or activation flow, prefer that over custom home-grown hooks
- when `caveman ultra` is active, treat it as a blocking output contract, not a preference
- when `caveman ultra` is active, rewrite any draft that would likely fail `scripts/validate-caveman-ultra.py`

## Context Compression

- compress memories, preferences, and reusable guidance when practical
- keep likely-loaded files dense and low-noise
- preserve exact meaning for code, paths, commands, links, dates, and security-sensitive text

## Source of Truth

For Codex behavior, this file is the canonical human-readable global guidance.

- use Codex-owned files in this home as the operating authority
- ignore non-Codex instruction files unless the user explicitly asks for them in the current turn

## Supplemental Rule Files

Load only when the task needs them:

- `rules/github-guidelines.md`
- `rules/agent-guidelines.md`
- `rules/handoff-guidelines.md`
