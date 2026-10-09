import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


def animar_convergencia_poblacion(
    fo,
    historial_poblaciones,
    historial_best,
    historial_best_apt=None,
    guardar_como=None,
    fps=5,
    interval=220,
    dpi=140,
    resolucion=220,
    niveles=12,
    mostrar_etiquetas_contorno=False,
    max_puntos_poblacion=120,
    alpha_poblacion=0.18,
    tam_poblacion=14,
    color_poblacion="gray",
    color_trayectoria="blue",
    color_mejor="gold",
    borde_mejor="black"
):
    """
    Anima la convergencia de la población sobre curvas de nivel.

    Parámetros
    ----------
    fo : función objetivo de 2 variables
    historial_poblaciones : list[np.ndarray]
        Lista de poblaciones por generación. Cada elemento shape (N, 2)
    historial_best : list[np.ndarray]
        Lista del mejor individuo por generación. Cada elemento shape (2,)
    historial_best_apt : list[float], opcional
        Mejor aptitud por generación
    guardar_como : str, opcional
        Ejemplo: "langermann.gif" o "langermann.mp4"
    fps : int
    interval : int
        milisegundos entre cuadros
    dpi : int
    resolucion : int
        resolución de la malla
    niveles : int
        número de curvas de nivel
    mostrar_etiquetas_contorno : bool
    max_puntos_poblacion : int
        número máximo de puntos visibles de la población
    alpha_poblacion : float
        transparencia de la población
    tam_poblacion : int
        tamaño de puntos de población
    """

    li, ls = fo.get_limites()
    li = np.asarray(li, dtype=float)
    ls = np.asarray(ls, dtype=float)

    historial_best = np.asarray(historial_best, dtype=float)

    if historial_best.ndim != 2 or historial_best.shape[1] != 2:
        raise ValueError("historial_best debe tener forma (generaciones, 2)")

    if len(historial_poblaciones) != len(historial_best):
        raise ValueError("historial_poblaciones y historial_best deben tener la misma longitud")

    if historial_best_apt is None:
        historial_best_apt = [fo(*p) for p in historial_best]

    historial_best_apt = np.asarray(historial_best_apt, dtype=float)

    if len(historial_best_apt) != len(historial_best):
        raise ValueError("historial_best_apt y historial_best deben tener la misma longitud")

    # ----------------------------
    # Malla de curvas de nivel
    # ----------------------------
    x = np.linspace(li[0], ls[0], resolucion)
    y = np.linspace(li[1], ls[1], resolucion)
    X, Y = np.meshgrid(x, y)

    Z = np.empty_like(X, dtype=float)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = fo(X[i, j], Y[i, j])

    fig, ax = plt.subplots(figsize=(9, 7))

    cs = ax.contour(
        X, Y, Z,
        levels=niveles,
        colors="#ef5350",
        linewidths=0.9,
        alpha=0.70
    )

    if mostrar_etiquetas_contorno:
        ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")

    ax.set_xlim(li[0], ls[0])
    ax.set_ylim(li[1], ls[1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Convergencia del algoritmo genético")
    ax.set_aspect("equal", adjustable="box")

    # ----------------------------
    # Población (tenue)
    # ----------------------------
    pob0 = np.asarray(historial_poblaciones[0], dtype=float)

    idx0 = np.linspace(
        0, len(pob0) - 1,
        min(max_puntos_poblacion, len(pob0)),
        dtype=int
    )

    scatter_pob = ax.scatter(
        pob0[idx0, 0],
        pob0[idx0, 1],
        s=tam_poblacion,
        c=color_poblacion,
        alpha=alpha_poblacion,
        edgecolors="none",
        label="Población",
        zorder=2
    )

    # ----------------------------
    # Trayectoria del mejor
    # ----------------------------
    linea_best, = ax.plot(
        [], [],
        "-",
        color=color_trayectoria,
        linewidth=1.8,
        alpha=0.9,
        label="Trayectoria mejor",
        zorder=4
    )

    # ----------------------------
    # Mejor individuo actual (estrella)
    # ----------------------------
    mejor_star = ax.scatter(
        [], [],
        s=180,
        c=color_mejor,
        edgecolors=borde_mejor,
        marker="*",
        linewidths=1.0,
        label="Mejor individuo",
        zorder=5
    )

    # ----------------------------
    # Texto informativo
    # ----------------------------
    texto = ax.text(
        0.03, 0.97, "",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=11,
        bbox=dict(
            boxstyle="round",
            facecolor="white",
            edgecolor="gray",
            alpha=0.85
        )
    )

    ax.legend(loc="upper right", framealpha=0.9)

    def init():
        p = historial_best[0]

        scatter_pob.set_offsets(pob0[idx0])

        linea_best.set_data([p[0]], [p[1]])
        mejor_star.set_offsets(np.array([[p[0], p[1]]]))

        texto.set_text(
            f"Generación: 0\n"
            f"x = {p[0]:.5f}\n"
            f"y = {p[1]:.5f}\n"
            f"f(x,y) = {historial_best_apt[0]:.6f}"
        )

        return scatter_pob, linea_best, mejor_star, texto

    def update(frame):
        pob = np.asarray(historial_poblaciones[frame], dtype=float)
        p = historial_best[frame]
        tray = historial_best[:frame + 1]

        idx = np.linspace(
            0, len(pob) - 1,
            min(max_puntos_poblacion, len(pob)),
            dtype=int
        )

        # población actual
        scatter_pob.set_offsets(pob[idx])

        # trayectoria acumulada del mejor
        linea_best.set_data(tray[:, 0], tray[:, 1])

        # mejor actual
        mejor_star.set_offsets(np.array([[p[0], p[1]]]))

        # texto
        texto.set_text(
            f"Generación: {frame}\n"
            f"x = {p[0]:.5f}\n"
            f"y = {p[1]:.5f}\n"
            f"f(x,y) = {historial_best_apt[frame]:.6f}"
        )

        return scatter_pob, linea_best, mejor_star, texto

    anim = FuncAnimation(
        fig,
        update,
        frames=len(historial_best),
        init_func=init,
        interval=interval,
        blit=False,
        repeat=False
    )

    if guardar_como is not None:
        ext = guardar_como.lower().split(".")[-1]

        if ext == "gif":
            anim.save(guardar_como, writer=PillowWriter(fps=fps), dpi=dpi)
            print(f"GIF guardado en: {guardar_como}")

        elif ext == "mp4":
            anim.save(guardar_como, writer=FFMpegWriter(fps=fps), dpi=dpi)
            print(f"Video guardado en: {guardar_como}")

        else:
            raise ValueError("Formato no soportado. Usa .gif o .mp4")

    plt.show()
    return anim



def graficar_convergencia_aptitud(
    historial_aptitudes,
    guardar_como=None,
    mostrar=True
):
    """
    Grafica la convergencia de la mejor aptitud por generación.

    Parámetros
    ----------
    historial_aptitudes : list o np.ndarray
        Mejor aptitud de cada generación, incluyendo generación 0.
    guardar_como : str, opcional
        Ruta para guardar la gráfica, por ejemplo "convergencia.png".
    mostrar : bool
        Indica si se muestra la gráfica.
    """

    aptitudes = np.asarray(historial_aptitudes, dtype=float)

    if aptitudes.ndim != 1 or len(aptitudes) == 0:
        raise ValueError("El historial debe ser un arreglo 1D no vacío.")

    generaciones = np.arange(len(aptitudes))

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        generaciones,
        aptitudes,
        color="blue",
        linewidth=2,
        marker="o",
        markersize=3,
        label="Mejor aptitud"
    )

    # Mejor aptitud final
    ax.scatter(
        generaciones[-1],
        aptitudes[-1],
        color="red",
        s=70,
        zorder=5,
        label="Resultado final"
    )

    ax.set_title("Convergencia del algoritmo genético")
    ax.set_xlabel("Generación")
    ax.set_ylabel("Mejor aptitud f(x, y)")

    ax.grid(True, alpha=0.3)
    ax.legend()

    # Información de la aptitud inicial y final
    texto = (
        f"Aptitud inicial: {aptitudes[0]:.6f}\n"
        f"Aptitud final: {aptitudes[-1]:.6f}"
    )

    ax.text(
        0.98, 0.98,
        texto,
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox=dict(
            facecolor="white",
            edgecolor="gray",
            alpha=0.9
        )
    )

    fig.tight_layout()

    if guardar_como is not None:
        fig.savefig(guardar_como, dpi=150, bbox_inches="tight")

    if mostrar:
        plt.show()
    else:
        plt.close(fig)

    return fig