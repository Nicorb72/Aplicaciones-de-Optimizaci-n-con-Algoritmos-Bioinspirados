"""Ejecuta una configuración de la Parte 1 y resume resultados y costos."""
import numpy as np

from .rosenbrock import rosenbrock
from .rastrigin import rastrigin
from .gradient_descent_rosenbrock import run_gradient_descent_rosenbrock
from .gradient_descent_rastrigin import run_gradient_descent_rastrigin
from .pso import run_pso
from .evolutionary import run_evolutionary
from .differential_evolution import run_differential_evolution
from .statistics import summarize_results

FUNCTIONS = {"rosenbrock": rosenbrock, "rastrigin": rastrigin}
METHODS = {"pso": run_pso, "evolutionary": run_evolutionary, "de": run_differential_evolution}
GD = {"rosenbrock": run_gradient_descent_rosenbrock, "rastrigin": run_gradient_descent_rastrigin}


def run_configuration(config):
    """Cada corrida usa seed + índice; los contadores son los del optimizador."""
    name, method, dimension = config["function"], config["method"], config["dimension"]
    if name not in FUNCTIONS or method not in {"gd", *METHODS} or dimension not in (2, 3):
        raise ValueError("Función, método o dimensión no admitidos en la Parte 1.")
    if type(config["runs"]) is not int or config["runs"] < 1:
        raise ValueError("runs debe ser un entero positivo.")
    low, high = config["domain"]["lower"], config["domain"]["upper"]
    if not np.isfinite(low) or not np.isfinite(high) or low >= high:
        raise ValueError("El dominio debe tener límites finitos y ordenados.")
    parameters = config["parameters"]
    results = []
    for i in range(config["runs"]):
        seed = config["seed"] + i
        if method == "gd":
            if type(parameters["iterations"]) is not int or parameters["iterations"] < 0:
                raise ValueError("iterations debe ser un entero no negativo.")
            if not np.isfinite(parameters["learning_rate"]) or parameters["learning_rate"] <= 0:
                raise ValueError("learning_rate debe ser finita y positiva.")
            initial = np.random.default_rng(seed).uniform(low, high, size=dimension)
            result = GD[name](initial, **parameters)
            result["initial_point"] = initial
        else:
            result = METHODS[method](FUNCTIONS[name], [(low, high)] * dimension, seed=seed, **parameters)
        result["seed"] = seed
        results.append(result)
    summary = summarize_results(results, config["success_threshold"])
    # Promedios sobre TODAS las corridas, incluidas las que divergieron.
    for key in ("function_evaluations", "gradient_evaluations"):
        summary[f"mean_{key}"] = float(np.mean([r[key] for r in results]))
    summary["mean_equivalent_evaluations"] = summary["mean_function_evaluations"] + 2 * dimension * summary["mean_gradient_evaluations"]
    summary["gradient_equivalence_factor"] = 2 * dimension
    return results, summary
