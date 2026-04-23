# Global Codex Home

This repository is the versionable subset of `~/.codex`.

It is tuned to keep always-on context small without lowering code quality, review quality, or validation quality.

## Repository Layout

- `agents/`: custom subagent definitions
- `skills/`: reusable capabilities and playbooks, not role mirrors
- `scripts/`: helper scripts and local validators; `agent-runtime.py` is compatibility-only, not the default coordination path
- `rules/`: human-readable operating guidance
- `hooks.json`: session-start hooks
- `config.example.toml`: shareable baseline config

## Roles vs Skills

Keep one source of truth per concern:

- `agents/*.toml` owns role behavior for delegation and orchestration
- `skills/` owns reusable capabilities and multi-step playbooks
- do not duplicate role definitions across agents and skills
- if a workflow needs a team lead, route it through the agent layer; if it needs a reusable procedure, keep it as a skill

## Default Operating Model

Keep always-on context small. Store only universal rules in always-loaded files. Move specialized policy into separate files and read it only when the task needs it.

Current defaults:

- `caveman ultra` auto-loaded on startup/resume and kept for the full session unless the user disables it
- `gpt-5.4` with `medium` reasoning effort as the default baseline
- `multi_agent = true` in the local home config so delegation is available when needed
- `GitHub`, `Linear`, and core hooks enabled
- `Playwright` and `Stitch` stored as commented on-demand blocks in `config.toml`

## Rule Files

Always-on rule file:

- `rules/global-guidelines.md`

Load supplemental rule files only when relevant:

- `rules/github-guidelines.md`: GitHub issues, pull requests, reviews, and branch publishing
- `rules/agent-guidelines.md`: multi-agent work, worktrees, delegated implementation, delegated review
- `rules/handoff-guidelines.md`: handoff document updates
- `rules/ecosystem-guidelines.md`: boundary rules for roles, skills, playbooks, and de-duplication

This split keeps default prompt weight lower while preserving the same guidance when a task actually needs it.

## Memory Usage

`AGENTS.md` is intentionally minimal.

Use memory lazily:

- do not inline recent observation lists by default
- use `mem-search` or `get_observations([...])` only when prior work is relevant
- fetch only the smallest amount of prior context that unblocks the task

## Tooling Strategy

Default-on tools should be the tools you regularly need.

Recommended baseline:

- keep `GitHub` enabled if you often inspect, review, or publish PRs
- keep `Linear` enabled if you actively track work there
- keep browser and design MCP servers disabled unless you are actively using them
- enable multi-agent mode only for tasks that truly benefit from parallel execution

If you need an on-demand server, uncomment its block in `config.toml` and restart Codex.

## Communication Validation

Use the local validator when refining `caveman ultra` output examples:

```bash
python3 scripts/validate-caveman-ultra.py --text "status update here"
python3 scripts/validate-caveman-ultra.py --file /path/to/draft.txt
```

## Caveman Launchers

Use the local wrappers when you want the strongest possible local caveman injection at session start:

```bash
~/.codex/scripts/codex-caveman-start.sh
~/.codex/scripts/codex-caveman-start.sh -- fix the navbar spacing
~/.codex/scripts/codex-caveman-resume.sh --last
~/.codex/scripts/codex-caveman-exec.sh -- --skip-git-repo-check -- summarize this folder
~/.codex/scripts/codex-caveman-review.sh --uncommitted
```

Argument rule:

- pass Codex flags before `--`
- pass the optional task after `--`

Shell aliases live in `scripts/caveman-aliases.zsh`.
If your shell sources that file, you get:

- `cvx` -> caveman interactive start
- `cvxr` -> caveman resume last session
- `cvxe` -> caveman non-interactive exec
- `cvxrv` -> caveman review of uncommitted changes

Limit:

- these wrappers strengthen the local startup prompt
- they do not override system or developer instructions imposed by the host runtime

## Ignored Local State

`.gitignore` excludes machine-local and sensitive runtime artifacts, including:

- auth and session state
- SQLite databases and logs
- caches and plugin cache
- shell snapshots and sessions
- local `config.toml`
- local `memories/`
- generated local `AGENTS.md`

## Maintenance Rules

- keep always-loaded files short
- avoid duplicating the same policy across rules, memory files, and README text
- avoid duplicating the same role contract across `agents/` and `skills/`
- prefer on-demand tools over permanently enabled tool stacks
- raise reasoning effort only for tasks that truly need deeper analysis
