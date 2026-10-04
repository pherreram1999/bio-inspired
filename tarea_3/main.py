import numpy as np

from geneticoReal import GeneticoReal
from langermann import Langermann
from objective_function import ObjetiveFunction





N = 100

def main():

    # generamos una poblacion uniforme
    fo = Langermann()
    b = GeneticoReal(fo,N)
    b.run()

if __name__ == "__main__":
    main()
