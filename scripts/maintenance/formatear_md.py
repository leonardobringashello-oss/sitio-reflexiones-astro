#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

CARPETA_ARTICULOS = Path("reflexiones_escalante_2026/articulos_completos")

SEPARADOR_ENCABEZADO = "-" * 3
SEPARADOR_CONTENIDO = "-" * 3

ETIQUETAS = {
    "titulo": re.compile(r"^(?:TÍTULO:\s*|Titulo:\s*|#\s*)(.+)$"),
    "fecha": re.compile(r"^(?:FECHA:\s*|\*\*Fecha:\*\*\s*|- Fecha:\s*)(.+)$"),
    "url": re.compile(r"^(?:URL ORIGEN:\s*|\*\*URL de origen:\*\*\s*|- URL ORIGEN:\s*)(.+)$"),
    "imagen": re.compile(
        r"^(?:IMAGEN DESTACADA LOCAL:\s*|\*\*Imagen destacada local:\*\*\s*|- Imagen:\s*)(.+)$"
    ),
    "audio": re.compile(r"^(?:AUDIO LOCAL:\s*|\*\*Audio local:\*\*\s*|- Audio Local:\s*)(.+)$"),
}

SEPARADOR_CONTENIDO_REGEX = re.compile(r"^(?:CONTENIDO:|Contenido:)\s*$", re.IGNORECASE)


def ya_formateado(texto: str) -> bool:
    return texto.startswith(SEPARADOR_ENCABEZADO) and "- Titulo:" in texto


def extraer_metadatos(texto: str) -> dict:
    datos = {"titulo": "", "fecha": "", "url": "", "imagen": "", "audio": ""}
    for linea in texto.splitlines():
        for campo, patron in ETIQUETAS.items():
            if datos[campo]:
                continue
            m = patron.match(linea.strip())
            if m:
                datos[campo] = m.group(1).strip()
    return datos


def extraer_contenido(texto: str) -> str:
    lineas = texto.splitlines()
    inicio = 0
    for i, linea in enumerate(lineas):
        if SEPARADOR_CONTENIDO_REGEX.match(linea.strip()):
            inicio = i + 1
            break
    return "\n".join(lineas[inicio:]).strip()


def formatear_archivo(ruta: Path) -> bool:
    texto = ruta.read_text(encoding="utf-8")
    if ya_formateado(texto):
        return False

    datos = extraer_metadatos(texto)
    contenido = extraer_contenido(texto)

    nuevo = (
        SEPARADOR_ENCABEZADO
        + "\n\n"
        + f"- Titulo: {datos['titulo']}\n"
        + f"- Fecha: {datos['fecha']}\n"
        + f"- URL ORIGEN: {datos['url']}\n"
        + f"- Imagen: {datos['imagen'] or 'Ninguna'}\n"
        + f"- Audio Local: {datos['audio'] or 'Ninguno'}\n"
        + "\n"
        + SEPARADOR_CONTENIDO
        + "\n\n"
        + "Contenido:\n\n"
        + contenido
        + "\n\n"
        + SEPARADOR_ENCABEZADO
        + "\n"
    )

    ruta.write_text(nuevo, encoding="utf-8")
    return True


def main() -> None:
    if not CARPETA_ARTICULOS.exists():
        log.error("No existe la carpeta %s", CARPETA_ARTICULOS)
        sys.exit(1)

    archivos = sorted(CARPETA_ARTICULOS.glob("*.md"))
    formateados = 0
    omitidos = 0

    for ruta in archivos:
        if formatear_archivo(ruta):
            formateados += 1
            log.info("Formateado: %s", ruta.name)
        else:
            omitidos += 1

    log.info("Listo: %s formateados, %s ya estaban en el formato nuevo.", formateados, omitidos)


if __name__ == "__main__":
    main()
