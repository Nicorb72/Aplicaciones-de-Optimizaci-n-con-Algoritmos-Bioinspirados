import numpy as np

from .rastrigin import rastrigin


def run_gradient_descent_rastrigin(initial_point, learning_rate=1e-3, iterations=1000):
    x = np.asarray(initial_point, dtype=float).copy()
    for _ in range(iterations):
        grad = 2 * x + 20 * np.pi * np.sin(2 * np.pi * x)
        x -= learning_rate * grad
    return {"best_solution": x, "best_value": float(rastrigin(x))}
