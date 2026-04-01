# Claude Dev Ecosystem v2 — Architecture Reference

## Overview

Claude Dev Ecosystem v2 is a parallel multi-agent coordination system for Claude Code CLI. It provides a formal Task State Engine, typed agent messaging, distributed locks, and a shared timeline — enabling agents to work concurrently without a single bottleneck.

---

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Parallelism first** | Tasks without dependencies are always available for concurrent claiming |
| **Async coordination** | Agents communicate via messages; no synchronous RPC between sessions |
| **Task claiming** | Agents self-assign work from a shared queue; no central dispatcher |
| **Explicit handoffs** | Agents message each other directly when passing work between phases |
| **Shared memory** | `docs/` layer persists knowledge across cycles; `.agent-cache/` tracks runtime state |
| **Graceful degradation** | System works without `docs/` or `.agent-cache/` — agents create them when missing |

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User / Claude Code                 │
├─────────────────────────────────────────────────────┤
│              Team Leads (product-manager,            │
│               pr-comment-responder)                  │
│         Create tasks → monitor for blockers          │
├────────────────────┬────────────────────────────────┤
│   Execution Agents │   Discovery Agents              │
│   software-engineer│   context-manager               │
│   migration-engineer   stack-analyzer                │
│   devops-engineer  │   repo-analyzer                 │
│                    │   solution-architect             │
├────────────────────┼────────────────────────────────┤
│        Review Agents (parallel)                      │
│   qa-engineer          security-reviewer             │
│   tech-writer                                        │
├─────────────────────────────────────────────────────┤
│              Task State Engine                       │
│         .agent-cache/tasks.json                      │
│         .agent-cache/messages.jsonl                  │
│         .agent-cache/timeline.log                    │
│         .agent-cache/locks/                          │
├─────────────────────────────────────────────────────┤
│           Knowledge Layer (docs/)                    │
│   STACK_PROFILE  INVENTORY  ARCHITECTURE  DECISIONS  │
│   TASKS          REVIEWS                             │
└─────────────────────────────────────────────────────┘
```

---

## Task State Machine

```
         ┌─────────┐
         │ pending │ ← task created by Team Lead
         └────┬────┘
              │  task claim --id X --owner agent
              ▼
         ┌─────────┐
         │ claimed │
         └────┬────┘
              │  task update --id X --status running
              ▼
         ┌─────────┐        ┌─────────┐
         │ running │───────►│ blocked │ ← dependency not resolved
         └────┬────┘        └────┬────┘
              │                  │ blocker resolved
              │  ◄───────────────┘
              ▼
         ┌────────┐
         │ review │ ← execution agent sent handoff; awaiting reviewer
         └────┬───┘
              │
         ┌────┴────┬──────────────┐
         ▼         ▼              ▼
      ┌──────┐ ┌──────┐    ┌────────┐
      │ done │ │failed│    │blocked │ ← reviewer escalated
      └──────┘ └──────┘    └────────┘
```

### Valid states

| State | Meaning |
|-------|---------|
| `pending` | Created, not yet claimed |
| `claimed` | Agent has reserved this task |
| `running` | Agent is actively working |
| `blocked` | Waiting on dependency or external input |
| `review` | Work complete; awaiting reviewer decision |
| `done` | Accepted; outputs available |
| `failed` | Terminal failure; reason recorded |

### Transition rules

- Any agent can claim a `pending` task if all `depends_on` tasks are `done`.
- Only the owning agent should move a task from `claimed` → `running` → `review`/`done`/`failed`.
- Reviewers move tasks from `review` → `done` (approve) or back to `running` (request changes).
- Any agent can move a task to `blocked` and must send a `blocked` message to the product-manager.

---

## Task Schema

```json
{
  "id": "a1b2c3d4",
  "title": "Implement auth endpoint",
  "owner": "software-engineer",
  "status": "running",
  "priority": "high",
  "depends_on": ["x9y8z7w6"],
  "inputs": "Follow docs/ARCHITECTURE.md §3. Files: src/auth/.",
  "outputs": "",
  "reviewer": "qa-engineer",
  "created_at": "2026-03-14T10:00:00Z",
  "updated_at": "2026-03-14T10:05:00Z"
}
```

---

## Message Schema

```json
{
  "id": "m1m2m3m4",
  "from": "software-engineer",
  "to": "qa-engineer",
  "task_id": "a1b2c3d4",
  "type": "handoff",
  "summary": "Implementation complete. Modified: src/auth/handler.ts. Please validate.",
  "files": ["src/auth/handler.ts", "src/auth/handler.test.ts"],
  "needs_reply": false,
  "read": false,
  "created_at": "2026-03-14T10:30:00Z"
}
```

### Message types

| Type | Direction | Meaning |
|------|-----------|---------|
| `assignment` | Lead → Agent | Team Lead assigning a task |
| `handoff` | Agent → Agent | Passing completed work to next agent |
| `question` | Agent → Agent | Requesting clarification before proceeding |
| `review_request` | Execution → Reviewer | Requesting a specific review |
| `review_result` | Reviewer → Execution | APPROVE / REQUEST_CHANGES decision |
| `blocked` | Agent → Lead | Cannot proceed; needs intervention |
| `done` | Agent → Lead | Task complete; summary of outputs |

---

## Parallel Execution Model

### Typical cycle (feature implementation)

```
Team Lead creates tasks:
  T1: stack-analyzer      (no deps)  ─┐
  T2: repo-analyzer       (no deps)  ─┤─ claimed and run in parallel
  T3: context-manager     (no deps)  ─┘
  T4: solution-architect  (deps: T1, T2, T3)
  T5: software-engineer   (deps: T4)
  T6: qa-engineer         (deps: T5, reviewer)  ─┐ run in parallel
  T7: security-reviewer   (deps: T5, reviewer)  ─┘
  T8: tech-writer         (deps: T6, T7)
```

- T1, T2, T3 start immediately without waiting for each other.
- T4 becomes claimable only when T1 + T2 + T3 are all `done`.
- T6 and T7 run in parallel after T5 completes (software-engineer sends a handoff message to both).
- T8 waits for both T6 and T7 to complete.

### Key pattern: reviewer parallelism

After implementation, the software-engineer sends two messages simultaneously:

```bash
# Message to qa-engineer
python ~/.claude/scripts/agent-runtime.py message send \
  --from software-engineer --to qa-engineer \
  --task-id T5 --type handoff --summary "..." --files "src/..."

# Message to security-reviewer (same time)
python ~/.claude/scripts/agent-runtime.py message send \
  --from software-engineer --to security-reviewer \
  --task-id T5 --type review_request --summary "..." --files "src/..."
```

Both reviewers work concurrently. Neither waits for the other.

---

## Global vs Repo-Local Separation

### Global (`~/.claude/`)

Installed once. Applies to all repositories.

```
~/.claude/
├── agents/                 # Agent role definitions
├── skills/                 # Reusable capability definitions
├── commands/               # Workflow orchestrations
├── hooks/
│   └── hooks.json          # PreToolUse safety gates
├── scripts/
│   ├── pre-edit-check.sh   # Edit safety gate
│   ├── validate-local.sh   # Validation runner
│   └── agent-runtime.py    # Task State Engine CLI
├── templates/
│   └── local-scaffold/     # Optional repo bootstrap
├── reference/              # System documentation
└── CLAUDE.md               # Global operating rules
```

### Repo-local

Created per repository. Never committed (except `docs/`).

```
<repo>/
├── CLAUDE.md               # Optional repo-specific overrides
├── .claude/
│   └── settings.local.json # Local Claude Code settings
├── docs/                   # Knowledge layer (committable, optional)
│   ├── STACK_PROFILE.md
│   ├── INVENTORY.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── TASKS.md            # Human-readable task summary
│   └── REVIEWS.md          # Review history
└── .agent-cache/           # Runtime state (gitignored, always)
    ├── tasks.json
    ├── messages.jsonl
    ├── timeline.log
    ├── locks/
    └── repo-map.json
```

---

## Runtime CLI Reference

All runtime commands use `python ~/.claude/scripts/agent-runtime.py <command> <subcommand> [options]`.

### Task commands

```bash
task create  --title STR --owner AGENT [--priority low|medium|high|critical]
             [--depends-on ID,ID] [--inputs STR] [--reviewer AGENT]
task list    [--status STATE] [--owner AGENT]
task claim   --id ID --owner AGENT
task update  --id ID [--status STATE] [--outputs STR] [--reviewer AGENT]
task complete --id ID [--outputs STR]
task fail    --id ID [--reason STR]
```

### Message commands

```bash
message send  --from AGENT --to AGENT --type TYPE --summary STR
              [--task-id ID] [--files PATH,PATH] [--needs-reply]
message inbox --agent AGENT [--unread]
```

### Lock commands

```bash
lock acquire --name NAME --owner AGENT [--ttl SECONDS]
lock release --name NAME
lock status  [--name NAME]
```

### Timeline

```bash
timeline append --event STR
```

---

## Guardrails

All guardrails from v1 remain in effect. See `reference/GUARDRAILS.md`.

Key additions in v2:
- Agents must check `message inbox` before assuming no work is available.
- Agents must update task status to `running` immediately after claiming.
- Agents must not hold locks longer than their TTL (default 30 min).
- Review agents must issue an explicit decision (`review_result` message) — silent completion is not accepted.
- Critical security findings (CRITICAL severity) must immediately set the task to `blocked` and notify the product-manager.

---

## Failure Handling

| Failure | Response |
|---------|----------|
| Task claim denied (wrong state) | Check current state; re-claim only if `pending` |
| Dependency not done | Task stays `pending`; runtime enforces this |
| Implementation fails QA | qa-engineer sends `review_result` with REQUEST_CHANGES; software-engineer re-opens task |
| Critical security issue | security-reviewer sets `blocked`, sends `blocked` message to product-manager; cycle stops |
| Lock timeout | Lock is auto-evicted after TTL; new agent can claim |
| Validation script fails | Read `.agent-cache/last-run/failure_summary.md`; fix before retry |
