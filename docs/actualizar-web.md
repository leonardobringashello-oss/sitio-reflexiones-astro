# Cómo actualizar la web (nuestro sitio Astro) desde la web del pastor

> Aclaración clave: hay DOS webs distintas.
> - **Web del pastor (origen, WordPress):** https://prwalterescalante.com/ — ahí publica él. Nosotros NO publicamos ahí.
> - **Nuestra web (destino, Astro estático):** este repo (`sitio-reflexiones-astro`) — biblioteca navegable generada desde `content/`.
> "Actualizar la web" = traer lo nuevo del pastor → regenerar → pushear a `main` → el hosting redespliega `dist/`.

Fuente de verdad: `content/articulos/*.md` (+ `content/imagenes/`, `content/audios/`).
Derivados (NO se commitean, se regeneran): `public/data/*.json`, `public/imagenes/`, `public/audios/`, `dist/`.

## Proceso paso a paso (el que se siguió el 13/09/2026)

### 1. Verificar qué hay de nuevo en el origen

Abrir la portada https://prwalterescalante.com/ y mirar los últimos posts.
El 13/09/2026 el último era `Des-graciados` (`/2026/09/13/3661/`), seguido de `Coronas` (12/09) y `Conspiranoicos` (11/09).

Comparar con local:

```bash
# ver slugs locales que contienen X
ls content/articulos/ | grep -i "3661\|coronas\|3649"
```

Resultado del 13/09: los 3 ya existían en local (`3661.md`, `coronas.md`, `3649.md`), más `inconmensurable.md`, `adaptarnos-sin-amoldarnos.md`, `arrogantes.md`. Local al día.

### 2. Correr el scraper (una pasada)

```bash
python scripts/scraper/scraper.py --once
```

- Usa headers Chrome, delay 5s entre descargas, deduplica por slug (no re-descarga lo existente).
- Si se corre dentro de la carpeta del proyecto, reutiliza la ruta actual (warning esperado, evita carpetas anidadas).
- Salida esperada cuando no hay nada nuevo: `No se encontraron más posts del año 2026 en la página actual.`
- Si HAY posts nuevos, crea `content/articulos/<slug>.md` + imagen en `content/imagenes/` (+ audio si existe). Esos archivos SÍ se commitean.

Resultado del 13/09: 0 nuevos (los del 12 y 13/09 ya estaban como untracked en git, ver paso 5).

### 3. Regenerar datos derivados

```bash
npm run build:data     # node scripts/builder/build-data.mjs → public/data/reflexiones.json + copia imagenes/audios a public/
npm run linking:build  # node scripts/linking/build.mjs → public/data/relaciones.json
```

Resultado del 13/09: `reflexiones.json (1160.1 KB)`, 243 imágenes, `relaciones.json (242 slugs, umbral 3)`.

### 4. Build completo del sitio

```bash
npm run build   # = build:data + astro build → dist/
```

Resultado del 13/09: `244 page(s) built` (242 reflexiones + index + resto), `sitemap-index.xml` creado.

### 5. Verificar que lo nuevo quedó en `dist/`

```bash
ls dist/reflexion/ | grep -i "3661\|coronas"   # deben existir las carpetas
grep -c "<item>" dist/rss.xml                   # debe ser 242
```

Chequeo rápido en Node (o abrir `http://localhost:4321` con `npm run dev` / `npm run preview` y buscar el título).

Resultado del 13/09: `dist/reflexion/3661`, `coronas` y `3649` OK; `rss.xml` con 242 `<item>` incluyendo ambos.

### 6. Calidad mínima antes de publicar

```bash
npm test          # vitest: parser, taxonomy, search
npm run seo:check # 0 errores esperado; aviso "SITE no definido" es normal en local
```

Resultado del 13/09: 7/7 tests OK; SEO `242 items, 0 errores, 1 aviso` (SITE relativo, solo afecta prod si no se define la env).

### 7. Publicar (actualizar la web real)

```bash
git status --short
git add content/articulos/3661.md content/articulos/coronas.md content/imagenes/3661.png content/imagenes/coronas.png docs/actualizar-web.md
git commit -m "feat: nuevas reflexiones 12-13/09/2026 (coronas, des-graciados) + docs actualización"
git push origin main
```

- Solo se commitea `content/` (+ docs/código). `public/data`, `public/imagenes`, `public/audios` y `dist/` están en `.gitignore` a propósito.
- El hosting (Netlify / Vercel / Cloudflare Pages) debe estar configurado con **Build command:** `npm run build`, **Publish directory:** `dist`, **Env:** `SITE=https://tudominio.com` + `NODE_VERSION=18`. Al pushear a `main`, el CI hace `npm ci` → regenera derivados → publica `dist/`.
- Si el hosting es estático puro por FTP (sin build), generar local y subir `dist/` a mano (ver README §5).

### 8. Confirmar en producción

1. Esperar el deploy en el dashboard del hosting.
2. Abrir `https://tudominio.com/reflexion/3661` y `/reflexion/coronas`.
3. Revisar home: buscador + filtro por mes `2026-09` con contador actualizado.

## Comandos de referencia (tabla)

| Quiero... | Comando |
|---|---|
| Traer novedades (1 pasada) | `python scripts/scraper/scraper.py --once` |
| Vigilar cada 15 min (local/cron) | `python scripts/scraper/scraper.py --interval 15` |
| Solo regenerar JSON | `npm run build:data` |
| Solo enlazado cruzado | `npm run linking:build` |
| Build completo | `npm run build` |
| Ver local | `npm run dev` → http://localhost:4321 |
| Ver `dist/` | `npm run preview` |
| Tests + SEO | `npm test && npm run seo:check` |

## Errores típicos

- `Se detectó que el script se ejecuta dentro de la carpeta de destino` → warning normal, sigue.
- `No se encontraron más posts del año 2026` → no hay nada nuevo, nada que commitear.
- `env SITE no definido` en `seo:check` → normal en local; en hosting definir `SITE` real.
- Nunca editar `public/data/*.json` a mano: se sobrescribe en cada `build:data`. Editar siempre `content/articulos/*.md` (formato en README §6: `Titulo / Fecha DD/MM/YYYY / URL ORIGEN / Imagen / Audio Local` + `Contenido:`).
