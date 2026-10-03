from optimization.gradient_descent_rastrigin import run_gradient_descent_rastrigin


def test_gd_rastrigin_returns_result_dict():
    result = run_gradient_descent_rastrigin([2.0, 2.0], iterations=10)
    assert "best_solution" in result
    assert "best_value" in result
