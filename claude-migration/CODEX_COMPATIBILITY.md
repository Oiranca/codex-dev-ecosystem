# Codex Compatibility Contract (Final)

Date: 2026-03-25
Scope: all migrated assets from `~/.claude` to `~/.codex`

## Guaranteed State

- Migrated skills live under `~/.codex/skills/*` (excluding `.system`).
- Every migrated `SKILL.md` has valid frontmatter with `name` and `description`.
- Migration is Codex-native:
  - Coordination uses the current Codex thread.
  - Delegation guidance uses `spawn_agent` / `send_input`.
  - Legacy runtime control-plane commands are removed from skill workflows.
- Legacy scripts remain available for compatibility only:
  - `~/.codex/scripts/*`
  - `~/.codex/scripts/claude-compat/*`

## Non-Goals

- This migration does not force-delete legacy compatibility scripts.
- This migration does not change Codex system skills under `~/.codex/skills/.system`.

## Ongoing Validation

Run:

```bash
bash ~/.codex/claude-migration/verify-codex-migration.sh
```

This verifier checks:
- migrated skill count,
- frontmatter integrity,
- banned legacy references,
- Codex Native Note presence,
- shell/python script syntax.

## Rollback

Backups are stored in:

`~/.codex/claude-migration-backups/`

Use the latest timestamped backup directory to restore previous state if needed.
