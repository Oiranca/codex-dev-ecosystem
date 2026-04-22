---
name: aia-cli
description: "AIA CLI usage reference. Use when running AIA workflows, managing agents, monitoring executions, or using any `aia` command. Covers: aia init, agent create/list/edit/delete, mcp add/list/remove, workflow create/run/resume/stop/merge/send, analysis run/show/optimize, logs, execution lifecycle, worktrees, variants, consensus termination, rate limit auto-resume, and persistence structure. Triggers: aia, bunx aia, workflow run, agent create, mcp registry, execution, worktree, merge, analysis, logs, inbox."
---

# AIA CLI Reference

How to use the `aia` CLI to manage agents, workflows, and executions.

## Setup

```bash
bun install           # install dependencies
bunx aia init --name "project-name"   # initialize AIA project in cwd
```

Project config is stored in `aia/config.json`. Agents in `aia/agents/`, workflows in `aia/workflows/`.

### Installing `aia` globally

From the repo root:

```bash
bun run link          # builds @aia-core/cli and registers ~/.bun/bin/aia via bun link
```

`bun run link` runs `scripts/install-cli.sh`, which: checks that `bun` is installed, runs `bun install` if `node_modules/` is missing, builds `@aia-core/cli` (and its workspace deps), `chmod +x dist/bin.js`, then `bun link` from `apps/cli`. Make sure `~/.bun/bin` is on your `PATH`.

### Updating

```bash
aia upgrade                # git pull --ff-only + bun install + rebuild
aia upgrade --no-pull      # just rebuild (after local edits you don't want to commit)
aia upgrade --force        # pull even if the working tree is dirty
aia upgrade --json         # machine-readable envelope: { upgraded, repoRoot, branch, beforeSha, afterSha, version, pulled }
```

The command resolves the source repo from the realpath of the running binary. It only works for installs created via `bun run link`; it exits with `repo_not_found` if you copied `dist/bin.js` elsewhere.

## Agents

Agents are JSON definitions with a behavior prompt, model, and execution limits.

```bash
# List agents
bunx aia agent list

# Create (interactive or non-interactive)
bunx aia agent create
bunx aia agent create \
  --name "Developer" \
  --card "Senior TypeScript developer" \
  --behavior "You are a senior developer. ..." \
  --max-sessions 1 \
  --max-retries 2

# View / edit / delete
bunx aia agent show <id>
bunx aia agent edit <id>           # interactive editor
bunx aia agent delete <id> --force
```

**Agent definition fields:**
- `id` — slug derived from name
- `name`, `card` — display name and short description
- `behaviorPrompt` — the system prompt injected into every agent invocation
- `blacklist` — blocked shell commands (empty = no restrictions)
- `maxParallelSessions` — concurrent sessions (usually 1)
- `maxRetries` — retries on failure
- `model?` — optional model override (e.g., `"claude-haiku-4-5-20251001"`)
- `provider?` — optional AI provider override such as `"claude"` or `"codex"`. Overrides the project default provider for this agent.


## MCP Registry

Project-level MCP server registry stored at `aia/mcp.json`. All agents share it.

```bash
# Add or update an MCP server
bunx aia mcp add <name> <command>
bunx aia mcp add linear "npx" --args "@linear/mcp-server" --env "LINEAR_API_KEY=abc"

# List registered servers
bunx aia mcp list

# Remove a server
bunx aia mcp remove <name>
```

MCP servers are synced to `.claude/settings.json` before each workflow execution and removed after.


## Skills

Project-level knowledge injected into every agent's prompt. Stored at `aia/skills/<name>/SKILL.md`.

```bash
# List skills
bunx aia skill list

# Create a new skill (opens editor)
bunx aia skill create <name>

# View skill content
bunx aia skill show <name>

# Delete a skill
bunx aia skill delete <name>
```

Skill names: lowercase alphanumeric with hyphens (e.g., `my-skill`). Content is injected as a `## <name>` section into every agent prompt.

## Workflows

Workflows connect agents in a directed graph with optional variant-based routing.

```bash
# List workflows
bunx aia workflow list

# Create
bunx aia workflow create \
  --name "My Workflow" \
  --entry-point developer \
  --cycle-limit 10

# Set connections (from:to pairs)
bunx aia workflow edit my-workflow \
  --connections "developer:tester,tester:reviewer,reviewer:developer"

# View / delete
bunx aia workflow show <id>
bunx aia workflow delete <id> --force
```

**Workflow definition fields:**
- `id`, `name` — identifier and display name
- `entryPointAgentId` — which agent receives the initial prompt
- `connections` — `[{ from, to }]` array defining the message graph
- `cycleLimit?` — max cycles before stopping (undefined = run until queues are empty)
- `variants?` — named routing modes, each with its own entry point, connections, and optional cycleLimit/color

### Variants

Workflows can define variants for dynamic per-cycle routing. When a workflow has variants and a classifier provider is available, the engine selects the best variant each cycle based on the message content.

Each variant has: `description`, `entryPointAgentId`, `connections[]`, optional `color` and `cycleLimit`.

## Running Workflows

```bash
# Foreground (blocks terminal, shows live progress)
bunx aia workflow run my-workflow \
  --prompt "Implement feature X" \
  --yolo \
  --foreground \
  --analysis \
  --loops 3

# Background (returns immediately)
bunx aia workflow run my-workflow \
  --prompt "Implement feature X" \
  --yolo \
  --loops 3

# From file
bunx aia workflow run my-workflow --file prompt.txt --yolo --foreground
```

**Key flags:**
- `--prompt <text>` — prompt to start the workflow (skips interactive input)
- `--yolo` — unrestricted mode: disables agent blacklists
- `--foreground` — run in terminal (required for `--analysis`)
- `--analysis` — run AI analysis after completion (writes `ANALYSIS.md`)
- `--loops <n>` — repeat the workflow N times (each loop builds on previous)
- `--no-worktree` — run in cwd instead of creating a git worktree (default: creates worktree)
- `--file <path>` — read prompt from file

**Worktrees:** By default, `workflow run` creates a git worktree in `.aia/worktrees/<exec-id>/` so agents work on an isolated copy. All loops share the same worktree. After completion, use `workflow merge` to integrate changes.

## Monitoring & Control

```bash
# Check active executions
bunx aia workflow status

# View conversation logs
bunx aia logs                          # list all conversations
bunx aia logs <conversation-id>        # view specific conversation
bunx aia logs --follow <execution-id>  # live tail

# Inject a message into a running workflow (consumed at next cycle, extends cycleLimit)
bunx aia workflow send <execution-id> "Focus on the auth module"

# Graceful stop (writes pause.signal, waits for current agent to finish, can be resumed)
bunx aia workflow stop <execution-id>

# Hard kill (terminates immediately)
bunx aia workflow kill <execution-id> --force

# Resume a paused/stopped execution
bunx aia workflow resume <execution-id>
bunx aia workflow resume <execution-id> --prompt "Now fix the tests" --loops 2 --yolo
```

## After Completion

```bash
# Merge worktree changes into current branch
bunx aia workflow merge <execution-id>

# Discard worktree without merging
bunx aia workflow merge <execution-id> --discard

# Mark as merged (for manual merges)
bunx aia workflow merge <execution-id> --mark-merged

# Run/view AI analysis
bunx aia analysis run <execution-id>           # generate analysis
bunx aia analysis run <execution-id> --force   # overwrite existing
bunx aia analysis show <execution-id>          # display analysis
bunx aia analysis optimize <execution-id>      # apply analysis recommendations
```

## Execution Lifecycle

```
run → [worktree created] → classifying → planning → running → agents execute → messages route
  → cycle limit or consensus → completed/paused/failed
  → [analysis generated] → merge worktree → done
```

**States:** `classifying` → `planning` → `running` → `paused` (can resume) → `completed` / `failed` → `merged`

**Planner:** When `plannerProvider` is set, the engine generates a `PLAN.md` (detailed implementation plan) before the first agent runs. If the task is ambiguous, the planner rejects with `PLAN_REJECTED` and the execution fails. Only runs once per execution (skipped on resume).

**Consensus termination:** Agents can emit `WORKFLOW_DONE` token to vote done. When all agents that ran in the current cycle have voted done, the workflow completes. Agents that never ran (no messages) abstain and don't block consensus. The protocol is injected via `--append-system-prompt`.

**Rate limit auto-resume:** When `rateLimitProvider` is set, rate limit errors trigger a poll loop (every 10 min) instead of pausing. The engine probes with Haiku until the limit clears.

## Persistence

All execution artifacts live in `.aia/executions/<exec-id>/`:

```
state.json                    # execution metadata, status, cycle count
conversations/<conv-id>.jsonl # agent message history
queues/<agent-id>.jsonl       # inter-agent message queues
inbox.jsonl                   # external messages (via 'workflow send')
pause.signal                  # graceful pause request (consumed by engine)
progress.jsonl                # event stream for monitoring
PLAN.md                       # implementation plan (generated by WorkflowPlanner)
ANALYSIS.md                   # AI analysis output
ANALYSIS.pending              # sentinel while analysis is running
```

## Project Architecture Reference

For internal architecture details (types, service layer, provider patterns, testing conventions, etc.), see `CLAUDE.md` in the project root.
