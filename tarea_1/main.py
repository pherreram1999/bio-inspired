import gradient
from animate import animate
from gradient import gradient
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_point(point, name):
    trayectoria, table = gradient(point)

    # guardamos en disco
    with open(name + '_data.txt', 'w') as f:
        f.write(
            tabulate(table, headers=['epoch', 'xk', 'vf', 'xk_next', 'tolerance','f(x1,x2)'],
                     floatfmt=".4f")
        )
    pass

    animate(trayectoria, output_path=name+"_trayectoria.gif")

pass



def main():
    puntos_inicio = [
        # propuestas originales
        [-1,-1],
        [-4, 4],
        # puntos adicionales
        [ 0, 3],
        [2,3],
        [0,0],
        [2,0]
    ]

    with ThreadPoolExecutor(max_workers=len(puntos_inicio)) as executor:
        futures = []
        for i, punto in enumerate(puntos_inicio):
            futures.append(
                executor.submit(process_point, punto, "punto_" + str(i + 1))
            )

        for f in futures:
            f.result() # para ver si lanza ninguna excepcion
    pass


pass

if __name__ == "__main__":
    main()
