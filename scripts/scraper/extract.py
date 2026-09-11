"""extract.py — Module Extract (deep module)
Interface: extraer_contenido_profundo(session, url_articulo, slug, carpeta_audios): (texto, audio|None)
"""
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urljoin
import logging
import re
import sys
try:
    from .peticiones import realizar_peticion
except ImportError:  # ejecución como script suelto
    _SCRAPER_DIR = Path(__file__).resolve().parent
    if str(_SCRAPER_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRAPER_DIR))
    from peticiones import realizar_peticion

log = logging.getLogger(__name__)

# Tags de bloque que delimitan párrafos reales en WordPress (.entry-content).
# Todo lo inline (em, strong, a, span...) se une con espacio, nunca con salto.
_BLOCK_TAGS = ("p", "h1", "h2", "h3", "h4", "li", "blockquote", "pre")

# Colas de WordPress que no son contenido (se filtran también en parser.mjs).
_TAIL_RE = re.compile(r"(Comparte esto:|Relacionado|Me gusta|Cargando\.\.\.)", re.IGNORECASE)


def _limpiar_fragmento(texto: str) -> str:
    t = re.sub(r"\s+", " ", texto).strip()
    # pega la puntuación que quedó separada por el join: "talit ," -> "talit,"
    t = re.sub(r"\s+([,.;:!?%)\]\u00bb\u201d'\"])", r"\1", t)
    t = re.sub(r"([¿¡«\u201c\"'(\[])\s+", r"\1", t)
    return t.strip()


def html_a_parrafos(contenedor) -> str:
    """Convierte .entry-content en texto con \n\n solo entre bloques reales."""
    bloques: List[str] = []
    # hijos de bloque directos; si no hay <p> (tema raro), fallback a bloques anidados
    candidatos = contenedor.find_all(_BLOCK_TAGS, recursive=False)
    if not candidatos:
        candidatos = contenedor.find_all(_BLOCK_TAGS)
    if not candidatos:
        # último recurso: texto plano con espacios (nunca \n por tag inline)
        t = _limpiar_fragmento(contenedor.get_text(separator=" ", strip=True))
        return t
    for b in candidatos:
        # ignora bloques de compartir/relacionados dentro del contenido
        clases = " ".join(b.get("class", []))
        if "sharedaddy" in clases or "related" in clases or ("wp-block" in clases and "share" in clases):
            continue
        t = _limpiar_fragmento(b.get_text(separator=" ", strip=True))
        if not t:
            continue
        # Labels sueltos de botones de compartir (tema WP): no son contenido
        if t in ("X", "Facebook"):
            continue
        if _TAIL_RE.search(t):
            break
        bloques.append(t)
    return "\n\n".join(bloques).strip()


def descargar_recurso(session, url: str, carpeta_destino: Path, nombre_base: str) -> Optional[str]:
    url = url.strip()
    if not url:
        return None
    ext = Path(url.split("?")[0]).suffix.lstrip(".") or "bin"
    ruta_destino = carpeta_destino / f"{nombre_base}.{ext}"
    if ruta_destino.exists():
        log.info("Ya existe %s, se reutiliza.", ruta_destino.name)
        return ruta_destino.name
    try:
        log.info("Descargando %s -> %s", url, ruta_destino)
        resp = session.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        with open(ruta_destino, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return ruta_destino.name
    except Exception as exc:
        log.error("Excepción al descargar %s: %s", url, exc)
    return None


def extraer_contenido_profundo(session, url_articulo: str, slug: str, carpeta_audios: Path) -> Tuple[str, Optional[str]]:
    soup = realizar_peticion(session, url_articulo)
    if not soup:
        return "Contenido no disponible.", None
    contenedor = soup.find("div", class_="entry-content")
    if not contenedor:
        return "Contenedor de texto no encontrado.", None
    audio_local = None
    tag_audio = contenedor.find("audio")
    if tag_audio:
        audio_src = tag_audio.get("src")
        if not audio_src:
            source = tag_audio.find("source", src=True)
            audio_src = source["src"] if source else None
        if audio_src:
            url_audio = urljoin(url_articulo, audio_src)
            ext = Path(url_audio.split("?")[0]).suffix.lstrip(".") or "bin"
            ruta = carpeta_audios / f"{slug}.{ext}"
            if ruta.exists():
                audio_local = ruta.name
            else:
                audio_local = descargar_recurso(session, url_audio, carpeta_audios, slug)
    texto = html_a_parrafos(contenedor)
    if not texto:
        texto = _limpiar_fragmento(contenedor.get_text(separator=" ", strip=True))
    return texto, audio_local
