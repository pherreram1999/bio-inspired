import numpy as np

from geneticoReal import GeneticoReal
from langermann import Langermann
from objective_function import ObjetiveFunction





N = 100
Nc = 2

def main():

    # generamos una poblacion uniforme
    fo = Langermann()
    b = GeneticoReal(fo,N,Nc,.7)
    b.run()

if __name__ == "__main__":
    main()
