from numbers import Integral, Real

import numpy as np

from .rosenbrock import rosenbrock, rosenbrock_gradient


def run_gradient_descent_rosenbrock(initial_point, learning_rate=1e-3, iterations=1000):
    if isinstance(iterations, bool) or not isinstance(iterations, Integral) or iterations < 0:
        raise ValueError("iterations debe ser un entero no negativo.")
    if (isinstance(learning_rate, bool) or not isinstance(learning_rate, Real)
            or not np.isfinite(learning_rate) or learning_rate <= 0):
        raise ValueError("learning_rate debe ser un número finito positivo.")
    x = np.asarray(initial_point, dtype=float).copy()
    if x.ndim != 1 or x.size < 2 or not np.all(np.isfinite(x)):
        raise ValueError("initial_point debe ser un vector finito con al menos dos coordenadas.")
    trajectory = [x.copy()]
    function_evaluations = 0
    gradient_evaluations = 0
    status = "completed"
    for _ in range(iterations):
        with np.errstate(over="ignore", invalid="ignore"):
            grad = rosenbrock_gradient(x)
            gradient_evaluations += 1
            next_x = x - learning_rate * grad
        if not np.all(np.isfinite(grad)) or not np.all(np.isfinite(next_x)):
            status = "diverged"
            break
        x = next_x
        trajectory.append(x.copy())
    with np.errstate(over="ignore", invalid="ignore"):
        final_value = float(rosenbrock(x))
    function_evaluations += 1
    if not np.isfinite(final_value):
        status = "diverged"
    return {
        "best_solution": x,
        "best_value": final_value,
        "trajectory": np.asarray(trajectory),
        "function_evaluations": function_evaluations,
        "gradient_evaluations": gradient_evaluations,
        "status": status,
        "iterations_completed": len(trajectory) - 1,
    }
