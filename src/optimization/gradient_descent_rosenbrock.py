import numpy as np

from .rosenbrock import rosenbrock


def run_gradient_descent_rosenbrock(initial_point, learning_rate=1e-3, iterations=1000):
    x = np.asarray(initial_point, dtype=float).copy()
    for _ in range(iterations):
        grad = np.zeros_like(x)
        grad[:-1] += -400 * x[:-1] * (x[1:] - x[:-1] ** 2) - 2 * (1 - x[:-1])
        grad[1:] += 200 * (x[1:] - x[:-1] ** 2)
        x -= learning_rate * grad
    return {"best_solution": x, "best_value": float(rosenbrock(x))}
