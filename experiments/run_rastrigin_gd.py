from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from optimization.gradient_descent_rastrigin import run_gradient_descent_rastrigin
from optimization.benchmark import run_configuration
from optimization.result_storage import save_results
from visualization.animations import animate_saved
from visualization.plot_benchmark import plot_configuration, select_run
import argparse
import numpy as np
import yaml





def run_experiment(config_path, dimension):
    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return _run_single(config, dimension)


def _run_single(config, dimension, seed=None):
    if config["function"] != "rastrigin":
        raise ValueError("Este experimento solo admite la función Rastrigin.")
    if seed is None:
        seed = config["seed"]
    rng = np.random.default_rng(seed)
    initial_point = rng.uniform(
        config["domain"]["lower"], config["domain"]["upper"], size=dimension
    )
    result = run_gradient_descent_rastrigin(
        initial_point,
        learning_rate=config["learning_rate"],
        iterations=config["iterations"],
    )
    result["initial_point"] = initial_point
    result["seed"] = seed
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ejecuta GD sobre Rastrigin (2D y 3D) con inicio aleatorio y genera los GIF."
    )
    parser.add_argument(
        "--config", type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "rastrigin.yaml",
    )
    parser.add_argument("--frames", type=int, default=30)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--figures-dir", type=Path, default=ROOT / "results/figures/rastrigin_gd")
    parser.add_argument("--animations-dir", type=Path, default=ROOT / "results/animations/rastrigin_gd")
    args = parser.parse_args()
    if args.frames < 2 or not 1 <= args.fps <= 100:
        parser.error("Se requiere frames >= 2 y fps entre 1 y 100.")
    with open(args.config, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    output_dir = Path(config["output_dir"])
    if not output_dir.is_absolute():
        output_dir = Path(__file__).resolve().parents[1] / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for dimension in config["dimensions"]:
        experiment = {"function": config["function"], "method": "gd", "dimension": dimension,
                      "domain": config["domain"], "runs": config["runs"], "seed": config["seed"],
                      "success_threshold": config["success_threshold"],
                      "parameters": {"learning_rate": config["learning_rate"], "iterations": config["iterations"]}}
        results, summary = run_configuration(experiment)
        raw = save_results(results, summary, experiment, output_dir / f"{dimension}d")
        plot_configuration(raw, args.figures_dir / f"{dimension}d")
        run_id = select_run(raw)
        if run_id:
            gif_path = animate_saved(raw, args.animations_dir, run_id, args.frames, args.fps)
            print(f"GIF guardado en: {gif_path}", flush=True)
        print(f"Rastrigin {dimension}D: {summary}", flush=True)
