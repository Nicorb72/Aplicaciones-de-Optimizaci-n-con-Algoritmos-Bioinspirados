"""Validación y formato común para los métodos poblacionales."""
import numpy as np


def validate_population(bounds, size, steps, minimum=1):
    if type(size) is not int or size < minimum:
        raise ValueError(f"El tamaño de población debe ser un entero >= {minimum}.")
    if type(steps) is not int or steps < 0:
        raise ValueError("Las iteraciones deben ser un entero no negativo.")
    bounds = np.asarray(bounds, dtype=float)
    if bounds.ndim != 2 or bounds.shape[1] != 2 or not len(bounds):
        raise ValueError("bounds debe contener pares (inferior, superior).")
    if not np.all(np.isfinite(bounds)) or np.any(bounds[:, 0] >= bounds[:, 1]):
        raise ValueError("Los límites deben ser finitos y estar ordenados.")
    return bounds[:, 0], bounds[:, 1]


def population_result(trajectory, values, evaluations):
    """La trayectoria representa el mejor punto conocido, no un individuo."""
    trajectory = np.asarray(trajectory)
    return {
        "best_solution": trajectory[-1].copy(), "best_value": float(values[-1]),
        "initial_point": trajectory[0].copy(), "trajectory": trajectory,
        "value_history": np.asarray(values), "evaluation_history": np.asarray(evaluations),
        "function_evaluations": int(evaluations[-1]), "gradient_evaluations": 0,
        "iterations_completed": len(trajectory) - 1,
        "status": "completed" if np.isfinite(values[-1]) else "diverged",
    }
