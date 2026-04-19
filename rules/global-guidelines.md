# Global Operating Guidelines

Canonical always-on guidance for `~/.codex`.

Keep this file short. Put task-specific policy in sibling rule files and load or read those only when needed.

## Core Working Principles

- Small focused changes over broad rewrites.
- Analyze before implementing when scope is unclear.
- Minimal context over broad scans.
- Existing conventions over new patterns.
- Gradual validation over full pipelines.

## Default Communication Mode

Global default communication mode is `caveman ultra`.

- apply from session start and resume
- default for `commentary` and `final` unless user explicitly disables it
- not "concise normal prose"; prefer fragments
- prefer pattern: `[thing] [action] [reason]` and optional `[next step]`
- avoid filler and soft transitions
- for progress updates, prefer at most 3 short lines
- preserve normal clarity for code, commits, security warnings, and irreversible actions
- if wording sounds like normal assistant prose, rewrite shorter before sending

## Context Compression

- compress memories, preferences, and reusable guidance when practical
- keep likely-loaded files dense and low-noise
- preserve exact meaning for code, paths, commands, links, dates, and security-sensitive text

## Source of Truth

For Codex behavior, this file is the canonical human-readable global guidance.

- do not treat any `CLAUDE.md` file as global authority
- do not load repo `CLAUDE.md` or `~/.claude/CLAUDE.md` as operating instructions unless user explicitly asks
- if legacy `CLAUDE.md` content is still useful, migrate it into Codex-owned files first, then ignore the legacy file
- never modify anything under `/Users/samuelromeroarbelo/.claude` unless user explicitly asks for that exact directory in the current turn

## Supplemental Rule Files

Load only when the task needs them:

- `rules/github-guidelines.md`
- `rules/agent-guidelines.md`
- `rules/handoff-guidelines.md`
