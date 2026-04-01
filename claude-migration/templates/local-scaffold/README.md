# Local Scaffold (v2)

This directory contains optional templates you can copy into a project repository to enable full multi-agent workflow support.

## Contents

### docs/
Repository knowledge artifact templates. Copy these to your project's `docs/` directory.

| File | Owner Agent | Purpose |
|------|-------------|---------|
| STACK_PROFILE.md | stack-analyzer | Detected stack and framework profile |
| INVENTORY.md | repo-analyzer | Repository structural inventory |
| ARCHITECTURE.md | solution-architect | Architecture plan for the current milestone |
| DECISIONS.md | all agents | Chronological engineering decision log |
| TASKS.md | product-manager | Human-readable task summary for current cycle |
| REVIEWS.md | qa-engineer, security-reviewer | Review history and decisions |
| QA_REPORT.md | qa-engineer | Validation results |
| SECURITY_REPORT.md | security-reviewer | Security findings |
| ROUTE_MAP.md | repo-analyzer | Application route inventory |
| MIGRATION_PLAN.md | migration-engineer | Migration planning document |

### mcp/
MCP configuration templates.

- `mcp.config.json` — MCP server configuration template.
- `mcp.allowlist.json` — Default read-only allowlist.
- `mcp.secrets.example` — Example secrets file (never commit real values).

## Runtime Cache Structure

The `.agent-cache/` directory is created automatically by the runtime. Never commit it.

```
.agent-cache/
├── tasks.json         # Task State Engine (all tasks and their states)
├── messages.jsonl     # Agent message log (one JSON object per line)
├── timeline.log       # Shared audit timeline
├── locks/             # Named lock files (name.lock)
│   └── *.lock
└── repo-map.json      # Repository map cache (optional, created by context-manager)
```

Add to your `.gitignore`:

```
.agent-cache/
```

## Usage

These templates are **optional**. Agents create docs/ artifacts from scratch if none exist. The `.agent-cache/` directory is created by the runtime on first use.

Copy only what you need:

```bash
# Copy docs templates to your project
mkdir -p docs
cp templates/local-scaffold/docs/*.md docs/