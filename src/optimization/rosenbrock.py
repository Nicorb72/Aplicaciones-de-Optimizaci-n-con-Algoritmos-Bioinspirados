import numpy as np


def rosenbrock(x):
    x = np.asarray(x, dtype=float)
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def rosenbrock_gradient(x):
    """Calcula el gradiente analítico de Rosenbrock para un vector de coordenadas."""
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    grad[:-1] += -400 * x[:-1] * (x[1:] - x[:-1] ** 2) - 2 * (1 - x[:-1])
    grad[1:] += 200 * (x[1:] - x[:-1] ** 2)
    return grad
