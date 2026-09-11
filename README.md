# Biblioteca de Reflexiones — Pr. Walter Escalante (2026)

Sitio estático que publica **+240 reflexiones (enero–septiembre 2026)** como biblioteca navegable por mes, con búsqueda, cards, página de lectura individual con audio, SEO completo, RSS y sitemap.

> **Estado:** proyecto personal de práctica / concepto no oficial.
> **Sitio oficial del autor del contenido:** https://prwalterescalante.com/ (WordPress).
> Este repo **no lo reemplaza hoy**. Es una exploración técnica de cómo se vería una alternativa liviana, hecha desde cero con Astro.
>
> **Autoría clara:**
> - Código, diseño y pipeline: **Leonardo Bringas** (MIT, ver `LICENSE`).
> - Textos, imágenes y audios de las reflexiones: **Pr. Walter Escalante** (todos los derechos reservados, uso pastoral / demostrativo). No están cubiertos por MIT.
> - Para mostrar este proyecto en portafolio usar solo **capturas / video**, con crédito y aclarando “concepto no oficial”, salvo autorización expresa del pastor.

---

## 1. Demo y capturas (para portafolio)

Como el contenido es de un tercero, **no se publica el sitio completo como propio**. Para `leobringasatlife.site` usar:

1. Home / biblioteca con buscador por palabra, tema o versículo + filtro por mes.
2. Card + destacada + sidebar.
3. Lector `/reflexion/[slug]` con hero, versículos, audio `<audio controls preload="none">`, tiempo de lectura, anterior/siguiente.
4. Responsive móvil + ViewTransitions.

Texto sugerido para la ficha (copiar/pegar):

> **Biblioteca de reflexiones — concepto personal (Astro)**
> Rediseño conceptual no oficial, hecho para practicar. Sitio estático de 240 páginas generado desde 239 archivos Markdown. Incluye búsqueda instantánea, filtro por mes, lector con audio, SEO/Open Graph, JSON-LD Article, RSS y sitemap. Sin plantillas ni WordPress: código desde cero, personalizable a cualquier rubro. Contenido original del Pr. Walter Escalante, mostrado solo con fines demostrativos.

Ver `docs/architecture.md` para el mapa de módulos profundos.

---

## 2. Características

- **240 páginas estáticas:** `index` + 239 `/reflexion/[slug]` vía `getStaticPaths()` en `src/pages/reflexion/[slug].astro:7-10`.
- **Búsqueda y filtrado client-side:** `src/js/modules/filtering.js` + `grouping.js` (lógica pura, sin DOM, testeable) + Fuse.js.
- **Taxonomía por mes:** `2026-01 … 2026-12` centralizada en `scripts/builder/taxonomy.mjs:4-17`.
- **Parser tolerante:** `scripts/builder/parser.mjs:10-80` — extrae `Titulo / Fecha / URL ORIGEN / Imagen / Audio Local / Contenido`, limpia “Comparte esto / Relacionado / X / Facebook / Me gusta”, genera `slug, excerpt (220 ch), fechaISO, lecturaMin (180 wpm, mín 2), palabras, versículos`.
- **Versículos automáticos:** `scripts/builder/verses.mjs` con regex + normalización (`Job 23:3`).
- **SEO / OG / Twitter / JSON-LD:** `src/lib/seo.js:5-30` + `src/layouts/Base.astro:19-38`. `og:image` fallback `imagenes/logos/logo-we.webp`. Canonical relativa que se absolutiza con `env SITE`.
- **RSS:** `src/pages/rss.xml.js:4-18` (usa `context.site ?? https://prwalterescalante.com` como fallback).
- **Sitemap:** `@astrojs/sitemap` en `astro.config.mjs:14-19` (requiere `SITE` en CI, ver §8).
- **Redirect legacy:** `public/_redirects:3` + `public/reflexion.html` (`?slug=X → /reflexion/X`) para Netlify / Cloudflare Pages.
- **Audio e imágenes locales:** copiados de `content/` a `public/` en build (no symlinks por Windows).
- **Tests:** `vitest` (`parser, taxonomy, search`) + `pytest` (`test_scraper_output_dir.py`).

---

## 3. Stack

- **Sitio:** Astro 5 (output `static`), `src/layouts/Base.astro` + ViewTransitions, CSS global en `src/styles/global.css`, componentes `Card.astro`, `Featured.astro`.
- **Datos:** Node 18+ ESM (`scripts/builder/*.mjs`), Python 3.10+ (`scripts/scraper/*.py` con `requests + beautifulsoup4`).
- **Búsqueda:** `fuse.js ^7.5.0`.
- **Imágenes:** `sharp ^0.35.4` (optimización).
- **Feed:** `@astrojs/rss ^4.0.19`.
- **Tests:** `vitest ^5`, `pytest`.
- **Formato:** Prettier + `prettier-plugin-astro` (`.prettierrc`).

---

## 4. Estructura (fuente de verdad vs derivado)

```
.
├── content/               # FUENTE DE VERDAD (versionado, sí se commitea)
│   ├── articulos/         # 239 .md con frontmatter "- Titulo / Fecha / URL..."
│   ├── imagenes/          # originales (incluye logos/logo-we.webp fallback)
│   └── audios/            # mp3 originales
├── src/                   # sitio Astro
│   ├── pages/
│   │   ├── index.astro              # home: carga loadItems(), arma clientItems
│   │   ├── reflexion/[slug].astro   # lector: prev/next, related por categoria, paragraphs
│   │   └── rss.xml.js               # feed
│   ├── components/        # Card.astro, Featured.astro
│   ├── layouts/           # Base.astro (SEO/OG + ViewTransitions + lang="es")
│   ├── lib/
│   │   ├── items.js       # loadItems(): lee content/articulos, parseMd, ordena desc, stats MESES, cache
│   │   └── seo.js         # seoForIndex(), seoForItem(), escapeHtml()
│   ├── styles/global.css
│   └── js/modules/        # filtering.js, grouping.js (deep modules, sin DOM)
├── scripts/
│   ├── scraper/           # scraper.py (orquestador), peticiones.py, extract.py
│   ├── builder/           # build-data.mjs (orquestador delgado) + parser.mjs + taxonomy.mjs + verses.mjs
│   ├── seo/check.mjs       # valida title 50-60ch, description 140-160ch, og, canonical
│   ├── linking/build.mjs   # genera public/data/relaciones.json (no muta reflexiones.json)
│   └── maintenance/       # parches legacy archivados (fix_json, reflow, formatear_md...)
├── public/                # estáticos que se copian a dist/ tal cual
│   ├── reflexion.html     # redirect legacy ?slug=X
│   ├── _redirects         # Netlify / Cloudflare
│   ├── data/              # DERIVADO: reflexiones.json + relaciones.json (ver §5)
│   ├── imagenes/          # DERIVADO: copia de content/imagenes en build
│   └── audios/            # DERIVADO: copia de content/audios en build
├── dist/                  # DERIVADO: salida `astro build` (deploy)
├── content/ ↔ public/ ↔ dist/  # ver §5 para regla de oro
├── docs/architecture.md   # seams, interfaces y depth (vocabulario codebase-design)
├── tests/                 # taxonomy.test.mjs, parser.test.mjs, search.test.mjs, test_scraper_output_dir.py
├── .agents/skills/        # extraccion-metadatos, generador-resumenes-snippets, enlazado-cruzado, generador-seo-og, ui-helpers-previews
└── package.json / pyproject.toml / astro.config.mjs
```

**Regla de oro:**

- `content/` = entrada manual / scrapeada. **Se versiona.**
- `public/data/ + public/imagenes/ + public/audios/` = salida generada por `node scripts/builder/build-data.mjs`. **No se versiona, se regenera.**
- `dist/` = salida de `astro build`. **No se versiona, se despliega.**

---

## 5. Corrección importante sobre `.gitignore` y deploy

> Versión anterior de este README (y un comentario del autor) decía “el deploy está a medias porque `.gitignore` ignora `public/data`, `public/imagenes`, `dist`”. **Eso es impreciso y se corrige aquí.**

`.gitignore` actual (`lines 22-26, 18`):

```
dist/
public/data/reflexiones.json
public/data/relaciones.json
public/imagenes/
public/audios/
```

**Esto es correcto y es buena práctica.** Esos archivos son derivados y pesan mucho (cientos de imágenes/audios). No deben ir a git porque:

1. La fuente de verdad es `content/` (liviana en git).
2. El CI/CD los regenera en cada deploy con `npm run build` (que primero corre `build-data.mjs` y luego `astro build`).
3. Evita conflictos y repos gigantes.

**Lo que sí faltaba (y faltaba documentar) era el pipeline de deploy.** No es que el `.gitignore` esté mal, es que sin CI documentado el deploy parece roto. Ver §8 para el pipeline correcto:

```bash
npm ci
npm run build   # = node scripts/builder/build-data.mjs && astro build
# publicar dist/
```

Si el hosting no corre build (hosting estático puro por FTP), entonces sí hay que generar local y subir `dist/` a mano. Pero en Netlify / Vercel / Cloudflare Pages / GitHub Pages con Actions, **no se commitea `dist/` ni `public/data/`**.

---

## 6. Formato de contenido (contrato)

Cada `content/articulos/<slug>.md`:

```md
---
- Titulo: "El Dios que ve"
- Fecha: 12/03/2026
- URL ORIGEN: https://prwalterescalante.com/2026/...
- Imagen: 2026-03-12-el-dios-que-ve.webp
- Audio Local: 2026-03-12-el-dios-que-ve.mp3
---

Contenido:
Texto limpio de la reflexión...
```

Reglas (`extraccion-metadatos/SKILL.md`, `scripts/builder/parser.mjs`):

- `Fecha` siempre `DD/MM/YYYY`. Se convierte a `fechaISO YYYY-MM-DD` y `ts` para ordenar desc.
- `Imagen: Ninguna / Ninguno` o `Audio Local: Ninguno` → `null` (sin hero / sin player, con fallback).
- `Contenido:` termina donde empieza `Comparte esto / Relacionado / X / Facebook`. El parser lo recorta.
- `slug` = nombre del archivo sin `.md` (ej: `2026-03-12-el-dios-que-ve`).
- `categoria` = `categoriaPorFecha(fechaISO)` → `2026-01 … 2026-12`. Si no hay fecha, `2026-01`.
- Límites: `excerpt 220ch + …`, `contenido.slice(0,8000)` en JSON para no inflar `reflexiones.json`.

Ejemplo real: abrir cualquier `content/articulos/*.md` y comparar con su salida en `reflexiones.json`.

---

## 7. Pipeline completo

```
prwalterescalante.com
  ↓ scripts/scraper/scraper.py --once (delay 5s, headers Chrome, deduplica por slug)
content/articulos/*.md + content/imagenes/* + content/audios/*
  ↓ scripts/builder/build-data.mjs (parseMd + MESES + extractVerses, orden desc, stats)
public/data/reflexiones.json {generatedAt, total, categories[{id,label,short,mes,count}], items[]}
  + copia content/imagenes → public/imagenes, content/audios → public/audios
  ↓ src/lib/items.js:loadItems() (misma semántica, con cache en memoria)
src/pages/index.astro + src/pages/reflexion/[slug].astro
  ↓ astro build
dist/ (index.html + reflexion/<slug>/index.html + rss.xml + sitemap-*.xml)
```

`scripts/linking/build.mjs` genera aparte `public/data/relaciones.json` (`relatedFor(slug)` por scoring de tema/versículos/contenido, ver skill `enlazado-cruzado`). Hoy `[slug].astro:21` usa related simple por misma categoría (slice 4); migrar a `relaciones.json` es Fase 2.

---

## 8. Requisitos

- Node 18+ (ESM). Verificado con Astro 5.
- Python 3.10+ solo si vas a scrapear.
- Windows / Linux / macOS (copia con `fs.cpSync`, no symlinks, por Windows).

```bash
node -v   # v18+
python --version  # 3.10+
```

---

## 9. Instalación

```bash
# 1) Clonar (solo trae content/, no trae derivados)
git clone <repo> reflexiones_escalante_2026
cd reflexiones_escalante_2026

# 2) Deps Node
npm install

# 3) Deps Python (solo scraper)
pip install requests beautifulsoup4
# o:
pip install -e ".[dev]"
```

No necesitás crear `public/data/` ni `public/imagenes/` a mano: `npm run build:data` los genera.

---

## 10. Uso

```bash
# Dev (lee directo content/ vía loadItems, sin necesidad de JSON previo)
npm run dev              # http://localhost:4321

# Build completo (genera JSON + copia activos + compila Astro a dist/)
npm run build            # node scripts/builder/build-data.mjs && astro build

# Solo datos (para seo:check o debug sin compilar Astro)
npm run build:data

# Preview de dist/
npm run preview

# Scraper — una pasada, luego regenera JSON
npm run scrape:once      # python scripts/scraper/scraper.py --once && npm run build:data

# Scraper — modo watch cada 15 min (ideal cron local, no CI)
npm run scrape:watch
python scripts/scraper/scraper.py --once --help  # ver flags --interval, --delay, --year-filter

# SEO check
npm run seo:check        # node scripts/seo/check.mjs (title 50-60, desc 140-160, og, canonical)

# Enlazado cruzado
npm run linking:build    # node scripts/linking/build.mjs → public/data/relaciones.json

# Tests
npm test                 # vitest run (parser, taxonomy, search)
pytest                   # test_scraper_output_dir.py
```

Variables de entorno:

```bash
# SITE se usa en Base.astro para absolutizar og:url / og:image / canonical
SITE=https://tudominio.com npm run build
# En Netlify/Vercel definir SITE en dashboard. Si no se define, sale relativo (ok local, mal SEO prod).
```

---

## 11. Deploy a producción (Netlify / Vercel / Cloudflare Pages)

**Build command:** `npm run build`
**Publish directory:** `dist`
**Env:** `SITE=https://tudominio.com` + `NODE_VERSION=18` (o 20).

Por qué funciona aunque `public/data` esté en `.gitignore`:

1. El CI hace `npm ci`.
2. Corre `node scripts/builder/build-data.mjs` → crea `public/data/reflexiones.json` + copia `public/imagenes|audios`.
3. Corre `astro build` → lee `content/` vía `loadItems()` y emite `dist/` con 242 páginas (240 contenido + 404 + robots) + `rss.xml` + `sitemap-index.xml`.
4. Publica `dist/`. `public/_redirects` se copia solo a `dist/_redirects`.

Checklist pre-prod (actualizado):

- [x] `SITE` configurable vía env con fallback demo (`astro.config.mjs` → `site: process.env.SITE || reflexiones-demo...`). Verificado: `SITE=https://ejemplo.com npm run build` genera sitemap y robots absolutos.
- [x] `src/pages/404.astro` con layout Base + estilos propios.
- [x] `src/pages/robots.txt.js` dinámico (`Allow: /` + `Sitemap: <SITE>/sitemap-index.xml`).
- [x] `src/pages/rss.xml.js` usa `context.site` (hereda de `astro.config`).
- [x] `npm run seo:check` limpio (0 errores) + `npm run seo:check:strict` para CI (falla si hay warnings).
- [ ] Definir dominio real + `SITE` real en hosting + HTTPS + redirect www→apex.
- [ ] Medir `/audios/*.mp3` totales (pueden ser cientos de MB → considerar CDN / streaming externo).
- [ ] Decidir workflow de publicación para el pastor (ver §12). Sin esto, no es reemplazo viable de WordPress.

---

## 12. Mantenimiento (para el pastor / no-técnico vs dev)

**Hoy WordPress gana en esto.** El pastor publica solo desde el celular. En este repo, publicar = correr comandos. Opciones si algún día migra:

**A) Simple (recomendada):** Decap CMS / Tina / Google Sheet → commit a `content/articulos/` → deploy automático. El pastor solo llena título/fecha/texto/audio.

**B) Asistida:** el pastor manda texto por WhatsApp, vos creás el `.md` con el formato §6, corrés `npm run build:data`, verificás `npm run dev`, pusheás.

**C) Automática:** cron diario `scraper.py --once` en GitHub Actions → commit si hay nuevos → build → deploy. Requiere cuidar `rate-limit (5s)`, `User-Agent`, y respeto a `robots.txt` del sitio origen + autorización.

Nunca editar `public/data/*.json` a mano: se sobrescribe. Editar siempre `content/articulos/*.md`.

---

## 13. Tests y calidad

```bash
npm test   # tests/parser.test.mjs (frontmatter roto, fechas, excerpt), taxonomy.test.mjs (MESES, categoriaPorFecha), search.test.mjs (filtering sin DOM)
pytest -q  # verifica que scraper no anide output dir y respeta slugs Windows-safe
npm run seo:check
```

Convenciones (`docs/architecture.md`):

- `parseFile(path, {fs})` acepta `fs` inyectado (no `new Fs()` adentro) → testeable con `MemoryAdapter`.
- `extractVerses(text): string[]` pura, no muta `item`.
- 1 función por módulo; `build-data.mjs` solo orquesta.
- Frontend: `src/js/modules/*.js` sin `document` → mismos tests en Node y browser.

---

## 14. Roadmap

- **Fase 1 (actual):** ordenar carpetas, dual-path `content/articulos` → fallback `articulos_completos/`, archivar legacy en `scripts/maintenance/`, documentar `.gitignore` (este archivo).
- **Fase 2:** migrar related a `relaciones.json`, extraer `filtering.js` completo + tests, `404.astro + robots.txt`, optimizar imágenes con `sharp`, paginación / búsqueda con Fuse en worker.
- **Fase 3:** higiene — pre-commit (Prettier + vitest), extraer `sites/iglesia` a repo propio, GitHub Action para scrape diario + deploy, CMS simple para el pastor.
- **No-objetivo:** clonar comentarios / plugins de WordPress. Si se necesitan, se evalúan aparte (Giscus, newsletter, analytics sin cookies).

---

## 15. Licencia y uso en portafolio

- **Código:** MIT © 2026 Leonardo Bringas. Podés reutilizar estructura, scripts, componentes y pipeline para clientes.
- **Contenido:** textos/imágenes/audios © Pr. Walter Escalante. Solo uso demostrativo/pastoral. No redistribuir, no vender, no publicar como propio.
- **En tu página de ventas:** usar capturas/video + crédito + “concepto no oficial”. Pedir permiso antes de vincular al sitio oficial o usar su nombre como testimonio.

---

## 16. FAQ

**¿Está apto para producción?**
Como demo/portafolio: sí. Como reemplazo del WordPress del pastor: no todavía (falta SITE real, CI documentado, workflow para no-técnicos y checklist §11).

**¿Por qué Astro y no WordPress?**
WordPress = publicar fácil + plugins + hosting pesado. Astro estático = rapidísimo, baratísimo de hostear, seguro, pero publicar requiere pipeline. Para un sitio de lectura diaria con 239 artículos, Astro rinde mejor en velocidad/SEO/costo; WordPress rinde mejor en autonomía del autor. Elegir según quién publica.

**¿Qué aprendí haciéndolo?**
Scraping respetuoso con rate-limit, parsing tolerante a frontmatter roto, taxonomía centralizada, SEO/OG/JSON-LD, RSS/sitemap, Astro `getStaticPaths` para 240 páginas, testing sin DOM, y la diferencia entre “funciona en local” y “mantenible en producción por un no-técnico”.

---

## 17. Créditos

- Contenido: Pr. Walter Escalante — Iglesia Restauración, Florencio Varela.
- Código y documentación: Leonardo Bringas — https://leobringasatlife.site/ (sitios desde cero, personalizables).
- Skills/guía en `.agents/skills/`: `extraccion-metadatos`, `generador-resumenes-snippets`, `enlazado-cruzado`, `generador-seo-og`, `ui-helpers-previews`.
