"""Optimización por Colonia de Hormigas (ACO) para el TSP."""

import numpy as np
from .cost_model import calculate_tour_cost


def run_ant_colony_tsp(
    cost_matrix,
    n_ants=25,
    iterations=100,
    alpha=1.0,
    beta=2.5,
    rho=0.1,
    q=100.0,
    seed=42,
    record_evolution=True,
):
    """
    Ejecuta el algoritmo de Colonias de Hormigas (ACO) sobre la matriz de costos.

    Parámetros:
        cost_matrix: matriz 2D (N, N) con los costos entre ciudades.
        n_ants: número de hormigas por iteración.
        iterations: número de ciclos de construcción y evaporación.
        alpha: peso de la feromona.
        beta: peso de la visibilidad heurística (1 / costo).
        rho: tasa de evaporación de feromona en [0, 1].
        q: constante de depósito de feromona.
        seed: semilla para reproducibilidad.
        record_evolution: si guarda tours intermedios para animaciones.

    Retorna:
        dict con best_tour, best_cost, cost_history y tour_evolution.
    """
    rng = np.random.default_rng(seed)
    n = cost_matrix.shape[0]

    # Matriz heurística: eta_ij = 1 / cost_ij (con seguridad para ceros en diagonal)
    with np.errstate(divide="ignore"):
        eta = np.where(cost_matrix > 0, 1.0 / cost_matrix, 0.0)

    # Inicializar feromona uniformemente
    tau0 = 1.0 / (n * np.mean(cost_matrix[cost_matrix > 0]))
    tau = np.full((n, n), tau0, dtype=float)

    best_tour = None
    best_cost = float("inf")
    cost_history = []
    tour_evolution = []

    for it in range(iterations):
        all_tours = []
        all_costs = []

        for ant in range(n_ants):
            start_city = rng.integers(0, n)
            visited = [start_city]
            unvisited = set(range(n)) - {start_city}

            current = start_city
            while unvisited:
                unvisited_list = list(unvisited)
                probs = []
                for nxt in unvisited_list:
                    p = (tau[current, nxt] ** alpha) * (eta[current, nxt] ** beta)
                    probs.append(p)
                probs = np.array(probs, dtype=float)
                total_p = probs.sum()
                if total_p == 0 or not np.isfinite(total_p):
                    # Elección uniforme si las probabilidades se anulan
                    probs = np.ones(len(unvisited_list)) / len(unvisited_list)
                else:
                    probs = probs / total_p

                next_city = rng.choice(unvisited_list, p=probs)
                visited.append(next_city)
                unvisited.remove(next_city)
                current = next_city

            tour = np.array(visited, dtype=int)
            cost = calculate_tour_cost(tour, cost_matrix)
            all_tours.append(tour)
            all_costs.append(cost)

            if cost < best_cost:
                best_cost = cost
                best_tour = tour.copy()
                if record_evolution:
                    tour_evolution.append((it, best_tour.copy(), best_cost))

        # Evaporación de feromona
        tau = (1.0 - rho) * tau

        # Depósito de feromona (acumulado por las hormigas del ciclo)
        for tour, cost in zip(all_tours, all_costs):
            deposit = q / cost
            for i in range(n):
                u = tour[i]
                v = tour[(i + 1) % n]
                tau[u, v] += deposit
                tau[v, u] += deposit

        # Refuerzo adicional al mejor global (elitismo ACO)
        deposit_best = (2.0 * q) / best_cost
        for i in range(n):
            u = best_tour[i]
            v = best_tour[(i + 1) % n]
            tau[u, v] += deposit_best
            tau[v, u] += deposit_best

        cost_history.append(best_cost)

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "cost_history": np.array(cost_history),
        "tour_evolution": tour_evolution,
        "method": "ACO",
        "iterations": iterations,
        "n_ants": n_ants,
        "seed": seed,
    }
