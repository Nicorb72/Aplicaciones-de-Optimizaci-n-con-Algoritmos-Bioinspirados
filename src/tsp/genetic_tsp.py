"""Algoritmo Genético (GA) para el problema del vendedor viajero (TSP)."""

import numpy as np
from .cost_model import calculate_tour_cost


def order_crossover(parent1, parent2, rng):
    """Cruce de orden (OX) preservando permutación sin ciudades repetidas."""
    n = len(parent1)
    cx1, cx2 = sorted(rng.choice(n, size=2, replace=False))
    child = np.full(n, -1, dtype=int)
    child[cx1:cx2 + 1] = parent1[cx1:cx2 + 1]

    copied_set = set(child[cx1:cx2 + 1])
    fill_candidates = [gene for gene in parent2 if gene not in copied_set]

    fill_idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill_candidates[fill_idx]
            fill_idx += 1
    return child


def inversion_mutation(tour, mutation_rate, rng):
    """Mutación por inversión de subsecuencia (2-opt style)."""
    if rng.random() < mutation_rate:
        n = len(tour)
        i, j = sorted(rng.choice(n, size=2, replace=False))
        tour[i:j + 1] = tour[i:j + 1][::-1]
    return tour


def run_genetic_tsp(
    cost_matrix,
    population_size=100,
    generations=200,
    mutation_rate=0.2,
    tournament_size=4,
    elite_size=2,
    seed=42,
    record_evolution=True,
):
    """
    Ejecuta el Algoritmo Genético (GA) para el TSP sobre la matriz de costos.

    Parámetros:
        cost_matrix: matriz 2D (N, N) de costos.
        population_size: tamaño de la población de individuos (rutas).
        generations: número de generaciones a evolucionar.
        mutation_rate: probabilidad de mutar cada hijo.
        tournament_size: tamaño del torneo para selección.
        elite_size: cantidad de mejores individuos clonados directamente.
        seed: semilla aleatoria.
        record_evolution: si guarda tours intermedios para animaciones.

    Retorna:
        dict con best_tour, best_cost, cost_history y tour_evolution.
    """
    rng = np.random.default_rng(seed)
    n = cost_matrix.shape[0]

    # Población inicial con permutaciones aleatorias
    population = [rng.permutation(n) for _ in range(population_size)]
    fitnesses = [calculate_tour_cost(ind, cost_matrix) for ind in population]

    best_idx = int(np.argmin(fitnesses))
    best_tour = population[best_idx].copy()
    best_cost = float(fitnesses[best_idx])

    cost_history = [best_cost]
    tour_evolution = [(0, best_tour.copy(), best_cost)] if record_evolution else []

    def tournament_select():
        candidates = rng.choice(population_size, size=tournament_size, replace=False)
        best_cand = candidates[np.argmin([fitnesses[c] for c in candidates])]
        return population[best_cand]

    for gen in range(1, generations + 1):
        # Elitismo: ordenar población por fitness (costo menor)
        sorted_indices = np.argsort(fitnesses)
        new_pop = [population[idx].copy() for idx in sorted_indices[:elite_size]]

        while len(new_pop) < population_size:
            p1 = tournament_select()
            p2 = tournament_select()
            child = order_crossover(p1, p2, rng)
            child = inversion_mutation(child, mutation_rate, rng)
            new_pop.append(child)

        population = new_pop
        fitnesses = [calculate_tour_cost(ind, cost_matrix) for ind in population]

        current_best_idx = int(np.argmin(fitnesses))
        current_best_cost = float(fitnesses[current_best_idx])

        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_tour = population[current_best_idx].copy()
            if record_evolution:
                tour_evolution.append((gen, best_tour.copy(), best_cost))

        cost_history.append(best_cost)

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "cost_history": np.array(cost_history),
        "tour_evolution": tour_evolution,
        "method": "GA",
        "generations": generations,
        "population_size": population_size,
        "seed": seed,
    }
