import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from optimization.rosenbrock import rosenbrock


def plot_rosenbrock(results_dir, output_dir, run_id=None):
    """Grafica datos guardados; las evaluaciones para dibujar no son costo de GD."""
    results_dir = Path(results_dir)
    payload = json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
    config, summary = payload["config"], payload["summary"]
    dimension = config["dimension"]
    if dimension not in (2, 3):
        raise ValueError("Las gráficas admiten únicamente dimensiones 2 y 3.")
    with (results_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    completed = [row for row in rows if row["status"] == "completed" and np.isfinite(float(row["final_value"]))]
    if run_id is None:
        selected = next((row for row in completed if row["success"] == "True"), completed[0] if completed else None)
    else:
        selected = next((row for row in completed if row["run_id"] == run_id), None)
        if selected is None:
            raise ValueError("run_id debe identificar una corrida completada con valor final finito.")
    output_dir = Path(output_dir) / f"{dimension}d"
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    figure_number = 1 if dimension == 2 else 3
    with np.load(results_dir / "trajectories.npz", allow_pickle=False) as trajectories:
        fig, ax = plt.subplots(figsize=(8, 5))
        for row in completed:
            trajectory = trajectories[row["run_id"]]
            values = np.array([rosenbrock(point) for point in trajectory])
            highlighted = row == selected
            ax.plot(
                np.maximum(values, 1e-16),
                color="tab:orange" if highlighted else "tab:blue",
                alpha=1.0 if highlighted else 0.25,
                label=f"{row['run_id']} · semilla {row['seed']}" if highlighted else None,
                zorder=3 if highlighted else 2,
            )
        ax.set_yscale("log")
        ax.axhline(max(summary["success_threshold"], 1e-16), color="black", linestyle="--", label="Umbral de éxito")
        if not completed:
            ax.text(0.5, 0.5, "No hay corridas completadas con valor final finito.", transform=ax.transAxes, ha="center")
        ax.set(xlabel="Iteración", ylabel="Valor de Rosenbrock f(x)", title=f"Figura {figure_number}. Convergencia de GD · Rosenbrock {dimension}D")
        ax.grid(True, alpha=0.2)
        ax.legend()
        fig.text(
            0.02, 0.02,
            f"Curvas incluidas: {len(completed)}/{len(rows)}; divergencias: {summary['diverged_runs']}. "
            f"Éxitos: {summary['successful_runs']}/{summary['runs']}; umbral: {summary['success_threshold']:g}.\n"
            "Solo para la escala logarítmica, f < 1e-16 se dibuja en 1e-16.\n"
            "Fuente: elaboración propia a partir de las corridas guardadas.",
            fontsize=8,
        )
        fig.tight_layout(rect=(0, 0.14, 1, 1))
        path = output_dir / "convergence.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        paths.append(path)

        if selected is not None:
            trajectory = trajectories[selected["run_id"]]
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d" if dimension == 3 else None)
            if dimension == 2:
                lower = np.minimum(trajectory.min(axis=0), config["domain"]["lower"])
                upper = np.maximum(trajectory.max(axis=0), config["domain"]["upper"])
                lower, upper = np.minimum(lower, 1.0), np.maximum(upper, 1.0)
                padding = np.maximum(0.05 * (upper - lower), 0.1)
                x = np.linspace(lower[0] - padding[0], upper[0] + padding[0], 200)
                y = np.linspace(lower[1] - padding[1], upper[1] + padding[1], 200)
                X, Y = np.meshgrid(x, y)
                Z = np.array([[rosenbrock([xi, yi]) for xi in x] for yi in y])
                ax.contour(X, Y, Z, levels=np.geomspace(1e-3, Z.max(), 20), colors="0.7", linewidths=0.7)
                ax.set_aspect("equal")
            else:
                ax.set_zlabel("x3")
            ax.plot(*trajectory.T, color="tab:blue", label="Trayectoria GD")
            ax.scatter(*trajectory[0], color="tab:green", s=50, label="Inicio")
            ax.scatter(*trajectory[-1], color="tab:red", s=45, label="Final")
            ax.scatter(*np.ones(dimension), color="black", marker="*", s=110, label="Mínimo global")
            ax.set(xlabel="x1", ylabel="x2", title=f"Figura {figure_number + 1}. Trayectoria de GD · Rosenbrock {dimension}D")
            ax.legend(loc="upper left")
            fig.text(
                0.02, 0.02,
                f"{selected['run_id']} · semilla {selected['seed']} · f final = {float(selected['final_value']):.6g}\n"
                "Fuente: elaboración propia a partir de la trayectoria guardada.",
                fontsize=9,
            )
            fig.subplots_adjust(bottom=0.15, top=0.9)
            path = output_dir / f"trajectory_{selected['run_id']}.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            plt.close(fig)
            paths.append(path)
    return paths


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Genera gráficas de Rosenbrock desde resultados guardados.")
    parser.add_argument("--results-dir", type=Path, default=root / "results/raw/rosenbrock_gd/2d")
    parser.add_argument("--output-dir", type=Path, default=root / "results/figures/rosenbrock_gd")
    parser.add_argument("--run-id", help="Corrida completada que se dibujará; por defecto, la primera exitosa, o la primera completada si no hay éxitos.")
    args = parser.parse_args()
    for path in plot_rosenbrock(args.results_dir, args.output_dir, args.run_id):
        print(f"Figura guardada en: {path}")
