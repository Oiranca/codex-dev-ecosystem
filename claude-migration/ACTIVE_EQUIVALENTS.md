# Claude -> Codex Active Equivalents

Date: 2026-04-01

This file records which Claude settings have an active Codex equivalent and which were preserved as reference-only because Codex does not expose a 1:1 global setting.

## Active equivalents already present in `~/.codex/config.toml`

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` -> `features.multi_agent = true`
- GitHub plugin enabled in Claude -> `[plugins."github@openai-curated"] enabled = true`
- Claude status line intent -> Codex `tui.status_line = ["model-with-reasoning", "context-remaining", "project-root", "git-branch", "context-used"]`
- Project trust semantics -> `[projects."..."] trust_level = "trusted"`

## Preserved as compatibility references only

- `hooks/hooks.json`
  - Codex does not execute Claude hook events directly.
  - Stored at `~/.codex/claude-migration/hooks/hooks.claude.json`.
- `settings.json` / `settings.example.json`
  - Claude-specific schema and plugin ids are not loaded by Codex.
  - Stored for reference at `~/.codex/claude-migration/settings.active.claude.json` and `settings.example.claude.json`.
- `.mcp.json`
  - Preserved as source reference. Codex MCP configuration is managed through `~/.codex/config.toml` and connector/plugin tooling.
- `.claude-plugin/plugin.json`
  - Preserved as source metadata at `~/.codex/claude-migration/plugin/plugin.claude.json`.
- `statusline-command.sh`
  - Preserved as a Claude-compatible script reference. Codex is currently using a native `tui.status_line` array instead of a shell callback.

## Usable migrated assets

- Claude agents are already available as Codex skills under `~/.codex/skills/agent-*`.
- Claude agents are also available as Codex custom subagents under `~/.codex/agents/*.toml`.
- Claude commands are already available as Codex skills under `~/.codex/skills/command-*`.
- Claude reusable skills are already available under `~/.codex/skills/*`.
- Claude scripts remain available under:
  - `~/.codex/scripts/*`
  - `~/.codex/scripts/claude-compat/*`
- Claude references, plans, templates, and memory are now preserved under:
  - `~/.codex/claude-migration/reference/`
  - `~/.codex/claude-migration/plans/`
  - `~/.codex/claude-migration/templates/`
  - `~/.codex/memories/`
