---
name: "skill-authoring-tdd"
description: "Use when creating or revising Codex skills and you need concise structure plus validation before rollout."
---

# Skill Authoring TDD

Use this skill when authoring skills for Codex.

## Principles

- Keep `SKILL.md` lean. Put only workflow-critical instructions in it.
- The frontmatter `description` should explain **when to use** the skill, not summarize the workflow.
- Validate a skill against realistic prompts before trusting it.
- Tighten the skill only where baseline failures show real ambiguity.

## Workflow

### 1. Define the trigger

Write a precise `name` and `description`:
- `name`: short, stable, hyphenated.
- `description`: starts with `Use when...` and describes triggering conditions.

### 2. Run a RED baseline

Before writing or revising the skill, define 1 to 3 realistic prompts that should trigger it.

Record what fails without the skill:
- wrong trigger;
- skipped workflow step;
- too-broad context loading;
- incorrect tool choice;
- weak validation.

### 3. Write the minimal skill

Create or update:
- `SKILL.md` with frontmatter and concise workflow;
- optional `references/` only for details that should not live inline;
- optional `scripts/` only when deterministic execution matters.

Do not create README-style extras.

### 4. Run a GREEN validation

Re-run the same prompts and verify:
- the skill triggers when it should;
- it does not over-trigger on nearby tasks;
- the body is sufficient without carrying unnecessary prose;
- bundled references are only loaded when needed.

### 5. Refactor

Tighten wording where the agent still rationalizes around the workflow.
Prefer removing text over adding text unless the failure proves a real gap.

## Validation Checklist

- Trigger is specific enough to fire on the right tasks.
- Description does not contain workflow shortcuts that let the model skip the body.
- Workflow is actionable and ordered.
- Tool guidance matches Codex, not another runtime.
- References are one level deep from `SKILL.md`.
- No legacy mentions to tools that do not exist in this environment.

## Output

### Skill Goal
What behavior the skill is supposed to improve.

### RED Findings
How the baseline failed without the skill.

### Implemented Skill Shape
Files created or updated.

### GREEN Result
Why the revised skill now works better.

### Residual Risks
What ambiguity is still left.
