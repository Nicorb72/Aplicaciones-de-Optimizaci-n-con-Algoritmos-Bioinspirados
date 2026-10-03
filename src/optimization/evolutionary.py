import numpy as np


def run_evolutionary(objective, bounds, population_size=20, generations=50, seed=0):
    rng = np.random.default_rng(seed)
    low = np.array([b[0] for b in bounds], dtype=float)
    high = np.array([b[1] for b in bounds], dtype=float)
    population = rng.uniform(low, high, size=(population_size, len(bounds)))

    for _ in range(generations):
        fitness = np.array([objective(ind) for ind in population])
        elite = population[np.argsort(fitness)[: population_size // 2]]
        noise = rng.normal(0, 0.1, size=elite.shape)
        offspring = np.clip(elite + noise, low, high)
        population = np.vstack([elite, offspring])

    fitness = np.array([objective(ind) for ind in population])
    idx = int(np.argmin(fitness))
    return {"best_solution": population[idx], "best_value": float(fitness[idx])}
