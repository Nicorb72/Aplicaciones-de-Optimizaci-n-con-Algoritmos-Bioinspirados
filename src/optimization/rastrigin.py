import numpy as np


def rastrigin(x):
    x = np.asarray(x, dtype=float)
    n = x.size
    return 10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def rastrigin_gradient(x):
    x = np.asarray(x, dtype=float)
    return 2 * x + 20 * np.pi * np.sin(2 * np.pi * x)