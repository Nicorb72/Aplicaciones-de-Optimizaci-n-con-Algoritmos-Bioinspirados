from optimization.gradient_descent_rosenbrock import run_gradient_descent_rosenbrock


def test_gd_rosenbrock_returns_result_dict():
    result = run_gradient_descent_rosenbrock([-1.2, 1.0], iterations=10)
    assert "best_solution" in result
    assert "best_value" in result
