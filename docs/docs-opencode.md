# docs-opencode — historial de cambios

Entradas más recientes arriba. Una entrada por cambio, con formato completo. El historial no se reescribe: solo se agrega.

## 2026-09-14 — Botón GitHub en header (4 commits del usuario)

- **Commits:** `54bb5ca`, `3113b13`, `66463b4`, `ae13c24`
- **Tipo:** código/estilos
- **Qué:** Botón "Ver código en GitHub" en el header de home y lector: SVGs dark/light en `public/iconos/`, markup en ambas páginas, estilos desktop+reader, línea en README.
- **Por qué:** Enlazar el repo desde el sitio.
- **Archivos:** `public/iconos/github_dark.svg`, `public/iconos/github_light.svg`, `src/pages/index.astro`, `src/pages/reflexion/[slug].astro`, `src/styles/global.css`, `README.md`.
- **Verificación:** iconos referenciados con `withBase()` (seguros en subruta Pages); solo se usa la variante dark, la light queda sin uso; `npm run build` 244 páginas OK.
- **Nota:** entradas agrupadas (una feature en 4 commits del usuario).

## 2026-09-14 — Icono GitHub en el topbar (home + lectora)

- **Commit:** `54bb5ca, 3113b13, 66463b4, ae13c24`
- **Tipo:** código/estilos
- **Qué:** Botón con icono GitHub a la derecha del buscador en el home (`index.astro`) y alineado a la derecha en la lectora (`[slug].astro`, que no tiene buscador). Icono elegido: `public/iconos/github_dark.svg` (blanco, visible sobre el topbar negro); `github_light.svg` queda como reserva para fondos claros. En móvil (≤900px) el botón queda en la esquina superior derecha (fila 1) y el buscador baja a full-width (fila 2). Reusa `.icon-btn` + clase `.github-link`, con `withBase()` para el path (GitHub Pages sirve en subruta).
- **Por qué:** Pedido del usuario: link visible al repo desde el header, en desktop y móvil.
- **Archivos:** `public/iconos/github_dark.svg`, `public/iconos/github_light.svg` (nuevos), `src/pages/index.astro`, `src/pages/reflexion/[slug].astro`, `src/styles/global.css`, `README.md` (línea de `iconos/` en §4).
- **Verificación:** `npm run build` (244 páginas), link e icono confirmados en `dist/index.html` y `dist/reflexion/*/index.html`, `npm test` 7/7; push a `main`.

## 2026-09-14 — Fin de los ❌ de Pages: Source a Actions + paths-ignore

- **Commit:** `74e5b72`
- **Tipo:** config
- **Qué:** Los ❌ rojos en `pages build and deployment` eran el builder viejo de Jekyll, que seguía corriendo en cada push porque el Source de Pages nunca se había cambiado (`build_type: legacy`). No afectaban al sitio (publicaba nuestro workflow Astro, siempre verde), pero metían ruido y alarma. Solución: (1) `build_type` pasado a `workflow` por API (`gh api PUT repos/.../pages`), o sea Source = GitHub Actions, con lo que el Jekyll fantasma ya no se dispara; (2) `paths-ignore` en `deploy.yml` (`docs/**`, `.agents/**`, `AGENTS.md`, `opencode.json`) para que cambios solo-docs no disparen deploys.
- **Por qué:** Eliminar los errores y evitar deploys inútiles.
- **Archivos:** `.github/workflows/deploy.yml` (cambio por API en Settings, sin archivo).
- **Verificación:** `gh api .../pages` devuelve `build_type: workflow`; tras el push, en Actions debe correr solo "Deploy Astro..." sin ningún `pages-build-deployment`.
- **Cómo evitarlos:** si vuelve a aparecer `pages-build-deployment`, revisar que Source siga en GitHub Actions (`gh api repos/.../pages --jq .build_type` debe dar `workflow`); nunca volver a "Deploy from a branch" (Jekyll no compila Astro y `dist/` está en `.gitignore`).

## 2026-09-14 — Re-scrape 3661 "Des-graciados" + guardia de párrafos

- **Commit:** `630ddfe`
- **Tipo:** código/contenido
- **Qué:** `content/articulos/3661.md` se había scrapeado en una sola línea (el `.entry-content` no expuso bloques `<p>` esa vez y cayó al fallback plano de `extract.py:45`); la página renderizaba 1 bloque. Se re-extrajo del blog oficial → 32 párrafos. Además `scripts/builder/build-data.mjs` ahora avisa `[WARN] sin saltos de párrafo: <slug>` cuando un cuerpo sale plano, para detectarlo en el build. Era el único de 242 en ese estado.
- **Por qué:** Sin `\n` el lector muestra todo agrupado; ningún script lo señalaba.
- **Archivos:** `content/articulos/3661.md`, `scripts/builder/build-data.mjs`.
- **Verificación:** `npm run build:data` sin WARN, `seo:check` 0 errores, `vitest` 7/7, `dist/reflexion/3661/index.html` con 32 `<p>`; push a `main`.

## 2026-09-14 — Open Graph completo (locale, site_name, dims, alt, article, JSON-LD)

- **Commit:** `dd29496`
- **Tipo:** código/seo
- **Qué:** Auditoría OG 76/100 → `src/layouts/Base.astro` ahora emite `og:site_name`, `og:locale` (`es_AR`), `og:image:width/height` (1200/630), `og:image:type` (según extensión), `og:image:alt` y `twitter:image:alt`; `og:type` es `website` en home y `article` en reflexiones (antes todo era `article`), con `article:published_time/modified_time/section/author` en artículos. JSON-LD en home (`WebSite` con `url`) y en artículos (`Article` con `mainEntityOfPage`, logo del publisher e imagen absoluta); más `meta author` y `meta robots`. `src/lib/seo.js` provee `ogType`, `ogImageAlt`, `article` y `jsonLd` de índice.
- **Por qué:** Faltaban dimensiones de imagen, alt, site_name, locale y structured data; el type `article` en la home era incorrecto.
- **No se hizo:** `twitter:site` (no hay usuario de X conocido; inventarlo empeora el SEO). "Missing H1" y "canonical differs" del analizador son falsos positivos: el H1 existe (`index.astro:142`) y la canónica con `/` final es intencional con `trailingSlash: 'never'`.
- **Archivos:** `src/layouts/Base.astro`, `src/lib/seo.js`, `src/pages/index.astro`, `src/pages/reflexion/[slug].astro`.
- **Verificación:** `npm run build` (244 páginas), `seo:check` 0 errores, `vitest` 7/7, head de `dist/index.html` y de un artículo verificados tag por tag; push a `main`.

## 2026-09-14 — Consistencia de favicon y og-image

- **Commit:** `6965e13`
- **Tipo:** código/estilos
- **Qué:** `public/favicon.svg` normalizado (atributos reordenados, `#000000` → `#000`, mismo render) y `public/og-image.png` re-exportado (48KB → 27KB). Cambio del usuario.
- **Por qué:** Consistencia de marca entre favicon y og-image.
- **Archivos:** `public/favicon.svg`, `public/og-image.png`.
- **Verificación:** `npm run build` (244 páginas), `seo:check` 0 errores; diff del svg confirma solo reordenamiento sin cambio visual.

## 2026-09-14 — Drawer móvil debajo del header real

- **Commit:** `cbfd517`
- **Tipo:** código/estilos
- **Qué:** El drawer móvil (`top: 0` del fix anterior) quedaba tras el header y tapaba el mes de septiembre. Ahora al abrir se calza con JS a la altura real del header (`offsetHeight`, que en móvil envuelve a 2 filas) y se re-sincroniza en `resize`; en desktop se limpia el estilo inline.
- **Por qué:** El header cubría el inicio del sidebar-scroll y ocultaba el mes actual.
- **Archivos:** `src/pages/index.astro` (script inline del drawer).
- **Verificación:** `npm run build` (244 páginas), `npm test` 7/7, JS con `offsetHeight` confirmado en el bundle de `dist/`; push a `main`.

## 2026-09-14 — Regla: docs-opencode viaja con cada cambio + commits del usuario

- **Commit:** `5b75561`
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
