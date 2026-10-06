from unittest.mock import patch

import numpy as np
import pytest

import optimization.gradient_descent_rosenbrock as gd
from optimization.gradient_descent_rosenbrock import run_gradient_descent_rosenbrock


def test_gd_rosenbrock_returns_result_dict():
    result = run_gradient_descent_rosenbrock([-1.2, 1.0], iterations=10)
    assert "best_solution" in result
    assert "best_value" in result


@pytest.mark.parametrize("initial_point", [[-1.2, 1.0], [-1.2, 1.0, 0.5]])
@pytest.mark.parametrize("iterations", [0, 1, 10])
def test_gd_rosenbrock_counts_actual_evaluations(initial_point, iterations):
    with (
        patch.object(gd, "rosenbrock", wraps=gd.rosenbrock) as counted_function,
        patch.object(gd, "rosenbrock_gradient", wraps=gd.rosenbrock_gradient) as counted_gradient,
    ):
        result = gd.run_gradient_descent_rosenbrock(initial_point, iterations=iterations)
    assert result["function_evaluations"] == counted_function.call_count == 1
    assert result["gradient_evaluations"] == counted_gradient.call_count == iterations


@pytest.mark.parametrize(
    "initial_point, expected_first_step",
    [
        ([-1.2, 1.0], [-0.9844, 1.088]),
        ([-1.2, 1.0, 0.5], [-0.9844, 0.888, 0.6]),
    ],
)
@pytest.mark.parametrize("iterations", [0, 1, 10])
def test_gd_rosenbrock_preserves_trajectory(initial_point, expected_first_step, iterations):
    x0 = np.array(initial_point)
    result = gd.run_gradient_descent_rosenbrock(x0, learning_rate=1e-3, iterations=iterations)
    trajectory = result["trajectory"]
    assert result["status"] == "completed"
    assert result["iterations_completed"] == iterations
    assert trajectory.shape == (iterations + 1, len(initial_point))
    np.testing.assert_array_equal(trajectory[0], initial_point)
    np.testing.assert_array_equal(trajectory[-1], result["best_solution"])
    np.testing.assert_array_equal(x0, initial_point)
    assert not np.shares_memory(trajectory, result["best_solution"])
    if iterations > 0:
        np.testing.assert_allclose(trajectory[1], expected_first_step)


@pytest.mark.parametrize("seed", [43, 60, 63])
def test_gd_stops_divergent_runs_and_keeps_finite_points(seed):
    x0 = np.random.default_rng(seed).uniform(-2, 2, size=3)
    with (
        patch.object(gd, "rosenbrock", wraps=gd.rosenbrock) as counted_function,
        patch.object(gd, "rosenbrock_gradient", wraps=gd.rosenbrock_gradient) as counted_gradient,
    ):
        result = gd.run_gradient_descent_rosenbrock(x0, iterations=10000)
    assert result["status"] == "diverged"
    assert 0 < result["iterations_completed"] < 10000
    assert np.all(np.isfinite(result["trajectory"]))
    np.testing.assert_array_equal(result["trajectory"][-1], result["best_solution"])
    assert result["iterations_completed"] == len(result["trajectory"]) - 1
    assert result["function_evaluations"] == counted_function.call_count == 1
    assert result["gradient_evaluations"] == counted_gradient.call_count
    assert result["gradient_evaluations"] == result["iterations_completed"] + 1


def test_gd_rejects_nonfinite_step_from_finite_gradient():
    result = gd.run_gradient_descent_rosenbrock([0.0, 0.0], learning_rate=1e308, iterations=10)
    assert result["status"] == "diverged"
    assert result["iterations_completed"] == 0
    assert result["gradient_evaluations"] == 1
    assert result["function_evaluations"] == 1
    assert result["best_value"] == 1.0
    np.testing.assert_array_equal(result["trajectory"], [[0.0, 0.0]])


def test_gd_marks_nonfinite_final_value_as_divergence():
    result = gd.run_gradient_descent_rosenbrock([1e100, 0.0], iterations=0)
    assert result["status"] == "diverged"
    assert result["iterations_completed"] == 0
    assert result["gradient_evaluations"] == 0
    assert result["function_evaluations"] == 1
    assert np.isinf(result["best_value"])
