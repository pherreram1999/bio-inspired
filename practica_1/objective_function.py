from typing import Protocol

import numpy as np

from contrastMeasure import ContrastMeasure


class ObjetiveFunction(Protocol):


    def __call__(self, *variables): ...

    def set_measure(self, measure: ContrastMeasure): ...
    def get_numero_variables(self) -> int: ...

    def get_name(self) -> str: ...



class Sigmoide(ObjetiveFunction):

    def __init__(self, measure: ContrastMeasure):
        self._measure = measure

    def get_numero_variables(self) -> int:
        return 2 # que son alpha y delta

    def get_name(self) -> str:
        return "Sigmoide"

    def __call__(self, *variables):
        img, alpha, delta = variables
        return - self._measure(1.0 / (1.0 + np.exp(-alpha * (img - delta))))





