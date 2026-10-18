from typing import Protocol

import numpy as np

from contrastMeasure import ContrastMeasure


class ObjetiveFunction(Protocol):


    def __call__(self, *variables): ...

    def set_measure(self, measure: ContrastMeasure): ...
    def get_numero_variables(self) -> int: ...

    def get_name(self) -> str: ...

    def get_limites(self): ...


class Sigmoide(ObjetiveFunction):

    def __init__(self, img,measure: ContrastMeasure):
        self._img = img
        self._measure = measure

    def get_limites(self):
        return (
            (0, 0),  # límites inferiores: alpha, delta
            (10, 1),  # límites superiores: alpha, delta
        )

    def get_numero_variables(self) -> int:
        return 2 # que son alpha y delta

    def get_name(self) -> str:
        return "Sigmoide"

    def transformar(self,alpha,delta):
        return 1.0 / (1.0 + np.exp(-alpha * (self._img - delta)))

    def __call__(self, *variables):
        alpha, delta = variables
        return - self._measure(self.transformar(alpha,delta))





