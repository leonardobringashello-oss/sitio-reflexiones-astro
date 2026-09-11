# Arquitectura — Biblioteca de Reflexiones

> Lenguaje: `codebase-design` (Module / Interface / Seam / Adapter / Depth / Leverage / Locality).

## Objetivo

Hacer el proyecto **profundo**: mucho comportamiento detrás de interfaces pequeñas, en seams bien puestos, testeable por la interfaz.

## Mapa de módulos

| Módulo | Interfaz (qué debe saber el caller) | Seam | Depth / Leverage | Implementación actual |
|---|---|---|---|---|
| **ContentParser** | `parseFile(path): Item` | `scripts/builder/parser.mjs` | Esconde frontmatter roto `build-data.js:41-45`, normaliza título/fecha/imagen | `build-data.js:38-118` |
| **Taxonomy** | `categoriaPorFecha(fechaISO): CategoryId` | `scripts/builder/taxonomy.mjs` | Tabla `MESES` centralizada, 1 lugar para agregar 2026-09 | `build-data.js:14-36` |
| **Verses** | `extractVerses(contenido): string[]` | `scripts/builder/verses.mjs` | Regex `build-data.js:89` + normalización `Job 23:3` | `build-data.js:88-94` |
| **DataBuilder** | `build(items): {total,categories,items}` | `scripts/builder/build-data.mjs` | Ordena `build-data.js:125`, stats `build-data.js:128` | `build-data.js:121-142` |
| **Scraper/Http** | `realizar_peticion(url): Soup` | `scripts/scraper/http.py` | Reintentos `blog-scraper.py:107`, headers, rate-limit | `blog-scraper.py:107-138` |
| **Scraper/Extract** | `extraer_contenido_profundo(url,slug): (texto,audio)` | `scripts/scraper/extract.py` | Contenedor `entry-content` + `audio` fallback | `blog-scraper.py:195-227` |
| **Filtering** | `filteredItems(items,{category,query}): Item[]` | `src/js/modules/filtering.js` | Reutilizable sin DOM, mismo que `js/app.js:63-78` | `js/app.js:63` |
| **UI Helpers** | `renderCard/renderFeatured/renderSidebarItem` | `js/ui-helpers.js:49-110` | Ya es deep module (escaping+fallback+line-clamp) | `js/ui-helpers.js:1` |
| **SEO** | `seoFor(item\|index): HeadTags` | `scripts/seo/` | Title 50-60ch, description 140-160ch | `generador-seo-og/SKILL.md` |
| **Linking** | `relatedFor(slug): Related[]` | `scripts/linking/` + `public/data/relaciones.json` | Scoring `enlazado-cruzado/SKILL.md:52` | — |

## Seams externos vs internos

- **Externo**: `content/articulos/*.md` ↔ `public/data/reflexiones.json` (filesystem). Adapters: `FsAdapter` (real) vs `MemoryAdapter` (tests).
- **Interno** (no exponer): `parser` usa `verses` y `taxonomy` como detalles privados. Tests cruzan el seam externo (`build()`), no los internos.

## Reglas de profundidad

- **Accept dependencies, don't create them.** `parseFile(path, {fs})` no `new Fs()` adentro.
- **Return results, don't produce side effects.** `extractVerses(text): string[]` no muta `item`.
- **Small surface area.** 1 función por módulo; `build-data.mjs` orquesta 3 módulos, no 10 params.
- **Deletion test.** Si borrás `Taxonomy`, ¿dónde reaparece la lógica? En N callers → merece módulo. Si solo pasa-through → no.

## Estructura de carpetas ↔ seams

```
content/        # seam: fuente de verdad (inputs)
public/         # seam: derivado servido (outputs) — deploy Netlify/Vercel apunta aquí
scripts/        # seam: pipelines (scraper/builder) — CLI
src/js/modules/ # seam: lógica frontend testeable sin DOM
```

Legacy en raíz (`articulos_completos/`, `data/`, `css/`, `js/`) se mantiene como **Adapter de compatibilidad** en Fase 1 (dual-path). Se elimina en Fase 3.

## Decisiones

- **Dual-path Fase 1**: `scripts/builder/build-data.mjs` lee `content/articulos/` y `articulos_completos/` (fallback) y escribe a `public/data/` + `data/` para no romper `npm run dev:root`.
- **public/imagenes,audios**: copiados (no symlink en Windows) por builder; `imagenPath` sigue siendo `imagenes/{file}` relativo a `public/`.
- **sites/iglesia**: extraído de `iglesia_restauracion_pagina/` (proyecto distinto). Fase 1: copia espejo; Fase 3: repo propio o `git submodule`.

## Contratos a respetar

- Frontmatter: `---` + `- Titulo / - Fecha / - URL ORIGEN / - Imagen / - Audio Local` (`extraccion-metadatos`).
- `data/reflexiones.json:items[].categoria` ∈ `2026-01..2026-09` (`taxonomy.mjs`).
- `ui-helpers.js` es única fuente de `escapeHtml` + fallback imagen (`ui-helpers-previews` skill).

## Próximos pasos (Fase 2)

1. Extraer `parser.mjs`/`verses.mjs`/`taxonomy.mjs` desde `build-data.js:14-118`.
2. Extraer `filtering.js` desde `js/app.js:63-78` + tests.
3. `scripts/linking/build.mjs` genera `public/data/relaciones.json` sin mutar `reflexiones.json`.
