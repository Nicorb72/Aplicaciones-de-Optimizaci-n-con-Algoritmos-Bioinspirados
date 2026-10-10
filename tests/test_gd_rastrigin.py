import pytest

from optimization.gradient_descent_rastrigin import run_gradient_descent_rastrigin


def test_gd_rastrigin_returns_result_dict():
    result = run_gradient_descent_rastrigin([2.0, 2.0], iterations=10)
    assert "best_solution" in result
    assert "best_value" in result


@pytest.mark.parametrize(
    "kwargs",
    [
        {"iterations": -1},
        {"iterations": 1.5},
        {"iterations": True},
        {"learning_rate": 0},
        {"learning_rate": float("nan")},
        {"learning_rate": True},
        {"initial_point": [[1, 1]]},
        {"initial_point": [1]},
        {"initial_point": [1, float("inf")]},
    ],
)
def test_gd_rastrigin_rejects_invalid_direct_calls(kwargs):
    arguments = {"initial_point": [1.0, 1.0], "iterations": 0, "learning_rate": 0.001}
    arguments.update(kwargs)

    with pytest.raises(ValueError):
        run_gradient_descent_rastrigin(**arguments)
