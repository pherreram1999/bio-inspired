import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


def animar_convergencia_estilo_curvas(
    fo,
    historial_best,
    historial_best_apt=None,
    historial_poblaciones=None,
    resolucion=250,
    niveles=18,
    interval=300,
    fps=5,
    guardar_como=None,
    dpi=120,
    mostrar_poblacion=False,
    mostrar_labels_contorno=True,
    mostrar_valor_funcion=True,
    color_contorno="red",
    color_trayectoria="blue",
    color_poblacion="gray"
):
    """
    Animación estilo curvas de nivel limpias, mostrando la trayectoria
    del mejor individuo y opcionalmente la población.

    Parámetros
    ----------
    fo : función objetivo de 2 variables
    historial_best : lista de mejores individuos por generación, shape (2,)
    historial_best_apt : lista de mejores aptitudes
    historial_poblaciones : lista de poblaciones por generación (opcional)
    resolucion : resolución de la malla
    niveles : número de curvas de nivel
    interval : ms entre frames
    fps : fps para guardar
    guardar_como : archivo de salida (.gif o .mp4)
    dpi : resolución de guardado
    mostrar_poblacion : si True, dibuja población actual
    mostrar_labels_contorno : si True, etiqueta curvas de nivel
    mostrar_valor_funcion : si True, muestra f(x,y) en el texto
    """

    li, ls = fo.get_limites()
    li = np.array(li, dtype=float)
    ls = np.array(ls, dtype=float)

    if len(li) != 2:
        raise ValueError("Esta animación solo funciona para funciones de 2 variables.")

    # Malla
    x = np.linspace(li[0], ls[0], resolucion)
    y = np.linspace(li[1], ls[1], resolucion)
    X, Y = np.meshgrid(x, y)

    Z = np.empty_like(X, dtype=float)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = fo(X[i, j], Y[i, j])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Solo curvas de nivel
    cs = ax.contour(X, Y, Z, levels=niveles, colors=color_contorno, linewidths=0.8, alpha=0.55)

    if mostrar_labels_contorno:
        ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")

    ax.set_xlim(li[0], ls[0])
    ax.set_ylim(li[1], ls[1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Convergencia del algoritmo genético")

    # Trayectoria del mejor
    linea_best, = ax.plot([], [], "-", color=color_trayectoria, linewidth=1.8, alpha=0.9)

    # Punto actual del mejor
    punto_best, = ax.plot([], [], "o", color=color_trayectoria, markersize=7)

    # Texto informativo
    texto = ax.text(
        0.03, 0.97, "",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="gray")
    )

    # Población opcional
    if mostrar_poblacion and historial_poblaciones is not None:
        pob0 = historial_poblaciones[0]
        scat = ax.scatter(
            pob0[:, 0],
            pob0[:, 1],
            s=18,
            color=color_poblacion,
            alpha=0.35
        )
    else:
        scat = None

    def init():
        if scat is not None:
            scat.set_offsets(historial_poblaciones[0])

        p0 = np.array(historial_best[0])
        linea_best.set_data([p0[0]], [p0[1]])
        punto_best.set_data([p0[0]], [p0[1]])

        if historial_best_apt is not None and mostrar_valor_funcion:
            texto.set_text(
                f"Generación: 0\n"
                f"x = {p0[0]:.4f}\n"
                f"y = {p0[1]:.4f}\n"
                f"f(x,y) = {historial_best_apt[0]:.6f}"
            )
        else:
            texto.set_text(
                f"Generación: 0\n"
                f"x = {p0[0]:.4f}\n"
                f"y = {p0[1]:.4f}"
            )

        artists = [linea_best, punto_best, texto]
        if scat is not None:
            artists.append(scat)
        return tuple(artists)

    def update(frame):
        p = np.array(historial_best[frame])

        # trayectoria acumulada
        tray = np.array(historial_best[:frame + 1])
        linea_best.set_data(tray[:, 0], tray[:, 1])

        # punto actual
        punto_best.set_data([p[0]], [p[1]])

        # población del frame actual
        if scat is not None:
            scat.set_offsets(historial_poblaciones[frame])

        # texto con x, y y f
        if historial_best_apt is not None and mostrar_valor_funcion:
            texto.set_text(
                f"Generación: {frame}\n"
                f"x = {p[0]:.4f}\n"
                f"y = {p[1]:.4f}\n"
                f"f(x,y) = {historial_best_apt[frame]:.6f}"
            )
        else:
            texto.set_text(
                f"Generación: {frame}\n"
                f"x = {p[0]:.4f}\n"
                f"y = {p[1]:.4f}"
            )

        artists = [linea_best, punto_best, texto]
        if scat is not None:
            artists.append(scat)
        return tuple(artists)

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
            raise ValueError("Solo se soporta .gif o .mp4")

    plt.show()
    return anim


import numpy as np
import matplotlib.pyplot as plt


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