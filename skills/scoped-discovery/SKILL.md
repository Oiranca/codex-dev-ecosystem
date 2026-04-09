---
name: "scoped-discovery"
description: "Use before broad repository reading to find the smallest relevant file set and produce a ranked reading plan."
allowed-tools: ["read", "search"]
---

# Scoped Discovery

Default low-cost discovery pass before analysis, implementation, QA, security review, or refactoring.

## Purpose

Produce a compact handoff with scope, likely files, trusted artifacts, and skip surfaces.

## Gating Policy

- **Cost Class**: CHEAP.
- **Trigger**: Run when the relevant file set is not already known with high confidence.
- **Skip Conditions**:
  - Skip if the exact files are already known.
  - Skip if the task explicitly requires a full repository scan.

## Hard Rules

- Maximum 10 search queries.
- Maximum 5 full file reads.
- Never return more than 20 candidate files.
- Prefer exact symbols and narrow patterns before broad keyword search.
- Do not read `node_modules`, `.git`, `dist`, `build`, `vendor`, or generated artifacts.
- Do not edit files or execute shell commands.

## Workflow

### 1. Check useful artifacts first

Check whether these exist and are likely fresh:
- `docs/STACK_PROFILE.md`
- `docs/INVENTORY.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`

If they are fresh and relevant, include them in the reading order before source files.

### 2. Establish likely scope

Identify likely app, test, config, and route surfaces.

### 3. Run targeted discovery

Search in this order:
1. exact symbol name;
2. import or export references;
3. route, endpoint, or config key;
4. feature keyword;
5. broader fallback search only if narrow search fails.

### 4. Exclude irrelevant surfaces

List directories or patterns downstream work should ignore.

## Output

### Task Scope
Short description of what the task requires.

### Artifact Status
| Artifact | Path | Status |
|----------|------|--------|

### Candidate Files
| Priority | File or Pattern | Reason |
|----------|-----------------|--------|

### Likely Primary File
The single most relevant file if confidence is high.

### Skip List
| Path or Pattern | Reason |
|----------------|--------|

### Search Confidence
`HIGH` | `MEDIUM` | `LOW`

## Completion Rules

- `HIGH`: exact definition or clearly bounded file set found.
- `MEDIUM`: related references found but multiple candidate files remain.
- `LOW`: only weak keyword matches found.
- If discovery stays broad after the limits above, stop and explicitly recommend a wider inventory pass.
