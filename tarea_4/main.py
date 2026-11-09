from geneticoReal import GeneticoReal
from graficador import animar_resultado, graficar_resultado
from ObjetiveFunction import ObjetiveFunction
from Restrictions import G1, G2


def ejecutar(fo, restricciones, params, mostrar=True):
    ag = GeneticoReal(
        fo,
        params["Epochs"],
        params["N"],
        params["Nc"],
        params["Pc"],
        params["Pm"],
        params["Nm"],
        params["Cp"],
        restricciones,
    )
    best = ag.run()

    graficar_resultado(
        fo,
        restricciones,
        ag.get_historial_poblaciones(),
        ag.get_historial_best(),
        ag.get_historial_best_apt(),
        guardar_como=f"resultado_cp{params['Cp']}.png",
        mostrar=False,
    )

    animar_resultado(
        fo,
        restricciones,
        ag.get_historial_poblaciones(),
        ag.get_historial_best(),
        ag.get_historial_best_apt(),
        guardar_como=f"animacion_cp{params['Cp']}.gif",
        mostrar=mostrar,
        paso=2,
    )

    violacion = sum(max(r(*best), 0.0) for r in restricciones)
    print(f"Cp = {params['Cp']}")
    print(f"  Mejor: x = {best[0]:.5f}, y = {best[1]:.5f}")
    print(f"  f(x, y) = {fo(*best):.6f}")
    print(f"  Violación total = {violacion:.3e}")
    for r in restricciones:
        print(f"  {r.get_name()}: {r(*best):+.5f}")
    return best


def main():
    fo = ObjetiveFunction()
    restricciones = [G1(), G2()]

    params = {
        "N": 100,       # tamaño de población (par)
        "Nc": 20,       # índice de distribución del cruzamiento
        "Pc": 0.9,      # prob. de cruzamiento
        "Pm": 0.1,      # prob. de mutación por variable
        "Nm": 20,       # índice de distribución de la mutación
        "Epochs": 100,  # generaciones
        "Cp": 200,      # coeficiente de penalización
    }

    ejecutar(fo, restricciones, params)
    print("Óptimo teórico aproximado: x = 0.4, y = 1.2, f = %.4f" % fo(0.4, 1.2))


if __name__ == "__main__":
    main()
