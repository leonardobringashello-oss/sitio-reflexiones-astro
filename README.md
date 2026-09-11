# Biblioteca de Reflexiones — Pr. Walter Escalante (2026)

Sitio estático que publica 239 reflexiones pastorales (enero–septiembre 2026) como biblioteca navegable por mes, con búsqueda, cards y lector individual con audio.

> Fuente canónica de contenido: `content/articulos/*.md` + `content/imagenes/` + `content/audios/` → derivado `public/data/reflexiones.json` (+ copia de activos a `public/imagenes/` y `public/audios/`).

---

## Estructura

```
.
├── content/               # fuente de verdad (versionado)
│   ├── articulos/         # 239 .md con frontmatter "- Titulo/Fecha/URL..."
│   ├── imagenes/
│   └── audios/
├── src/                   # sitio Astro
│   ├── pages/             # index.astro + reflexion/[slug].astro (240 páginas)
│   ├── components/        # Card, Featured
│   ├── layouts/           # Base (SEO/OG + ViewTransitions)
│   ├── lib/               # items.js (loader vía scripts/builder), seo.js
│   ├── styles/global.css
│   └── js/modules/        # filtering.js, grouping.js (deep modules, sin DOM)
├── public/                # estáticos copiados a dist/ tal cual
│   ├── reflexion.html     # redirect legacy ?slug=X → /reflexion/X
│   ├── _redirects
│   ├── data/              # generado por scripts/builder (ignorado en git)
│   ├── imagenes/          # copiados desde content/imagenes (build, ignorado)
│   └── audios/
├── dist/                  # salida `npm run build` (deploy, ignorado en git)
├── scripts/
│   ├── scraper/           # ingesta desde prwalterescalante.com
│   ├── builder/           # parser/taxonomy/verses + build-data.mjs
│   ├── seo/               # check SEO/OG
│   ├── linking/           # enlazado cruzado → relaciones.json
│   └── maintenance/       # parches legacy archivados
├── docs/architecture.md   # seams, interfaces y depth
└── package.json / pyproject.toml
```

---

## Requisitos

- Node 18+ (ESM)
- Python 3.10+ (`pip install -r requirements.txt` o `pip install -e .`)

---

## Uso

```bash
# 1) Instalar
pip install requests beautifulsoup4
# o: pip install -e ".[dev]"

# 2) Scraper — una pasada (ideal cron)
python scripts/scraper/scraper.py --once

# 3) Build Astro — 240 páginas (index + 239 /reflexion/[slug]) a dist/
npm install
npm run build                     # build-data (JSON + assets a public/) + astro build → dist/
npm run build:data                # solo JSON public/data/reflexiones.json (para seo:check)

# 4) Dev server
npm run dev                       # astro dev
npm run preview                   # astro preview de dist/
```

---

## Pipeline

`scripts/scraper/scraper.py` (`ejecutar_scraper`) → `content/articulos/*.md` → `src/lib/items.js` (`parseMd` + `categoriaPorFecha` + `versículos` de `scripts/builder/`) → `src/pages/index.astro` + `src/pages/reflexion/[slug].astro` → `dist/`.

Skills disponibles (ver `.agents/skills/`): `extraccion-metadatos`, `generador-resumenes-snippets`, `enlazado-cruzado`, `generador-seo-og`, `ui-helpers-previews`.

---

## Convenciones

- Frontmatter: bloque `---` con `- Titulo / - Fecha (DD/MM/YYYY) / - URL ORIGEN / - Imagen / - Audio Local` (`extraccion-metadatos/SKILL.md`).
- Taxonomía por mes: `2026-01` … `2026-09` (`scripts/builder/taxonomy.mjs`).
- SEO: `og:image` fallback `imagenes/logos/logo-we.webp` (`generador-seo-og/SKILL.md`).

---

## Roadmap fases

- **Fase 1** (esta): ordenar carpetas, dual-path build, archivar legacy.
- **Fase 2**: profundizar módulos (`parser.mjs`, `verses.mjs`, `taxonomy.mjs`, `filtering.js`).
- **Fase 3**: higiene (`.gitignore` `public/data`, pre-commit, extraer `sites/iglesia` a repo propio).
