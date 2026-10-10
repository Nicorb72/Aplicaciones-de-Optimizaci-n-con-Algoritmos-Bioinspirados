import numpy as np

from .population_utils import population_result, validate_population


def run_pso(objective, bounds, particles=20, iterations=100, seed=0, inertia=0.7, cognitive=1.4, social=1.4):
    "PSO: minimiza objective; cuesta particles + iterations * particles evaluaciones de f."

    low, high = validate_population(bounds, particles, iterations)
    # Coeficientes inválidos darían resultados sin sentido, así que se corta antes.

    if not np.all(np.isfinite([inertia, cognitive, social])) or min(inertia, cognitive, social) < 0:
        raise ValueError("Los coeficientes de PSO deben ser finitos y no negativos.")
    rng = np.random.default_rng(seed)
    dim = len(bounds)

    x = rng.uniform(low, high, size=(particles, dim))
    v = np.zeros_like(x)
    # Al inicio, él único punto que cada partícula ha visitado es el inicial.
    p_best = x.copy()
    p_best_val = np.array([objective(p) for p in p_best])
    g_best_idx = int(np.argmin(p_best_val))
    g_best = p_best[g_best_idx].copy()
    # Las evaluaciones iniciales también cuentan en el presupuesto.
    trajectory, values_history, evaluations = [g_best.copy()], [p_best_val[g_best_idx]], [particles]
    swarm_history = [x.copy()]

    for _ in range(iterations):
        # Aleatorios nuevos por partícula y coordenada, para que no se muevan todas igual.
        r1 = rng.random(size=x.shape)
        r2 = rng.random(size=x.shape)
        # Inercia + jalón hacia su mejor punto + jalón hacia el mejor enjambre.
        v = inertia * v + cognitive * r1 * (p_best - x) + social * r2 * (g_best - x)
        # Se recorta al dominio, pero la velocidad no se anula, esto es decisión de diseño.
        x = np.clip(x + v, low, high)

        values = np.array([objective(p) for p in x])
        # Solo las mejoras escritas actualizan el mejor punto personal.
        improved = values < p_best_val
        p_best[improved] = x[improved]
        p_best_val[improved] = values[improved]
        # p_best_val nunca empeora, así que el valor g_best tampoco.
        g_best_idx = int(np.argmin(p_best_val))
        g_best = p_best[g_best_idx].copy()
        trajectory.append(g_best.copy())
        values_history.append(p_best_val[g_best_idx])
        # Cada iteración evalúa f una vez por partícula.
        evaluations.append(evaluations[-1] + particles)
        swarm_history.append(x.copy())

    result = population_result(trajectory, values_history, evaluations)
    # Posiciones de todo el enjambre en cada iteración, para el GIF.
    result["population_history"] = np.asarray(swarm_history)
    return result
