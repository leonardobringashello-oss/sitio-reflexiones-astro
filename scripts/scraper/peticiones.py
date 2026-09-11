"""http.py — Module Http (deep module, internal seam del scraper)
Interface: realizar_peticion(session, url): BeautifulSoup|None
Esconde reintentos, headers y logging. Testeable con adapter FakeSession.
"""
import time
import logging
from typing import Optional

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def realizar_peticion(session, url: str, retries: int = 3, timeout: int = 15) -> Optional[BeautifulSoup]:
    for intento in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "html.parser")
            log.warning("Petición %s devolvió %s (intento %s/%s)", url, resp.status_code, intento, retries)
        except Exception as exc:
            log.warning("Error al conectar con %s (intento %s/%s): %s", url, intento, retries, exc)
        time.sleep(2)
    log.error("No se pudo obtener %s tras %s intentos.", url, retries)
    return None
