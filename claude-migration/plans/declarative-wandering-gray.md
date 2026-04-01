# Plan: Eliminar páginas creadas por error

## Context
El usuario pidió migrar los **componentes** pendientes en las issues de Todo. Por error, también se crearon dos páginas (`gracias.astro` y `privacidad.astro`) que corresponden a issues de páginas (#34, #36), no de componentes.

## Acción requerida
1. Eliminar `src/pages/gracias.astro` (creado por error)
2. Eliminar `src/pages/privacidad.astro` (creado por error)
3. Continuar solo con los componentes: esperar al agente C (ContactForm + useFormValidation) y no crear más páginas
