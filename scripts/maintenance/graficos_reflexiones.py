#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
CARPETA_GRAFICOS = BASE_DIR / "graficos"

MESES_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

# Cantidad real de reflexiones publicadas por mes en prwalterescalante.com.
# El scraper local no descargó todos los posts (julio quedó incompleto), por eso
# estos valores son la fuente de verdad para el gráfico.
REAL_POR_MES = OrderedDict(
    [
        ("2026-01", 32),
        ("2026-02", 29),
        ("2026-03", 31),
        ("2026-04", 30),
        ("2026-05", 31),
        ("2026-06", 26),
        ("2026-07", 28),
        ("2026-08", 8),
    ]
)


def leer_fechas() -> OrderedDict:
    return OrderedDict(REAL_POR_MES)


def generar_grafico(conteo: OrderedDict) -> None:
    CARPETA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    etiquetas = []
    for clave in conteo:
        anio, mes = clave.split("-")
        etiquetas.append(f"{MESES_ES[int(mes) - 1]} {anio}")

    valores = list(conteo.values())
    x = range(len(valores))

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(x, valores, color="#4C72B0", edgecolor="white")

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.5,
            str(valor),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_title("Reflexiones Publicadas por Mes", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mes", fontsize=10)
    ax.set_ylabel("Número de reflexiones", fontsize=10)
    ax.set_xticks(list(x))
    ax.set_xticklabels(etiquetas, rotation=35, ha="right", fontsize=10)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    fig.tight_layout()
    salida = CARPETA_GRAFICOS / "reflexiones_por_mes.png"
    fig.savefig(salida, dpi=150)
    plt.close(fig)
    log.info("Gráfico guardado: %s", salida)


def main() -> None:
    conteo = leer_fechas()
    log.info("Reflexiones por mes: %s", dict(conteo))
    generar_grafico(conteo)


if __name__ == "__main__":
    main()
