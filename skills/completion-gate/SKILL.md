---
name: "completion-gate"
description: "Use before any completion or fix claim, or before merge, PR, branch, or cleanup decisions, to require fresh evidence."
---

# Completion Gate

Use this before:
- saying a task is complete;
- saying a bug is fixed;
- handing work back to the user;
- deciding merge, PR, branch retention, or cleanup actions.

## Hard Rules

1. No success claim without fresh evidence from this turn.
2. Partial checks do not justify broad claims.
3. Branch or cleanup actions come only after verification.
4. Destructive actions require explicit user intent.

## Verification Gate

For every claim:
1. identify the command or check that proves it;
2. run it fresh;
3. read the real result;
4. state the claim only if the evidence supports it.

## Integration Options

After verification, present only the options relevant to the current state:
- keep changes as-is;
- continue with more implementation;
- prepare for review;
- open or prepare a PR;
- merge locally;
- clean up temporary branch or worktree;
- discard work only with explicit confirmation.

## Output

### Claim Being Tested
What you are about to assert.

### Verification Evidence
Exact command or check and the result.

### Actual Status
What is true right now.

### Next Options
Only the relevant next actions for this state.
