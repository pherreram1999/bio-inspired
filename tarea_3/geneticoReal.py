from random import random

import numpy as np

from objective_function import ObjetiveFunction


class GeneticoReal:

    def __init__(self, fo: ObjetiveFunction,epochs, n, nc, pc, pm, nm) -> None:
        self._fo = fo
        self._poblacion = None
        self._aptitudes = np.empty(n)
        nv = fo.get_numero_variables()
        self._hijos = np.empty((n,nv))
        self._padres = np.empty(n,dtype=int)
        self._n = n
        self._nc = nc
        self._pc = pc
        self._pm = pm
        self._nm = nm
        self._epochs = epochs

        self._best = np.empty(nv)
        pass

    def _general_poblacion(self):
        li, ls = self._fo.get_limites()
        nv = self._fo.get_numero_variables()
        self._poblacion = np.random.uniform(low=li, high=ls, size=(self._n,nv))

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
            if rand < self._pc:
                u = random()
                for v in range(nv):
                    p1_i = self._poblacion[self._padres[i]][v] # valor del primer padre en la variable v
                    p2_i = self._poblacion[self._padres[i+1]][v] #valor del segundo padre en la variabe v
                    # beta
                    b = 1 + ( (2  / ( p2_i - p1_i )) * np.min( [p1_i - li[v], ls[v] - p2_i] ) )
                    # alpha
                    a = 2 - abs(b) ** -(self._nc + 1)

                    a_inverso = 1 / a


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

    def _mutacion(self):
        nv = self._fo.get_numero_variables()
        li, ls = self._fo.get_limites()
        for i in range(self._n):
            for j in range(nv):
                if not random() <= self._pm:
                    continue

                r = random()
                hijo = self._hijos[i]
                d = np.min([ls[j] - hijo[j], hijo[j] - li[j]]) / (ls[j] - li[j])

                if r <= 0.5:
                    dq = (2*r + (1 - 2*r) * ((1 - d) ** (self._nm + 1))) ** (1 / (self._nm + 1)) - 1
                else:
                    dq = 1 - (2*(1 - r) + 2*(r - 0.5) * ((1 - d) ** (self._nm + 1))) ** (1 / (self._nm + 1))

                self._hijos[i][j] = self._hijos[i][j] + dq * (ls[j] - li[j])

    def _elitismo(self):
        best_i = np.argmin(self._aptitudes)
        self._best = self._poblacion[best_i].copy()

    def _sutitucion(self):
        self._poblacion = self._hijos.copy()
        rand_i = np.random.randint(self._n)
        self._poblacion[rand_i] = self._best


    def run(self):
        self._general_poblacion()
        self._evaluar_fo()
        for i in range(self._epochs):
            self._seleccion_padres()
            self._cruzamiento()
            self._mutacion()
            self._elitismo()
            self._sutitucion()
            self._evaluar_fo()

        return self._poblacion[np.argmin(self._aptitudes)]



