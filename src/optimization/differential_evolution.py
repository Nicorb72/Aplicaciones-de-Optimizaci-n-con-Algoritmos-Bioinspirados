import numpy as np


def run_differential_evolution(objective, bounds, population_size=20, generations=50, f=0.8, cr=0.7, seed=0):
    rng = np.random.default_rng(seed)
    dim = len(bounds)
    low = np.array([b[0] for b in bounds], dtype=float)
    high = np.array([b[1] for b in bounds], dtype=float)
    pop = rng.uniform(low, high, size=(population_size, dim))
    scores = np.array([objective(ind) for ind in pop])

    for i in range(generations):
        for j in range(population_size):
            idx = [k for k in range(population_size) if k != j]
            a, b, c = pop[rng.choice(idx, size=3, replace=False)]
            mutant = np.clip(a + f * (b - c), low, high)
            cross_points = rng.random(dim) < cr
            if not np.any(cross_points):
                cross_points[rng.integers(0, dim)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_score = objective(trial)
            if trial_score < scores[j]:
                pop[j] = trial
                scores[j] = trial_score

    best_idx = int(np.argmin(scores))
    return {"best_solution": pop[best_idx], "best_value": float(scores[best_idx])}
