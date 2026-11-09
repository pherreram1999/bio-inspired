from ast import Tuple

from ObjetiveFunction import ObjetiveFunction

class RestrictionDefinition(ObjetiveFunction):

    def evaluate_condition(self, value) -> bool: ...


class G1(RestrictionDefinition):

    def get_name(self) -> str:
        return "Restricción g1"

    def __call__(self, *variables) -> float:
        x,y = variables
        return (2 * x) + y - 2

    def evaluate_condition(self,value) -> bool:
        return value <= 0


class G2(RestrictionDefinition):
    def get_name(self) -> str:
        return "Restricción g2"

    def __call__(self, *variables) -> float:
        x,y = variables
        return (3*x) + (4*y) - 6

    def evaluate_condition(self,value) -> bool:
        return value <= 0