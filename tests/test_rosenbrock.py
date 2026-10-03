from optimization.rosenbrock import rosenbrock


def test_rosenbrock_minimum_at_one():
    assert rosenbrock([1.0, 1.0]) == 0.0
