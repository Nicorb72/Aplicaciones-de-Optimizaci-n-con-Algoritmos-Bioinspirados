from optimization.evolutionary import run_evolutionary
from optimization.rastrigin import rastrigin


def test_evolutionary_returns_result_dict():
    result = run_evolutionary(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)], generations=2)
    assert "best_solution" in result
    assert "best_value" in result
