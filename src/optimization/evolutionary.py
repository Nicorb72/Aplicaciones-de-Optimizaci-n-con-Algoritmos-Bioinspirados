import numpy as np

from .population_utils import population_result, validate_population


def run_evolutionary(objective, bounds, population_size=20, generations=50, seed=0, mutation_sigma=0.1):
    """Selección, cruce aritmético, mutación gaussiana y conservación de élites."""
    low, high = validate_population(bounds, population_size, generations, minimum=2)
    if not np.isfinite(mutation_sigma) or mutation_sigma < 0:
        raise ValueError("mutation_sigma debe ser finita y no negativa.")
    rng = np.random.default_rng(seed)
    population = rng.uniform(low, high, size=(population_size, len(bounds)))
    fitness = np.array([objective(ind) for ind in population])
    best = int(np.argmin(fitness))
    trajectory, values, evaluations = [population[best].copy()], [fitness[best]], [population_size]
    elite_size = population_size // 2
    children_count = population_size - elite_size

    for _ in range(generations):
        selected = np.argsort(fitness)[:elite_size]
        elite, elite_scores = population[selected], fitness[selected]
        parents = rng.integers(elite_size, size=(children_count, 2))
        weight = rng.random((children_count, 1))
        children = weight * elite[parents[:, 0]] + (1 - weight) * elite[parents[:, 1]]
        children += rng.normal(0, mutation_sigma, size=children.shape)
        children = np.clip(children, low, high)
        children_scores = np.array([objective(ind) for ind in children])
        population = np.vstack([elite, children])
        fitness = np.concatenate([elite_scores, children_scores])
        best = int(np.argmin(fitness))
        trajectory.append(population[best].copy())
        values.append(fitness[best])
        evaluations.append(evaluations[-1] + children_count)

    return population_result(trajectory, values, evaluations)
