import numpy as np

from geneticoReal import GeneticoReal
from graficador import graficar_convergencia_aptitud, animar_convergencia_poblacion
from langermann import Langermann


N = 512 # poblacion
Nc = 2
Pc = 0.7
Pm = 0.02
Nm = 20
Epochs = 50

def main():

    # generamos una poblacion uniforme
    fo = Langermann()
    b = GeneticoReal(fo,Epochs,N,Nc,Pc, Pm, Nm)
    best = b.run()


    animar_convergencia_poblacion(
        fo=fo,
        historial_poblaciones=b.get_historial_poblaciones(),
        historial_best=b.get_historial_best(),
        historial_best_apt=b.get_historial_best_apt(),
        guardar_como="langermann_poblacion.gif",
        fps=5,
        interval=220,
        niveles=12,
        max_puntos_poblacion=100,
        alpha_poblacion=0.50
    )

    # Gráfica de aptitud
    graficar_convergencia_aptitud(
        b.get_historial_best_apt(),
        guardar_como="convergencia_langermann.png"
    )

    print("Mejor resultado:", best)

if __name__ == "__main__":
    main()
