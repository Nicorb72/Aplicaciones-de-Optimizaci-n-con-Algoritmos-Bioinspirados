import numpy as np

from .population_utils import population_result, validate_population


def tournament_selection(population, fitness, rng, tournament_size=3):
    """Selecciona por torneo el individuo con menor valor de la función."""
    indices = rng.choice(len(population), size=tournament_size, replace=False)
    winner_index = indices[np.argmin(fitness[indices])]
    return population[winner_index].copy()


def blx_alpha_crossover(parent1, parent2, rng, alpha=0.3):
    """Genera un hijo mediante cruce BLX-alpha."""
    lower = np.minimum(parent1, parent2)
    upper = np.maximum(parent1, parent2)
    distance = upper - lower

    return rng.uniform(
        lower - alpha * distance,
        upper + alpha * distance,
    )


def gaussian_mutation(child, rng, low, high, mutation_rate, mutation_sigma):
    """Aplica mutación gaussiana y mantiene al hijo dentro del dominio."""
    mutated = child.copy()

    for i in range(len(mutated)):
        if rng.random() < mutation_rate:
            mutated[i] += rng.normal(0.0, mutation_sigma)

    return np.clip(mutated, low, high)


def run_evolutionary(
    objective,
    bounds,
    population_size=40,
    generations=1998,
    tournament_size=3,
    crossover_alpha=0.3,
    mutation_rate=None,
    mutation_sigma=0.1,
    elite_fraction=0.5,
    seed=0,
    show_config=False,
):
    """
    Minimiza una función mediante un algoritmo evolutivo con selección
    por torneo, cruce BLX-alpha, mutación gaussiana y elitismo.

    Evaluaciones de f:
    population_size + (population_size - elite_size) * generations
    """

    low, high = validate_population(
        bounds, population_size, generations, minimum=2
    )

    dimension = len(bounds)

    if not isinstance(tournament_size, int) or not 2 <= tournament_size <= population_size:
        raise ValueError(
            "tournament_size debe ser un entero entre 2 y population_size."
        )

    if not np.isfinite(crossover_alpha) or crossover_alpha < 0:
        raise ValueError("crossover_alpha debe ser finito y no negativo.")

    if mutation_rate is None:
        mutation_rate = 1.0 / dimension

    if not np.isfinite(mutation_rate) or not 0 <= mutation_rate <= 1:
        raise ValueError("mutation_rate debe estar entre 0 y 1.")

    if not np.isfinite(mutation_sigma) or mutation_sigma < 0:
        raise ValueError("mutation_sigma debe ser finita y no negativa.")

    if not np.isfinite(elite_fraction) or not 0 < elite_fraction < 1:
        raise ValueError("elite_fraction debe estar entre 0 y 1, sin incluirlos.")

    elite_size = max(1, round(population_size * elite_fraction))

    if elite_size >= population_size:
        raise ValueError("La élite debe ser menor que el tamaño de la población.")

    children_count = population_size - elite_size

    if show_config:
        print(
            f"Élite: {elite_size} de {population_size} "
            f"({100 * elite_size / population_size:.1f}%)"
        )

    rng = np.random.default_rng(seed)

    population = rng.uniform(
        low,
        high,
        size=(population_size, dimension),
    )

    fitness = np.array(
        [objective(individual) for individual in population]
    )

    best_index = np.argmin(fitness)

    trajectory = [population[best_index].copy()]
    values = [float(fitness[best_index])]
    evaluations = [population_size]

    for _ in range(generations):
        elite_indices = np.argsort(fitness)[:elite_size]

        elite = population[elite_indices].copy()
        elite_fitness = fitness[elite_indices].copy()

        children = []

        while len(children) < children_count:
            parent1 = tournament_selection(
                population, fitness, rng, tournament_size
            )
            parent2 = tournament_selection(
                population, fitness, rng, tournament_size
            )

            child = blx_alpha_crossover(
                parent1,
                parent2,
                rng,
                alpha=crossover_alpha,
            )

            child = gaussian_mutation(
                child,
                rng,
                low,
                high,
                mutation_rate,
                mutation_sigma,
            )

            children.append(child)

        children = np.asarray(children)

        children_fitness = np.array(
            [objective(child) for child in children]
        )

        # La élite ya estaba evaluada, por eso solo se evalúan los hijos.
        population = np.vstack((elite, children))
        fitness = np.concatenate((elite_fitness, children_fitness))

        best_index = np.argmin(fitness)

        trajectory.append(population[best_index].copy())
        values.append(float(fitness[best_index]))

        evaluations.append(
            evaluations[-1] + children_count
        )

    return population_result(
        trajectory,
        values,
        evaluations,
    )