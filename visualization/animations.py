"""Animaciones de trayectorias guardadas de optimización."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

from optimization.rosenbrock import rosenbrock


def animate_rosenbrock(results_dir, output_dir, run_id="run_001", frames=120, fps=10):
    """Genera un GIF 2D o 3D; frames limita fotogramas, no iteraciones de GD."""
    if type(frames) is not int or frames < 2:
        raise ValueError("frames debe ser un entero mayor o igual a 2.")
    if type(fps) is not int or not 1 <= fps <= 100:
        raise ValueError("fps debe ser un entero entre 1 y 100.")
    results_dir = Path(results_dir)
    payload = json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
    dimension = payload["config"]["dimension"]
    if dimension not in (2, 3):
        raise ValueError("Esta animación admite únicamente Rosenbrock 2D o 3D.")
    with (results_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    selected = next((row for row in rows if row["run_id"] == run_id), None)
    if selected is None or selected["status"] != "completed" or not np.isfinite(float(selected["final_value"])):
        raise ValueError("run_id debe identificar una corrida completada con valor final finito.")
    with np.load(results_dir / "trajectories.npz", allow_pickle=False) as data:
        trajectory = data[run_id]
    indices = np.linspace(0, len(trajectory) - 1, min(frames, len(trajectory)), dtype=int)

    lower = np.minimum(trajectory.min(axis=0), 1.0)
    upper = np.maximum(trajectory.max(axis=0), 1.0)
    padding = np.maximum(0.15 * (upper - lower), 0.1)
    palette = {
        "background": "#fff7f3", "panel": "#fffcfa", "border": "#e7ccd9",
        "text": "#59384f", "muted": "#856575", "rose": "#b83b76",
        "lavender": "#8260aa", "gold": "#b8883d", "tape": "#f3bbd1",
    }
    fig = plt.figure(figsize=(10, 6.5), facecolor=palette["background"])
    ax = fig.add_axes([0.07, 0.205, 0.50, 0.64], projection="3d" if dimension == 3 else None, facecolor=palette["panel"])
    if dimension == 2:
        center = (lower + upper) / 2
        height = max(upper[1] - lower[1] + 2 * padding[1], (upper[0] - lower[0] + 2 * padding[0]) / 1.2)
        half_size = np.array([1.2 * height, height]) / 2
        x = np.linspace(center[0] - half_size[0], center[0] + half_size[0], 200)
        y = np.linspace(center[1] - half_size[1], center[1] + half_size[1], 200)
        X, Y = np.meshgrid(x, y)
        Z = np.array([[rosenbrock([xi, yi]) for xi in x] for yi in y])
        levels = np.geomspace(1e-4, Z.max(), 28)
        cmap = LinearSegmentedColormap.from_list("valley", ["#fff8ed", "#f9dce6", "#e4cee9", "#baa5d2"])
        ax.contourf(X, Y, Z, levels=levels, cmap=cmap, norm=LogNorm(), extend="min", zorder=0)
        ax.contour(X, Y, Z, levels=levels[::2], colors=palette["lavender"], alpha=0.4, linewidths=0.6, zorder=1)
        ax.set_aspect("equal")
    else:
        # Los tres ejes son coordenadas de entrada; f(x) aparece en la tarjeta.
        ax.set(xlim=(lower[0] - padding[0], upper[0] + padding[0]),
               ylim=(lower[1] - padding[1], upper[1] + padding[1]),
               zlim=(lower[2] - padding[2], upper[2] + padding[2]), zlabel="$x_3$")
        ax.set_box_aspect(upper - lower + 2 * padding)
        ax.view_init(elev=25, azim=-60)
        for axis, color in zip((ax.xaxis, ax.yaxis, ax.zaxis), ("#f9dce6", "#e4cee9", "#fff8ed")):
            axis.set_pane_color(color)
            axis.label.set_color(palette["muted"])
            axis.line.set_color(palette["border"])
    glow, = ax.plot([], [], color=palette["rose"], linewidth=7, alpha=0.12, zorder=3)
    line, = ax.plot([], [], color=palette["rose"], linewidth=2, label="Recorrido", zorder=4)
    halo, = ax.plot([], [], "o", color=palette["rose"], markersize=19, alpha=0.12, zorder=5)
    point, = ax.plot([], [], marker="$\\heartsuit$", color=palette["rose"], markersize=12, markeredgecolor=palette["panel"], markeredgewidth=0.6, label="Punto actual", zorder=6)
    ax.scatter(*trajectory[0], facecolor=palette["panel"], edgecolor=palette["text"], s=40, label="Inicio", zorder=5)
    ax.scatter(*np.ones(dimension), color=palette["gold"], marker="*", s=150, edgecolor=palette["background"], label="Mínimo global", zorder=5)
    ax.set(xlabel="$x_1$", ylabel="$x_2$")
    ax.tick_params(colors=palette["muted"], labelsize=9, length=3)
    ax.xaxis.label.set_color(palette["muted"])
    ax.yaxis.label.set_color(palette["muted"])
    for spine in ax.spines.values():
        spine.set_color(palette["border"])
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), ncol=4, frameon=False, labelcolor=palette["text"], fontsize=9, handlelength=1.6, columnspacing=1.1)

    # Una tarjeta de libreta: papel redondeado, renglones y cinta decorativa.
    panel = fig.add_axes([0.64, 0.205, 0.30, 0.64])
    panel.set(xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[])
    panel.set_axis_off()
    panel.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.04", facecolor=palette["panel"], edgecolor=palette["border"], clip_on=False, zorder=0))
    for ruled_y in np.arange(0.12, 0.9, 0.1):
        panel.axhline(ruled_y, xmin=0.04, xmax=0.96, color=palette["border"], linewidth=0.6, alpha=0.45, zorder=1)
    panel.text(0.08, 0.92, "notas del recorrido", color=palette["lavender"], fontsize=14, family="DejaVu Serif", style="italic")
    state = panel.text(0.08, 0.81, "En progreso", color=palette["rose"], fontsize=15, weight="bold")
    panel.text(0.08, 0.66, "VALOR DE LA FUNCIÓN", color=palette["muted"], fontsize=9)
    value_label = panel.text(0.08, 0.55, "", color=palette["text"], fontsize=25, family="DejaVu Sans Mono")
    panel.text(0.08, 0.42, "ITERACIÓN", color=palette["muted"], fontsize=9)
    title = panel.text(0.08, 0.34, "", color=palette["text"], fontsize=16, family="DejaVu Sans Mono")
    panel.add_patch(Rectangle((0.08, 0.25), 0.84, 0.018, facecolor=palette["border"]))
    progress = Rectangle((0.08, 0.25), 0, 0.018, facecolor=palette["rose"])
    panel.add_patch(progress)
    progress_label = panel.text(0.92, 0.17, "", ha="right", color=palette["muted"], fontsize=10)
    panel.text(0.08, 0.075, f"Tasa de aprendizaje  {payload['config']['learning_rate']:g}", color=palette["muted"], fontsize=9)
    for tape_x, angle in [(0.25, 3), (0.75, -3)]:
        fig.add_artist(Rectangle((tape_x, 0.837), 0.09, 0.022, angle=angle, transform=fig.transFigure, facecolor=palette["tape"], alpha=0.65, zorder=10))
    fig.text(0.07, 0.925, "Rosenbrock", color=palette["rose"], fontsize=30, family="DejaVu Serif", style="italic")
    fig.text(0.355, 0.933, "$\\heartsuit$", color=palette["lavender"], fontsize=20, rotation=12)
    dimension_label = "DOS" if dimension == 2 else "TRES"
    fig.text(0.072, 0.878, f"DESCENSO POR GRADIENTE  /  {dimension_label} DIMENSIONES", color=palette["muted"], fontsize=9)
    fig.text(0.94, 0.93, f"{run_id.upper()}  ·  SEMILLA {selected['seed']}", ha="right", color=palette["muted"], fontsize=10)
    fig.text(0.94, 0.884, f"Umbral de éxito  {payload['summary']['success_threshold']:g}", ha="right", color=palette["muted"], fontsize=9)
    fig.text(
        0.07, 0.028,
        f"{len(indices)} fotogramas · {len(trajectory)} puntos guardados · {fps} fps · El recorrido conserva todos los puntos.\n"
        "Fuente: elaboración propia. El tiempo de reproducción no representa el tiempo de cómputo.",
        fontsize=8, color=palette["muted"], linespacing=1.6,
    )

    def update(index):
        if dimension == 2:
            line.set_data(trajectory[:index + 1].T)
            glow.set_data(line.get_data())
            point.set_data(trajectory[index:index + 1].T)
            halo.set_data(point.get_data())
        else:
            line.set_data_3d(trajectory[:index + 1].T)
            glow.set_data_3d(line.get_data_3d())
            point.set_data_3d(trajectory[index:index + 1].T)
            halo.set_data_3d(point.get_data_3d())
        value = rosenbrock(trajectory[index])
        value_label.set_text(f"{value:.3e}")
        title.set_text(f"{index:,} / {len(trajectory) - 1:,}".replace(",", " "))
        fraction = index / (len(trajectory) - 1) if len(trajectory) > 1 else 1.0
        progress.set_width(0.84 * fraction)
        progress_label.set_text(f"{fraction:.0%} del recorrido")
        if index == len(trajectory) - 1:
            state.set_text("Umbral alcanzado" if value <= payload["summary"]["success_threshold"] else "Recorrido completo")
        else:
            state.set_text("En progreso")
        return line, point, title, glow, halo, value_label, progress, progress_label, state

    output_dir = Path(output_dir) / f"{dimension}d"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"trajectory_{run_id}.gif"
    animation = FuncAnimation(fig, update, frames=indices, interval=1000 / fps, repeat=True)
    try:
        animation.save(path, writer=PillowWriter(fps=fps), dpi=100)
    finally:
        plt.close(fig)
    return path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Genera un GIF de Rosenbrock 2D o 3D desde una trayectoria guardada.")
    parser.add_argument("--results-dir", type=Path, default=root / "results/raw/rosenbrock_gd/2d")
    parser.add_argument("--output-dir", type=Path, default=root / "results/animations/rosenbrock_gd")
    parser.add_argument("--run-id", default="run_001")
    parser.add_argument("--frames", type=int, default=120, help="Máximo de fotogramas; incluye inicio y final.")
    parser.add_argument("--fps", type=int, default=10, help="Fotogramas por segundo (1 a 100).")
    args = parser.parse_args()
    path = animate_rosenbrock(args.results_dir, args.output_dir, args.run_id, args.frames, args.fps)
    print(f"GIF guardado en: {path}")
