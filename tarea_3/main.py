import numpy as np

from geneticoReal import GeneticoReal
from graficador import animar_convergencia_estilo_curvas, graficar_convergencia_aptitud
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

    animar_convergencia_estilo_curvas(
        fo=fo,
        historial_best=b.get_historial_best(),
        historial_best_apt=b.get_historial_best_apt(),
        guardar_como="langermann_estilo.gif",
        fps=24,
        interval=250,
        mostrar_poblacion=False
    )

    # Gráfica de aptitud
    graficar_convergencia_aptitud(
        b.get_historial_best_apt(),
        guardar_como="convergencia_langermann.png"
    )

    print("Mejor resultado:", best)

if __name__ == "__main__":
    main()
