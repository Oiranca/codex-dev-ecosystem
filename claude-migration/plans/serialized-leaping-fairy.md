# Plan: Remaining Issues Sprint

## Context

All remaining open issues from the KnitsDigital project board need to be resolved in a single branch and single PR targeting `develop`. Additionally: remove the skip-to-main link added in PR #82, and apply width/height/spacing dimensions from `kd-web-2.0` to the current repo components.

Issue #66 (logo swap) is excluded — handled manually.

---

## Branch & PR

- **Branch:** `fix/remaining-issues-sprint`
- **PR target:** `develop`
- **PR title:** `fix: resolve remaining project issues + apply kd-web-2.0 dimensions`
- **Closes:** #72, #74, #75, #76, #77, #79, #83

---

## Execution Order (blocker → importance)

---

### Step 1 — #74 [P1] Fix CSS token duplication ← UNBLOCKS ALL CSS WORK

Conflicting `--hover-btn-primary` values between files make all token changes unreliable.

| File | Action |
|---|---|
| `src/index.css` | Remove ALL CSS custom property declarations. Keep only: CSS reset, typography, responsive font scale |
| `src/styles/theme.css` | Becomes single source of truth for all design tokens |

---

### Step 2 — #72 [P2] Fix `transition: all` on block elements

| File | Action |
|---|---|
| `src/styles/theme.css` (lines 151–163) | Change selector to `body, button, input, textarea, a, nav`. Replace `transition: all` with `color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease, fill 0.3s ease`. Remove `div, section, main, header, footer` |
| `src/styles/buttons/buttons.css` | Audit and restrict any `transition: all` usage to targeted properties |

---

### Step 3 — #75 [P2] Fix card widths + Apply kd-web-2.0 dimensions

These are combined: kd-web-2.0 is the reference for dimensions across all components.

#### 3a — Card layout fix (#75)

| File | Action |
|---|---|
| `src/components/commons/card/card-icon/CardIcon.css` | Remove `width: 328px` at 768px; set `width: 100%` |
| `src/components/commons/card/card-number/CardNumber.css` | Remove `width: 304px` at 1024px; set `width: 100%` |
| Parent containers (Services, Collaborators, etc.) | Add `display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem` |

#### 3b — Apply kd-web-2.0 dimensions to kd-web components

**Footer** (`src/components/footer/Footer.tsx` + `Footer.css`):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Footer container | `py-10` (40px top/bottom) | Set section padding |
| Isotype/logo image | `64×64px` | Set image dimensions |
| Logo text | `32px` height | Set logo height |
| Social icons | `36×36px` (h-9 w-9), SVG `20×20px` (h-5 w-5) | Update icon container sizes |
| Copyright bar | `py-7` (28px top/bottom) | Set copyright padding |
| Footer body layout | `flex-col` mobile → `md:flex-row` | Apply responsive flex |
| Legal links | `gap-3` (12px) flex-col | Set link spacing |

**Navbar** (`src/components/navbar/**/*.css`):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Navbar min-height | `64px` mobile / `80px` (lg) | `min-height: 64px; @media (min-width:1024px) { min-height: 80px }` |
| Header padding | `12px` mobile / `16px` (lg) | Vertical padding |
| Nav link padding | `px-4 py-2` → `lg: px-5 py-2.5` | Padding per breakpoint |
| Mobile toggle tap target | `44×44px` min | Accessibility min tap target |
| Mobile drawer top | `4.75rem` (76px) | Position from navbar bottom |
| Mobile drawer max-h | `calc(100vh - 6rem)` | Max-height |
| Dropdown min-width | `220px` | Min-width |

**Container** (`src/index.css` or layout CSS):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Max-width (xl) | `1320px` | `.container { max-width: 1320px }` at xl breakpoint |
| Horizontal padding | `16px` (px-4) | Default horizontal container padding |

**Section spacing** (global CSS):
| Type | kd-web-2.0 reference | Apply |
|---|---|---|
| Regular section | `py-12` mobile / `xl:py-14` | 48px → 56px |
| Small section | `py-8` mobile / `xl:py-10` | 32px → 40px |

**CardIcon** (after #75 grid fix):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Icon container | `48×48px` (h-12 w-12) | Icon wrapper size |
| Card padding | `p-5` (20px) | Internal padding |
| Card gap | `gap-6` (24px) | Flex gap |

**CardNumber** (after #75 grid fix):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Card max-width | `377px` | Keep as max-width ceiling |
| Card padding | `p-5` (20px) | Internal padding |
| Card gap | `gap-6` (24px) | Flex gap |

**Form inputs** (`src/components/contact/ContactForm.css` or equivalent):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Input padding | `px-4 py-2` | Input padding |
| Textarea min-height | `120px` | min-height |
| Form gap | `gap-6` (24px) | Between form fields |

**Buttons** (`src/styles/buttons/*.css`):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| Base padding | `px-6 py-3` (24×12px) | Default button padding |
| Small padding | `px-4 py-1.5` | Small button variant |
| Border-radius | `rounded-full` | Pill shape |

**404 page** (`src/pages/NotFound.tsx` or equivalent):
| Element | kd-web-2.0 reference | Apply |
|---|---|---|
| 404 number | `text-[8rem]` / `leading-none` | Giant 404 text |
| Animation container | `w-64` (256px) | Width for any illustration |

---

### Step 4 — #83 Fix nested `<a><button>` in DesktopNavbar

| File | Action |
|---|---|
| `src/components/navbar/desktopNavbar/DesktopNavbar.tsx` | Replace `<Link><Button>Contactar</Button></Link>` with a single `<Link>` styled as a button. Remove the wrapping `<Link>` and apply button styles directly to the `<Link>` element, OR use `useNavigate` inside Button's `onClick` |

Acceptance: no `<a>` wrapping `<button>`, visual and navigation behavior unchanged, no accessibility regression.

---

### Step 5 — Remove skip-to-main link

User request: remove the skip link added in PR #82.

| File | Action |
|---|---|
| `src/App.tsx` | Remove `<a href='#main-content' className='skip-link'>Saltar al contenido principal</a>` (line ~15) |
| `src/App.css` | Remove `.skip-link` and `.skip-link:focus` rules (lines 3–15) |
| `src/App.tsx` | Remove `id='main-content'` and `tabIndex={-1}` from `<main>` if present |

---

### Step 6 — #76 [P3] Add eslint-plugin-jsx-a11y

| File | Action |
|---|---|
| `package.json` | Add `eslint-plugin-jsx-a11y` as devDependency |
| `eslint.config.js` | Import plugin and add `jsxA11y.flatConfigs.recommended` |

Command: `npm install --save-dev eslint-plugin-jsx-a11y`

---

### Step 7 — #79 [P3] Document aria-disabled pattern

| File | Action |
|---|---|
| `src/components/commons/button/Button.tsx` | Add comment above `aria-disabled` explaining intentional pattern: keeps button focusable for keyboard users, click handler blocks action when aria-disabled="true" |

---

### Step 8 — #77 [P3] Add automated a11y testing

Commands:
```
npm install --save-dev jest-axe @types/jest-axe @axe-core/react
```

| File | Action |
|---|---|
| `src/main.tsx` | Add `@axe-core/react` in `import.meta.env.DEV` guard |
| `src/components/cookies/Cookies.test.tsx` | New — axe test |
| `src/components/commons/card/card-icon/CardIcon.test.tsx` | Extend existing with axe test |
| `src/components/commons/card/card-number/CardNumber.test.tsx` | Extend existing with axe test |
| `src/components/navbar/desktopNavbar/DesktopNavbar.test.tsx` | New — axe test |

After writing test files: run `npm run build` to verify `tsconfig.app.json` excludes them.

---

## Validation

1. `npm run build` — no TS or build errors
2. `npm run lint` — no eslint-plugin-jsx-a11y violations
3. `npm test` — all tests pass including new axe tests
4. Manual: navbar renders correctly, no nested `<a><button>`
5. Manual: theme toggle transitions without layout thrash
6. Manual: card grids align correctly at all breakpoints
7. Manual: footer layout correct at mobile / tablet / desktop
8. Manual: skip link is fully removed

---

## Files Modified Summary

| File | Steps |
|---|---|
| `src/index.css` | #74, container max-width |
| `src/styles/theme.css` | #74, #72 |
| `src/styles/buttons/buttons.css` | #72, button dimensions |
| `src/App.css` | skip-main removal |
| `src/App.tsx` | skip-main removal |
| `src/components/commons/card/card-icon/CardIcon.css` | #75, card dimensions |
| `src/components/commons/card/card-number/CardNumber.css` | #75, card dimensions |
| Parent section CSS files | #75 grid fix |
| `src/components/footer/Footer.css` (or equivalent) | Footer dimensions |
| Navbar CSS files | Navbar dimensions |
| `src/components/commons/button/Button.tsx` | #79 |
| `src/components/navbar/desktopNavbar/DesktopNavbar.tsx` | #83 |
| `eslint.config.js` | #76 |
| `src/main.tsx` | #77 |
| New/extended test files | #77 |
| `package.json` | #76, #77 |
