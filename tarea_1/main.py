import numpy as np
from tabulate import tabulate
from constants import ROUND, TOLERANCIA_MAX, EPOCHS
from styblinski import styblinski_dev, styblinski
from animate import animate

def main():
    xk = np.array([-1, -1], dtype=float)

    alpha = 0.01
    # almacenamos todos los resultados de la tabla
    table_results = []
    # guardamos todos los datos de la trayectoria
    trajectory = []

    last_epoch = 0

    for epoch in range(EPOCHS):
        last_epoch = epoch
        # gradiente
        vf = np.array([
            styblinski_dev(xk[0]),
            styblinski_dev(xk[1]),
        ])

        # xk +1 = xk + ak * vf
        xk_next = xk - alpha * vf

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

    printable_data = tabulate(
        table_results,
        headers=['epoch', 'xk', 'vf', 'xk +1', 'tolerance', 'f(x1,x2)'],
        floatfmt=".4f"
    )

    # guardamos la tabla en disco

    with open("output.txt", "w") as f:
        f.write(printable_data)


    print("Last epoch:", last_epoch)

    animate(trajectory)


pass

if __name__ == "__main__":
    main()
