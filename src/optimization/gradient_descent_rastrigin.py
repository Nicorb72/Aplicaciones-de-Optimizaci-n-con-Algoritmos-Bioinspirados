import numpy as np

from .rastrigin import rastrigin, rastrigin_gradient


def run_gradient_descent_rastrigin(initial_point=None, learning_rate=1e-3, iterations=1000, punto_inicial=None, i=None):
    if initial_point is None:
        initial_point = punto_inicial
    if i is not None:
        iterations = i
    x = np.asarray(initial_point, dtype=float).copy()
    trajectory = [x.copy()]
    function_evaluations = 0
    gradient_evaluations = 0
    status = "completed"
    for _ in range(iterations):
        with np.errstate(over="ignore", invalid="ignore"):
            grad = rastrigin_gradient(x)
            gradient_evaluations += 1
            next_x = x - learning_rate * grad
        if not np.all(np.isfinite(grad)) or not np.all(np.isfinite(next_x)):
            status = "diverged"
            break
        x = next_x
        trajectory.append(x.copy())
    with np.errstate(over="ignore", invalid="ignore"):
        final_value = float(rastrigin(x))
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
        "Mejor_solucion": x,
        "Mejor_valor": final_value,
        "trayectoria": np.asarray(trajectory),
        "funcion_de_evaluacion": function_evaluations,
        "Evaluacion_del_gradiante": gradient_evaluations,
        "estado": "completado" if status == "completed" else "divergieron",
        "iteraciones_completadas": len(trajectory) - 1,
    }
