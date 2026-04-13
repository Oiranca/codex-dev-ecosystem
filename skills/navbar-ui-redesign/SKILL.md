---
name: navbar-ui-redesign
description: Use when redesigning a website navbar or header and you need compact guidance for visual hierarchy, CTA emphasis, theme-toggle de-emphasis, spacing, and mobile menu brand treatment.
---

# Navbar UI Redesign

Use this skill for header or navbar redesign work in existing web projects.

## Goals

- Make the primary CTA the strongest control in the header.
- Keep the theme toggle clearly available but visually secondary.
- Preserve brand recognition before adding decorative copy.
- Give navigation links enough spacing to scan quickly.
- Treat mobile menus as intentional brand surfaces, not utility drawers.

## Workflow

1. Read only the navbar component tree and its tests.
2. Identify the visual hierarchy:
   - brand;
   - navigation links;
   - primary CTA;
   - secondary utilities such as theme toggle.
3. Reduce competition with the CTA:
   - theme toggle should use lower-contrast styling, smaller footprint, or icon-first treatment;
   - avoid giving the toggle the same filled or bordered visual weight as the main CTA.
4. Improve scanability:
   - increase spacing between nav items when links feel crowded;
   - keep touch targets at least 44x44.
5. Prefer brand assets over extra marketing copy inside the navbar.
6. Keep responsive breakpoints aligned so only one navbar system is active per range.
7. Validate with focused tests and a production build after edits.

## Guardrails

- Preserve existing navigation logic unless the task explicitly asks for behavior changes.
- Do not introduce new global tokens if the existing theme can support the redesign.
- Keep accessibility semantics intact: visible focus, labels, and hidden states for collapsed menus.
