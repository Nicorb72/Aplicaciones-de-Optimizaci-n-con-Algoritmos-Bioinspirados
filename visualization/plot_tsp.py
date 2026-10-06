"""Visualización del TSP sobre el mapa de capitales peninsulares de España."""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

from tsp.cost_model import load_tsp_data, calculate_tour_cost


def plot_spain_tour(tour, cost_matrix, output_path, title=None, data_dir=None):
    """Genera una imagen estática con el recorrido sobre las 47 capitales de España."""
    data = load_tsp_data(data_dir)
    capitals = data["capitals"]
    lons = np.array([c["lon"] for c in capitals])
    lats = np.array([c["lat"] for c in capitals])

    tour = np.asarray(tour, dtype=int)
    closed_tour = np.append(tour, tour[0])
    cost = calculate_tour_cost(tour, cost_matrix)

    fig, ax = plt.subplots(figsize=(10, 8), facecolor="#fcfbfa")
    ax.set_facecolor("#f6f8fb")

    # Trazar recorrido
    ax.plot(
        lons[closed_tour], lats[closed_tour],
        color="#2b5c8f", linewidth=1.8, alpha=0.85, zorder=2,
        label="Ruta óptima",
    )

    # Trazar ciudades
    ax.scatter(
        lons, lats,
        color="#c83e4d", edgecolor="#ffffff", s=45, zorder=3,
        label="Capitales (47)",
    )

    # Resaltar ciudad de salida (Madrid o tour[0])
    start = tour[0]
    ax.scatter(
        [lons[start]], [lats[start]],
        color="#f39c12", marker="*", s=160, edgecolor="#ffffff", zorder=4,
        label=f"Salida: {capitals[start]['city']}",
    )

    # Nombres de capitales seleccionadas para no saturar
    key_cities = {"Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "A Coruña", "Zaragoza", "Málaga"}
    for c in capitals:
        if c["city"] in key_cities:
            ax.annotate(
                c["city"], (c["lon"], c["lat"]),
                textcoords="offset points", xytext=(4, 4), fontsize=8,
                weight="bold", color="#2c3e50",
            )

    ax.set_xlim(-9.8, 3.8)
    ax.set_ylim(35.8, 44.2)
    ax.set_xlabel("Longitud (°)", fontsize=10)
    ax.set_ylabel("Latitud (°)", fontsize=10)

    if title is None:
        title = f"Recorrido TSP — 47 Capitales de España (Costo: {cost:.2f} €)"
    ax.set_title(title, fontsize=12, weight="bold", pad=12)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend(loc="lower left", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def animate_tsp_tour_evolution(tour_evolution, cost_matrix, output_gif_path, fps=5, data_dir=None):
    """
    Genera un GIF animado mostrando la evolución del mejor recorrido en el mapa.
    tour_evolution: lista de tuplas (iteración, tour, costo).
    """
    if not tour_evolution:
        raise ValueError("tour_evolution no puede estar vacío.")

    data = load_tsp_data(data_dir)
    capitals = data["capitals"]
    lons = np.array([c["lon"] for c in capitals])
    lats = np.array([c["lat"] for c in capitals])

    fig, ax = plt.subplots(figsize=(10, 8), facecolor="#fcfbfa")
    ax.set_facecolor("#f6f8fb")
    ax.scatter(lons, lats, color="#c83e4d", edgecolor="#ffffff", s=40, zorder=3)

    line, = ax.plot([], [], color="#2b5c8f", linewidth=1.8, alpha=0.85, zorder=2)
    start_pt, = ax.plot([], [], "*", color="#f39c12", markersize=14, zorder=4)

    title_text = ax.text(
        0.03, 0.95, "", transform=ax.transAxes,
        fontsize=11, weight="bold", color="#2c3e50",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#bdc3c7", alpha=0.9),
    )

    ax.set_xlim(-9.8, 3.8)
    ax.set_ylim(35.8, 44.2)
    ax.set_xlabel("Longitud (°)", fontsize=10)
    ax.set_ylabel("Latitud (°)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.3)

    def init():
        line.set_data([], [])
        start_pt.set_data([], [])
        title_text.set_text("")
        return line, start_pt, title_text

    def update(frame):
        it, tour, cost = tour_evolution[frame]
        closed = np.append(tour, tour[0])
        line.set_data(lons[closed], lats[closed])
        start_pt.set_data([lons[tour[0]]], [lats[tour[0]]])
        title_text.set_text(f"Iteración/Generación: {it} | Costo total: {cost:.2f} €")
        return line, start_pt, title_text

    anim = FuncAnimation(fig, update, frames=len(tour_evolution), init_func=init, blit=False)
    output_gif_path = Path(output_gif_path)
    output_gif_path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(output_gif_path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return output_gif_path
