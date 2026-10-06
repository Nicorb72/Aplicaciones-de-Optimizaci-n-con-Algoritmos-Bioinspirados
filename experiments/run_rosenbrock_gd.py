import argparse
from pathlib import Path

import numpy as np
import yaml

from optimization.gradient_descent_rosenbrock import run_gradient_descent_rosenbrock
from optimization.result_storage import save_results
from optimization.statistics import summarize_results


def run_experiment(config_path):
    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return _run_single(config)


def _run_single(config, seed=None):
    if config["function"] != "rosenbrock":
        raise ValueError("Este experimento solo admite la función Rosenbrock.")
    if seed is None:
        seed = config["seed"]
    rng = np.random.default_rng(seed)
    initial_point = rng.uniform(
        config["domain"]["lower"], config["domain"]["upper"], size=config["dimension"]
    )
    result = run_gradient_descent_rosenbrock(
        initial_point,
        learning_rate=config["learning_rate"],
        iterations=config["iterations"],
    )
    result["initial_point"] = initial_point
    result["seed"] = seed
    return result


def run_experiments(config_path):
    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
    runs = config["runs"]
    if type(runs) is not int or runs < 1:
        raise ValueError("runs debe ser un entero positivo.")
    return [_run_single(config, config["seed"] + i) for i in range(runs)]


def run_and_save(config_path):
    """Ejecuta las corridas, guarda sus archivos e imprime el resumen."""
    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
    results = run_experiments(config_path)
    summary = summarize_results(results, config["success_threshold"])
    output_dir = Path(config["output_dir"])
    if not output_dir.is_absolute():
        output_dir = Path(__file__).resolve().parents[1] / output_dir
    output_dir = output_dir / f"{config['dimension']}d"
    save_results(results, summary, config, output_dir)
    for index, result in enumerate(results, start=1):
        print(
            f"Corrida {index}: seed={result['seed']}, status={result['status']}, "
            f"iteraciones={result['iterations_completed']}, f_final={result['best_value']:.6g}"
        )
    print("\nResumen de valores finales de corridas completadas y finitas:")
    print(
        f"Corridas: {summary['runs']}; completadas: {summary['completed_runs']}; "
        f"divergentes: {summary['diverged_runs']}"
    )
    print(f"Incluidas en estadísticas: {summary['included_runs']}; excluidas: {summary['excluded_runs']}")
    for label, key in [
        ("Media", "mean_value"), ("Desviación estándar muestral", "std_value"),
        ("Mejor valor", "best_value"), ("Peor valor", "worst_value"),
    ]:
        value = summary[key]
        print(f"{label}: {value:.6g}" if value is not None else f"{label}: no definida")
    print(
        f"Éxitos (f <= {summary['success_threshold']:.6g}, estado completed): "
        f"{summary['successful_runs']}/{summary['runs']} ({summary['success_rate']:.2%})"
    )
    print(f"Archivos guardados en: {output_dir}")
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta GD sobre Rosenbrock con inicio aleatorio.")
    parser.add_argument(
        "--config", type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "rosenbrock.yaml",
    )
    args = parser.parse_args()
    run_and_save(args.config)
