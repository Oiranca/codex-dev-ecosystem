---
name: "root-cause-debugging"
description: "Use for bugs, failing tests, build failures, or unexpected behavior when you need root-cause investigation before fixing."
---

# Root Cause Debugging

Default debugging workflow.

## Hard Rules

1. No fix before root-cause investigation.
2. No production change without a failing reproduction unless automation is impossible.
3. Test one hypothesis at a time.
4. No completion claim without fresh verification evidence.

## Workflow

### Phase 1 — Investigate

Before changing code:
- read the full error or failing output;
- reproduce consistently;
- inspect recent changes;
- trace data or state flow until the bad value, branch, or assumption is found.

If the issue spans multiple layers, instrument boundaries first.

### Phase 2 — Compare and isolate

- find the closest working example in the same codebase;
- list the differences between working and broken paths;
- form one explicit hypothesis for the root cause.

### Phase 3 — Write the failing reproduction

Prefer the narrowest proof:
- targeted automated test;
- focused script;
- deterministic command sequence.
Verify that it fails for the expected reason.

### Phase 4 — Implement the minimal fix

- change only what the hypothesis requires;
- avoid opportunistic refactors;
- avoid stacking multiple speculative fixes.

### Phase 5 — Verify

Run the smallest check that proves the fix:
- failing reproduction now passes;
- nearby affected tests still pass;
- broader `ci-checks` only if impact extends beyond the local surface.
Then pass through `completion-gate`.

## Output

### Symptom
What was failing.

### Root Cause
What actually caused it.

### Reproduction
What proof failed before the fix.

### Fix
What changed.

### Verification
What now passes and what remains risky.
