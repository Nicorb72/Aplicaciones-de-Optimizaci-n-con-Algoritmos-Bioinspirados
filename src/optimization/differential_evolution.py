import numpy as np

from .population_utils import population_result, validate_population



def run_differential_evolution(objective, bounds, population_size=40, generations=50, f=0.7, cr=0.9, seed=0):
    low, high = validate_population(bounds, population_size, generations, minimum=4)
    if not np.isfinite(f) or f <= 0 or not np.isfinite(cr) or not 0 <= cr <= 1:
        raise ValueError("DE requiere f > 0 y 0 <= cr <= 1, ambos finitos.")
    rng = np.random.default_rng(seed)
    dim = len(bounds)
    pop = rng.uniform(low, high, size=(population_size, dim))
    scores = np.array([objective(ind) for ind in pop])
    best = int(np.argmin(scores))
    trajectory, values, evaluations = [pop[best].copy()], [scores[best]], [population_size]

    for i in range(generations):
        new_pop, new_scores = pop.copy(), scores.copy()
        
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
                new_pop[j], new_scores[j] = trial, trial_score
    
        pop, scores = new_pop, new_scores
        best = int(np.argmin(scores))
        trajectory.append(pop[best].copy())
        values.append(scores[best])
        evaluations.append(evaluations[-1] + population_size)

    return population_result(trajectory, values, evaluations)
