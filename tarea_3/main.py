from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np

from dropwave import Dropwave
from geneticoReal import GeneticoReal
from graficador import graficar_convergencia_aptitud, animar_convergencia_poblacion
from langermann import Langermann






def ejecutar(fo, params):
    # generamos una poblacion uniforme
    N = params['N']
    Nc = params['Nc']
    Pc = params['Pc']
    Pm = params['Pm']
    Nm = params['Nm']
    Epochs = params['Epochs']

    b = GeneticoReal(fo, Epochs, N, Nc, Pc, Pm, Nm)
    best = b.run()

    animar_convergencia_poblacion(
        fo=fo,
        historial_poblaciones=b.get_historial_poblaciones(),
        historial_best=b.get_historial_best(),
        historial_best_apt=b.get_historial_best_apt(),
        guardar_como= fo.get_name() + "_.gif",
        fps=5,
        interval=220,
        niveles=12,
        max_puntos_poblacion=100,
        alpha_poblacion=0.50
    )

    # Gráfica de aptitud
    graficar_convergencia_aptitud(
        b.get_historial_best_apt(),
        guardar_como= f"apitutud_{fo.get_name()}.png"
    )

    print("Mejor resultado:", best)


def ejecutar_langermann():
    ejecutar(
        Langermann(),
        {
            'N': 512,
            'Nc': 2,
            'Pc': 0.7,
            'Pm': 0.02,
            'Nm': 20,
            'Epochs': 15,
        }
    )


def ejecutar_dropwave():
    ejecutar(
        Dropwave(),
        {
            'N': 512,
            'Nc': 2,
            'Pc': 0.7,
            'Pm': 0.02,
            'Nm': 20,
            'Epochs': 15,
        }
    )


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(ejecutar_langermann)
        f2 = executor.submit(ejecutar_dropwave)

        f1.result()
        f2.result()
    pass

if __name__ == "__main__":
    main()
