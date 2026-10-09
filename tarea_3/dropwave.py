import math
from ast import Tuple

from objective_function import ObjetiveFunction


class Dropwave(ObjetiveFunction):

    def get_name(self) -> str:
        return "Dropwave"

    def get_limites(self):
        return (
            (-5.12, -5.12),
            (5.12, 5.12)
        )

    def get_numero_variables(self) -> int:
        return 2

    def __call__(self, *args, **kwargs):
        x, y = args
        cuadtrica = x**2 +  y**2
        r = (1 + math.cos(12 * math.sqrt(cuadtrica))) / ((.5 * cuadtrica) + 2)
        return  -r