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
from optimization.rastrigin import rastrigin


def rosenbrock_isosurface(x1, x2, level):
    """Despeja x3 en f(x1,x2,x3)=level; devuelve las dos ramas de la superficie."""
    base = 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2 + (1 - x2) ** 2
    offset = np.sqrt(np.maximum(level - base, 0) / 100)
    return tuple(np.where(base <= level, x2 ** 2 + sign * offset, np.nan) for sign in (-1, 1))


def animation_positions(trajectory, frames, pacing="iterations", populations=None):
    """Devuelve tiempos de la trayectoria, fraccionarios solo en modo movement.

    El 90% del tiempo visual sigue la distancia recorrida y el 10% las
    iteraciones. Así los tramos casi inmóviles no monopolizan la animación.
    En PSO se mide el desplazamiento conjunto de las partículas reales.
    """
    if pacing not in ("iterations", "movement"):
        raise ValueError("pacing debe ser iterations o movement.")
    last = len(trajectory) - 1
    if pacing == "iterations" or last == 0:
        return np.linspace(0, last, min(frames, last + 1), dtype=int)
    points = trajectory if populations is None else populations
    steps = np.diff(points, axis=0).reshape(last, -1)
    distances = np.linalg.norm(steps, axis=1)
    total = distances.sum()
    weights = 0.9 * distances / total + 0.1 / last if total > 0 else np.full(last, 1 / last)
    clock = np.concatenate(([0.], np.cumsum(weights)))
    positions = np.interp(np.linspace(0, clock[-1], frames), clock, np.arange(last + 1))
    positions[0], positions[-1] = 0, last
    return positions


def interpolate_position(points, position):
    """Interpola solo entre dos estados consecutivos; no ejecuta el algoritmo."""
    left = int(position)
    fraction = position - left
    if fraction == 0:
        return points[left].copy()
    return points[left] + fraction * (points[left + 1] - points[left])


def animate_saved(results_dir, output_dir, run_id="run_001", frames=120, fps=10, pacing="iterations"):
    """Genera un GIF 2D o 3D; frames limita fotogramas, no iteraciones de GD."""
    if type(frames) is not int or frames < 2:
        raise ValueError("frames debe ser un entero mayor o igual a 2.")
    if type(fps) is not int or not 1 <= fps <= 100:
        raise ValueError("fps debe ser un entero entre 1 y 100.")
    results_dir = Path(results_dir)
    payload = json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
    dimension = payload["config"]["dimension"]
    if dimension not in (2, 3):
        raise ValueError("Esta animación admite únicamente dimensiones 2D o 3D.")
    config = payload["config"]
    name, method = config["function"], config.get("method", "gd")
    objective = {"rosenbrock": rosenbrock, "rastrigin": rastrigin}[name]
    minimum = np.ones(dimension) if name == "rosenbrock" else np.zeros(dimension)
    with (results_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    selected = next((row for row in rows if row["run_id"] == run_id), None)
    if selected is None or selected["status"] != "completed" or not np.isfinite(float(selected["final_value"])):
        raise ValueError("run_id debe identificar una corrida completada con valor final finito.")
    with np.load(results_dir / "trajectories.npz", allow_pickle=False) as data:
        trajectory = data[run_id]
    populations = None
    if method == "pso":
        with np.load(results_dir / "populations.npz", allow_pickle=False) as data:
            populations = data[run_id]
    indices = animation_positions(trajectory, frames, pacing, populations)

    points = trajectory if populations is None else populations.reshape(-1, dimension)
    lower = np.minimum(points.min(axis=0), minimum)
    upper = np.maximum(points.max(axis=0), minimum)
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
        Z = np.array([[objective([xi, yi]) for xi in x] for yi in y])
        levels = np.geomspace(1e-4, Z.max(), 28)
        cmap = LinearSegmentedColormap.from_list("valley", ["#fff8ed", "#f9dce6", "#e4cee9", "#baa5d2"])
        ax.contourf(X, Y, Z, levels=levels, cmap=cmap, norm=LogNorm(), extend="min", zorder=0)
        ax.contour(X, Y, Z, levels=levels[::2], colors=palette["lavender"], alpha=0.4, linewidths=0.6, zorder=1)
        ax.set_aspect("equal")
    else:
        # Los tres ejes son coordenadas de entrada; f(x) aparece en la tarjeta.
        if name == "rosenbrock":
            X, Y = np.meshgrid(np.linspace(lower[0] - padding[0], upper[0] + padding[0], 100),
                               np.linspace(lower[1] - padding[1], upper[1] + padding[1], 100))
            for level, color in [(10.0, "#b49bd0"), (1.0, "#ed9bbf")]:
                for surface in rosenbrock_isosurface(X, Y, level):
                    surface = np.where((surface >= lower[2] - padding[2]) & (surface <= upper[2] + padding[2]), surface, np.nan)
                    if np.count_nonzero(np.isfinite(surface)) >= 4:
                        ax.plot_surface(X, Y, surface, color=color, alpha=0.23, linewidth=0,
                                        rcount=40, ccount=40, shade=False)
            ax.text2D(0.01, 0.96, "Superficies: f = 1 (rosa), f = 10 (lavanda)",
                      transform=ax.transAxes, fontsize=8, color=palette["text"])
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
    line, = ax.plot([], [], color=palette["rose"], linewidth=2, label="Recorrido" if method == "gd" else "Mejor conocido", zorder=4)
    halo, = ax.plot([], [], "o", color=palette["rose"], markersize=19, alpha=0.12, zorder=5)
    point, = ax.plot([], [], marker="$\\heartsuit$", color=palette["rose"], markersize=12, markeredgecolor=palette["panel"], markeredgewidth=0.6, label="Punto actual", zorder=6)
    ax.scatter(*trajectory[0], facecolor=palette["panel"], edgecolor=palette["text"], s=40, label="Inicio", zorder=5)
    ax.scatter(*minimum, color=palette["gold"], marker="*", s=150, edgecolor=palette["background"], label="Mínimo global", zorder=5)
    swarm = None
    if populations is not None:
        swarm, = ax.plot([], [], linestyle="None", marker="o", color=palette["lavender"], markersize=4, alpha=0.65)
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
    panel.text(0.08, 0.66, "VALOR EN EL PUNTO DIBUJADO" if pacing == "movement" else "VALOR DE LA FUNCIÓN", color=palette["muted"], fontsize=9)
    value_label = panel.text(0.08, 0.55, "", color=palette["text"], fontsize=25, family="DejaVu Sans Mono")
    panel.text(0.08, 0.42, "ITERACIÓN", color=palette["muted"], fontsize=9)
    title = panel.text(0.08, 0.34, "", color=palette["text"], fontsize=16, family="DejaVu Sans Mono")
    panel.add_patch(Rectangle((0.08, 0.25), 0.84, 0.018, facecolor=palette["border"]))
    progress = Rectangle((0.08, 0.25), 0, 0.018, facecolor=palette["rose"])
    panel.add_patch(progress)
    progress_label = panel.text(0.92, 0.17, "", ha="right", color=palette["muted"], fontsize=10)
    detail = (f"Tasa de aprendizaje  {config.get('learning_rate', config.get('parameters', {}).get('learning_rate', 0)):g}"
              if method == "gd" else f"Enjambre: {populations.shape[1]} partículas lavanda" if populations is not None else "Mejor punto conocido")
    panel.text(0.08, 0.075, detail, color=palette["muted"], fontsize=9)
    for tape_x, angle in [(0.25, 3), (0.75, -3)]:
        fig.add_artist(Rectangle((tape_x, 0.837), 0.09, 0.022, angle=angle, transform=fig.transFigure, facecolor=palette["tape"], alpha=0.65, zorder=10))
    fig.text(0.07, 0.925, name.capitalize(), color=palette["rose"], fontsize=30, family="DejaVu Serif", style="italic")
    fig.text(0.355, 0.933, "$\\heartsuit$", color=palette["lavender"], fontsize=20, rotation=12)
    dimension_label = "DOS" if dimension == 2 else "TRES"
    method_label = {"gd": "DESCENSO POR GRADIENTE", "pso": "ENJAMBRE DE PARTÍCULAS", "evolutionary": "EVOLUTIVO", "de": "EVOLUCIÓN DIFERENCIAL"}[method]
    fig.text(0.072, 0.878, f"{method_label}  /  {dimension_label} DIMENSIONES", color=palette["muted"], fontsize=9)
    fig.text(0.94, 0.93, f"{run_id.upper()}  ·  SEMILLA {selected['seed']}", ha="right", color=palette["muted"], fontsize=10)
    fig.text(0.94, 0.884, f"Umbral de éxito  {payload['summary']['success_threshold']:g}", ha="right", color=palette["muted"], fontsize=9)
    fig.text(
        0.07, 0.028,
        f"{len(indices)} fotogramas · {len(trajectory)} puntos guardados · {fps} fps · El recorrido conserva todos los puntos.\n"
        + ("Fuente: elaboración propia. Interpolación visual entre iteraciones; tiempo repartido por movimiento."
         if pacing == "movement" else "Fuente: elaboración propia. El tiempo de reproducción no representa el tiempo de cómputo."),
        fontsize=8, color=palette["muted"], linespacing=1.6,
    )

    def update(position):
        index = int(position)
        current = interpolate_position(trajectory, position)
        trail = trajectory[:index + 1]
        if position != index:
            trail = np.vstack((trail, current))
        if dimension == 2:
            line.set_data(trail.T)
            glow.set_data(line.get_data())
            point.set_data(current[:, None])
            halo.set_data(point.get_data())
        else:
            line.set_data_3d(trail.T)
            glow.set_data_3d(line.get_data_3d())
            point.set_data_3d(current[:, None])
            halo.set_data_3d(point.get_data_3d())
        if swarm is not None:
            population = interpolate_position(populations, position)
            if dimension == 2:
                swarm.set_data(population.T)
            else:
                swarm.set_data_3d(population.T)
        value = objective(current)
        value_label.set_text(f"{value:.3e}")
        iteration_label = f"≈ {position:.1f}" if position != index else str(index)
        title.set_text(f"{iteration_label} / {len(trajectory) - 1}")
        fraction = position / (len(trajectory) - 1) if len(trajectory) > 1 else 1.0
        progress.set_width(0.84 * fraction)
        progress_label.set_text(f"{fraction:.0%} de las iteraciones")
        if index == len(trajectory) - 1:
            state.set_text("Umbral alcanzado" if value <= payload["summary"]["success_threshold"] else "Recorrido completo")
        else:
            state.set_text("En progreso")
        artists = (line, point, title, glow, halo, value_label, progress, progress_label, state)
        return artists + (swarm,) if swarm is not None else artists

    output_dir = Path(output_dir) / f"{dimension}d"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"trajectory_{run_id}.gif"
    animation = FuncAnimation(fig, update, frames=indices, interval=1000 / fps, repeat=True)
    try:
        animation.save(path, writer=PillowWriter(fps=fps), dpi=100)
    finally:
        plt.close(fig)
    return path


def animate_rosenbrock(results_dir, output_dir, run_id="run_001", frames=120, fps=10, pacing="iterations"):
    """Nombre conservado para los comandos y pruebas anteriores de Persona 1."""
    return animate_saved(results_dir, output_dir, run_id, frames, fps, pacing)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Genera un GIF de Rosenbrock 2D o 3D desde una trayectoria guardada.")
    parser.add_argument("--results-dir", type=Path, default=root / "results/raw/rosenbrock_gd/2d")
    parser.add_argument("--output-dir", type=Path, default=root / "results/animations/rosenbrock_gd")
    parser.add_argument("--run-id", default="run_001")
    parser.add_argument("--frames", type=int, default=120, help="Máximo de fotogramas; incluye inicio y final.")
    parser.add_argument("--fps", type=int, default=10, help="Fotogramas por segundo (1 a 100).")
    parser.add_argument("--pacing", choices=["iterations", "movement"], default="iterations")
    args = parser.parse_args()
    path = animate_rosenbrock(args.results_dir, args.output_dir, args.run_id, args.frames, args.fps, args.pacing)
    print(f"GIF guardado en: {path}")
