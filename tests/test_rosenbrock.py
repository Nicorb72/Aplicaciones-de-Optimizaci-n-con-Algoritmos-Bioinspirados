import numpy as np
import pytest

from optimization.rosenbrock import rosenbrock, rosenbrock_gradient


@pytest.mark.parametrize("dimension", [2, 3])
def test_rosenbrock_minimum_at_one(dimension):
    x = np.ones(dimension)
    assert rosenbrock(x) == 0.0
    np.testing.assert_array_equal(rosenbrock_gradient(x), np.zeros(dimension))


@pytest.mark.parametrize("point", [[-1.2, 1.0], [-1.2, 1.0, 0.5]])
def test_rosenbrock_gradient_matches_central_differences(point):
    x = np.asarray(point, dtype=float)
    h = 1e-6
    numerical_gradient = np.zeros_like(x)
    for i in range(x.size):
        offset = np.zeros_like(x)
        offset[i] = h
        numerical_gradient[i] = (rosenbrock(x + offset) - rosenbrock(x - offset)) / (2 * h)
    np.testing.assert_allclose(rosenbrock_gradient(x), numerical_gradient, rtol=1e-5, atol=1e-6)
