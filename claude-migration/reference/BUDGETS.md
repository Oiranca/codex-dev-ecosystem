# Skill Budget Rules

This file defines the lightweight operational budgeting used by the normalized Copilot CLI workflow.

Budgeting exists to prevent repeated expensive analysis while keeping agent cycles responsive and predictable.

Budgeting does not change agent responsibilities or skill behavior.  
It only constrains **when repeated execution is allowed within a cycle**.

---

## Budget tiers

Skills conceptually fall into three cost tiers.

### Low-cost

Inexpensive structural or lookup work.

Examples:

- fingerprint
- stack-detection
- repo-inventory
- code-search

These may run freely when directly relevant to the active milestone.

---

### Broader validation

Moderate-cost validation covering wider repository checks.

Examples:

- ci-checks
- route-mapper
- broader structural analysis

These should run deliberately and should not repeat without new evidence.

---

### High-cost specialized validation

Expensive or deep analysis work.

Examples:

- smoke-journeys
- heavy dependency audits
- deep runtime validation

These require explicit justification.

They should not repeat within the same cycle unless the repository fingerprint changes.

---

## Per-cycle defaults

Default limits per cycle:

Low-cost work  
No numeric cap when directly relevant.

Broader validation  
- maximum **2 runs per cycle**
- maximum **1 run per skill per cycle**

High-cost specialized validation  
- maximum **1 run per skill per cycle**
- **explicit justification required**

---

## Skip conditions

Skip a skill execution when any of the following is true:

- the current cycle already consumed the allowed budget for that skill tier
- the same high-cost specialized skill already ran in the current cycle
- the same broader validation already ran and no new fingerprint evidence exists
- justification is missing for a high-cost specialized validation run

Fingerprint changes reset the justification requirement for deeper validation.

---

## Runtime state

When a repository adopts the local scaffold, budget tracking lives in:

.agent-cache/skill_budget_state.json

This state may capture:

- current cycle identifier
- repository fingerprint
- recorded skill runs
- skip reasons

Agents should consult this state before re-running expensive work.

---

## Budget Principles

Agents should follow these principles:

1. Prefer low-cost discovery first.
2. Escalate to broader validation only when necessary.
3. Require explicit justification before high-cost specialized validation.
4. Avoid repeating expensive analysis in the same cycle.
5. Respect artifact freshness before regenerating repository knowledge.

---

## Purpose

Skill budgeting exists to:

- reduce duplicated work
- prevent repeated expensive validation
- keep multi-agent workflows predictable
- maintain fast Claude Code response cycles

Budgeting is a guardrail layer, not a scheduling system.