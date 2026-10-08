from optimization.rastrigin import rastrigin


def test_rastrigin_minimum_at_zero():
    assert rastrigin([0.0, 0.0]) == 0.0


def test_rastrigin_gradient_matches_central_differences():
    import numpy as np
    from optimization.rastrigin import rastrigin_gradient

    for x in (np.array([.3, -1.2]), np.array([2.1, -.7, 1.3])):
        h = 1e-6
        offsets = h * np.eye(len(x))
        numerical = np.array([(rastrigin(x + v) - rastrigin(x - v)) / (2 * h) for v in offsets])
        np.testing.assert_allclose(rastrigin_gradient(x), numerical, rtol=1e-5, atol=1e-6)
