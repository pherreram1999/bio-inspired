from matplotlib import pyplot as plt
from constants import RANGE_MAX, RANGE_MIN
from styblinski import styblinski
import numpy as np
import matplotlib.animation as animation

def animate(trajectory,output_path="trajectory.gif",max_frames=300, malla_n = 400):

    trajectory = np.asarray(trajectory) # para evitar problemas con las operaciones de slicing
    trajectory_anim = None
    trajectory_len = len(trajectory)

    if trajectory_len > max_frames:
        # con linspace obtenemos indices espaciados uniformente
        # solo se toman un maximo para la animacion
        idx = np.linspace(0,trajectory_len - 1, max_frames).astype(int)
        trajectory_anim = trajectory[idx] # con la indices tomamos los valores
    else:
        trajectory_anim = trajectory
    pass

    # creamos nuestra malla

    x = np.linspace(RANGE_MIN, RANGE_MAX, malla_n)
    X1, X2 = np.meshgrid(x, x)
    # esto es posible gracias a numpy
    Z = styblinski(X1, X2)
    fig, ax = plt.subplots(figsize=(8, 8))

    contour = ax.contour(X1, X2, Z, levels=30,cmap='viridis')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    # donde se va renderizado la linea, empeiza vacio y su formato de renderizad
    line, = ax.plot([],[],"r.-", linewidth=1, markersize=4, label="trayectoria")
    dot, = ax.plot([], [], "ro", markersize=8)
    ax.legend(loc="upper right")


    # funciones de animacion

    def init():
        line.set_data([],[])
        dot.set_data([],[])
        return line,dot

    def update(frame):
        # va a tomar progresivamente los valroes de la trayectoria
        # pare el efecto de animacion
        # es decir de la forma: [1], [1,2], [1,2,..n]
        xs = trajectory_anim[:frame + 1, 0]
        ys = trajectory_anim[:frame + 1, 1]
        line.set_data(xs, ys)
        dot.set_data([xs[-1]], [ys[-1]])
        ax.set_title(f"Descenso de gradiente")
        return line, dot

    anim = animation.FuncAnimation(
        fig,update, frames=len(trajectory_anim),
        interval=80, blit=True,init_func=init,
    )

    anim.save(output_path, writer='pillow', fps=15)
    plt.close(fig)
pass

