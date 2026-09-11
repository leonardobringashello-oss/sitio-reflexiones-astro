#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reflujo de contenido: une saltos de línea sin sentido (tags inline rotos).

Causa original: contenedor.get_text(separator="\n") partía cada <em>/<strong>/<a>
en una línea. Este script une esos fragmentos en content/articulos/*.md sin
fusionar párrafos reales (prev termina en .!?… + next empieza en mayúscula).

Uso: python scripts/maintenance/reflow_contenido.py [--check] [--write]
  --check: solo reporta, no escribe.  --write: aplica (default: --write).
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ART_DIR = BASE / "content" / "articulos"

TERMINAL = re.compile(r"[.!?…\u00bb\u201d\"'\)\]]\s*$")
NEXT_LOWER_OR_PUNCT = re.compile(r"^[a-záéíóúñü\d,\.;:!?%)\]\}\u00bb\u201d'\"\…\-\–]")
NEXT_UPPER = re.compile(r"^[A-ZÁÉÍÓÚÑ¿¡«\u201c\"'(\[]")
VERSE_CITE = re.compile(r"^\([^)]*\d+[:.]\d+[^)]*\)\.?$")
TAIL_RE = re.compile(r"^(Comparte esto:|Compartir en|Comparte en|Me gusta|Cargando\.\.\.|Relacionado)\s*", re.IGNORECASE)

# Labels sueltos de botones (X/Facebook/...) que quedan como últimos párrafos.
# Solo se eliminan al FINAL del documento, nunca en medio del texto.
JUNK_TAIL_RE = re.compile(
    r"^(X|Facebook|Me gusta.*|Cargando\.*|Compartir.*|Comparte.*|Relacionado.*|Seguir.*|Suscribir.*)$",
    re.IGNORECASE,
)


def limpiar_espacios(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.;:!?%)\]\u00bb\u201d'\"])", r"\1", t)
    t = re.sub(r"([¿¡«\u201c\"'(\[])\s+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def debe_unir(prev: str, nxt: str) -> bool:
    if not prev or not nxt:
        return False
    # Citas de versículo siempre párrafo propio
    if VERSE_CITE.match(nxt):
        return False
    if VERSE_CITE.match(prev):
        return True if NEXT_LOWER_OR_PUNCT.match(nxt) else False
    # Comilla/puntuación suelta (artefacto de split inline) -> pegar a prev
    if len(nxt) == 1 and nxt in "'\"«»“”‘’….,;:!?)]}":
        return True
    # Fragmento evidente: next empieza en minúscula o puntuación -> unir
    if NEXT_LOWER_OR_PUNCT.match(nxt):
        return True
    # Prev no terminó oración (sin .!?…) -> continuación -> unir
    if not TERMINAL.search(prev):
        return True
    # Prev terminó oración y next empieza en mayúscula -> párrafo nuevo
    return False


def reflow_segmentos(segmentos):
    paras = []
    buf = ""
    for seg in segmentos:
        seg = limpiar_espacios(seg)
        if not seg:
            continue
        if TAIL_RE.match(seg):
            break
        if not buf:
            buf = seg
            continue
        if debe_unir(buf, seg):
            # pega puntuación suelta sin espacio: "talit" + ", los" -> "talit, los"
            if re.match(r"^[,.;:!?%)\]\}\u00bb\u201d'\"]", seg):
                buf = limpiar_espacios(buf + seg)
            else:
                buf = limpiar_espacios(buf + " " + seg)
        else:
            paras.append(buf)
            buf = seg
    if buf:
        paras.append(buf)
    return paras


# Labels de botones de compartir que quedaron como línea suelta (X, Facebook).
# Un párrafo real jamás es solo "X" o "Facebook": se descartan en el cuerpo.
BUTTON_LABEL_RE = re.compile(r"^(X|Facebook)$")


def procesar_archivo(ruta: Path):
    raw = ruta.read_text(encoding="utf-8")
    # Separa encabezado / cuerpo (dos formatos: con o sin marcador "Contenido:")
    m = re.search(r"(?im)^Contenido:\s*$", raw)
    if m:
        head = raw[: m.end()]
        cuerpo_raw = raw[m.end():]
        con_marcador = True
    else:
        # Formato sin marcador: encabezado = hasta el segundo "---", resto es cuerpo
        sep = list(re.finditer(r"(?m)^---\s*$", raw))
        if len(sep) < 2:
            return None
        head = raw[: sep[1].end()]
        cuerpo_raw = raw[sep[1].end():]
        con_marcador = False
    # Corta cola legacy y separador final
    cuerpo_raw = re.split(r"(?m)^---\s*$", cuerpo_raw)[0]
    # Respeta párrafos ya correctos (\n\n) como grupos con break forzado
    grupos = re.split(r"\n\s*\n", cuerpo_raw)
    paras_out = []
    for g in grupos:
        segmentos = [l.strip() for l in g.splitlines()]
        # Descarta labels de botones sueltos antes de refluir (evita "X Facebook")
        segmentos = [s for s in segmentos if s and not BUTTON_LABEL_RE.match(s)]
        if not segmentos:
            continue
        paras_out.extend(reflow_segmentos(segmentos))
    # Limpia colas de compartir al final del documento (nunca en medio del texto)
    while paras_out and JUNK_TAIL_RE.match(paras_out[-1]):
        paras_out.pop()
    # Reconstruye cuerpo con \n\n entre párrafos reales
    cuerpo_nuevo = "\n\n".join(paras_out).strip() + "\n"
    # Mantiene encabezado tal cual (normaliza fin) + cuerpo + separador
    head = head.rstrip() + "\n\n"
    if con_marcador:
        nuevo = head + cuerpo_nuevo + "\n---\n"
    else:
        nuevo = head + cuerpo_nuevo
    return nuevo


def main():
    check = "--check" in sys.argv
    archivos = sorted(ART_DIR.glob("*.md"))
    if not archivos:
        print(f"No hay .md en {ART_DIR}")
        sys.exit(1)
    cambiados = 0
    total_paras_antes = 0
    total_paras_despues = 0
    for ruta in archivos:
        nuevo = procesar_archivo(ruta)
        if nuevo is None:
            print(f"SKIP (sin Contenido:): {ruta.name}")
            continue
        viejo = ruta.read_text(encoding="utf-8")
        if nuevo != viejo:
            cambiados += 1
            if not check:
                ruta.write_text(nuevo, encoding="utf-8")
        # stats
        total_paras_antes += len([l for l in viejo.splitlines() if l.strip()])
        total_paras_despues += nuevo.count("\n\n")
    print(f"Archivos: {len(archivos)}, cambiados: {cambiados}{' (check, sin escribir)' if check else ''}")
    print(f"Lineas no vacias antes: {total_paras_antes}, breaks \n\n despues: {total_paras_despues}")


if __name__ == "__main__":
    main()
