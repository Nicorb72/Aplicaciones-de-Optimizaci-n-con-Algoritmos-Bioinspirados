import numpy as np

from optimization.evolutionary import (
    blx_alpha_crossover,
    gaussian_mutation,
    run_evolutionary,
)
from optimization.rastrigin import rastrigin


def test_evolutionary_returns_common_result():
    result = run_evolutionary(
        rastrigin,
        [(-5.12, 5.12), (-5.12, 5.12)],
        population_size=10,
        generations=2,
        seed=42,
    )

    assert "best_solution" in result
    assert "best_value" in result
    assert "trajectory" in result
    assert "value_history" in result
    assert "function_evaluations" in result
    assert result["gradient_evaluations"] == 0
    assert result["status"] == "completed"


def test_evolutionary_uses_40000_evaluations():
    result = run_evolutionary(
        rastrigin,
        [(-5.12, 5.12), (-5.12, 5.12)],
        population_size=40,
        generations=1998,
        elite_fraction=0.5,
        seed=42,
    )

    assert result["function_evaluations"] == 40000


def test_blx_alpha_crossover_respects_interval():
    rng = np.random.default_rng(42)

    parent1 = np.array([1.0, -2.0])
    parent2 = np.array([3.0, 2.0])
    alpha = 0.3

    lower = np.minimum(parent1, parent2)
    upper = np.maximum(parent1, parent2)
    distance = upper - lower

    minimum_allowed = lower - alpha * distance
    maximum_allowed = upper + alpha * distance

    for _ in range(100):
        child = blx_alpha_crossover(
            parent1,
            parent2,
            rng,
            alpha=alpha,
        )

        assert np.all(child >= minimum_allowed)
        assert np.all(child <= maximum_allowed)


def test_gaussian_mutation_respects_bounds():
    rng = np.random.default_rng(42)

    child = np.array([4.9, -4.9])
    low = np.array([-5.12, -5.12])
    high = np.array([5.12, 5.12])

    mutated = gaussian_mutation(
        child,
        rng,
        low,
        high,
        mutation_rate=1.0,
        mutation_sigma=10.0,
    )

    assert np.all(mutated >= low)
    assert np.all(mutated <= high)