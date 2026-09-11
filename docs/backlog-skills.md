# Ejecutar una sola vez (ideal para cron)
python blog-scraper.py --once

# Ejecutar en modo "vigilancia": revisa cada 15 minutos
python blog-scraper.py --interval 15


Ejecutar en local
> python -m http.server 8000

----

Estoy organizando un breve plan para proponer y priorizar las habilidades del proyecto.
Inventario de habilidades: Lista de 15 tipos de habilidades útiles para este proyecto (corpus de reflexiones).

[] Ingesta y Normalización: importa Markdown/HTML desde articulos_completos, limpia metadatos y unifica formato.
[x] Extracción de Metadatos: detecta título, fecha, URL original, imagen y audio; valida frontmatter.
[] Resolución de Referencias Bíblicas: detecta citas (p.ej. “Juan 3:16”), normaliza forma y enlaza pasajes (o consulta API bíblica).
[] Clasificación Temática / Etiquetado: asigna temas (fe, restauración, liderazgo) usando modelos ligeros o reglas.
[x] Generador de Resúmenes y Snippets: crea resumenes cortos, meta-descripciones y extractos para listings/SEO.
[x] Enlazado Cruzado: detecta relaciones entre reflexiones y sugiere links “Relacionado” automáticos.
[x] SEO y Metadatos Web: genera meta tags, OpenGraph y sugerencias de título/slug optimizados.
[] Procesamiento de Audio: indexa audios locales, extrae duraciones, genera transcripts (si procede).
[] Conversión y Exportación: transforma a HTML/AMP/PDF y empaqueta para publicación o migración.
[] Calidad y Linter de Contenido: aplica reglas del corpus (ver guía-de-interpretación-del-corpus.md) y marca inconsistencias.
[] Indexador y Búsqueda: crea índice invertido / vectores para búsqueda por texto y semántica.
[] Análisis y Métricas: recolecta estadísticas de palabras clave, temas y cambios a lo largo del tiempo.
[] Internacionalización / Traducción: pipeline para traducción automática y revisión humana.
[] CLI y Orquestador: comandos para ejecutar pipelines por lotes (ingesta → extracción → indexado → export).
[x] UI Helpers / Previews: API para generar previews en el sitio (reflexion.html) y componentes de lista.


¿Quieres que priorice estas SKILLS y genere los archivos de scaffold (esqueleto) para las 3 primeras?
