---
name: "stack-detection"
description: "Identify the repository technology stack using configuration and manifest files and produce a structured stack profile with evidence."
allowed-tools: ["read", "search", "edit"]
---

## Codex Native Note

- This skill runs natively in Codex.
- Any references to `local metadata cache` in this document are optional local metadata hints, not required control-plane dependencies.

# Stack Detection

Use this skill to identify the repository technology stack using configuration and manifest files.

This skill does not analyze source code.
It only reads configuration and manifest files.

## Purpose

Produce a structured stack profile describing:
- language
- framework
- runtime
- bundler
- package manager
- tooling signals
- deployment indicators
- run commands

## Gating Policy

- **Cost Class**: CHEAP (Low-cost).
- **Mandatory Sequence**: Runs only after `fingerprint` has completed.
- **Skip Conditions**:
  - Skip if `material_change = false`.
  - Skip if `docs/STACK_PROFILE.md` already exists and the repository fingerprint is unchanged.
  - Never run without fingerprint evidence.

## Hard Rules

- **Maximum files read**: 15.
- **Read policy**: Only read configuration or manifest files.
- **No source**: Never read source directories such as `src/`, `lib/`, or `components/`.
- **Evidence-based**: Never infer technologies without direct file evidence.
- **Traceability**: Every detection must cite its specific source file.
- **Termination**: Stop reading files once 15 files have been processed.

## File Priority Order

The agent must inspect files in this specific order and stop after 15 files:
1. `package.json`
2. `pnpm-workspace.yaml`
3. `tsconfig.json`
4. `astro.config.*`
5. `vite.config.*`
6. `next.config.*`
7. `nuxt.config.*`
8. `angular.json`
9. `svelte.config.*`
10. `turbo.json`
11. `nx.json`
12. `Dockerfile`
13. `docker-compose.yml`
14. `.github/workflows/*.yml` (first match)
15. `netlify.toml` or `vercel.json`
16. `pyproject.toml` or `requirements.txt`
17. `Cargo.toml`
18. `go.mod`

## Detection Targets

Extract signals and provide evidence for:
- **Language**: (e.g., TypeScript, JavaScript, Python, Rust, Go).
- **Framework**: (e.g., React, Astro, Vue, Angular, Svelte).
- **Runtime**: (e.g., Node.js, Bun, Deno, Python runtime).
- **Bundler**: (e.g., Vite, Webpack, Esbuild, Turbo).
- **Styling tools**: (e.g., Tailwind, Sass, PostCSS).
- **Package manager**: (e.g., npm, yarn, pnpm, bun, pip, cargo, go modules).
- **Testing framework**: (e.g., Jest, Vitest, Playwright, Cypress).
- **Deployment platform**: (e.g., Vercel, Netlify, AWS, Docker).
- **Build tooling**: (e.g., ESLint, Prettier, Husky).

## Run Command Extraction

Detect run commands specifically for `dev`, `build`, `test`, and `lint`.
- **Primary Source**: `package.json` scripts.
- **Fallback Sources**: `Makefile` or CI workflow commands.

## Confidence & Mode Rules

### Confidence Levels
- **HIGH** → 3 or more independent evidence signals.
- **MEDIUM** → 1–2 evidence signals.
- **LOW** → Weak or conflicting signals.

**If conflicting signals appear**: Mark detection as `CONFLICTING`, set confidence to `LOW`, and list both sources.

### Detection Mode
Record as one of: `config-evidence`, `partial-detection`, or `conflicting`.

## Output & Communication

The **stack-analyzer** is the owner of this artifact. Upon completion:
1. **Persistence**: Write the structured results to `docs/STACK_PROFILE.md`.
2. **Decision Log**: Append a short completion entry to `docs/DECISIONS.md`.
3. **Communicate**: Post the stack summary to the **current Codex thread** so the Team Lead can update project context.

### Required Output Structure (docs/STACK_PROFILE.md)
- **Summary**: High-level overview of the detected stack.
- **Confidence**: HIGH | MEDIUM | LOW.
- **Detection Mode**: config-evidence | partial-detection | conflicting.
- **Core Stack Table**: | Category | Technology | Evidence File |
- **Run Commands**: | Purpose | Command | Source |
- **Tooling and Deployment**: | Category | Signal Found | Evidence File |
- **Conflicts or Ambiguities**: List any conflicting signals found.