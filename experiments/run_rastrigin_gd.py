from optimization.gradient_descent_rastrigin import run_gradient_descent_rastrigin
from results.animations.rastrigin_animation import animate_trajectory
from pathlib import Path
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
    args = parser.parse_args()
    with open(args.config, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    output_dir = Path(config["output_dir"])
    if not output_dir.is_absolute():
        output_dir = Path(__file__).resolve().parents[1] / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for dimension in config["dimensions"]:
        result = _run_single(config, dimension)
        gif_path = output_dir / f"rastrigin_gd_{dimension}d.gif"
        last_move = animate_trajectory(result["trajectory"], config["domain"], gif_path)
        print(
            f"[{dimension}D] seed={result['seed']}, status={result['status']}, "
            f"x0={np.round(result['initial_point'], 4)}"
        )
        print(
            f"      x_final={np.round(result['best_solution'], 4)}, "
            f"f_final={result['best_value']:.6g}, "
            f"iteraciones={result['iterations_completed']} (convergió hacia la iteración {last_move})"
        )
        print(f"      GIF guardado en: {gif_path}")