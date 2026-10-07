"""Gráficas desde archivos guardados; sus evaluaciones no cuentan como optimización."""
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from optimization.benchmark import FUNCTIONS


def select_run(results_dir):
    with (Path(results_dir) / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = [r for r in csv.DictReader(file) if r["status"] == "completed" and np.isfinite(float(r["final_value"]))]
    row = next((r for r in rows if r["success"] == "True"), rows[0] if rows else None)
    return row["run_id"] if row else None


def plot_configuration(results_dir, output_dir):
    results_dir, output_dir = Path(results_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
    config, summary = payload["config"], payload["summary"]
    name, method, dimension = config["function"], config["method"], config["dimension"]
    objective = FUNCTIONS[name]
    selected = select_run(results_dir)
    with (results_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    fig, ax = plt.subplots(figsize=(8, 5))
    with np.load(results_dir / "trajectories.npz", allow_pickle=False) as trajectories:
        for row in rows:
            if row["status"] != "completed" or not np.isfinite(float(row["final_value"])):
                continue
            points = trajectories[row["run_id"]]
            values = np.array([objective(point) for point in points])
            ax.plot(np.maximum(values, 1e-16), color="#b83b76" if row["run_id"] == selected else "#8260aa",
                    alpha=1 if row["run_id"] == selected else 0.2,
                    label=selected if row["run_id"] == selected else None)
        ax.axhline(max(summary["success_threshold"], 1e-16), color="black", linestyle="--", label="Umbral")
        ax.set(yscale="log", xlabel="Iteración / generación", ylabel="f del punto GD" if method == "gd" else "Mejor f conocido",
               title=f"Convergencia · {name.capitalize()} {dimension}D · {method.upper()}")
        ax.legend()
        ax.grid(alpha=0.2)
        fig.text(0.02, 0.02, f"Fuente: elaboración propia. Éxitos: {summary['successful_runs']}/{summary['runs']}; divergencias: {summary['diverged_runs']}.\n"
                 "Solo corridas completadas y finitas. Valores < 1e-16 se dibujan en 1e-16 para la escala logarítmica.", fontsize=8)
        fig.tight_layout(rect=(0, 0.1, 1, 1))
        fig.savefig(output_dir / "convergence.png", dpi=120)
        plt.close(fig)
        if selected is None:
            (output_dir / "trajectory.png").unlink(missing_ok=True)
            return
        trajectory = trajectories[selected]
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d" if dimension == 3 else None)
    if dimension == 2:
        low = np.minimum(trajectory.min(axis=0), config["domain"]["lower"])
        high = np.maximum(trajectory.max(axis=0), config["domain"]["upper"])
        x, y = np.linspace(low[0], high[0], 120), np.linspace(low[1], high[1], 120)
        X, Y = np.meshgrid(x, y)
        Z = np.array([[objective([a, b]) for a in x] for b in y])
        ax.contour(X, Y, Z, levels=np.geomspace(1e-3, max(Z.max(), 1), 20), colors="#b49bd0", linewidths=0.6)
        ax.set_aspect("equal")
    else:
        ax.set_zlabel("x3")
    ax.plot(*trajectory.T, color="#b83b76", label="GD" if method == "gd" else "Mejor conocido (no un individuo)")
    ax.scatter(*trajectory[0], color="#8260aa", label="Inicio")
    ax.scatter(*trajectory[-1], color="#b83b76", label="Final")
    minimum = np.ones(dimension) if name == "rosenbrock" else np.zeros(dimension)
    ax.scatter(*minimum, marker="*", s=120, color="#b8883d", label="Mínimo global")
    ax.set(xlabel="x1", ylabel="x2", title=f"Trayectoria · {name.capitalize()} {dimension}D · {method.upper()}")
    ax.legend(fontsize=8)
    fig.text(0.02, 0.02, f"Fuente: elaboración propia. Corrida {selected}; selección: primera exitosa, o primera completada si no hay éxitos.", fontsize=8)
    fig.savefig(output_dir / "trajectory.png", dpi=120)
    plt.close(fig)
