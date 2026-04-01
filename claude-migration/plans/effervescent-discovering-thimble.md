# Plan: Issues a resolver antes de migrar las pages

## Context

La rama activa es `feature/todo-components-migration`. Hay dos PRs abiertos
(#69 y #63) con trabajo ya hecho. Las pages (#30–#36) dependen de que los
componentes compartidos (Footer, iconos, logos, imágenes) estén migrados
primero para no bloquear el trabajo de cada página.

---

## Estado actual de los PRs

| PR | Issues cubiertas | Estado |
|----|-----------------|--------|
| #69 (rama actual) | #13 #14 #15 #20 #24 #25 #28 #29 #41 | Abierto, pendiente de merge |
| #63 | #17 #18 #19 (CardIcon, CardNumber, CardImage) | Abierto, pendiente de merge |

**Paso 0:** Mergear o cerrar estos dos PRs antes de empezar trabajo nuevo.

---

## Issues a resolver antes de las pages (orden recomendado)

### Bloqueos directos para las pages

| # | Issue | Por qué bloquea |
|---|-------|----------------|
| **#16** | Migrate Card component (base) | Componente base que usan las pages de contenido |
| **#26** | Migrate ThemeSwitcher | Está en el Header, todas las pages lo incluyen |
| **#23** | Migrate Footer component | Todas las pages incluyen Footer |
| **#44** | Migrate icons (Iconoir → react-icons) | Iconos usados en componentes de todas las pages |
| **#43** | Migrate logos and isotypes | Usados en Header/Footer de todas las pages |
| **#45** | Migrate social media icons and links | Usados en Footer |
| **#42** | Migrate and optimize images | Pages muestran imágenes |
| **#40** | Migrate Lottie animations | Si alguna page usa Lottie, debe estar listo antes |

### Mejoras rápidas (no bloquean pero conviene hacerlas ya)

| # | Issue | Por qué hacerlo ahora |
|---|-------|----------------------|
| **#66** | Fix decorative emojis in cookies.astro — add aria-hidden | Accessibility fix puntual, 1 archivo |
| **#65** | Configure vite-tsconfig-paths in Storybook | DX: permite que el dev workflow no falle al escribir stories de pages |

### No bloquean pages (se pueden hacer después o en paralelo)

| # | Issue | Nota |
|---|-------|------|
| **#53** | Add "Digital Accessibility" service category | Contenido nuevo, se añade a la page ya migrada |
| **#62** | Restore search trigger in header | Feature opcional, no bloquea nada |
| **#64** | Fix cookie policy copy | Contenido, se hace en la page existente |

---

## Orden de ejecución propuesto

```
1. Merge PR #69 + PR #63
2. #26  ThemeSwitcher
3. #23  Footer
4. #44  Icons (Iconoir → react-icons)
5. #43  Logos / isotypes
6. #45  Social media icons
7. #42  Images
8. #40  Lottie animations
9. #16  Card base
10. #66  Emoji aria-hidden fix (quick win)
11. #65  Storybook TS paths
--- ENTONCES: pages (#30 → #36) ---
```

---

## Verificación

- `yarn build` sin errores tras cada issue
- `yarn lint` pasa en los archivos modificados
- Visual check en `yarn dev` de Header + Footer en cada page

