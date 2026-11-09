import numpy as np
import matplotlib.pyplot as plt


def _malla(fo, resolucion):
    li, ls = fo.get_limites()
    x = np.linspace(li[0], ls[0], resolucion)
    y = np.linspace(li[1], ls[1], resolucion)
    X, Y = np.meshgrid(x, y)
    return X, Y


def graficar_resultado(
    fo,
    restricciones,
    historial_poblaciones,
    historial_best,
    historial_best_apt,
    guardar_como=None,
    mostrar=True,
    resolucion=300,
    niveles=20,
    max_puntos_poblacion=100,
):
    """
    Renderiza en una sola figura:
      - Izquierda: curvas de nivel de la función objetivo, las fronteras de las
        restricciones (g = 0), la región factible sombreada, la población
        inicial y final y la trayectoria del mejor individuo.
      - Derecha: convergencia de la mejor aptitud (penalizada) por generación.

    Parámetros
    ----------
    fo : función objetivo de 2 variables
    restricciones : lista de restricciones g(x, y) <= 0
    historial_poblaciones : list[np.ndarray] con forma (N, 2) por generación
    historial_best : list[np.ndarray] mejor individuo por generación
    historial_best_apt : list[float] mejor aptitud penalizada por generación
    guardar_como : ruta del PNG a guardar (opcional)
    mostrar : si True, abre la ventana de matplotlib
    """
    li, ls = fo.get_limites()
    best = np.asarray(historial_best, dtype=float)
    apt = np.asarray(historial_best_apt, dtype=float)

    if best.ndim != 2 or best.shape[1] != 2:
        raise ValueError("historial_best debe tener forma (generaciones, 2)")

    # valor real de f del mejor de cada generación
    f_real = np.array([fo(*p) for p in best])
    gens = np.arange(len(best))

    fig, (ax, ax_c) = plt.subplots(1, 2, figsize=(15, 6.5))

    # ------------------------------------------------------------------
    # Panel 1: superficie, restricciones y trayectoria
    # ------------------------------------------------------------------
    X, Y = _malla(fo, resolucion)
    Z = fo(X, Y)

    cs = ax.contour(X, Y, Z, levels=niveles, cmap="viridis", linewidths=0.8, alpha=0.8)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")

    # región factible: todas las g_i <= 0
    if restricciones:
        g_max = np.maximum.reduce([r(X, Y) for r in restricciones])
        ax.contourf(X, Y, g_max, levels=[-np.inf, 0], colors=["#66bb6a"], alpha=0.25)

        colores = ["#e53935", "#fb8c00", "#8e24aa", "#00acc1"]
        handles = []
        for k, r in enumerate(restricciones):
            color = colores[k % len(colores)]
            ax.contour(X, Y, r(X, Y), levels=[0], colors=[color], linewidths=2.2)
            handles.append(plt.Line2D([], [], color=color, lw=2.2, label=f"{r.get_name()} = 0"))
        handles.append(plt.Rectangle((0, 0), 1, 1, fc="#66bb6a", alpha=0.35, label="Región factible"))
    else:
        handles = []

    def muestra(pob):
        pob = np.asarray(pob, dtype=float)
        idx = np.linspace(0, len(pob) - 1, min(max_puntos_poblacion, len(pob)), dtype=int)
        return pob[idx]

    p0 = muestra(historial_poblaciones[0])
    pf = muestra(historial_poblaciones[-1])
    sc0 = ax.scatter(p0[:, 0], p0[:, 1], s=14, c="gray", alpha=0.45, label="Población inicial", zorder=3)
    scf = ax.scatter(pf[:, 0], pf[:, 1], s=14, c="blue", alpha=0.55, label="Población final", zorder=3)
    tray, = ax.plot(best[:, 0], best[:, 1], "-", color="black", lw=1.2, alpha=0.7, label="Trayectoria del mejor", zorder=4)
    star = ax.scatter(best[-1, 0], best[-1, 1], s=220, c="gold", edgecolors="black",
                      marker="*", label="Mejor final", zorder=5)

    ax.set_xlim(li[0], ls[0])
    ax.set_ylim(li[1], ls[1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"{fo.get_name()}: superficie y restricciones")
    ax.legend(handles=handles + [sc0, scf, tray, star], loc="upper right", fontsize=8, framealpha=0.9)
    ax.text(
        0.03, 0.03,
        f"x = {best[-1, 0]:.5f}\ny = {best[-1, 1]:.5f}\n"
        f"f = {f_real[-1]:.6f}",
        transform=ax.transAxes, va="bottom", ha="left", fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9),
    )

    # ------------------------------------------------------------------
    # Panel 2: convergencia
    # ------------------------------------------------------------------
    ax_c.plot(gens, apt, color="blue", lw=2, label="Aptitud penalizada")
    ax_c.set_xlabel("Generación")
    ax_c.set_ylabel("Valor de la función")
    ax_c.grid(True, alpha=0.3)

    ax_c.legend(loc="upper right")
    ax_c.set_title("Convergencia")

    fig.tight_layout()

    if guardar_como is not None:
        fig.savefig(guardar_como, dpi=150, bbox_inches="tight")
        print(f"Gráfica guardada en: {guardar_como}")

    if mostrar:
        plt.show()
    else:
        plt.close(fig)

    return fig


def animar_resultado(
    fo,
    restricciones,
    historial_poblaciones,
    historial_best,
    historial_best_apt,
    guardar_como=None,
    mostrar=True,
    resolucion=300,
    niveles=20,
    max_puntos_poblacion=100,
    paso=1,
    fps=8,
    dpi=90,
):
    """
    Anima la evolución del algoritmo genético:
      - Izquierda: curvas de nivel + región factible + fronteras de las
        restricciones (fijas); la población, el mejor y su trayectoria se
        mueven generación a generación.
      - Derecha: la convergencia (aptitud penalizada)
        se va dibujando conforme avanzan las generaciones.

    paso : usa una de cada `paso` generaciones (acelera el render del GIF).
    guardar_como : ruta .gif (opcional).
    """
    from matplotlib.animation import FuncAnimation, PillowWriter

    li, ls = fo.get_limites()
    best = np.asarray(historial_best, dtype=float)
    apt = np.asarray(historial_best_apt, dtype=float)
    f_real = np.array([fo(*p) for p in best])
    frames = list(range(0, len(best), paso))
    if frames[-1] != len(best) - 1:
        frames.append(len(best) - 1)

    fig, (ax, ax_c) = plt.subplots(1, 2, figsize=(15, 6.5))

    # ---------------- panel izquierdo: fondo estático ----------------
    X, Y = _malla(fo, resolucion)
    Z = fo(X, Y)
    cs = ax.contour(X, Y, Z, levels=niveles, cmap="viridis", linewidths=0.8, alpha=0.8)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")

    handles = []
    if restricciones:
        g_max = np.maximum.reduce([r(X, Y) for r in restricciones])
        ax.contourf(X, Y, g_max, levels=[-np.inf, 0], colors=["#66bb6a"], alpha=0.25)
        colores = ["#e53935", "#fb8c00", "#8e24aa", "#00acc1"]
        for k, r in enumerate(restricciones):
            color = colores[k % len(colores)]
            ax.contour(X, Y, r(X, Y), levels=[0], colors=[color], linewidths=2.2)
            handles.append(plt.Line2D([], [], color=color, lw=2.2, label=f"{r.get_name()} = 0"))
        handles.append(plt.Rectangle((0, 0), 1, 1, fc="#66bb6a", alpha=0.35, label="Región factible"))

    ax.set_xlim(li[0], ls[0])
    ax.set_ylim(li[1], ls[1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    def muestra(pob):
        pob = np.asarray(pob, dtype=float)
        idx = np.linspace(0, len(pob) - 1, min(max_puntos_poblacion, len(pob)), dtype=int)
        return pob[idx]

    # ---------------- artistas dinámicos ----------------
    sc_pob = ax.scatter([], [], s=16, c="royalblue", alpha=0.6, label="Población", zorder=3)
    linea_best, = ax.plot([], [], "-", color="black", lw=1.4, alpha=0.8, label="Trayectoria del mejor", zorder=4)
    star = ax.scatter([], [], s=220, c="gold", edgecolors="black", marker="*", label="Mejor", zorder=5)
    texto = ax.text(
        0.03, 0.03, "", transform=ax.transAxes, va="bottom", ha="left", fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9),
    )
    ax.legend(handles=handles + [sc_pob, linea_best, star], loc="upper right", fontsize=8, framealpha=0.9)

    # ---------------- panel derecho: convergencia ----------------
    n = len(best)
    ax_c.set_xlim(0, n - 1)
    margen = 0.05 * ((apt.max() - apt.min()) or 1.0)
    ax_c.set_ylim(apt.min() - margen, apt.max() + margen)
    ax_c.set_xlabel("Generación")
    ax_c.set_ylabel("Valor de la función")
    ax_c.set_title("Convergencia")
    ax_c.grid(True, alpha=0.3)
    l_apt, = ax_c.plot([], [], color="blue", lw=2, label="Aptitud penalizada")
    punto, = ax_c.plot([], [], "o", color="blue", ms=7)

    ax_c.legend(handles=[l_apt], loc="upper right")

    def update(frame):
        pob = muestra(historial_poblaciones[frame])
        p = best[frame]
        sc_pob.set_offsets(pob)
        linea_best.set_data(best[:frame + 1, 0], best[:frame + 1, 1])
        star.set_offsets(np.array([[p[0], p[1]]]))
        ax.set_title(f"{fo.get_name()}: generación {frame}/{n - 1}")
        texto.set_text(
            f"x = {p[0]:.5f}\ny = {p[1]:.5f}\n"
            f"f = {f_real[frame]:.6f}"
        )

        g = np.arange(frame + 1)
        l_apt.set_data(g, apt[:frame + 1])
        punto.set_data([frame], [apt[frame]])
        return sc_pob, linea_best, star, texto, l_apt, punto

    fig.tight_layout()
    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False, repeat=False)

    if guardar_como is not None:
        anim.save(guardar_como, writer=PillowWriter(fps=fps), dpi=dpi)
        print(f"Animación guardada en: {guardar_como}")

    if mostrar:
        plt.show()
    else:
        plt.close(fig)

    return anim
