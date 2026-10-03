from optimization.pso import run_pso
from optimization.rastrigin import rastrigin


def test_pso_returns_result_dict():
    result = run_pso(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)], iterations=2)
    assert "best_solution" in result
    assert "best_value" in result
