---
name: "context-pruning"
description: "Reduce unnecessary context usage by identifying the minimum relevant file set for the current task before any broad repository reads occur."
allowed-tools: ["read", "search"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Context Pruning

Use this skill to identify the smallest relevant set of files and directories for the current task before delegating to any implementation, analysis, or validation agent.

This skill reduces wasted reads and keeps multi-agent cycles efficient by enforcing context isolation.

## Purpose

Prevent agents from performing broad repository reads when only a narrow surface is relevant to the active task.

Specific problems this skill solves:
- Agents reading entire `src/` directories when only one module matters.
- Repeated reads of documentation that is already fresh.
- Triggering expensive skills when cheap lookups would suffice.
- Agents re-analyzing stack or inventory when artifacts are current.

## Gating Policy

- **Cost Class**: CHEAP.
- **Trigger**: Run before any agent that would otherwise start with broad reads.
- **Coordination**: Typically executed by the **context-manager** or the **product-manager** (Team Lead) to prepare the current Codex thread.
- **Skip Conditions**:
  - Skip if the file set is already known with high confidence.
  - Skip if the task explicitly requires a full repository scan.

## Hard Rules

- Maximum 5 file reads.
- Maximum 10 search queries.
- Do not read source file bodies in full — use pattern matching only.
- Do not read `node_modules`, `.git`, `dist`, `build`, or `vendor` directories.
- Output reading plan must not exceed 20 files.
- If the task scope is too broad to prune, say so explicitly.

## Steps

### 1. Check existing documentation artifacts
For each of the following, check whether the file exists and estimate whether it is likely fresh:
- `docs/STACK_PROFILE.md`
- `docs/INVENTORY.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`

Also check `local artifact freshness metadata` when present to verify ownership and timestamps.

- **If relevant artifacts are fresh**: Include them in the reading plan and deprioritize source reads.
- **If artifacts are missing or stale**: Include targeted source reads in the plan.

### 2. Identify relevant directories
Based on the task description and any available stack signals, identify the most likely directories:
- Where is the primary application code?
- Where are the tests?
- Where are the configuration files?
- Are there multiple packages or a single application?

### 3. Search for task-specific patterns
Use targeted searches via `code-search` to find files related to the task:
- Specific symbol names.
- Route or endpoint patterns.
- Configuration keys.
- Framework-specific file patterns.

### 4. Classify irrelevant surfaces
Explicitly identify directories and file patterns that are not relevant to the current task and should be excluded from downstream reads.

### 5. Produce the reading plan
Return a ranked reading plan with the most relevant files first and a skip list of irrelevant surfaces.

## Expected Output (Communication to current Codex thread)

The result of this skill serves as the "Context" payload for the **current Codex thread**.

### Task Scope
Short description of what the task requires.

### Artifact Status
| Artifact | Path | Status |
|----------|------|--------|
| Stack Profile | docs/STACK_PROFILE.md | fresh / stale / missing |
| Inventory | docs/INVENTORY.md | fresh / stale / missing |
| Architecture | docs/ARCHITECTURE.md | fresh / stale / missing |

### Recommended Reading Order
| Priority | File or Pattern | Reason |
|----------|----------------|--------|

### Skip List
| Path or Pattern | Reason to Skip |
|----------------|----------------|

### Handoff Notes
Short guidance for the downstream agent (e.g., software-engineer or qa-engineer).

## Final Rules

- Never read source file contents in full during this skill.
- Never produce a reading plan longer than 20 files.
- If the task requires broader analysis, say so and hand off to **product-manager**.
- Record the pruning outcome in `docs/DECISIONS.md` when that file is present.