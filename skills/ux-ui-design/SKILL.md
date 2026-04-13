---
name: ux-ui-design
description: Use when working on UX/UI design tasks for web products, including new interface design, redesigns, navigation, hierarchy, spacing, calls to action, form usability, responsive behavior, and accessibility-aware visual decisions.
---

# UX/UI Design

Use this skill for interface design work in existing products or new UI work.

## Objectives

- Make interface hierarchy obvious at first glance.
- Prioritize primary actions over utilities and secondary controls.
- Improve scanability through spacing, grouping, rhythm, and contrast.
- Preserve brand recognition without adding ornamental copy that weakens clarity.
- Keep responsive layouts intentionally recomposed, not merely scaled.
- Treat accessibility as part of visual and interaction design.

## Workflow

1. Read only the components, styles, tests, and route surfaces involved in the requested UI.
2. Identify the user-facing hierarchy:
   - brand;
   - orientation or navigation;
   - primary CTA;
   - secondary actions;
   - utilities;
   - supporting copy.
3. Decide what must dominate visually and what must step back.
4. Adjust the design using these levers:
   - spacing;
   - grouping;
   - size;
   - weight;
   - contrast;
   - motion;
   - icon usage;
   - copy length.
5. For navigation:
   - ensure links are easy to scan;
   - keep CTA visually strongest;
   - keep theme toggles and utility actions visibly secondary;
   - avoid cramped link clusters.
6. For forms and interactive UI:
   - preserve visible focus;
   - keep controls legible in all states;
   - ensure controls do not compete equally when their priority differs.
7. For mobile and tablet:
   - recompose layout per breakpoint;
   - keep touch targets at least 44x44;
   - hide collapsed content semantically, not only visually.
8. Validate with focused tests and production build after edits.

## Guardrails

- Preserve existing behavior unless the task asks for UX flow changes.
- Reuse the project's existing token system before inventing new globals.
- Avoid decorative copy inside structural UI unless it strengthens navigation or trust.
- Prefer concise, intentional interfaces over feature-stacked layouts.
