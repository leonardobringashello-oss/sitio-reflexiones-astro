# Maintenance — scripts legacy archivados

> Fase 1: estos archivos estaban en raíz y se movieron aquí sin modificar para preservar compatibilidad.
> No usar en pipeline nuevo. El pipeline canónico es `scripts/scraper/scraper.py` + `scripts/builder/build-data.mjs`.

| Archivo | Origen | Propósito original | Estado |
|---|---|---|---|
| `fix_json.py` | `fix_json.py:1` | Verifica terminadores de párrafos en `data/reflexiones.json` | Archivado |
| `fix_json2.py` | `fix_json2.py:1` | Debug `quien-sos-2` párrafos | Archivado |
| `fix_reflexiones.py` | `fix_reflexiones.py:1` | Parche reflexiones | Archivado |
| `formatear_md.py` | `formatear_md.py:1` | Formatear MDs `articulos_completos/` | Archivado |
| `graficos_reflexiones.py` | `graficos_reflexiones.py:1` | Genera `graficos/` | Archivado |

Si necesitás recuperar lógica, importar desde aquí hacia `scripts/builder/parser.mjs` o `scripts/linking/` con interfaz profunda.
