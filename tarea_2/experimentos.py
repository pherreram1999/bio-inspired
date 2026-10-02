"""Sintonización de parámetros: barrido de pc, pm y tamaño de población.

Cada configuración se ejecuta REPETICIONES veces (200 generaciones) y se
reporta la mediana, media, peor valor, desviación estándar y cuántas
ejecuciones llegaron al óptimo (f < UMBRAL).
"""
import itertools
import sys

import numpy as np
from printable import readable

from main import EPOCHS, ejecutar

REPETICIONES = 10
UMBRAL = 1e-3


def barrido(nombre, configuraciones):
    filas = []
    for pc, pm, pob in configuraciones:
        fs = np.array([ejecutar(pc, pm, pob)[1] for _ in range(REPETICIONES)])
        filas.append({
            "pc": pc, "pm": pm, "población": pob,
            "mejor": f"{fs.min():.2e}", "mediana": f"{np.median(fs):.2e}",
            "media": f"{fs.mean():.2e}", "peor": f"{fs.max():.2e}",
            "desv": f"{fs.std():.2e}",
            "óptimo": f"{int((fs < UMBRAL).sum())}/{REPETICIONES}",
        })
        print(f"  {nombre}: pc={pc} pm={pm} pob={pob} listo", file=sys.stderr)
    print(f"\n### {nombre}\n")
    print(readable(filas, grid="markdown"))


def main():
    print(f"Generaciones por ejecución: {EPOCHS}, repeticiones: {REPETICIONES}")
    barrido("Población (pc=0.7, pm=0.02)",
            [(.7, .02, p) for p in (10, 20, 50, 100, 512)])
    barrido("Tasa de cruzamiento (pm=0.02, población=50)",
            [(pc, .02, 50) for pc in (.1, .3, .5, .7, .9)])
    barrido("Tasa de mutación (pc=0.7, población=50)",
            [(.7, pm, 50) for pm in (0.0, .01, .02, .1, .3, .6)])
    barrido("Cruce pc x pm (población=20)",
            list(itertools.product((.3, .7, .9), (.02, .2), (20,))))


if __name__ == "__main__":
    main()
