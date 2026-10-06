"""Modelo de costos para el TSP de las 47 capitales peninsulares de España."""

import csv
from pathlib import Path
import numpy as np
import yaml


def get_default_data_dir():
    root = Path(__file__).resolve().parents[2]
    return root / "data" / "tsp"


def load_tsp_data(data_dir=None):
    """Carga las capitales, matrices de distancia, tiempo y peajes, y especificaciones del vehículo."""
    if data_dir is None:
        data_dir = get_default_data_dir()
    else:
        data_dir = Path(data_dir)

    capitals = []
    with (data_dir / "spain_capitals.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            capitals.append({
                "id": int(row["id"]),
                "city": row["city"],
                "province": row["province"],
                "region": row["region"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
            })

    matrices = np.load(data_dir / "matrices.npz")
    distances_km = matrices["distances_km"]
    times_hours = matrices["times_hours"]
    tolls_eur = matrices["tolls_eur"]

    with (data_dir / "vehicle_specs.yaml").open(encoding="utf-8") as f:
        specs = yaml.safe_load(f)

    return {
        "capitals": capitals,
        "distances_km": distances_km,
        "times_hours": times_hours,
        "tolls_eur": tolls_eur,
        "specs": specs,
    }


def compute_total_cost_matrix(
    hourly_rate=25.0,
    consumption_l_per_100km=5.4,
    fuel_price_eur_per_l=1.58,
    data_dir=None,
):
    """Calcula la matriz completa de costos C_ij en euros."""
    data = load_tsp_data(data_dir)
    distances_km = data["distances_km"]
    times_hours = data["times_hours"]
    tolls_eur = data["tolls_eur"]

    fuel_cost = (consumption_l_per_100km / 100.0) * distances_km * fuel_price_eur_per_l
    time_cost = hourly_rate * times_hours
    total_cost = time_cost + tolls_eur + fuel_cost

    np.fill_diagonal(total_cost, 0.0)
    return total_cost


def calculate_tour_cost(tour, cost_matrix):
    """Calcula el costo total de un recorrido cerrado tour (lista o array de índices de ciudades)."""
    tour = np.asarray(tour, dtype=int)
    n = len(tour)
    cost = 0.0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        cost += cost_matrix[u, v]
    return float(cost)


def get_tour_breakdown(tour, data_dir=None, hourly_rate=25.0):
    """Desglosa el costo de un recorrido en tiempo (horas y €), distancia, combustible y peajes."""
    data = load_tsp_data(data_dir)
    distances = data["distances_km"]
    times = data["times_hours"]
    tolls = data["tolls_eur"]
    specs = data["specs"]
    consumption = specs["vehicle"]["homologated_consumption_wltp_l_per_100km"]
    fuel_price = specs["fuel_price"]["price_eur_per_liter"]

    tour = np.asarray(tour, dtype=int)
    n = len(tour)

    total_dist = 0.0
    total_time = 0.0
    total_tolls = 0.0

    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        total_dist += distances[u, v]
        total_time += times[u, v]
        total_tolls += tolls[u, v]

    total_fuel = (consumption / 100.0) * total_dist * fuel_price
    total_time_cost = hourly_rate * total_time
    total_cost = total_time_cost + total_tolls + total_fuel

    return {
        "total_cost_eur": total_cost,
        "total_distance_km": total_dist,
        "total_time_hours": total_time,
        "fuel_cost_eur": total_fuel,
        "toll_cost_eur": total_tolls,
        "time_cost_eur": total_time_cost,
        "hourly_rate": hourly_rate,
    }
