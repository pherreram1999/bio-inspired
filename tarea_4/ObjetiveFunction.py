from FunctionDefinition import FunctionDefinition

class ObjetiveFunction(FunctionDefinition):

    def get_numero_variables(self) -> int:
        return 2
    def get_name(self) -> str:
        return "circulo desplazado"

    def get_limites(self):
        return (
            #x,y
            (0,0),
            (1,2)
        )

    def __call__(self, *variables) -> float:
        x, y = variables
        return (4 * ((x - 3) ** 2)) + (3 * ((y -3) ** 2))


