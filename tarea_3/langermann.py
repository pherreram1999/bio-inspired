import math

from objective_function import ObjetiveFunction


class Langermann(ObjetiveFunction):

    def get_limites(self):
        return (
            (0,0), # limites inferiores
            (10,10) # limites superiores
        )

    def get_numero_variables(self):
        return 2


    def __call__(self, *variables):

        if len(variables) != 2:
            raise ValueError("Debes pasar 2 valores de argumento")

        x1,x2 = variables
        r = 0.0

        a = [3,5,2,1,7]
        b = [5,2,1,4,9]
        c = [1,2,5,2,3]

        for i in range(5):
            d1 = (x1 -  a[i]) ** 2
            d2 = (x2 - b[i]) ** 2

            r = r + (
                (c[i] * math.cos(math.pi * ( d1 + d2))) / (math.e ** ((d1 + d2) / math.pi) )
            )

        return -r
