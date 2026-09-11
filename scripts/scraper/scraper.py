#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import re
import sys
import time
from datetime import datetime, time as time_class
from pathlib import Path

from typing import Optional, Set, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# Bootstrap para permitir ejecución como script suelto:
# `python scripts/scraper/scraper.py` no tiene parent package,
# así que los imports relativos (from .extract) fallan.
# Añadimos el directorio del scraper al sys.path para que
# el fallback `from extract import ...` funcione.
_SCRAPER_DIR = Path(__file__).resolve().parent
if str(_SCRAPER_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRAPER_DIR))


# CONFIGURACIÓN GENERAL
DEFAULT_URL_PORTADA = "https://prwalterescalante.com/"
DEFAULT_YEAR_FILTER = "/2026/"
DEFAULT_DELAY_SEGUNDOS = 5
DEFAULT_INTERVALO_REVISION = 10

DEFAULT_INTERVALO_FUERA = 60
DEFAULT_ACTIVE_START = 10
DEFAULT_ACTIVE_END = 17
# Importante: esta carpeta no debe crearse dentro de sí misma.
# Si el script se ejecuta desde dentro de la misma carpeta de salida,
# se reutiliza el directorio actual para evitar anidación duplicada.
DEFAULT_OUTPUT_DIR = Path("reflexiones_escalante_2026")


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


# UTILIDADES COMUNES
def safe_slug(text: str) -> str:
    """Devuelve un nombre de archivo libre de caracteres prohibidos en Windows."""
    text = re.sub(r"[^\w\-\.]", "_", text)
    return text[:120]


def cargar_posts_descargados(articulos_dir: Path) -> Set[str]:
    """Lee los archivos existentes en la carpeta de artículos y devuelve sus slugs."""
    if not articulos_dir.exists():
        return set()
    slugs_txt = {path.stem for path in articulos_dir.glob("*.txt") if path.is_file()}
    slugs_md = {path.stem for path in articulos_dir.glob("*.md") if path.is_file()}
    return slugs_txt | slugs_md


def resolver_ruta_salida(output_dir: Path) -> Path:
    """Normaliza la ruta de salida para no crear carpetas anidadas."""
    if output_dir.is_absolute():
        return output_dir

    cwd = Path.cwd()
    target_relative = cwd / output_dir

    # Reutilizamos la carpeta actual solo si coincide con la raíz del proyecto del scraper real: contiene el layout esperado (package.json + content/).
    project_markers = [cwd / "package.json", cwd / "content", cwd / "README.md"]
    if output_dir.name == cwd.name and any(marker.exists() for marker in project_markers):
        log.warning(
            "Se detectó que el script se ejecuta dentro de la carpeta de destino (%s). "
            "Se reutiliza la ruta actual para evitar carpetas duplicadas.",
            cwd,
        )
        return cwd

    return target_relative.resolve()


def crear_estructura_directorios(base_dir: Path) -> Tuple[Path, Path, Path]:
    """Crea las carpetas de salida necesarias y devuelve sus rutas."""
    # Fase 1: dual-path — canónico es content/, compatibilidad es raíz
    # Si base_dir es el project root (contiene content/), usa content/
    content_dir = base_dir / "content"
    if (base_dir / "content").exists() or (base_dir / "package.json").exists():
        articulos_dir = base_dir / "content" / "articulos"
        audios_dir = base_dir / "content" / "audios"
        imagenes_dir = base_dir / "content" / "imagenes"
        # espejo public/ (para deploy)
        for p in [base_dir / "public" / "imagenes", base_dir / "public" / "audios", base_dir / "public" / "data"]:
            p.mkdir(parents=True, exist_ok=True)
    else:
        articulos_dir = base_dir / "articulos_completos"
        audios_dir = base_dir / "audios"
        imagenes_dir = base_dir / "imagenes"

    for path in (articulos_dir, audios_dir, imagenes_dir):
        path.mkdir(parents=True, exist_ok=True)

    return articulos_dir, audios_dir, imagenes_dir


def esta_en_ventana_activa(start_hour: int, end_hour: int) -> bool:
    """Devuelve True si la hora actual está dentro de la ventana activa."""
    ahora = datetime.now().time()
    inicio = time_class(start_hour, 0)
    fin = time_class(end_hour, 0)
    return inicio <= ahora <= fin


# SOLICITUD HTTP
def realizar_peticion(
    session: requests.Session,
    url: str,
    retries: int = 3,
    timeout: int = 15,
) -> Optional[BeautifulSoup]:
    """GET con cabecera de navegador y reintentos. Devuelve BeautifulSoup o None."""
    for intento in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "html.parser")

            log.warning(
                "Petición %s devolvió %s (intento %s/%s)",
                url,
                resp.status_code,
                intento,
                retries,
            )
        except Exception as exc:
            log.warning(
                "Error al conectar con %s (intento %s/%s): %s",
                url,
                intento,
                retries,
                exc,
            )
        time.sleep(2)

    log.error("No se pudo obtener %s tras %s intentos.", url, retries)
    return None


# DESCARGAS DE RECURSOS
def descargar_recurso(
    session: requests.Session,
    url: str,
    carpeta_destino: Path,
    nombre_base: str,
) -> Optional[str]:
    """Descarga cualquier recurso binario y devuelve el nombre del archivo guardado."""
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


def descargar_imagen_post(
    session: requests.Session,
    url_imagen: str,
    carpeta_imagenes: Path,
    nombre_base: str,
) -> Optional[str]:
    return descargar_recurso(session, url_imagen, carpeta_imagenes, nombre_base)


def descargar_audio_post(
    session: requests.Session,
    url_audio: str,
    carpeta_audios: Path,
    nombre_base: str,
) -> Optional[str]:
    return descargar_recurso(session, url_audio, carpeta_audios, nombre_base)


# EXTRACCIÓN DE CONTENIDO DEL POST
def extraer_contenido_profundo(
    session: requests.Session,
    url_articulo: str,
    slug: str,
    carpeta_audios: Path,
) -> Tuple[str, Optional[str]]:
    """
    Descarga la página del artículo, extrae el texto y, si hay audio, lo descarga.
    Devuelve (texto, nombre_archivo_audio|None).
    Une tags inline con espacio y solo separa párrafos por bloques <p>/h/li.
    """
    log.debug("Extrayendo contenido profundo de %s", url_articulo)
    try:
        from .extract import html_a_parrafos, _limpiar_fragmento
    except ImportError:  # ejecución como script suelto: python scripts/scraper/scraper.py
        from extract import html_a_parrafos, _limpiar_fragmento
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
            audio_local = descargar_audio_post(session, url_audio, carpeta_audios, slug)

    texto = html_a_parrafos(contenedor)
    if not texto:
        texto = _limpiar_fragmento(contenedor.get_text(separator=" ", strip=True))
    return texto, audio_local


# SCRAPER PRINCIPAL
def ejecutar_scraper(
    url_portada: str,
    year_filter: str,
    delay: int,
    once: bool = False,
    intervalo_minutos: int = DEFAULT_INTERVALO_REVISION,
    outside_interval: int = DEFAULT_INTERVALO_FUERA,
    active_start: int = DEFAULT_ACTIVE_START,
    active_end: int = DEFAULT_ACTIVE_END,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> None:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    base_dir = resolver_ruta_salida(Path(output_dir))
    log.info("Directorio de salida: %s", base_dir)
    articulos_dir, audios_dir, imagenes_dir = crear_estructura_directorios(base_dir)

    posts_descargados = cargar_posts_descargados(articulos_dir)

    url_actual = url_portada

    while True:
        if not once and not esta_en_ventana_activa(active_start, active_end):
            log.info(
                "No está en la ventana activa (%s-%s).",
                active_start,
                active_end,
            )
            log.info("Esperando %s minutos antes de la siguiente revisión...", outside_interval)
            time.sleep(outside_interval * 60)
            continue

        log.info("Procesando página índice: %s", url_actual)
        soup_index = realizar_peticion(session, url_actual)
        if not soup_index:
            log.error("No se pudo leer la página de índice. Abortando.")
            break

        articulos = soup_index.find_all("article")
        if not articulos:
            log.info("No se encontraron <article> en la página actual.")
            break

        posts_en_pagina = 0
        for art in articulos:
            titulo_tag = art.find("h1", class_="entry-title")
            if not titulo_tag:
                continue

            link = titulo_tag.find("a", href=True)
            if not link:
                continue

            url_articulo = urljoin(url_actual, link["href"])
            if year_filter not in url_articulo:
                continue

            slug = safe_slug(Path(url_articulo.rstrip("/")).name or f"post_{int(time.time())}")
            ruta_md = articulos_dir / f"{slug}.md"

            if ruta_md.exists() or slug in posts_descargados:
                log.debug("Post %s ya descargado, se omite.", slug)
                continue

            posts_en_pagina += 1
            posts_descargados.add(slug)

            titulo = link.get_text(strip=True)
            fecha_tag = art.find("time", class_="entry-date")
            fecha = fecha_tag.get_text(strip=True) if fecha_tag else "Sin fecha"

            imagen_local = None
            figura = art.find("figure", class_="entry-thumbnail")
            if figura:
                img = figura.find("img", src=True)
                if img:
                    imagen_local = descargar_imagen_post(
                        session,
                        urljoin(url_actual, img["src"]),
                        imagenes_dir,
                        slug,
                    )

            log.debug("Esperando %s segundos antes de profundizar en el post.", delay)
            time.sleep(delay)

            contenido, audio_local = extraer_contenido_profundo(session, url_articulo, slug, audios_dir)

            with ruta_md.open("w", encoding="utf-8") as f:
                f.write("-" * 3 + "\n\n")
                f.write(f"- Titulo: {titulo}\n")
                f.write(f"- Fecha: {fecha}\n")
                f.write(f"- URL ORIGEN: {url_articulo}\n")
                f.write(f"- Imagen: {imagen_local or 'Ninguna'}\n")
                f.write(f"- Audio Local: {audio_local or 'Ninguno'}\n")
                f.write("\n")
                f.write("-" * 3 + "\n\n")
                f.write("Contenido:\n\n")
                f.write(f"{contenido}\n")
                f.write("\n")
                f.write("-" * 3 + "\n")

            log.info("Post guardado: %s", ruta_md)

        if posts_en_pagina == 0:
            log.info(
                "No se encontraron más posts del año %s en la página actual.",
                year_filter.strip("/"),
            )
            if once:
                break

        siguiente = soup_index.find("a", class_="next")
        if siguiente and siguiente.get("href"):
            url_actual = urljoin(url_actual, siguiente["href"])
        else:
            log.info("No se encontró enlace a página siguiente.")
            if once:
                break
            url_actual = url_portada

        if once:
            break

        log.info("Esperando %s minutos antes de la siguiente revisión...", intervalo_minutos)
        time.sleep(intervalo_minutos * 60)


# INTERFAZ DE LÍNEA DE COMANDOS
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scraper de entradas del blog de Escalante (año 2026) con detección automática de nuevos posts."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL_PORTADA,
        help="URL de la portada del blog (por defecto: %(default)s)",
    )
    parser.add_argument(
        "--year-filter",
        default=DEFAULT_YEAR_FILTER,
        help="Sub-ruta que identifica el año deseado (por defecto: %(default)s)",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=DEFAULT_DELAY_SEGUNDOS,
        help="Segundos de espera entre la descarga de la imagen y la extracción del contenido (por defecto: %(default)s)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ejecutar una sola pasada y terminar (útil para pruebas o cron).",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVALO_REVISION,
        help="Minutos entre revisiones cuando se está dentro de la ventana activa.",
    )
    parser.add_argument(
        "--outside-interval",
        type=int,
        default=DEFAULT_INTERVALO_FUERA,
        help="Minutos entre revisiones cuando se está fuera de la ventana activa.",
    )
    parser.add_argument(
        "--active-start",
        type=int,
        default=DEFAULT_ACTIVE_START,
        help="Hora de inicio de la ventana activa (0-23).",
    )
    parser.add_argument(
        "--active-end",
        type=int,
        default=DEFAULT_ACTIVE_END,
        help="Hora de fin de la ventana activa (0-23).",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directorio base de salida (por defecto: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ejecutar_scraper(
        url_portada=args.url,
        year_filter=args.year_filter,
        delay=args.delay,
        once=args.once,
        intervalo_minutos=args.interval,
        outside_interval=args.outside_interval,
        active_start=args.active_start,
        active_end=args.active_end,
        output_dir=Path(args.output_dir),
    )
