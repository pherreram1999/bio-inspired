import math
import random
from array import ArrayType
from typing import Protocol, Tuple

import numpy as np


LIMITE_INFERIOR = -5.12
LIMITE_SUPERIOR = 5.12
PRECISION = 4
NUMERO_POBLACION = 200
PROBABILIDAD_CRUZAMIENTO = 0.6
PROBABILIDAD_MUTACION = 0.2

EPOCHS = 10


class MathFunction(Protocol):
    def __call__(self, *variables) -> float: ...

    def get_limites(self) -> Tuple[float, float]: ...

    def get_numero_variables(self) -> int: ...


class Rastring:

    def __init__(self, limites: Tuple[float, float]):
        self._limites = limites

    def get_limites(self) -> Tuple[float, float]:
        return self._limites

    def get_numero_variables(self) -> int:
        return 2


    def __call__(self, *args, **kwargs):
        x,y = args
        return 20 + (x ** 2 - 10 * math.cos(2 * math.pi * x)) + (y ** 2 - 10 * math.cos(2 * math.pi * y))




class GeneticoBasico:


    def __init__(
            self,
            objetive_function: MathFunction,
            numero_poblacion: int,
            precision: int,
            probabilidad_cruzamiento: float,
            probabilidad_mutacion: float,
            epochs = 100):

        self._epochs = epochs
        self._np = numero_poblacion
        self._pc = probabilidad_cruzamiento
        self._pm = probabilidad_mutacion

        self._precision = precision

        self._fo = objetive_function
        self._limits = self._fo.get_limites()
        self._l = int(math.log2((self._limits[1] - self._limits[0]) * (10 ** self._precision)) + .9)
        self._len_individuo = self._fo.get_numero_variables() * self._l
        self._matrix_size = (self._np, self._len_individuo)

        self._parents = np.empty(self._np, dtype=int)
        self._children = np.empty(self._matrix_size, dtype=int)
        self._aptitudes = np.empty(self._np)
        self._decodificados = np.empty((self._np,self._fo.get_numero_variables()))
        self._best_individual = np.empty(0)
        self._best_aptitude = float('inf')



    def _make_population(self):
        self._poblacion = np.random.randint(0, 2, size=self._matrix_size)

    def _decodificarReal(self,individuo: ArrayType):
        Xentero = int(np.dot(individuo[::-1].astype(np.int64), 2 ** np.arange(len(individuo))))
        return self._limits[0] + (Xentero * (self._limits[1] - self._limits[0]) / ((2 ** self._l) - 1))

    def _decodificar_individuo(self, individuo):
        Vreales = np.empty(self._fo.get_numero_variables())
        being = 0
        for v in range(self._fo.get_numero_variables()):
            end = being + self._l
            cromosoma = individuo[being:end]
            being = end
            Vreal = self._decodificarReal(cromosoma)
            if not self._limits[0] <= Vreal <= self._limits[1]:
                raise "Valor no dentro de los limites"
            Vreales[v] = Vreal
        pass
        return Vreales

    def _decodificar(self):
        if len(self._poblacion) == 0:
            raise "Población vacia"

        for i, individuo in enumerate(self._poblacion):
            # para ello tenemos que decodificar
            self._decodificados[i] = self._decodificar_individuo(individuo)
        pass

    def _evaluate_aptitudes(self):
        for i,vreal in enumerate(self._decodificados):
            self._aptitudes[i] = self._fo(*vreal)
        pass
    pass


    def _choose_parents(self):
        col1 = np.random.permutation(self._np)
        col2 = np.random.permutation(self._np)
        torneo = np.column_stack((col1, col2))  # shape (Np, 2)
        for i in range(self._np):
            p1_index, p2_index = torneo[i]
            p1, p2 = self._aptitudes[p1_index], self._aptitudes[p2_index]
            if p1 < p2: # buscamos minimizar
                self._parents[i] = p1_index
            else:
                self._parents[i] = p2_index
            pass

    def _crossing(self):

        i = 0
        while i < self._np:
            pto = np.sort(np.random.choice(range(1, self._len_individuo), size=2, replace=False))
            padre1 = self._poblacion[self._parents[i]]
            padre2 = self._poblacion[self._parents[i + 1]]
            r = random.random()
            if r <= self._pc:
                self._children[i] = np.concatenate([padre1[:pto[0]], padre2[pto[0]:pto[1]], padre1[pto[1]:]])
                self._children[i + 1] = np.concatenate([padre2[:pto[0]], padre1[pto[0]:pto[1]], padre2[pto[1]:]])
            else:
                self._children[i] = padre1
                self._children[i + 1] = padre2

            i = i + 2

        pass

    def _mutation(self):
        for i in range(self._np):
            rand_index = random.randint(0, self._len_individuo -1)
            r = random.random()
            if r <= self._pm:
                self._children[i][rand_index] = not self._children[i][rand_index]
        pass

    def _get_best_individual(self):
        return self._poblacion[np.argmin(self._aptitudes)]

    def _substitution(self):

        # de la poblacion antes de ser actualizada, obtenemos el mejor individuo
        mejor_individuo = self._get_best_individual()
        self._poblacion = self._children.copy()
        # en este caso, remplazamos uno a la nueva poblacion
        rand_index = random.randint(0, self._np -1)
        self._poblacion[rand_index] = mejor_individuo
        pass



    def run(self):
        """
        Donde sucede toda la magia
        :return:
        """
        self._make_population()
        self._decodificar()
        self._evaluate_aptitudes()
        for i in range(self._epochs):
            self._choose_parents()
            self._crossing()
            self._mutation()
            self._substitution()
            # volvemos a decodificar y evaluar
            self._decodificar()
            self._evaluate_aptitudes()
            #
            best_idx_individual = np.argmin(self._aptitudes)
            best_apt_current = self._aptitudes[best_idx_individual]

            if best_apt_current < self._best_aptitude:
                self._best_aptitude = best_apt_current
                self._best_individual = self._poblacion[best_idx_individual]

        pass

        return self._decodificar_individuo(self._best_individual)


    def __call__(self, *args, **kwargs):
        return self.run()


    pass





def main():
    # generamos una poblacion aleatoria inicial

    bio = GeneticoBasico(
        Rastring((LIMITE_INFERIOR, LIMITE_SUPERIOR)),
        NUMERO_POBLACION,
        PRECISION,
        PROBABILIDAD_CRUZAMIENTO,
        PROBABILIDAD_MUTACION
    )

    print(bio())




if __name__ == '__main__':
    main()