# Migración por fases — estado

## Fase 1 ✓ completada — Orden y dual-path

- Carpetas creadas: `content/`, `public/`, `scripts/{scraper,builder,seo,linking,maintenance}`, `src/js/modules`, `sites/iglesia`, `docs/`
- Contenido canónico: `content/articulos/` (229), `content/imagenes/` (231), `content/audios/` (1) — espejo en `articulos_completos/` legacy
- Site: `public/index.html`, `public/reflexion.html`, `public/css/`, `public/js/`, `public/data/reflexiones.json` + espejo raíz (`index.html` etc. se mantienen)
- Pipelines: `blog-scraper.py` → `scripts/scraper/scraper.py` (dual-path content/), `build-data.js` → `scripts/builder/build-data.mjs` (dual-path)
- Legacy archivado: `scripts/maintenance/{fix_json*,formatear_md,graficos_reflexiones}.py`
- `package.json` + `pyproject.toml` + `README.md` + `docs/architecture.md` + `docs/guia-de-interpretacion-del-corpus.md`
- Build verificado: `node scripts/builder/build-data.mjs` escribe `public/data/` + `data/` (1127 KB, 229 items)

## Fase 2 ✓ completada — Profundizar (deep modules)

- `scripts/builder/taxonomy.mjs` — `MESES` + `categoriaPorFecha()` (interface pequeña)
- `scripts/builder/verses.mjs` — `extractVerses()` + `normalizeVerseBookChapter()` (return results)
- `scripts/builder/parser.mjs` — `parseMd(filePath, {fs})` (accept dependencies)
- `scripts/builder/build-data.mjs` refactorizado a orquestador delgado (imports taxonomy/parser)
- `src/js/modules/filtering.js` + `public/js/modules/filtering.js` + `grouping.js` — `filteredItems()` testeable sin DOM
- `js/app.js:63` delegado a `filterItems()` (deep module), `public/js/app.js` actualizado a `./modules/filtering.js`
- `scripts/scraper/http.py` + `extract.py` — internal seams del scraper
- `scripts/seo/check.mjs` y `scripts/linking/build.mjs` (stub Fase 2, scoring real en Fase 3)

Verificación: `node scripts/seo/check.mjs` (0 warnings), `node scripts/linking/build.mjs` (umbral 3, 229 slugs)

## Fase 3 ⏳ higiene — próxima

- `.gitignore` creado (node_modules, __pycache__, .env)
- Pendiente (no bloqueante):
  - [ ] Decidir si `public/data/*.json` se ignora y se regenera en CI (hoy versionado para compatibilidad)
  - [ ] `sites/iglesia/` → repo propio o `git submodule` (hoy espejo Fase 1, no acoplado al build)
  - [ ] Pre-commit (`setup-pre-commit` skill: Husky + Prettier para `js/` + Ruff/Black para `scripts/scraper/`)
  - [ ] Eliminar espejos raíz (`articulos_completos/`, `data/`, `css/`, `js/` raíz) cuando deploy apunte a `public/` (Netlify `publish: public`)
  - [ ] Implementar scoring real en `scripts/linking/build.mjs` (`enlazado-cruzado/SKILL.md:52`)
  - [ ] `npm run dev` como default, deprecate `dev:root`

## Cómo usar ahora

```bash
npm run build        # vs npm run build:legacy
npm run dev          # sirve public/ :8000
npm run dev:root     # sirve raíz (compat)
npm run seo:check
npm run linking:build -- --umbral 3
python scripts/scraper/scraper.py --once
```

No se rompió compatibilidad: todo lo viejo sigue funcionando en raíz.
