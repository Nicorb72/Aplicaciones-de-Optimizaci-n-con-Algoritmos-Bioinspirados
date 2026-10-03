import numpy as np


def run_pso(objective, bounds, particles=20, iterations=100, seed=0):
    rng = np.random.default_rng(seed)
    dim = len(bounds)
    low = np.array([b[0] for b in bounds], dtype=float)
    high = np.array([b[1] for b in bounds], dtype=float)

    x = rng.uniform(low, high, size=(particles, dim))
    v = np.zeros_like(x)
    p_best = x.copy()
    p_best_val = np.array([objective(p) for p in p_best])
    g_best_idx = int(np.argmin(p_best_val))
    g_best = p_best[g_best_idx].copy()

    for _ in range(iterations):
        r1 = rng.random(size=x.shape)
        r2 = rng.random(size=x.shape)
        v = 0.7 * v + 1.4 * r1 * (p_best - x) + 1.4 * r2 * (g_best - x)
        x = np.clip(x + v, low, high)

        values = np.array([objective(p) for p in x])
        improved = values < p_best_val
        p_best[improved] = x[improved]
        p_best_val[improved] = values[improved]
        g_best_idx = int(np.argmin(p_best_val))
        g_best = p_best[g_best_idx].copy()

    return {"best_solution": g_best, "best_value": float(objective(g_best))}
