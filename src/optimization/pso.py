import numpy as np

from .population_utils import population_result, validate_population


def run_pso(objective, bounds, particles=20, iterations=100, seed=0, inertia=0.7, cognitive=1.4, social=1.4):
    low, high = validate_population(bounds, particles, iterations)
    if not np.all(np.isfinite([inertia, cognitive, social])) or min(inertia, cognitive, social) < 0:
        raise ValueError("Los coeficientes de PSO deben ser finitos y no negativos.")
    rng = np.random.default_rng(seed)
    dim = len(bounds)

    x = rng.uniform(low, high, size=(particles, dim))
    v = np.zeros_like(x)
    p_best = x.copy()
    p_best_val = np.array([objective(p) for p in p_best])
    g_best_idx = int(np.argmin(p_best_val))
    g_best = p_best[g_best_idx].copy()
    trajectory, values_history, evaluations = [g_best.copy()], [p_best_val[g_best_idx]], [particles]
    swarm_history = [x.copy()]

    for _ in range(iterations):
        r1 = rng.random(size=x.shape)
        r2 = rng.random(size=x.shape)
        v = inertia * v + cognitive * r1 * (p_best - x) + social * r2 * (g_best - x)
        x = np.clip(x + v, low, high)

        values = np.array([objective(p) for p in x])
        improved = values < p_best_val
        p_best[improved] = x[improved]
        p_best_val[improved] = values[improved]
        g_best_idx = int(np.argmin(p_best_val))
        g_best = p_best[g_best_idx].copy()
        trajectory.append(g_best.copy())
        values_history.append(p_best_val[g_best_idx])
        evaluations.append(evaluations[-1] + particles)
        swarm_history.append(x.copy())

    result = population_result(trajectory, values_history, evaluations)
    result["population_history"] = np.asarray(swarm_history)
    return result
