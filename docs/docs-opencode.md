# docs-opencode — historial de cambios

Entradas más recientes arriba. Una entrada por cambio, con formato completo. El historial no se reescribe: solo se agrega.

## 2026-09-14 — Regla: docs-opencode viaja con cada cambio + commits del usuario

- **Commit:** `sin commit`
- **Tipo:** docs
- **Qué:** Se cambió la regla del skill `documentar-cambios`: `docs-opencode.md` ahora viaja en el mismo commit del cambio (antes quedaba sin commit). Además se registran dos commits hechos por el usuario: `05326d6` (retoque de formato/claridad del hero en `src/pages/index.astro`, 9+/8-) y `9b9eac3` (alta de `AGENTS.md`, `docs/docs-opencode.md` y `opencode.json` al repo; verificado sin secretos ni rutas locales).
- **Por qué:** El usuario decidió que es más prolijo que el changelog viaje con cada cambio.
- **Archivos:** `.agents/skills/documentar-cambios/SKILL.md`, `docs/docs-opencode.md`.
- **Verificación:** revisión de `git show --stat` de ambos commits; escaneo de secretos negativo en los tres archivos publicados.

## 2026-09-14 — Nueva descripción del hero

- **Commit:** `1a322c0`
- **Tipo:** contenido
- **Qué:** Se reemplazó el párrafo del hero ("Me senté a pensar… dejá tus comentarios…") por: "Cada día, un pensamiento del Pr. Walter Escalante para meditar la Palabra: reflexiones, devocionales y bosquejos del púlpito de Iglesia Restauración, Florencio Varela. Empezá el día con Dios y compartilo con quien lo necesite."
- **Por qué:** Texto más claro, cálido y accionable; además eliminaba la invitación a comentar, función que el sitio estático no tiene.
- **Archivos:** `src/pages/index.astro` (párrafo `hero-sub`).
- **Verificación:** `npm run build` (244 páginas), `npm test` 7/7, texto nuevo confirmado en `dist/index.html`; push a `main`.

## 2026-09-14 — Fixes móviles (heroMeta + drawer)

- **Commit:** `25067f5`
- **Tipo:** código/estilos
- **Qué:** `.hero-controls` con `flex-wrap: wrap` y `#heroMeta` con `min-width: 0` (ellipsis ante títulos largos en ~320px); drawer móvil a `top: 0` (altura completa tras el header fijo, sin costura arbitraria en 3.5rem).
- **Por qué:** Dos detalles cosméticos detectados en la auditoría responsive.
- **Archivos:** `src/styles/global.css`.
- **Verificación:** `npm run build` (244 páginas), `npm test` 7/7, 3 checks PASS en CSS compilado de `dist/`; push a `main`.

## 2026-09-14 — Header a todo ancho

- **Commit:** `cbc3dcb`
- **Tipo:** código/estilos
- **Qué:** `.topbar-inner` pasó de `max-width: 80rem` a `max-width: none` en `src/styles/global.css`. El brand queda pegado al margen izquierdo como el "Explorar" del sidebar; el buscador sigue a la derecha.
- **Por qué:** Los estilos del brand sí estaban aplicados en producción (verificado: HTML fresco + CSS con hash nuevo); lo que se veía separado era el contenedor centrado de 80rem en pantallas anchas. El fix anterior de padding (10px) era imperceptible ahí.
- **Archivos:** `src/styles/global.css`.
- **Verificación:** `npm run build` (244 páginas), `npm test` 7/7, regla confirmada en CSS compilado de `dist/`; push a `main`.

## 2026-09-14 — Fix deploy GitHub Pages: workflow Actions + base-path

- **Commit:** `sin commit`
- **Tipo:** config + código/estilos
- **Qué:** Pages fallaba con `Invalid YAML front matter in content/articulos/3649.md` porque estaba en modo "Deploy from a branch" (Jekyll). Se agregó `.github/workflows/deploy.yml` (build Astro + deploy Pages), `base` configurable por env `PAGES_BASE` en `astro.config.mjs`, helper `src/lib/base.js` (`withBase`/`basePrefix`) aplicado a todos los links/imgs (Base, Card, Featured, index, [slug], 404, RSS, sidebar, JS client-side vía `DATA.base`), `site.webmanifest` con rutas relativas y `public/reflexion.html` con base runtime-relativa.
- **Por qué:** Sin esto la web no se podía publicar: Jekyll no compila Astro y `dist/` está en `.gitignore`, así que el único deploy viable es por Actions. Además, project Pages sirve en subruta y los links absolutos se rompían.
- **Archivos:** `.github/workflows/deploy.yml` (nuevo), `src/lib/base.js` (nuevo), `astro.config.mjs`, `src/layouts/Base.astro`, `src/components/Card.astro`, `src/components/Featured.astro`, `src/pages/index.astro`, `src/pages/reflexion/[slug].astro`, `src/pages/404.astro`, `src/pages/rss.xml.js`, `public/site.webmanifest`, `public/reflexion.html`.
- **Verificación:** build local OK (244 páginas, tests 7/7, seo 0 errores); build simulando CI (`PAGES_BASE`+`SITE`) con 13 checks PASS (favicon/cards/imgs/sidebar/prev-next/RSS/sitemap/404/manifest/legacy con subruta, cero links fuera de base). Falta paso manual: Settings → Pages → Source: GitHub Actions.

## 2026-09-14 — Skill documentar-cambios + este changelog

- **Commit:** `sin commit`
- **Tipo:** docs
- **Qué:** Se creó el skill `documentar-cambios` (`.agents/skills/documentar-cambios/SKILL.md`) y se completó este archivo con todos los cambios anteriores del repo.
- **Por qué:** Pedido del usuario: cada cambio documentado en `docs-opencode.md`, siempre, incluyendo cambios ya hechos.
- **Archivos:** `.agents/skills/documentar-cambios/SKILL.md` (nuevo), `docs/docs-opencode.md` (completado).
- **Verificación:** revisión visual de ambos archivos; skill sigue el formato frontmatter + flujo de los skills existentes del repo.

## 2026-09-14 — Brand del header más a la izquierda

- **Commit:** `13d6e3e`
- **Tipo:** código/estilos
- **Qué:** Se redujo el padding izquierdo de `.topbar-inner` en `src/styles/global.css` (desktop `0 1.125rem` → `0 1.125rem 0 0.5rem`; móvil `0.5rem 0.75rem 0.625rem` → `... 0.375rem`). El brand queda ~10px más cerca del margen en desktop y ~6px en móvil, en home y lector.
- **Por qué:** El brand se veía muy separado del margen izquierdo.
- **Archivos:** `src/styles/global.css`.
- **Verificación:** `npm run build` (244 páginas OK) y regla confirmada en el CSS compilado de `dist/_astro/`; push a `main`.

## 2026-09-13 — Nuevas reflexiones 12–13/09 + guía de actualización

- **Commit:** `f76c0f6`
- **Tipo:** contenido + docs
- **Qué:** Se agregaron `Coronas` (12/09) y `Des-graciados` (13/09, slug `3661`) con sus imágenes, y se creó `docs/actualizar-web.md` con el proceso de actualización.
- **Por qué:** La web del pastor tenía posts nuevos no reflejados en el repo (estaban sin commitear); el usuario pidió actualizar la web y documentar el proceso.
- **Archivos:** `content/articulos/3661.md`, `content/articulos/coronas.md`, `content/imagenes/3661.png`, `content/imagenes/coronas.png`, `docs/actualizar-web.md`.
- **Verificación:** portada del pastor chequeada (último post = `3661`, coincide con local); `scraper.py --once` sin novedades; `build:data` → 242 ítems; `astro build` → 244 páginas con `3661`/`coronas` en `dist/` y 242 `<item>` en RSS; `npm test` 7/7; `seo:check` 0 errores; push a `main`.

## 2026-09-11 — Skill i-have-adhd

- **Commit:** `9b78674`
- **Tipo:** docs
- **Qué:** Se agregó el skill `i-have-adhd` con detalles de fuente y ruta.
- **Por qué:** Personalización del asistente para lector con ADHD.
- **Archivos:** `skills-lock.json` (+6 líneas, registro del skill).
- **Verificación:** `no registrado` (entrada reconstruida desde historial git).

- **Commit:** `fcd9fbd`
- **Tipo:** código/estilos
- **Qué:** Tema oscuro completo, set de favicons y `og-image` 1200x630.
- **Por qué:** Cierre visual y SEO social del sitio.
- **Archivos:** `src/styles/global.css`, `src/layouts/Base.astro`, `src/lib/seo.js`, `src/pages/404.astro`, `src/pages/index.astro`, `scripts/seo/gen-favicons.mjs` + `gen-og.mjs` (nuevos), `public/og-image.png`, favicons (`favicon.ico/svg`, `favicon-16/32`, `apple-touch-icon`, `android-chrome-192/512`), `public/site.webmanifest`, `package.json` (17 archivos).
- **Verificación:** `no registrado` (entrada reconstruida desde historial git).

## 2026-09-11 — Favicon set + theme-color

- **Commit:** `9ba26e6`
- **Tipo:** código/estilos
- **Qué:** Set de favicons sencillo (svg + png + apple-touch + manifest) + `theme-color`.
- **Por qué:** Identidad del sitio en pestañas y móviles.
- **Archivos:** `public/favicon.svg`, `public/favicon-32x32.png`, `public/apple-touch-icon.png`, `public/site.webmanifest`, `src/layouts/Base.astro` (5 archivos).
- **Verificación:** `no registrado` (entrada reconstruida desde historial git).

## 2026-09-11 — 404, robots dinámico, SITE configurable, seo:check strict + README

- **Commit:** `31f4180`
- **Tipo:** código/estilos + config + docs
- **Qué:** Página 404, `robots.txt` dinámico, `SITE` por variable de entorno, modo estricto de `seo:check` y README completo.
- **Por qué:** Checklist pre-producción y documentación del proyecto.
- **Archivos:** `src/pages/404.astro` (nueva), `src/pages/robots.txt.js` (nuevo), `src/pages/rss.xml.js`, `src/pages/index.astro`, `src/layouts/Base.astro`, `scripts/seo/check.mjs`, `astro.config.mjs`, `package.json`, `README.md` (9 archivos).
- **Verificación:** `no registrado` (entrada reconstruida desde historial git).

## 2026-09-11 — Commit inicial: sitio Astro + scraper + 240 reflexiones

- **Commit:** `2fde4d9`
- **Tipo:** contenido + código/estilos + config
- **Qué:** Alta inicial del proyecto: sitio Astro estático, pipeline scraper (`scripts/scraper/`) + builder (`scripts/builder/`), y 240 reflexiones en `content/`.
- **Por qué:** Punto de partida del proyecto.
- **Archivos:** base completa (`astro.config.mjs`, `package.json`, `pyproject.toml`, `.gitignore`, `README.md`, `LICENSE`, `src/`, `scripts/`, `tests/`, `content/articulos/` con 240 `.md`, `content/imagenes/`, `content/audios/`).
- **Verificación:** `no registrado` (entrada reconstruida desde historial git).
