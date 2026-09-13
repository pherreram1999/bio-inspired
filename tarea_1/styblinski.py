def styblinski_base(x):
    return 0.5 * ((x ** 4) - (16 * (x ** 2)) + (5 * x))


def styblinski(x1, x2):
    return styblinski_base(x1) + styblinski_base(x2)


# definimos la funcion que esencia es la misma para ambos para x1 y x2
# el cual ya esta derivada
def styblinski_dev(x):
    return 2 * (x ** 3) - 16 * x + 5 / 2