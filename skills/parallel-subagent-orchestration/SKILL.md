---
name: "parallel-subagent-orchestration"
description: "Use only when work splits into 2 or more independent lanes and each lane can own disjoint writes or a strictly separate responsibility."
---

# Parallel Subagent Orchestration

Use this only when parallelism reduces cycle time without creating merge risk.
This skill is a helper for the lead workflow. It does not replace `product-manager` or `repo-task-orchestrator`.

## Gate

Use it only if all are true:
- there are 2 or more independent lanes;
- the immediate blocking step stays local;
- each lane has disjoint writes or a separate responsibility.

Keep work local if scope is still unclear, edits would overlap, or one answer determines the rest.

## Core Rules

1. Do the immediate blocking task locally.
2. Delegate only bounded sidecar work or clearly separable slices.
3. Give each subagent explicit ownership: allowed files, forbidden files, responsibility.
4. Do not fork full context unless shared thread state is required.
5. Do not wait reflexively; continue non-overlapping local work.
6. Integrate in the main thread.

## Workflow

1. Decompose each lane into: goal, owner, allowed files, forbidden files, validation, dependency.
2. If two lanes need the same file, merge them into one lane or keep that work local.
3. Pick the narrowest role that fits:
   - discovery: `context-manager` or `explorer`
   - implementation: `software-engineer` or `worker`
   - review: `qa-engineer`, `security-reviewer`
   - infra: `devops-engineer`
   - migration: `migration-engineer`
4. Spawn implementation or discovery lanes in parallel only when the main thread can keep moving.
5. Use `send_input` only for scope changes or new blockers. Use `wait_agent` only when the next step truly depends on a result.
6. Review returned edits, check for overlap, run minimum combined validation, then pass through `completion-gate` before claiming success.

## Prompt Shape

Each delegated lane should include goal, ownership, constraints, validation, and no-revert guidance.

```text
Objective: <one concrete outcome>

Ownership:
- Allowed files: <paths>
- Do not modify: <paths or modules>

Context:
- Relevant files/docs: <paths>
- Constraints: <rules>

Validation:
- Run <checks> if applicable

Return:
- Summary
- Files changed
- Validation
- Risks/blockers

You are not alone in the codebase. Do not revert others' edits. Adjust to existing changes if needed.
```

## Output

- Main Thread Plan: local blocking task, delegated lanes, integration point.
- Lane Table: `Lane | Owner | Goal | Allowed Files | Depends On`
- Handoff Rule: every subagent returns summary, files changed, validation, blockers.
