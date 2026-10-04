import numpy as np

from objective_function import ObjetiveFunction


class GeneticoReal:

    def __init__(self, fo: ObjetiveFunction, n) -> None:
        self._fo = fo
        self._poblacion = None
        self._aptitudes = np.empty(n)
        nv = fo.get_numero_variables()
        self._hijos = np.empty((n,nv))
        self._padres = np.empty(n,dtype=int)
        self._n = n
        pass

    def _general_poblacion(self):
        li, ls = self._fo.get_limites()
        self._poblacion = np.random.uniform(low=li, high=ls, size=(self._n,2))

    def _seleccion_padres(self):
        # generamos posiciones de lucha para el torneo
        c1 = np.random.permutation(self._n)
        c2 = np.random.permutation(self._n)
        torneo = np.column_stack((c1, c2))

        for i in range(self._n):
            p1i, p2i = torneo[i]
            ap1 = self._aptitudes[p1i]
            ap2 = self._aptitudes[p2i]
            if ap1 < ap2: # se busca minimizar
                self._padres[i] = p1i
            else:
                self._padres[i] = p2i




    def _evaluar_fo(self):
        for i in range(self._n):
            self._aptitudes[i] = self._fo(*self._poblacion[i])

    def _cruzamiento(self):
        nv = self._fo.get_numero_variables()
        i = 0
        while i < self._n:

            i = i + 2 # saltamos de 2 en 2 para selecionar 2 padres


    def _cruzamiento_sbx(p1, p2, lim_min, lim_max, u: float, nc: float, num_vars):

        hijos = np.empty((2, num_vars), dtype=float)

        for i in range(num_vars):
            p1_i = p1[i]  # valor del padre 1
            p2_i = p2[i]  # valor del padre 2

            p1_l = lim_min[i]  # limite inferior
            p2_l = lim_max[i]  # limite superior

            b = 1 + (2 / (p2_i - p1_i)) * np.min((p1_i - p1_l, p2_l - p2_i))

            alpha = 2 - abs(b) ** -(nc + 1)

            alpha_inverso = 1 / alpha

            bc = None
            if u <= alpha_inverso:
                bc = (u * alpha) ** (1 / (nc + 1))
            else:
                bc = (1 / (2 - (u * alpha))) ** (1 / (nc + 1))

            if bc is None:
                raise ValueError("Bc es nulo")

            hijos[0][i] = .5 * ((p1_i + p2_i) - bc * abs(p2_i - p1_i))
            hijos[1][i] = .5 * ((p1_i + p2_i) + bc * abs(p2_i - p1_i))

        return hijos

    def run(self):
        self._general_poblacion()
        self._evaluar_fo()
        self._seleccion_padres()
        print(self._padres)