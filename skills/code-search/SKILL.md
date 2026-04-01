---
name: "code-search"
description: "Locate relevant code, definitions, usages, route handlers, and configuration references before reading or editing files."
allowed-tools: ["search", "read"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Code Search

Use this skill to find the minimum relevant set of files before analysis, implementation, QA review, or security review.

This skill is for locating code only.
It does not edit files.
It does not execute commands.

## Purpose

Reduce unnecessary file reads by locating:
- symbol definitions.
- symbol usages.
- component references.
- route handlers.
- API endpoints.
- configuration references.
- imports and exports.

before downstream work begins.

## Gating Policy

- **Cost Class**: LOW-COST (CHEAP).
- **Trigger**: May run whenever a downstream agent needs file-level discovery.
- **Strategy**: Prefer this skill before broad repository reading to respect context isolation.
- **Skip Conditions**:
  - Skip if the target files are already known with high confidence.
  - Check `local artifact freshness metadata` if searching for structural inventory already covered by `repo-analyzer`.

## Hard Rules

- Maximum 10 search queries per run.
- Maximum 20 files returned as candidate results.
- Prefer narrow, targeted queries over broad scans.
- Do not read source files in full unless needed after search.
- Do not edit files.
- Do not execute shell commands.
- Exclude obvious non-source paths when possible:
  - `node_modules/`, `.git/`, `dist/`, `build/`, `vendor/`, and generated artifacts.

## Search Goals

This skill may be used to find:

### Definitions
Examples:
- function definition, component definition, route definition, API handler definition, or exported symbol definition.

### Usages
Examples:
- where a function is called, where a component is rendered, where an environment variable is referenced, or where a route or endpoint is consumed.

### Structural references
Examples:
- imports of a module, exports from a file, config references, or middleware usage.

## Query Strategy

Use this order of search strategy:
1. **Exact symbol name**.
2. **Import/export references**.
3. **Related route or endpoint name**.
4. **Related feature keyword**.
5. **Fallback broader search** only if narrow search fails.

*Prefer exact search terms over conceptual search.*

## Output & Communication

Because context is not shared natively, the agent performing the search must **Communicate** the findings clearly to the **current Codex thread** so the next agent knows exactly which files to Claim.

### Search Result Structure
- **Search Objective**: What was being searched for.
- **Candidate Files**:
| File | Reason |
- **Likely Primary File**: The single most relevant file, if confidence is high.
- **Related Files**: Supporting files likely needed next.
- **Search Confidence**: HIGH | MEDIUM | LOW.

## Completion Rules

- **HIGH Confidence**: If an exact definition is found.
- **MEDIUM Confidence**: If only related references are found.
- **LOW Confidence**: If only weak keyword matches are found.
- **Empty Result**: If nothing relevant is found, return an empty result and say so clearly.