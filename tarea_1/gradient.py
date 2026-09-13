import numpy as np
from constants import EPOCHS, ALPHA, ROUND, TOLERANCIA_MAX
from styblinski import styblinski, styblinski_dev
from tabulate import tabulate



def gradient(x):
    xk = np.array(x, dtype=float)

    # almacenamos todos los resultados de la tabla
    table_results = []
    # guardamos todos los datos de la trayectoria
    trajectory = []

    for epoch in range(EPOCHS):
        last_epoch = epoch
        # gradiente
        vf = np.array([
            styblinski_dev(xk[0]),
            styblinski_dev(xk[1]),
        ])

        # xk +1 = xk + ak * vf
        xk_next = xk - ALPHA * vf

        tolerance = np.linalg.norm(xk_next - xk)

        ## la funcion evaluada
        f = styblinski(xk_next[0], xk_next[1])

        table_results.append(
            [
                epoch + 1,
                xk.round(ROUND).tolist(),
                vf.round(ROUND),
                xk_next.round(ROUND).tolist(),
                tolerance,
                f
            ]
        )

        trajectory.append(xk_next)

        xk = xk_next

        if tolerance < TOLERANCIA_MAX:
            break
    pass

    return trajectory, table_results
