# Claude -> Codex Global Migration

This folder was generated automatically to adapt a Claude multi-agent setup for global Codex use.

## What was migrated
- Skills: `~/.claude/skills/*` -> `~/.codex/skills/*`
- Agents: `~/.claude/agents/*.md` -> `~/.codex/skills/agent-*/SKILL.md`
- Custom subagents: `~/.claude/agents/*.md` -> `~/.codex/agents/*.toml`
- Commands: `~/.claude/commands/*.md` -> `~/.codex/skills/command-*/SKILL.md`
- Scripts: `~/.claude/scripts/*` -> `~/.codex/scripts/claude-compat/*` with `.claude` paths rewritten to `.codex`
- Reference docs: `~/.claude/reference/*` -> `~/.codex/claude-migration/reference/*`
- Templates: `~/.claude/templates/local-scaffold/*` -> `~/.codex/claude-migration/templates/local-scaffold/*`
- Memory: `~/.claude/memory/*` -> `~/.codex/memories/*`
- Plans: `~/.claude/plans/*` -> `~/.codex/claude-migration/plans/*`
- Claude config artifacts preserved for compatibility review:
  - `~/.claude/.mcp.json` -> `~/.codex/claude-migration/mcp.claude.json`
  - `~/.claude/settings.json` -> `~/.codex/claude-migration/settings.active.claude.json`
  - `~/.claude/settings.example.json` -> `~/.codex/claude-migration/settings.example.claude.json`
  - `~/.claude/hooks/hooks.json` -> `~/.codex/claude-migration/hooks/hooks.claude.json`
  - `~/.claude/.claude-plugin/plugin.json` -> `~/.codex/claude-migration/plugin/plugin.claude.json`
  - `~/.claude/statusline-command.sh` -> `~/.codex/claude-migration/statusline-command.claude.sh`

## Notes
- Codex does not execute Claude hooks/settings/plugin manifests directly; those are preserved as reference artifacts, not active runtime config.
- Active Codex-native equivalents are documented in `~/.codex/claude-migration/ACTIVE_EQUIVALENTS.md`.
- If a migrated workflow still references Claude-specific runtime semantics, adjust the corresponding `SKILL.md`.

## Rollback
Backups are in: `~/.codex/claude-migration-backups/`

## Cleanup Pass (20260325-150514)
- Rebuilt all migrated `agent-*` and `command-*` skills with a single frontmatter block.
- Normalized references from Claude wording to Codex wording across all migrated `SKILL.md` files.
- Normalized script labels and fixed missing Python import in `validate-local.sh`.
- Backup for this cleanup: `/Users/samuelromeroarbelo/.codex/claude-migration-backups/20260325-150514-cleanup`.

## Native V2 Pass (20260325-150759)
- Converted migrated `agent-*` and `command-*` skills to Codex-native orchestration guidance.
- Removed direct runtime command blocks based on `agent-runtime.py`.
- Kept legacy scripts available as compatibility utilities only.
- Backup for this pass: `/Users/samuelromeroarbelo/.codex/claude-migration-backups/20260325-150759-native-v2`.

## Supplemental Pass (2026-04-01)
- Migrated the remaining reusable non-runtime assets that were still only present in `~/.claude`.
- Preserved Claude-only config artifacts as compatibility references instead of pretending they are active Codex config.
- Added `ACTIVE_EQUIVALENTS.md` to document which Claude behaviors already have Codex-native coverage.
