from optimization.differential_evolution import run_differential_evolution
from optimization.rastrigin import rastrigin


def test_differential_evolution_returns_result_dict():
    result = run_differential_evolution(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)], generations=2)
    assert "best_solution" in result
    assert "best_value" in result
