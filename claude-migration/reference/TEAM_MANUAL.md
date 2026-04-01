# Claude Dev Ecosystem v2 — Team Manual

This manual documents how the global multi-agent environment works for Claude Code CLI.

It is a **global configuration document** and should not be copied into project repositories.

---

## Purpose

This manual exists for two audiences:

1. Humans configuring or maintaining the Claude Code multi-agent system.
2. Agents that need to understand how the system is structured.

It explains:

- how agents collaborate in parallel
- how the Task State Engine works
- how agents communicate between sessions
- how the knowledge layer (docs/) persists information across cycles
- how to use the runtime CLI

---

## 1. System Overview

The v2 system is a **parallel multi-agent coordination environment**. The key difference from v1 is that agents do not wait for a central dispatcher — they claim tasks from a shared queue, work autonomously, and communicate via messages.

```
User request
↓
product-manager (Team Lead)
↓ creates tasks
Task State Engine (.agent-cache/tasks.json)
↓ agents claim concurrently
stack-analyzer ──┐
repo-analyzer    ├── run in parallel
context-manager ─┘
↓ (all done)
solution-architect
↓
software-engineer
↓ (sends handoffs simultaneously)
qa-engineer ──────┐ run in parallel
security-reviewer ┘
↓ (both done)
tech-writer
```

The product-manager creates the task graph and monitors for blockers. It does not orchestrate each handoff — agents handle those directly.

---

## 2. Folder Architecture

### Global (`~/.claude/`)

```
agents/          Agent role definitions (markdown)
skills/          Reusable capability definitions (SKILL.md per skill)
commands/        Workflow orchestrations (markdown)
hooks/
  hooks.json     PreToolUse safety gates
scripts/
  pre-edit-check.sh   Edit safety gate
  validate-local.sh   Validation runner
  agent-runtime.py    Task State Engine CLI
templates/
  local-scaffold/ Bootstrap templates for new projects
reference/
  ARCHITECTURE_V2.md  This system's architecture
  TEAM_MANUAL.md      This document
  GUARDRAILS.md       Operational rules
  GUARDRAILS_REFERENCE.md  Detailed guardrail explanations
  BUDGETS.md          Skill budget tiers
  USAGE.md            Usage guide
CLAUDE.md        Global operating rules (loaded by Claude Code)
```

### Repo-local

```
CLAUDE.md             Optional repo-specific rule overrides
.claude/
  settings.local.json Local Claude Code settings
docs/                 Knowledge layer (committable, optional)
  STACK_PROFILE.md
  INVENTORY.md
  ARCHITECTURE.md
  DECISIONS.md
  TASKS.md
  REVIEWS.md
.agent-cache/         Runtime state (gitignored, never commit)
  tasks.json
  messages.jsonl
  timeline.log
  locks/
  repo-map.json
```

---

## 3. Task State Engine

The Task State Engine is the coordination backbone. It is a file-based store managed by `scripts/agent-runtime.py`.

### States

`pending` → `claimed` → `running` → `review` → `done`
                                   → `blocked`
                                   → `failed`

### Creating tasks (Team Lead)

```bash
python ~/.claude/scripts/agent-runtime.py task create \
  --title "Detect stack" \
  --owner stack-analyzer \
  --priority high \
  --inputs "Write output to docs/STACK_PROFILE.md"
```

### Claiming tasks (Execution agents)

```bash
python ~/.claude/scripts/agent-runtime.py task list --status pending
python ~/.claude/scripts/agent-runtime.py task claim --id <id> --owner software-engineer
python ~/.claude/scripts/agent-runtime.py task update --id <id> --status running
```

### Completing tasks

```bash
python ~/.claude/scripts/agent-runtime.py task complete --id <id> \
  --outputs "Modified: src/foo.ts, src/bar.ts"
```

### Failing tasks

```bash
python ~/.claude/scripts/agent-runtime.py task fail --id <id> \
  --reason "Cannot proceed: implementation plan missing §3"
```

---

## 4. Agent Messaging

Agents communicate between sessions via `messages.jsonl`. This is the primary mechanism for handoffs and review decisions.

### Sending a handoff

```bash
python ~/.claude/scripts/agent-runtime.py message send \
  --from software-engineer \
  --to qa-engineer \
  --task-id <id> \
  --type handoff \
  --summary "Implementation complete. Files: src/foo.ts, src/bar.ts" \
  --files "src/foo.ts,src/bar.ts"
```

### Reading the inbox

```bash
python ~/.claude/scripts/agent-runtime.py message inbox --agent qa-engineer --unread
```

### Message types

| Type | When to use |
|------|-------------|
| `assignment` | Team Lead assigning a task to an agent |
| `handoff` | Passing completed work to the next agent |
| `question` | Requesting clarification before proceeding |
| `review_request` | Requesting a specific review |
| `review_result` | APPROVE / REQUEST_CHANGES decision from a reviewer |
| `blocked` | Agent cannot proceed; needs intervention |
| `done` | Task complete; summary of outputs |

---

## 5. Knowledge Layer (docs/)

Repository knowledge persists in `docs/`. These files allow agents to avoid rediscovering the repository every cycle.

| File | Owner | Purpose |
|------|-------|---------|
| `STACK_PROFILE.md` | stack-analyzer | Detected stack, frameworks, confidence levels |
| `INVENTORY.md` | repo-analyzer | File structure, surfaces, dependencies |
| `ARCHITECTURE.md` | solution-architect | Implementation plan for current milestone |
| `DECISIONS.md` | all agents | Chronological engineering decisions |
| `TASKS.md` | product-manager | Human-readable task summary for the current cycle |
| `REVIEWS.md` | qa-engineer, security-reviewer | Review history and decisions |

These files are optional. The system degrades gracefully when they are absent — agents create them when they run.

---

## 6. Agent Roster

### Team Leads

| Agent | Model | Role |
|-------|-------|------|
| `product-manager` | sonnet | Plans, scopes, creates task graph, monitors for blockers |
| `pr-comment-responder` | sonnet | Specialized Team Lead for PR review response cycles |

### Discovery Agents

| Agent | Model | Role |
|-------|-------|------|
| `context-manager` | haiku | Repo discovery; produces scoped reading plans |
| `stack-analyzer` | haiku | Stack detection; produces `docs/STACK_PROFILE.md` |
| `repo-analyzer` | haiku | Repository inventory; produces `docs/INVENTORY.md` |
| `solution-architect` | sonnet | Architecture planning; produces `docs/ARCHITECTURE.md` |

### Execution Agents

| Agent | Model | Role |
|-------|-------|------|
| `software-engineer` | sonnet | Feature implementation, bug fixes |
| `migration-engineer` | sonnet | Framework and architecture migrations |
| `devops-engineer` | sonnet | Infrastructure, CI, runtime review |

### Review Agents

| Agent | Model | Role |
|-------|-------|------|
| `qa-engineer` | haiku | Validates quality; APPROVE / REQUEST_CHANGES / BLOCKED |
| `security-reviewer` | sonnet | Security audit; APPROVE / REQUEST_CHANGES / ESCALATE |
| `tech-writer` | haiku | Documentation updates |

---

## 7. Parallel Execution Patterns

### Pattern A: Independent discovery (start of cycle)

Create all discovery tasks with no dependencies. They run concurrently:

```bash
python ~/.claude/scripts/agent-runtime.py task create --title "Detect stack" --owner stack-analyzer --priority high
python ~/.claude/scripts/agent-runtime.py task create --title "Build inventory" --owner repo-analyzer --priority high
python ~/.claude/scripts/agent-runtime.py task create --title "Scope context" --owner context-manager --priority high
```

### Pattern B: Fan-out after implementation

After software-engineer completes, send handoffs to both reviewers simultaneously. They work in parallel:

```bash
python ~/.claude/scripts/agent-runtime.py message send --from software-engineer --to qa-engineer --type handoff ...
python ~/.claude/scripts/agent-runtime.py message send --from software-engineer --to security-reviewer --type review_request ...
```

### Pattern C: Blocked task recovery

When a task is blocked:

```bash
# Agent signals blocked
python ~/.claude/scripts/agent-runtime.py task update --id <id> --status blocked
python ~/.claude/scripts/agent-runtime.py message send --from <agent> --to product-manager --type blocked --summary "..."

# product-manager resolves and updates task back to pending
python ~/.claude/scripts/agent-runtime.py task update --id <id> --status pending
python ~/.claude/scripts/agent-runtime.py message send --from product-manager --to <agent> --type assignment --summary "Blocker resolved. Resume task."
```

---

## 8. Validation

Local validation is handled by `scripts/validate-local.sh`.

Validation order (stop at the lowest sufficient level):

1. `targeted-test-runner` — focused tests for changed files
2. `ci-checks` — lint, typecheck, test, build
3. `smoke-journeys` — E2E smoke checks (expensive; requires explicit justification)

The script:
- Detects package manager automatically (yarn/pnpm/bun/npm)
- Only runs scripts present in `package.json`
- Captures failure output to `.agent-cache/last-run/failure_summary.md`
- Never commits, pushes, or opens PRs
- Respects git hooks (husky, lint-staged)

---

## 9. Safety Guardrails

All agents must respect:

1. **Pre-edit gate**: `hooks/hooks.json` runs `scripts/pre-edit-check.sh` before every Write/Edit/MultiEdit. If it blocks, do not bypass.
2. **Budget tiers**: Low-cost skills run freely. Broader validation max 2/cycle. High-cost max 1/cycle with justification.
3. **Scope rules**: One milestone per cycle. Never expand scope beyond the active issue.
4. **Secret safety**: Never expose secrets in outputs. Never commit credentials.

See `reference/GUARDRAILS.md` and `reference/BUDGETS.md` for complete rules.

---

## 10. Example Prompts (v2)

### Prompt 1 — Full feature cycle

```
Invoke the product-manager agent.

Goal: implement the feature described in issue #42.

The product-manager should:
1. Read existing docs to understand the repository.
2. Determine the smallest valid milestone.
3. Create tasks in the Task State Engine for the required agents.
4. Monitor for blockers and resolve them.
5. Log the cycle in docs/DECISIONS.md.
```

### Prompt 2 — Parallel repository analysis

```
Invoke the product-manager agent.

Goal: analyze this repository for the first time.

Create tasks for:
- stack-analyzer (no dependencies)
- repo-analyzer (no dependencies)
- solution-architect (depends on stack-analyzer and repo-analyzer)

Let them run concurrently where possible.
```

### Prompt 3 — Check agent inbox

```
Invoke the qa-engineer agent.

Check your message inbox and process any pending handoff messages.
For each handoff:
1. Validate the changed files.
2. Send a review_result message to the software-engineer.
3. Update the task status.
```

### Prompt 4 — Security review in parallel

```
Invoke the security-reviewer agent.

Check your inbox for review_request messages.
For each request:
1. Audit only the files listed in the message.
2. Classify findings by severity.
3. Send a review_result message (APPROVE or REQUEST_CHANGES).
4. Never reproduce secret values in your output.
```

### Prompt 5 — Resolve a blocked task

```
Invoke the product-manager agent.

Check the task list for blocked tasks and your inbox for blocked messages.
For each blocked task:
1. Understand the reason.
2. Resolve the blocker or escalate to the user.
3. Reset the task to pending if the blocker is resolved.
```

### Prompt 6 — PR comment response

```
Invoke the pr-comment-responder agent.

Address the latest review comments on PR #17.
Create tasks in the Task State Engine for the required fixes.
Let agents work in parallel where possible.
```

---

## 11. Best Practices

- **Keep tasks small**: one focused objective per task, not multi-step epics.
- **Put context in inputs**: agents cannot share context natively. Everything they need must be in the task `inputs` field.
- **Prefer parallel**: only use `--depends-on` when a real data dependency exists.
- **Check inbox before claiming**: an agent may already have a handoff message directing it to specific work.
- **Update status immediately**: set `running` right after claiming so other agents don't re-claim the task.
- **Send explicit handoffs**: never assume a downstream agent will poll for your completion — message them.
- **Update docs/**: keeping `STACK_PROFILE.md`, `INVENTORY.md`, and `ARCHITECTURE.md` fresh improves future cycles.
- **Avoid re-running expensive skills**: check `skill_budget_state.json` before running high-cost skills.
