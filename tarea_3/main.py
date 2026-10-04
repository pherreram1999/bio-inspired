import numpy as np

from geneticoReal import GeneticoReal
from langermann import Langermann
from objective_function import ObjetiveFunction





N = 100
Nc = 2
Pc = 0.7
Pm = 0.02
Nm = 20
Epochs = 20

def main():

    # generamos una poblacion uniforme
    fo = Langermann()
    b = GeneticoReal(fo,Epochs,N,Nc,Pc, Pm, Nm)
    best = b.run()
    print(best)

if __name__ == "__main__":
    main()
