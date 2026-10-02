from typing import Tuple
import numpy as np


def cruzamiento_sbx(p1, p2, lim_min, lim_max, u: float, nc: float, num_vars):

    hijos = np.empty((2,num_vars), dtype=float)

    for i in range(num_vars):
        p1_i = p1[i] # valor del padre 1
        p2_i = p2[i] # valor del padre 2

        p1_l = lim_min[i] # limite inferior
        p2_l = lim_max[i]  # limite superior del padre

        b = 1 + (2 / (p2_i - p1_i)) * np.min( (p1_i - p1_l ,p2_l  - p2_i))

        alpha = 2 - abs(b) ** -(nc + 1)

        alpha_inverso = 1 / alpha

        bc = None
        if u <= alpha_inverso:
            bc = (u * alpha) ** (1 / (nc + 1))
        else:
            bc = (1 /( 2 - (u * alpha))) ** (1 / (nc + 1))

        if bc is None:
            raise ValueError("Bc es nulo")



        hijos[0][i] = .5 * ( (p1_i + p2_i) - bc * abs(p2_i - p1_i) )
        hijos[1][i] = .5 * ( (p1_i + p2_i) + bc * abs(p2_i - p1_i) )

    return hijos


def main():
    p1 = np.array([2.3, 4.5])
    p2 = np.array([1.4, -0.2])
    lmin = (1, -1)
    lmax = (3, 5)

    hijos = cruzamiento_sbx(p1,p2,lmin,lmax, .95,2,2);

    print(hijos)
    pass


if __name__ == "__main__":
    main()