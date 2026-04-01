# Claude Dev Ecosystem v2

A parallel multi-agent development environment for Claude Code CLI. Provides a formal Task State Engine, typed agent messaging, distributed locks, and a shared knowledge layer — enabling agents to work concurrently without a central bottleneck.

## What's new in v2

| Feature | v1 | v2 |
|---------|----|----|
| Task coordination | Shared Task List (informal) | Formal Task State Engine (tasks.json) |
| Agent communication | Via product-manager | Direct typed messages (messages.jsonl) |
| Parallel execution | Sequential phases | Concurrent claiming with dependency graph |
| Lock management | Basic lock files | TTL-based locks with auto-eviction |
| Shared timeline | None | timeline.log with atomic appends |
| Reviewer actions | Report only | APPROVE / REQUEST_CHANGES / ESCALATE |

---

## Structure

```
agents/                 # 12 specialized agent role definitions
skills/                 # 15 reusable skill definitions (SKILL.md per skill)
commands/               # 7 workflow orchestrations
hooks/
  hooks.json            # PreToolUse safety gates
scripts/
  pre-edit-check.sh     # Edit safety gate (hook script)
  validate-local.sh     # Validation runner (lint/typecheck/test/build)
  agent-runtime.py      # Task State Engine CLI ← core of v2
reference/
  ARCHITECTURE_V2.md    # v2 architecture reference
  TEAM_MANUAL.md        # Multi-agent team manual
  GUARDRAILS.md         # Operational guardrails
  GUARDRAILS_REFERENCE.md  # Detailed guardrail explanations
  BUDGETS.md            # Skill budget tiers
  USAGE.md              # Usage guide
templates/
  local-scaffold/       # Optional docs/ and mcp/ templates for new repos
.mcp.json               # MCP server config (filesystem + github)
CLAUDE.md               # Global ecosystem rules loaded by Claude Code
settings.example.json   # Example Claude Code settings
```

---

## Global vs Repo-Local

### Global (`~/.claude/`)

Installed once. Applies to all repositories.

```
~/.claude/
├── agents/
├── skills/
├── commands/
├── hooks/hooks.json
├── scripts/
│   ├── pre-edit-check.sh
│   ├── validate-local.sh
│   └── agent-runtime.py   ← Task State Engine
├── templates/
├── reference/
└── CLAUDE.md
```

### Repo-local

Created per repository. Keep `docs/` in git; keep `.agent-cache/` gitignored.

```
<repo>/
├── CLAUDE.md               # Optional repo-specific overrides
├── .claude/
│   └── settings.local.json
├── docs/                   # Knowledge layer (committable, optional)
│   ├── STACK_PROFILE.md
│   ├── INVENTORY.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── TASKS.md
│   └── REVIEWS.md
└── .agent-cache/           # Runtime state (gitignored)
    ├── tasks.json
    ├── messages.jsonl
    ├── timeline.log
    ├── locks/
    └── repo-map.json
```

---

## Agents

### Team Leads

| Agent | Model | Role |
|-------|-------|------|
| product-manager | sonnet | Plans, scopes, creates task graph, monitors blockers |
| pr-comment-responder | sonnet | Specialized Team Lead for PR review cycles |

### Discovery Agents

| Agent | Model | Role |
|-------|-------|------|
| context-manager | haiku | Repo discovery; scoped reading plans |
| stack-analyzer | haiku | Stack detection |
| repo-analyzer | haiku | Repository structural inventory |
| solution-architect | sonnet | Architecture planning |

### Execution Agents

| Agent | Model | Role |
|-------|-------|------|
| software-engineer | sonnet | Feature implementation |
| migration-engineer | sonnet | Framework migrations |
| devops-engineer | sonnet | Infrastructure review |

### Review Agents (run in parallel)

| Agent | Model | Role |
|-------|-------|------|
| qa-engineer | haiku | Quality validation |
| security-reviewer | sonnet | Security audit |
| tech-writer | haiku | Documentation maintenance |

---

## Runtime CLI

The Task State Engine is the coordination backbone. All agents use it.

```bash
# Create tasks (Team Lead)
python ~/.claude/scripts/agent-runtime.py task create \
  --title "Detect stack" --owner stack-analyzer --priority high \
  --inputs "Write to docs/STACK_PROFILE.md"

# Claim and work (Execution agents)
python ~/.claude/scripts/agent-runtime.py task list --status pending
python ~/.claude/scripts/agent-runtime.py task claim --id <id> --owner software-engineer
python ~/.claude/scripts/agent-runtime.py task update --id <id> --status running
python ~/.claude/scripts/agent-runtime.py task complete --id <id> --outputs "Modified: src/foo.ts"

# Communicate (all agents)
python ~/.claude/scripts/agent-runtime.py message send \
  --from software-engineer --to qa-engineer \
  --task-id <id> --type handoff \
  --summary "Implementation complete. Validate lint, types, tests." \
  --files "src/foo.ts,src/bar.ts"

python ~/.claude/scripts/agent-runtime.py message inbox --agent qa-engineer --unread

# Locks
python ~/.claude/scripts/agent-runtime.py lock acquire --name docs-write --owner tech-writer
python ~/.claude/scripts/agent-runtime.py lock release --name docs-write
```

Valid task states: `pending → claimed → running → review → done | failed | blocked`

---

## Skills

| Skill | Cost | Purpose |
|-------|------|---------|
| fingerprint | low | Change detection |
| stack-detection | low | Stack identification |
| repo-inventory | low | Structural mapping |
| code-search | low | Symbol and file discovery |
| context-pruning | low | Minimal relevant file set |
| docs-writer | low | README and CHANGELOG sync |
| route-mapper | medium | Route inventory |
| architecture-drift-check | medium | Architecture drift detection |
| targeted-test-runner | medium | Focused test execution |
| ci-checks | medium | Lint/typecheck/test/build |
| dependency-audit | medium | Vulnerability scanning |
| env-consistency | high | Environment variable consistency |
| secret-scan-lite | high | Secret hygiene scan |
| smoke-journeys | high | End-to-end smoke tests |
| react-vite-to-astro-migration | high | Component migration skill |

---

## Workflows

| Command | Purpose |
|---------|---------|
| `/existing-repo` | Full analysis workflow for existing repos |
| `/new-project` | Bootstrap workflow for new projects |
| `/unknown-stack` | Cautious analysis with human review gate |
| `/migration-react-vite-to-astro` | React + Vite → Astro migration |
| `/team-review` | Parallel multi-agent code review |
| `/refactor-module <path>` | Safe behavior-preserving refactor |
| `/security-audit` | Focused security audit |

---

## How to Trigger a Cycle

Do not use slash commands to start workflows. Invoke the appropriate Team Lead:

```
Run the product-manager agent to implement issue #42.
```

```
Run the pr-comment-responder agent to address PR #17 review comments.
```

The Team Lead creates the task graph. Agents claim tasks and coordinate via messages without needing the Team Lead to sequence each step.

---

## Setup

1. Copy or symlink this directory to `~/.claude/`.
2. Copy `settings.example.json` to `.claude/settings.json` in a test project.
3. Run Claude Code in the test project — agents and skills will be available.
4. Optionally copy `templates/local-scaffold/docs/` into the repo's `docs/` to bootstrap knowledge artifacts.
5. Ensure `.agent-cache/` is in the repo's `.gitignore`.

---

## Security

- Hooks run `scripts/pre-edit-check.sh` before every Write, Edit, or MultiEdit.
- Blocks edits to protected directories (`node_modules`, `.git`, `dist`).
- Blocks edits to sensitive files (`.env`, private keys, credentials).
- Warns when an agent holds an active lock on an artifact.
- Agents never expose secret values — report file:line location only.

---

## Further Reading

- `reference/ARCHITECTURE_V2.md` — detailed architecture, schemas, and state machine
- `reference/TEAM_MANUAL.md` — team manual with workflow patterns and examples
- `reference/GUARDRAILS.md` — operational guardrails
- `reference/BUDGETS.md` — skill budget tiers
