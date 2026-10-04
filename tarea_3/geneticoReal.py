from random import random

import numpy as np

from objective_function import ObjetiveFunction


class GeneticoReal:

    def __init__(self, fo: ObjetiveFunction, n, nc, pc) -> None:
        self._fo = fo
        self._poblacion = None
        self._aptitudes = np.empty(n)
        nv = fo.get_numero_variables()
        self._hijos = np.empty((n,nv))
        self._padres = np.empty(n,dtype=int)
        self._n = n
        self._nc = nc
        self._pc = pc
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
        li, ls = self._fo.get_limites()

        i = 0
        while i < self._n:
            rand = random()
            if self._pc < rand:
                for v in range(nv):
                    p1_i = self._poblacion[self._padres[i]][v] # valor del primer padre en la variable v
                    p2_i = self._poblacion[self._padres[i+1]][v] #valor del segundo padre en la variabe v
                    # beta
                    print()
                    b = 1 + ( (2  / ( p2_i - p1_i )) * np.min( [p1_i - li[v], ls[v] - p2_i] ) )
                    # alpha
                    a = 2 - abs(b) ** -(self._nc + 1)

                    a_inverso = 1 / a

                    u = random()

                    if u <= a_inverso:
                        bc = (u * a) ** (1 / (self._nc + 1))
                    else:
                        bc = (1 / (2 - (u * a))) ** (1 / (self._nc + 1))


                    self._hijos[i][v] = .5 * ( (p1_i + p2_i) - (bc * abs(p2_i - p1_i)) )
                    self._hijos[i+1][v] = .5 * ( (p1_i + p2_i) + (bc * abs(p2_i - p1_i)) )
            else:
                self._hijos[i] =  self._poblacion[self._padres[i]]
                self._hijos[i+1] =  self._poblacion[self._padres[i+1]]

            i = i + 2 # saltamos de 2 en 2 para selecionar 2 padres



    def run(self):
        self._general_poblacion()
        self._evaluar_fo()
        self._seleccion_padres()
        self._cruzamiento()


