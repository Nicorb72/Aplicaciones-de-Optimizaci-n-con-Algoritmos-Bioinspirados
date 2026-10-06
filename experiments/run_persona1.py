"""Ejecuta Rosenbrock + GD en 2D y 3D, sus gráficas y ambos GIF."""

import argparse
from pathlib import Path

import yaml

from experiments.run_rosenbrock_gd import run_and_save
from visualization.animations import animate_rosenbrock
from visualization.plot_rosenbrock import plot_rosenbrock


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-2d", type=Path, default=root / "configs/rosenbrock.yaml")
    parser.add_argument("--config-3d", type=Path, default=root / "configs/rosenbrock_3d.yaml")
    parser.add_argument("--figures-dir", type=Path, default=root / "results/figures/rosenbrock_gd")
    parser.add_argument("--animations-dir", type=Path, default=root / "results/animations/rosenbrock_gd")
    parser.add_argument("--run-id", default="run_001", help="Corrida completada para los GIF de ambas dimensiones.")
    parser.add_argument("--frames", type=int, default=120, help="Máximo de fotogramas del GIF (al menos 2).")
    parser.add_argument("--fps", type=int, default=10, help="Fotogramas por segundo (1 a 100).")
    args = parser.parse_args()

    configurations = [(2, args.config_2d), (3, args.config_3d)]
    for dimension, config_path in configurations:
        with config_path.open(encoding="utf-8") as file:
            config = yaml.safe_load(file)
        if config["function"] != "rosenbrock" or config["dimension"] != dimension:
            parser.error(f"{config_path} debe configurar Rosenbrock {dimension}D.")
    if args.frames < 2 or not 1 <= args.fps <= 100:
        parser.error("El GIF requiere frames >= 2 y fps entre 1 y 100.")

    for dimension, config_path in configurations:
        print(f"\n=== Rosenbrock {dimension}D ===", flush=True)
        results_dir = run_and_save(config_path)
        for path in plot_rosenbrock(results_dir, args.figures_dir):
            print(f"Figura guardada en: {path}", flush=True)
        print(f"Generando GIF {dimension}D…", flush=True)
        path = animate_rosenbrock(results_dir, args.animations_dir, args.run_id, args.frames, args.fps)
        print(f"GIF guardado en: {path}", flush=True)


if __name__ == "__main__":
    main()
