---
name: "command-security-audit"
description: "Focused security audit workflow. Prioritizes sensitive surfaces first, avoids reproducing secrets, and returns a remediation-oriented report."
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Command `security-audit`

## Codex Native Orchestration (v2)

1. Drive orchestration from the current Codex thread.
2. Split work into independent lanes and run them with `spawn_agent` when parallelism helps.
3. Use `send_input` to refine or redirect delegated lanes.
4. Integrate outputs in this thread with explicit ownership, files changed, and validation status.
5. Treat legacy runtime scripts as optional compatibility only, not a required control plane.

# /security-audit

You are the **Main Agent (Team Lead)**. Run a focused security audit on the repository or a specific path.

## Scope Priority
Audit in this order: 1. Secrets > 2. Dependencies > 3. Auth/Authz > 4. Env Hygiene > 5. Container/Deployment > 6. Input Handling.

## Swarm Execution (Parallel Specialist Lanes)

### Lane 1: Core Security Scan (security-reviewer)
Instruct the agent to execute:
- **Phase 1 (Secrets)**: Run `secret-scan-lite`. Redact all findings.
- **Phase 2 (Dependencies)**: Run `dependency-audit`. Limit to top 20 critical findings.
- **Phase 3 (Environment)**: Check Auth/CORS configs and env hygiene using `env-consistency`.

### Lane 2: Infrastructure Audit (devops-engineer)
- **Phase 4 (Containers)**: If Dockerfile/compose exists, check for root execution, insecure images, and exposed ports. Skip if no container config exists.

## Report Format
Consolidate results into the structured Security Audit Report (Summary, Status, Issues by Severity, Remediation Plan).

## Hard Rules
1. Never reproduce secret values. Redact all findings.
2. Do not introduce security tooling automatically.
3. Do not modify any files during the audit.
4. If a CRITICAL issue is found, escalate immediately to product-manager before continuing.
5. Log the audit in `docs/DECISIONS.md`.
