# Global Codex Home

This repository snapshot is the versionable subset of `~/.codex`.

## Intended tracked content

- `agents/`: custom Codex subagents in TOML format
- `skills/`: reusable custom and migrated skills
- `scripts/`: reusable helper scripts
- `rules/`: Codex rules
- `claude-migration/`: migration notes, references, templates, and compatibility docs
- `config.example.toml`: sanitized example config for recreating local setup

## Intentionally ignored

The `.gitignore` excludes machine-local state and sensitive/runtime artifacts, including:

- auth and session state
- SQLite databases and logs
- caches and plugin cache
- shell snapshots and sessions
- local `config.toml`
- local `memories/`
- migration backup directories

## Local setup

1. Keep your real local configuration in `config.toml`.
2. Use `config.example.toml` as the shareable baseline.
3. Add personal memories, auth, and runtime state locally only.
